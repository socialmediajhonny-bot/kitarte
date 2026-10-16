"""Carrosséis Evangelho do Dia: composição do kit, medições e provas reais.

Todas as fontes e imagens são servidas do checkout por HTTP de loopback.
O modelo não altera o kit nem busca obras na internet.
"""
from __future__ import annotations

from copy import deepcopy
from html import escape
from io import BytesIO
import json
from math import cos, sin, pi, hypot
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any
from urllib.parse import urlsplit

from PIL import Image, ImageDraw, ImageFont, ImageColor
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

from .base import (PROJECT, KIT, CRUZ_PATH, assinatura, await_fonts, color,
                   generate_tokens_css, html_document, montar_arte, nicho,
                   render_arte, resource_url, selo)
from .conteudo import load_content, date_label, expanded_reference, text_html, color_token
from .ficha import measure_page
from .renderizacao import local_server
from .validacao import validate_kit, validate_niche_pixels, validate_pngs


EXTRA_CSS = """
@page { margin:0; }
.aqr-post--cor .aqr-corpo {color:var(--sobre-cor);}
.aqr-corpo {text-wrap:balance;}
.aqr-credito {max-width:920px;}
"""
REQUIRED_FONTS = {'CormorantGaramond-SemiBold', 'CormorantGaramond-MediumItalic',
                  'Lato-Bold', 'Lato-Regular'}
LIMITS = {'titulo': 2, 'credito': 1, 'reflexao.titulo': 2,
          'reflexao.texto': 6, 'pergunta': 4, 'convite': 1}
NAMES = {1: 'Capa', 2: 'Versículo', 3: 'Para a Missa de hoje', 4: 'Para rezar hoje'}


def _text(tag: str, field: str, style: str, value: str, css: str = '',
          token: str = 'tinta', *, raw: bool = False) -> str:
    body = value if raw else text_html(value)
    return (f'<{tag} class="{style}" data-text="{field}" data-style="{style.split()[0]}" '
            f'data-element="{field}" data-cor-token="{token}" style="{css}">{body}</{tag}>')


def _header(day: dict) -> str:
    markup = selo('Evangelho do Dia', date_label(day['data']), day['referencia'])
    # Preserve the reusable Selo's structure, fonts and separate ink colours.
    markup = markup.replace('data-element="selo-serie"',
                            'data-element="selo-serie" data-text="selo" data-style="selo"')
    markup = markup.replace('data-element="selo-data"',
                            'data-element="selo-data" data-text="data" data-style="selo"')
    return markup.replace('data-element="selo-info"',
                          'data-element="selo-info" data-text="referencia" data-style="selo"')


def _ornament(on_color=False) -> str:
    style = 'color:var(--sobre-cor);' if on_color else ''
    return (f'<div class="aqr-ornamento" data-element="ornamento" '
            f'style="{style}margin-block:var(--espaco-3)">'
            f'<svg viewBox="0 0 18 30" aria-hidden="true"><path d="{CRUZ_PATH}" '
            'fill="currentColor"/></svg></div>')


