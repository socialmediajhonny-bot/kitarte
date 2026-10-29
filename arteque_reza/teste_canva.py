"""Experimento controlado de importação de texto no Canva, sem importar no serviço.

Cada PDF vem de um único documento e uma única chamada Chromium. Os dois
articles de origem são produzidos pelo gerador do Evangelho, sem cópia do HTML.
"""
from __future__ import annotations

from io import BytesIO
import json
from pathlib import Path
import shutil
from typing import Any
from urllib.parse import urlsplit

import fitz
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject

from .base import PROJECT, KIT, await_fonts, generate_tokens_css, load_tokens, resource_url
from .conteudo import load_content
from .evangelho import _document as gospel_document, _TEXT_JS
from .ficha import _MEASURE_JS
from .renderizacao import local_server
from .validacao import validate_kit


VARIANTS = [
    {'id': 'controle', 'nome': 'controle', 'incremento_px': 0, 'estilo': None},
    {'id': 'camada', 'nome': 'camada', 'incremento_px': 0, 'estilo': ('opacity', '0.999')},
    {'id': 'giro', 'nome': 'giro', 'incremento_px': 0, 'estilo': ('transform', 'rotate(0.5deg)')},
    {'id': 'respiro-32', 'nome': 'respiro 32', 'incremento_px': 16, 'estilo': 'margin'},
    {'id': 'respiro-48', 'nome': 'respiro 48', 'incremento_px': 32, 'estilo': 'margin'},
    {'id': 'respiro-80', 'nome': 'respiro 80', 'incremento_px': 64, 'estilo': 'margin'},
    {'id': 'respiro-128', 'nome': 'respiro 128', 'incremento_px': 112, 'estilo': 'margin'},
]
PAGE_CSS = '@page{size:1080px 1350px;margin:0;} .aqr-post{break-after:page;}'


def _specifications(tagged: bool) -> list[dict]:
    specs = []
    for variant in VARIANTS[:1] if tagged else VARIANTS:
        for kind in (2, 4):
            style = variant['estilo']
            if style == 'margin':
                style = ('margin-top' if kind == 2 else 'margin-bottom', f'{variant["incremento_px"]}px')
            specs.append({'pagina': len(specs)+1, 'card_origem': kind, 'variante': variant['id'],
                          'nome_variante': variant['nome'], 'incremento_px': variant['incremento_px'],
                          'elemento_alvo': 'trecho_ref' if kind == 2 else 'chamada_oracao',
                          'estilo_acrescentado': dict([style]) if style else {},
                          'par': {'superior': 'trecho' if kind == 2 else 'chamada_oracao',
                                  'inferior': 'trecho_ref' if kind == 2 else 'pergunta'}})
    return specs


def _assemble_document(page: Any, sources: dict[str, str], specs: list[dict], path: Path,
                       base_url: str) -> None:
    """Retain the complete source head, and clone only original DOM articles."""
    source_path = path.parent/'origem-card-2.html'
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text(sources['2'], encoding='utf-8')
    page.goto(base_url+resource_url(source_path), wait_until='load')
    await_fonts(page)
    page.evaluate("""args => {
      const articles=[];
      for(const spec of args.specs){
        const documentSource=new DOMParser().parseFromString(args.sources[String(spec.card_origem)],'text/html');
        const article=documentSource.querySelector('article.aqr-post');
        if(!article)throw new Error('Article do Evangelho ausente.');
        const target=article.querySelector(`[data-element="${spec.elemento_alvo}"]`);
        if(!target)throw new Error('Elemento alvo ausente: '+spec.elemento_alvo);
        for(const [property,value] of Object.entries(spec.estilo_acrescentado))target.style.setProperty(property,value);
        article.dataset.pagina=spec.pagina;
        articles.push(article);
      }
      document.body.replaceChildren(...articles);
      const style=document.createElement('style');style.dataset.experimento='paginacao';style.textContent=args.css;
      document.head.appendChild(style);
    }""", {'sources': sources, 'specs': specs, 'css': PAGE_CSS})
    path.write_text(page.content(), encoding='utf-8')
    # Load the actual saved HTML so both the PDF and its fixture refer to the
    # same standalone multi-page document, with all original local resources.
    page.goto(base_url+resource_url(path), wait_until='load')
    await_fonts(page)