def _document(day: dict, card_kind: int, css: Path, artwork: Path,
              quote_style: str = 'citacao-grande') -> str:
    top = _header(day)
    if card_kind == 1:
        image = nicho(680, 760, artwork)
        image = image.replace('style="width:680px;height:760px;"',
                              'style="width:680px;height:760px;margin-top:var(--espaco-3)"')
        image = image.replace('alt="Obra provisória"', 'alt="Obra do Evangelho"')
        image = image.replace('data-arquivo="obra-provisoria.png"',
                              f'data-arquivo="{escape(artwork.relative_to(PROJECT).as_posix(), quote=True)}" '
                              f'style="object-position:{escape(day["obra"]["foco"], quote=True)}"')
        body = image + _text('p', 'credito', 'credito aqr-credito', day['obra']['credito'],
                             'margin-top:var(--espaco-3)', 'tinta-suave')
        body += _text('h1', 'titulo', 'titulo aqr-titulo', day['titulo'],
                      'margin-top:var(--espaco-4);max-width:880px;text-align:center')
    elif card_kind == 2:
        body = '<div class="aqr-texto" style="margin-top:auto">'
        body += _text('p', 'trecho', quote_style + ' aqr-citacao', day['trecho'], 'max-width:880px')
        body += _text('p', 'trecho_ref', 'referencia aqr-referencia', day['trecho_ref'], token='ouro')
        body += '</div>'
    elif card_kind == 3:
        body = '<div class="aqr-texto" style="margin-top:auto">'
        body += _text('p', 'chamada_reflexao', 'selo aqr-suave', 'Para a Missa de hoje', token='tinta-suave')
        body += _text('h2', 'reflexao.titulo', 'titulo aqr-titulo', day['reflexao']['titulo'], 'max-width:880px')
        body += _ornament()
        body += _text('p', 'reflexao.texto', 'corpo aqr-corpo', day['reflexao']['texto'], 'max-width:760px')
        body += '</div>'
    else:
        body = '<div class="aqr-texto" style="margin-top:auto">'
        body += _text('p', 'chamada_oracao', 'selo', 'Para rezar hoje', token='sobre-cor')
        body += _text('p', 'pergunta', 'citacao aqr-citacao', day['pergunta'], 'max-width:860px', 'sobre-cor')
        body += _ornament(True)
        invitation = text_html('Abra sua Bíblia em ') + '<strong>' + text_html(expanded_reference(day['referencia'])) + '</strong>'
        body += _text('p', 'convite', 'corpo', invitation, token='sobre-cor', raw=True)
        body += '</div>'
    sig = assinatura('pergaminho' if card_kind == 4 else 'capela')
    post = montar_arte(top + body + sig, tema='pergaminho' if card_kind == 4 else 'capela',
                       cor_do_dia=color_token(day['cor']), cartao_cor=card_kind == 4)
    # Explicit use of the v2 logo, including when the base is used independently.
    if card_kind == 4:
        post = post.replace('logo-horizontal-capela.svg', 'logo-horizontal-sobre-cor.svg')
    return html_document(post, css, EXTRA_CSS, f'Evangelho do Dia · {day["data"]} · {NAMES[card_kind]}')


# Range fragments recover the actual line breaks chosen by Chromium. A visual
# baseline groups normal and <strong> runs of one line without counting the
# nested run twice. Forced <br> is preserved by the browser's ranges.
_TEXT_JS = r"""() => {
 const article = document.querySelector('.aqr-post'), ar = article.getBoundingClientRect();
 const rr = r => ({x:+(r.left-ar.left).toFixed(6),y:+(r.top-ar.top).toFixed(6),
   largura:+r.width.toFixed(6),altura:+r.height.toFixed(6)});
 const hex = value => '#'+value.match(/[\d.]+/g).slice(0,3).map(v=>(+v).toString(16).padStart(2,'0')).join('');
 const texts = [];
 for (const node of article.querySelectorAll('[data-text]')) {
   const walk = document.createTreeWalker(node, NodeFilter.SHOW_TEXT);
   const fragments = []; let tn;
   while (tn = walk.nextNode()) {
     for(let i=0;i<tn.textContent.length;i++) {
       const range=document.createRange(); range.setStart(tn,i);range.setEnd(tn,i+1);
       const rects=[...range.getClientRects()];
       const r=rects.find(r=>r.height>0 && r.width>0);
       if(r) fragments.push({c:tn.textContent[i],r});
     }
   }
   const groups=[];
   for(const f of fragments) {
     const middle=f.r.top+f.r.height/2;
     let g=groups.find(g=>Math.abs(g.middle-middle)<4);
     if(!g) {g={middle,chars:'',left:f.r.left,top:f.r.top,right:f.r.right,bottom:f.r.bottom};groups.push(g);}
     g.chars+=f.c;g.left=Math.min(g.left,f.r.left);g.top=Math.min(g.top,f.r.top);
     g.right=Math.max(g.right,f.r.right);g.bottom=Math.max(g.bottom,f.r.bottom);
   }
   const s=getComputedStyle(node), bounds=node.getBoundingClientRect();
   const leading=parseFloat(s.lineHeight);
   // Empty forced lines have no glyph Range. The rendered block still occupies
   // their line boxes, so retain them when counting the layout's actual lines.
   const lineCount=Math.max(groups.length, Math.round(bounds.height/leading));
   const lines=Array.from({length:lineCount},(_,i)=>({texto:'',
     caixa:rr({left:bounds.left,top:bounds.top+i*leading,width:0,height:leading})}));
   for(const g of groups.sort((a,b)=>a.middle-b.middle)) {
     const index=Math.max(0,Math.min(lineCount-1,Math.floor((g.middle-bounds.top)/leading)));
     lines[index]={texto:g.chars.trim(),
       caixa:rr({left:g.left,top:g.top,width:g.right-g.left,height:g.bottom-g.top})};
   }
   const strong=[...node.querySelectorAll('strong')].map(n=>({texto:n.textContent,
      peso:getComputedStyle(n).fontWeight,caixa:rr(n.getBoundingClientRect())}));
   texts.push({campo:node.dataset.text,conteudo:node.innerText,linhas:lines.map(l=>l.texto),
     caixas_das_linhas:lines.map(l=>l.caixa),quantidade_linhas:lines.length,
     estilo:node.dataset.style,cor:hex(s.color),caixa:rr(node.getBoundingClientRect()),
     alinhamento_canva:node.dataset.text==='referencia'?'end':['selo','data'].includes(node.dataset.text)?'start':'center',
     fonte:s.fontFamily.split(',')[0].replaceAll('"',''),peso:s.fontWeight,
     tamanho_px:parseFloat(s.fontSize),entrelinha_px:parseFloat(s.lineHeight),
     tracking_px:s.letterSpacing==='normal'?0:parseFloat(s.letterSpacing),destaques:strong});
 }
 const box = sel => {const n=article.querySelector(sel);return n?rr(n.getBoundingClientRect()):null};
 return {textos:texts,caixas:{nicho:box('.aqr-nicho'),obra:box('.aqr-nicho__obra'),
   logo:box('[data-element="logo"]'),selo:box('.aqr-selo'),referencia:box('.aqr-topo__info'),
   cruz:box('.aqr-selo__cruz'),bloco_texto:box('.aqr-texto')}};
}"""


def _measure(page, number: int, kind: int) -> dict:
    measured = page.evaluate(_TEXT_JS)
    measured.update({'card': number, 'tipo': NAMES[kind], 'modelo': kind,
                     'tema': 'pergaminho' if kind == 4 else 'capela',
                     'largura': 1080, 'altura': 1350,
                     'elementos': measure_page(page, number, NAMES[kind])['elements']})
    return measured


def _distance(a: dict, b: dict) -> float:
    dx=max(a['x']-b['x']-b['largura'],b['x']-a['x']-a['largura'],0)
    dy=max(a['y']-b['y']-b['altura'],b['y']-a['y']-a['altura'],0)
    return hypot(dx,dy)