def _measure_document(page: Any, specs: list[dict]) -> list[dict]:
    measured = []
    tokens = [item['name'] for item in load_tokens()['color']['tokens']]
    for index, spec in enumerate(specs):
        selector = f"document.querySelectorAll('.aqr-post')[{index}]"
        js = _TEXT_JS.replace("document.querySelector('.aqr-post')", selector, 1)
        card = page.evaluate(js)
        element_js = _MEASURE_JS.replace("document.querySelector('.aqr-post')", selector, 1)
        elements = page.evaluate(element_js, tokens)['elements']
        card.update(spec)
        card.update({'card': spec['pagina'], 'tipo': 'Versículo' if spec['card_origem']==2 else 'Para rezar hoje',
                     'modelo': spec['card_origem'], 'tema': 'capela' if spec['card_origem']==2 else 'pergaminho',
                     'largura': 1080, 'altura': 1350, 'elementos': elements})
        pair = spec['par']
        texts = {text['campo']: text for text in card['textos']}
        upper = texts[pair['superior']]['caixa']; lower = texts[pair['inferior']]['caixa']
        card['distancia_par_px'] = lower['y']-upper['y']-upper['altura']
        card['par']['caixa_superior'] = upper; card['par']['caixa_inferior'] = lower
        card['par']['linhas_superior'] = texts[pair['superior']]['caixas_das_linhas']
        card['par']['linhas_inferior'] = texts[pair['inferior']]['caixas_das_linhas']
        target = texts[spec['elemento_alvo']]
        card['elemento_alvo_texto'] = target['conteudo']
        card['estilo_computado_alvo'] = page.evaluate("""args => {
          const node=document.querySelectorAll('.aqr-post')[args.index].querySelector(`[data-element="${args.target}"]`);
          const style=getComputedStyle(node);
          return {position:style.position,opacity:style.opacity,transform:style.transform,
                  margin_top:style.marginTop,margin_bottom:style.marginBottom};
        }""", {'index':index,'target':spec['elemento_alvo']})
        measured.append(card)
    return measured


def _write_pdf(page: Any, output: Path, *, tagged: bool) -> int:
    """Preserve the catalog's tagged-PDF structure while correcting page boxes."""
    raw = page.pdf(width='1080px', height='1350px', print_background=True,
                   margin={'top':'0','right':'0','bottom':'0','left':'0'},
                   prefer_css_page_size=False, tagged=tagged)
    reader = PdfReader(BytesIO(raw))
    writer = PdfWriter(clone_from=reader)
    for pdf_page in writer.pages:
        pdf_page.add_transformation(Transformation().translate(ty=1012.5-float(pdf_page.mediabox.height)))
        pdf_page.mediabox = RectangleObject([0,0,810,1012.5])
        pdf_page.cropbox = RectangleObject([0,0,810,1012.5])
    with output.open('wb') as stream:
        writer.write(stream)
    return len(writer.pages)