def _validate_layout(day: dict, card: dict) -> dict:
    errors=[]; distances=[]
    for text in card['textos']:
        field=text['campo']; limit=LIMITS.get(field)
        if field == 'trecho': limit=3 if text['estilo']=='citacao-grande' else 4
        if limit and text['quantidade_linhas']>limit:
            errors.append(f'{day["data"]}, card {card["card"]}, {field}: {text["quantidade_linhas"]} linhas; limite {limit}.')
        for line in text['linhas']:
            if re.search(r'(?:^|\s)[aàeéoAÀEÉO][\W_]*$',line):
                errors.append(f'{day["data"]}, card {card["card"]}, {field}: palavra de uma letra no fim de {line!r}.')
        distance=_distance(text['caixa'],card['caixas']['logo'])
        distances.append({'campo':field,'logo_px':round(distance,6)})
        if distance < 32-0.01:
            errors.append(f'{day["data"]}, card {card["card"]}, {field}: distância ao logo {distance:.2f}px < 32px.')
        box=text['caixa']
        if box['x'] < 0 or box['y'] < 0 or box['x']+box['largura']>1080.01 or box['y']+box['altura']>1350.01:
            errors.append(f'{day["data"]}, card {card["card"]}, {field}: texto fora da arte.')
        for linebox in text['caixas_das_linhas']:
            if not linebox['largura']:
                continue
            if linebox['x'] < box['x']-0.1 or linebox['x']+linebox['largura'] > box['x']+box['largura']+0.1:
                errors.append(f'{day["data"]}, card {card["card"]}, {field}: linha transborda a largura do campo ({box["largura"]:g}px).')
            if linebox['x'] < -0.1 or linebox['y'] < -0.1 or linebox['x']+linebox['largura']>1080.1 or linebox['y']+linebox['altura']>1350.1:
                errors.append(f'{day["data"]}, card {card["card"]}, {field}: linha fora da arte.')
            if _distance(linebox,card['caixas']['logo']) < 32-0.01:
                errors.append(f'{day["data"]}, card {card["card"]}, {field}: linha a menos de 32px do logo.')
    top=_distance(card['caixas']['selo'],card['caixas']['referencia'])
    if top<32-0.01:
        errors.append(f'{day["data"]}, card {card["card"]}: selo e referência distam {top:.2f}px < 32px.')
    center=None
    if card['caixas']['bloco_texto']:
        block=card['caixas']['bloco_texto'];seal=card['caixas']['selo'];logo=card['caixas']['logo']
        upper=block['y']-(seal['y']+seal['altura']);lower=logo['y']-(block['y']+block['altura'])
        center={'respiro_superior_px':upper,'respiro_inferior_px':lower,'diferenca_px':abs(upper-lower)}
        if abs(upper-lower)>0.1: errors.append(f'{day["data"]}, card {card["card"]}: bloco de texto não centralizado.')
    result={'ok':not errors,'distancias_ao_logo':distances,'selo_referencia_px':top,
            'centralizacao_vertical':center,'errors':errors}
    if errors: raise ValueError('; '.join(errors))
    return result


def _pixels(path: Path, day: dict, card: dict) -> dict:
    samples=[];errors=[]
    with Image.open(path) as raw:
        image=raw.convert('RGB')
        def sample(label,x,y,value):
            point=(int(x),int(y));actual=image.getpixel(point);expected=ImageColor.getrgb(value)
            ok=actual==expected
            samples.append({'elemento':label,'pixel':list(point),'esperado':value,
                            'rgb':list(actual),'ok':ok})
            if not ok:errors.append(f'{day["data"]}, card {card["card"]}, {label}: pixel {actual}, esperado {expected}.')
        cross=card['caixas']['cruz'];on_color=card['modelo']==4
        expected=color('sobre-cor','pergaminho') if on_color else color(color_token(day['cor']),'capela')
        sample('cruz do selo',cross['x']+9,cross['y']+18,expected)
        bg=color(color_token(day['cor']),'pergaminho') if on_color else color('fundo','capela')
        sample('fundo',8,8,bg)
    niche=None
    if card['caixas']['nicho']:
        b=card['caixas']['nicho']
        niche=validate_niche_pixels(path,[{'name':'nicho','x':b['x'],'y':b['y'],
            'width':b['largura'],'height':b['altura'],'background':color('fundo','capela'),
            'filete':color(color_token(day['cor']),'capela')}])
        errors.extend(niche['errors'])
    result={'ok':not errors,'amostras':samples,'nicho':niche,'errors':errors}
    if errors:raise ValueError('; '.join(errors))
    return result


def _pdf_check(path: Path, day: dict, count: int) -> dict:
    import fitz
    errors=[];pages=[];font_records={};combined=''
    with fitz.open(path) as doc:
        if len(doc)!=count:errors.append(f'{path.name}: {len(doc)} páginas; esperado {count}.')
        for index,page in enumerate(doc,1):
            text=page.get_text();combined+=' '+text
            pages.append({'pagina':index,'largura_pt':page.rect.width,'altura_pt':page.rect.height,
                          'caracteres_extraidos':len(text)})
            if abs(page.rect.width-810)>0.01 or abs(page.rect.height-1012.5)>0.01:
                errors.append(f'{path.name}, página {index}: formato PDF errado.')
            for font in page.get_fonts(full=True):
                xref,ext,kind,name=font[:4]
                if xref in font_records:continue
                _,real_ext,_,data=doc.extract_font(xref)
                clean=re.sub(r'^[A-Z]{6}\+','',name)
                font_records[xref]={'nome':clean,'tipo':kind,'formato':real_ext,'embutida':bool(data),'bytes':len(data)}
                if not data:errors.append(f'{path.name}: fonte não embutida: {name}.')
    normalized=' '.join(combined.replace('\xa0',' ').split())
    title=' '.join(day['titulo'].split())
    if title not in normalized:errors.append(f'{path.name}: título ausente do texto extraído.')
    if 'Abra sua Bíblia' not in normalized:errors.append(f'{path.name}: convite ausente do texto extraído.')
    names={font['nome'] for font in font_records.values()}
    missing=REQUIRED_FONTS-names
    if missing:errors.append('Fontes ausentes: '+', '.join(sorted(missing)))
    poppler=None
    if shutil.which('pdffonts'):
        process=subprocess.run(['pdffonts',str(path)],capture_output=True,text=True,check=False)
        poppler=process.stdout
        if process.returncode:errors.append('pdffonts falhou: '+process.stderr)
        for required in REQUIRED_FONTS:
            if required not in poppler:errors.append(f'pdffonts não lista {required}.')
        for line in poppler.splitlines()[2:]:
            match=re.search(r'\s(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$',line)
            if match and match.group(1)!='yes':errors.append('pdffonts: fonte não embutida '+line)
    else:errors.append('pdffonts indisponível.')
    result={'ok':not errors,'paginas':pages,'fontes':list(font_records.values()),
            'pdffonts':poppler,'titulo_extraivel':title in normalized,
            'convite_extraivel':'Abra sua Bíblia' in normalized,'errors':errors}
    if errors:raise ValueError('; '.join(errors))
    return result


def _crop_proof(artwork: Path, output: Path, focus: str) -> None:
    """Map the real CSS cover crop back onto the full 1080 px artwork."""
    with Image.open(artwork) as raw:
        raw.load();source=raw.convert('RGB');w,h=source.size
        full=source.resize((1080,round(h*1080/w)),Image.Resampling.LANCZOS)
    tw,th=648,744;scale=max(tw/w,th/h)
    values=focus.split();keywords={'left':0,'top':0,'center':50,'right':100,'bottom':100}
    def percent(value):return float(value[:-1]) if value.endswith('%') else keywords[value]
    fx=percent(values[0])/100;fy=percent(values[1] if len(values)>1 else '50%')/100
    ox=(w*scale-tw)*fx;oy=(h*scale-th)*fy
    def inverse(x,y):return ((x+ox)/scale*1080/w,(y+oy)/scale*1080/w)
    curve=[inverse(tw/2+tw/2*cos(pi+i*pi/240),tw/2+tw/2*sin(pi+i*pi/240)) for i in range(241)]
    curve += [inverse(tw,th),inverse(0,th),curve[0]]
    draw=ImageDraw.Draw(full);draw.line(curve,fill='#faf6ee',width=9,joint='curve');draw.line(curve,fill='#5b2e70',width=4,joint='curve')
    full.save(output)