def _board(pdf: Path, pages: list[dict], output: Path) -> tuple[int, int]:
    # A 1350 px canvas has a half-pixel at 1/4; the PDF rasterizer rounds the
    # miniature height to 338 px while retaining exactly 270 px in width.
    margin = 24; gap = 24; mini_width = 270; mini_height = 338; label_height = 50
    width = margin*2+mini_width*2+gap; row_height = mini_height+label_height+24
    size = (width, margin*2+7*row_height)
    board = Image.new('RGB', size, '#f2eadb'); draw = ImageDraw.Draw(board)
    font = ImageFont.truetype(str(KIT/'fontes/Lato-Regular.ttf'), 15)
    with fitz.open(pdf) as document:
        for index, (page, info) in enumerate(zip(document, pages)):
            raster = page.get_pixmap(matrix=fitz.Matrix(mini_width/page.rect.width, mini_width/page.rect.width), alpha=False)
            image = Image.frombytes('RGB', (raster.width, raster.height), raster.samples)
            x = margin+(index%2)*(mini_width+gap); y = margin+(index//2)*row_height
            board.paste(image, (x,y))
            draw.text((x,y+mini_height+8), f'P{index+1} · {info["nome_variante"]} · card {info["card_origem"]}',
                      font=font, fill='#241b14')
            style = '; '.join(f'{key}: {value}' for key,value in info['estilo_acrescentado'].items()) or 'sem estilo acrescentado'
            draw.text((x,y+mini_height+29), style, font=font, fill='#665647')
    board.save(output)
    return size


def _readme(output: Path, ficha: dict, checks: dict) -> Path:
    lines = ['# Teste de importação no Canva', '',
             'Gerado por `python gerar.py teste-canva` a partir dos cards 2 e 4 do Evangelho de 29/11/2026, usando o mesmo `_document` do gerador.',
             '', 'Importe **os dois PDFs no Canva, sem editar nada**. Compare as caixas e o tamanho da referência Mc 13,37 e do rótulo Para rezar hoje. O objetivo é verificar se o Canva continua fundindo cada elemento ao texto vizinho.',
             '', '- [teste-canva-a.pdf](teste-canva-a.pdf): 14 páginas, sem marcação.',
             '- [teste-canva-b.pdf](teste-canva-b.pdf): 2 controles, com marcação estrutural.',
             '- [prancha.png](prancha.png): as páginas do A rasterizadas a 1/4, com a variante fora das artes (270 × 338 px; 1350/4 resulta em meio pixel, arredondado pelo rasterizador).',
             '', '| Páginas do A | Variante | Estilo na referência (card 2) | Estilo no rótulo (card 4) | Distância DOM do par |',
             '| --- | --- | --- | --- | --- |']
    pages = ficha['documentos']['a']['paginas']
    for index in range(0,14,2):
        first,second=pages[index:index+2]
        styles=[]
        for item in (first,second):
            styles.append('; '.join(f'{key}: {value}' for key,value in item['estilo_acrescentado'].items()) or 'nenhum')
        distances=f'{first["distancia_par_px"]:g} / {second["distancia_par_px"]:g} px'
        lines.append(f'| {index+1} e {index+2} | {first["nome_variante"]} | `{styles[0]}` | `{styles[1]}` | {distances} |')
    lines += ['', 'As páginas 1 e 2 do B correspondem às páginas 1 e 2 do A. Não há nomes de variantes dentro de nenhuma arte.',
              '', 'Cada PDF foi produzido por um documento HTML próprio e uma única chamada de `page.pdf`; o A usa `tagged=False` e o B `tagged=True`. A correção das caixas usa `PdfWriter(clone_from=reader)`, preservando o catálogo e a árvore estrutural do B.',
              '', 'No respiro, só a margem do elemento muda. O `gap` de 16 px do kit se soma a ela, e o bloco continua centralizado. Os controles e as demais variantes mantêm os estilos originais do Evangelho.',
              '', 'A validação automática está em [verificacao.json](verificacao.json): páginas e dimensões, fontes embutidas, texto integral, estrutura marcada, comparação visual dos controles e da camada, Form XObject de transparência, direção das linhas e crescimento dos espaços no PDF.',
              '', 'A igualdade do texto usa a ordem geométrica de leitura (`PyMuPDF sort=True` e `pdftotext -layout`), desconsiderando espaços e quebras. A camada e o giro podem pintar o alvo por último no fluxo interno do PDF; a ordem visual e o conteúdo continuam os mesmos.',
              '', 'A importação real no Canva **não foi executada**. A estrutura do PDF e as medições não permitem concluir como o importador vai tratar cada variante; esse resultado depende do teste manual acima.',
              '', '## Arquivos', '', '```text', 'saida/teste-canva/']
    names={path.relative_to(output).as_posix() for path in output.rglob('*') if path.is_file()};names.add('LEIA-ME.md')
    lines += ['  '+name for name in sorted(names)]+['```','']
    path=output/'LEIA-ME.md';path.write_text('\n'.join(lines),encoding='utf-8');return path


def generate(output: Path) -> dict:
    """Build both reviewable PDFs and block delivery on any failed check."""
    output=Path(output).resolve();target=output/'teste-canva';target.mkdir(parents=True,exist_ok=True)
    kit=validate_kit(PROJECT)
    if not kit['ok']:raise ValueError('Kit inválido: '+'; '.join(kit['errors']))
    day=next(day for day in load_content(PROJECT/'conteudo/evangelho.yaml') if day['data']=='2026-11-29')
    css=generate_tokens_css(output/'tokens.css')
    artwork=PROJECT/day['obra']['arquivo']
    if not artwork.is_file():artwork=PROJECT/'saida/obra-provisoria.png'
    sources={str(kind):gospel_document(day,kind,css,artwork) for kind in (2,4)}
    work=PROJECT/'work/teste-canva';work.mkdir(parents=True,exist_ok=True)
    fixture={'origem':{'serie':'Evangelho do Dia','data':day['data'],'cards':[2,4],
                       'pdf':'saida/evangelho/2026-11-29/evangelho-2026-11-29.pdf'},
             'documentos':{}}
    browser_errors=[]
    with local_server() as base_url,sync_playwright() as playwright:
        browser=playwright.chromium.launch(executable_path=shutil.which('chromium') or '/usr/bin/chromium',
                                          headless=True,args=['--no-sandbox'])
        context=browser.new_context(device_scale_factor=1,viewport={'width':1080,'height':1350})
        context.route('**/*',lambda route:route.continue_() if urlsplit(route.request.url).netloc==urlsplit(base_url).netloc else route.abort())
        page=context.new_page()
        page.on('pageerror',lambda error:browser_errors.append(str(error)))
        page.on('console',lambda message:browser_errors.append(message.text) if message.type=='error' else None)
        page.on('response',lambda response:browser_errors.append(f'HTTP {response.status}: {response.url}') if response.status>=400 else None)
        for key,tagged in [('a',False),('b',True)]:
            specs=_specifications(tagged);html=work/f'teste-canva-{key}.html'
            _assemble_document(page,sources,specs,html,base_url)
            measured=_measure_document(page,specs)
            pdf=target/f'teste-canva-{key}.pdf'
            page_count=_write_pdf(page,pdf,tagged=tagged)
            fixture['documentos'][key]={'arquivo':pdf.name,'marcado':tagged,'paginas':measured,
                                        'paginas_pdf':page_count,'documentos_html':1,'chamadas_page_pdf':1}
        browser.close()
    if browser_errors:raise RuntimeError('Erros de navegador: '+'; '.join(browser_errors))
    (target/'ficha.json').write_text(json.dumps(fixture,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    _board(target/'teste-canva-a.pdf',fixture['documentos']['a']['paginas'],target/'prancha.png')
    from .validacao_canva import validate_canva
    gospel_pdf=PROJECT/'saida/evangelho/2026-11-29/evangelho-2026-11-29.pdf'
    checks=validate_canva(target,gospel_pdf,fixture)
    checks['kit']=kit;checks['kit_final']=validate_kit(PROJECT)
    checks['browser']={'ok':True,'errors':[],'recursos_externos':False}
    checks['ok']=checks['ok'] and checks['kit_final']['ok']
    (target/'verificacao.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not checks['ok']:
        raise ValueError('Teste Canva falhou: '+'; '.join(checks.get('errors',[])))
    readme=_readme(target,fixture,checks)
    return {'dias':1,'cards':16,'pdfs':2,'pngs':1,'obras_pendentes':[],
            'leia_me':str(readme),'verificacoes':str(target/'verificacao.json')}