def _font(size=24):
    return ImageFont.truetype(str(KIT/'fontes/Lato-Regular.ttf'),size)


def _board(rows: list[tuple[str,list[Path]]], path: Path, columns: int) -> tuple[int,int]:
    gap=24;left=32;top=52;rowheight=450+80
    size=(2*left+columns*360+(columns-1)*gap,32+len(rows)*rowheight)
    board=Image.new('RGB',size,color('fundo','pergaminho'));draw=ImageDraw.Draw(board)
    for ri,(label,images) in enumerate(rows):
        y=32+ri*rowheight;draw.text((left,y),label,font=_font(24),fill=color('tinta','pergaminho'))
        for ci,image_path in enumerate(images):
            with Image.open(image_path) as image:
                board.paste(image.convert('RGB').resize((360,450),Image.Resampling.LANCZOS),(left+ci*(360+gap),y+top))
    board.save(path);return size


def _relpath(path: Path, output: Path) -> str:
    return path.relative_to(output).as_posix()


def _report(output: Path, records: list[dict], checks: dict, pending: list[str]) -> Path:
    lines=['# Evangelho do Dia','',
           '`python gerar.py evangelho` · seleção: `python gerar.py evangelho --data AAAA-MM-DD`','',
           '## Decisões','',
           '- Composição, medidas e espaços seguem PostEvangelho/preview.html e bundle.css; a capa usa um img dentro do arco CSS, sem SVG sobre a imagem.',
           '- O card final resolve a cor no tema pergaminho e usa o logo sobre-cor da versão 2. Os demais usam capela.',
           '- Textos sem quebras manuais usam balanceamento do navegador, inclusive o corpo da reflexão. Quebras YAML são `<br>`; espaços após a, à, e, é e o são inseparáveis.',
           '- O selo tem ficha separada para série e data porque as cores e pesos diferem. As caixas são do DOM e as linhas são medidas com Range, depois do carregamento das seis fontes locais.',
           '- A prancha de cores usa ouro como alias de liturgico-branco. As miniaturas medem exatamente 360 × 450 px; etiquetas ficam fora dos cards. A prancha principal indexa todas as datas já geradas, preservando as demais ao usar --data.',
           '- Só obras reais recebem recorte.png; nenhum recurso externo é acessado. Os HTML e PDFs de uma página usados na composição ficam em work/ e não são necessários para importar os PDFs finais.','',
           '## Linhas medidas no render','',
           '| Data | Card | Campo | Estilo | Linhas | Limite |',
           '| --- | --- | --- | --- | --- | --- |']
    for record in records:
        for card in record['cards']:
            for text in card['textos']:
                field=text['campo'];limit=LIMITS.get(field,'—')
                if field=='trecho':limit=3 if text['estilo']=='citacao-grande' else 4
                lines.append(f'| {record["data"]} | {card["card"]} | {field} | {text["estilo"]} | {text["quantidade_linhas"]} | {limit} |')
    lines += ['', '## Obras e legendas', '']
    for record in records:
        lines += [f'- **{record["data"]} — {record["celebracao"]}:** '+('obra pendente; foi usada obra-provisoria.png.' if record['obra_pendente'] else 'obra local real; recorte.png gerado.'),
                  f'  {record["obra"]["credito"]} — {record["obra"]["pagina"]}']
    lines += ['', '## Conferência', '',
              'PNG exatos; limites de linhas; palavras de uma letra; afastamento de 32 px; centralização vertical; cruz, fundo e filete por pixel; páginas PDF de 810 × 1012,5 pt; quatro variantes embutidas por pdffonts; título e convite extraíveis. Os valores estão em verificacao.json e ficha.json.',
              '', 'A importação dentro do editor do Canva não foi executada; a validação cobre o arquivo produzido (texto, fontes e dimensões), não o comportamento do editor.']
    if pending:
        lines += ['', 'Obras pendentes: '+', '.join(pending)+'. Não foi possível verificar seus focos nem gerar recortes reais; o lugar delas foi preservado com a obra provisória.']
    else:
        lines += ['', 'Todas as obras selecionadas foram encontradas localmente e receberam prova de recorte.']
    lines += ['', '## Árvore', '', '```text', 'saida/evangelho/']
    paths={child.relative_to(output).as_posix() for child in output.rglob('*') if child.is_file()}
    paths.add('RELATORIO.md')
    lines += ['  '+name for name in sorted(paths)]
    lines += ['```','']
    path=output/'RELATORIO.md';path.write_text('\n'.join(lines),encoding='utf-8');return path


def generate(output: Path, content_path: Path, date_filter: str | None = None) -> dict:
    """Generate final carousels, measurable fixtures and preview boards."""
    output=Path(output).resolve();target=output/'evangelho';target.mkdir(parents=True,exist_ok=True)
    days=load_content(content_path)
    if date_filter is not None:
        days=[day for day in days if day['data']==date_filter]
        if not days:raise ValueError(f'Nenhum conteúdo para --data {date_filter}.')
    kit_check=validate_kit(PROJECT)
    if not kit_check['ok']:raise ValueError('Kit inválido: '+'; '.join(kit_check['errors']))
    css=generate_tokens_css(output/'tokens.css');placeholder=output/'obra-provisoria.png'
    if not placeholder.is_file():raise FileNotFoundError('Obra provisória ausente; execute python gerar.py componentes.')
    work=PROJECT/'work/evangelho';work.mkdir(parents=True,exist_ok=True)
    expected={};records=[];checks={'kit':kit_check,'dias':{}};browser_errors=[]
    with local_server() as base_url,sync_playwright() as playwright:
        browser=playwright.chromium.launch(executable_path=shutil.which('chromium') or '/usr/bin/chromium',
                                           headless=True,args=['--no-sandbox'])
        context=browser.new_context(device_scale_factor=1)
        context.route('**/*',lambda route:route.continue_() if urlsplit(route.request.url).netloc==urlsplit(base_url).netloc else route.abort())
        page=context.new_page();page.on('pageerror',lambda error:browser_errors.append(str(error)))
        page.on('console',lambda message:browser_errors.append(message.text) if message.type=='error' else None)
        page.on('response',lambda response:browser_errors.append(f'HTTP {response.status}: {response.url}') if response.status>=400 else None)
        for day in days:
            folder=target/day['data'];folder.mkdir(parents=True,exist_ok=True)
            artwork=PROJECT/day['obra']['arquivo'];pending=not artwork.is_file()
            if pending:artwork=placeholder
            kinds=[1,2]+([3] if day.get('reflexao') else [])+[4]
            cards=[];pdf_parts=[];daychecks=[]
            for number,kind in enumerate(kinds,1):
                quote_style='citacao-grande';png=folder/f'card-{number}.png'
                temporary=work/day['data']/f'card-{number}.png'
                part=temporary.with_suffix('.pdf')
                markup=_document(day,kind,css,artwork,quote_style)
                render_arte(page,markup,temporary,pdf_path=part,base_url=base_url)
                card=_measure(page,number,kind)
                quote=next((t for t in card['textos'] if t['campo']=='trecho'),None)
                if quote and quote['quantidade_linhas']>3:
                    markup=_document(day,kind,css,artwork,'citacao')
                    render_arte(page,markup,temporary,pdf_path=part,base_url=base_url)
                    card=_measure(page,number,kind)
                layout=_validate_layout(day,card)
                shutil.copyfile(temporary,png);expected[str(png)]=(1080,1350)
                pixel=_pixels(png,day,card);daychecks.append({'card':number,'layout':layout,'pixels':pixel})
                cards.append(card);pdf_parts.append(part)
            pdf=folder/f'evangelho-{day["data"]}.pdf';writer=PdfWriter()
            for part in pdf_parts:
                reader=PdfReader(part)
                for pdfpage in reader.pages:writer.add_page(pdfpage)
            with pdf.open('wb') as stream:writer.write(stream)
            pdfcheck=_pdf_check(pdf,day,len(cards))
            if not pending:
                _crop_proof(artwork,folder/'recorte.png',day['obra']['foco'])
                with Image.open(folder/'recorte.png') as image:expected[str(folder/'recorte.png')]=image.size
            elif (folder/'recorte.png').exists():(folder/'recorte.png').unlink()
            # A rerun after removing a reflection must not leave a stale card-4.
            for old in folder.glob('card-*.png'):
                if int(old.stem.split('-')[-1])>len(cards):old.unlink()
            record={'data':day['data'],'celebracao':day['celebracao'],'cor':day['cor'],
                    'referencia':day['referencia'],'obra':day['obra'],'obra_pendente':pending,
                    'obra_usada':artwork.relative_to(PROJECT).as_posix(),'cards':cards}
            (folder/'ficha.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            records.append(record);checks['dias'][day['data']]={'cards':daychecks,'pdf':pdfcheck}
        # Refresh the board from every generated date, including dates untouched by
        # --data, so the board remains a useful index of the output directory.
        rows=[]
        for ficha in sorted(target.glob('????-??-??/ficha.json')):
            record=json.loads(ficha.read_text(encoding='utf-8'))
            label=f'{record["data"]} · {record["cor"]}'+(' · obra pendente' if record['obra_pendente'] else '')
            rows.append((label,[ficha.parent/f'card-{c["card"]}.png' for c in record['cards']]))
        expected[str(target/'prancha.png')]=_board(rows,target/'prancha.png',max(len(row[1]) for row in rows))
        # The colour proof always uses the actual 29 November content.
        base=next((day for day in load_content(content_path) if day['data']=='2026-11-29'),None)
        if base:
            colorrows=[]
            for cor in ['verde','roxo','ouro','vermelho','rosa']:
                variant=deepcopy(base);variant['cor']=cor;art=PROJECT/variant['obra']['arquivo']
                if not art.is_file():art=placeholder
                images=[]
                for kind in (1,4):
                    path=work/'cores'/f'{cor}-card-{kind}.png'
                    render_arte(page,_document(variant,kind,css,art),path,base_url=base_url)
                    card=_measure(page,kind,kind);_validate_layout(variant,card);_pixels(path,variant,card)
                    images.append(path)
                colorrows.append((f'{cor} · 2026-11-29'+(' · obra pendente' if art==placeholder else ''),images))
            expected[str(target/'prancha-cores.png')]=_board(colorrows,target/'prancha-cores.png',2)
        browser.close()
    if browser_errors:raise RuntimeError('Erros de navegador: '+'; '.join(browser_errors))
    checks['pngs']=validate_pngs(expected)
    checks['kit_final']=validate_kit(PROJECT)
    checks['browser']={'ok':True,'errors':[],'fontes_locais_por_render':6,'recursos_externos':False}
    checks['ok']=all(checks[key]['ok'] for key in ('kit','kit_final','pngs'))
    if not checks['ok']:raise RuntimeError('Falha de validação de PNG ou kit.')
    pending=[record['data'] for record in records if record['obra_pendente']]
    checks['obras_pendentes']=pending
    (target/'verificacao.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report=_report(target,records,checks,pending)
    return {'dias':len(records),'cards':sum(len(r['cards']) for r in records),
            'pdfs':len(records),'pngs':len(expected),'obras_pendentes':pending,
            'relatorio':str(report),'verificacoes':str(target/'verificacao.json')}
