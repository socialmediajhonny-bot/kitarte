"""Santo do Dia: santinhos e festas fiéis aos modelos locais do kit v3."""
from __future__ import annotations

from html import escape
import json
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any
from urllib.parse import urlsplit

from PIL import Image, ImageColor, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

from .base import (PROJECT, KIT, assinatura, color, generate_tokens_css,
                   html_document, montar_arte, nicho, render_arte, selo)
from .conteudo import color_token, date_label, local_artwork_path
from .conteudo_santo import load_saints
from .evangelho import _crop_proof, _distance, _measure as measure_evangelho, _ornament, _text
from .renderizacao import local_server
from .validacao import validate_kit, validate_niche_pixels, validate_pngs


SIZES = {'santinho': (340, 420), 'festa': (600, 680)}
EXTRA_CSS = '@page{margin:0;} .aqr-credito{max-width:920px;}'


def _header(day: dict) -> str:
    """Use the common seal, retaining its distinct date colour and weight."""
    series = 'Santo do Dia' if day['tipo'] == 'santinho' else day['grau']
    support = day['grau'] if day['tipo'] == 'santinho' else None
    markup = selo(series, date_label(day['data']), support)
    for original, field in [('selo-serie', 'selo'), ('selo-data', 'data'), ('selo-info', 'grau')]:
        markup = markup.replace(f'data-element="{original}"',
                                f'data-element="{original}" data-text="{field}" data-style="selo"')
    return markup


def _image(day: dict, artwork: Path) -> str:
    width, height = SIZES[day['tipo']]
    markup = nicho(width, height, artwork)
    if day['tipo'] == 'festa':
        markup = markup.replace(f'style="width:{width}px;height:{height}px;"',
                                f'style="width:{width}px;height:{height}px;margin-top:var(--espaco-3)"')
    markup = markup.replace('alt="Obra provisória"', 'alt="' + escape(day['nome'], quote=True) + '"')
    return markup.replace('data-arquivo="obra-provisoria.png"',
                          f'data-arquivo="{escape(artwork.relative_to(PROJECT).as_posix(), quote=True)}" '
                          f'style="object-position:{escape(day["obra"]["foco"], quote=True)}"')


def _document(day: dict, css: Path, artwork: Path) -> str:
    image = _image(day, artwork)
    if day['tipo'] == 'santinho':
        content = '<div class="aqr-santinho" data-element="cartao">' + image
        content += _text('h1', 'nome', 'titulo aqr-titulo', day['nome'],
                         'margin-top:var(--espaco-4);max-width:100%')
        content += _text('p', 'titulo', 'corpo aqr-suave', day['titulo'],
                         'margin-top:var(--espaco-1);max-width:100%', 'tinta-suave')
        content += _ornament()
        content += _text('p', 'frase', 'citacao aqr-citacao', '“' + day['frase'] + '”', 'max-width:700px')
        content += _text('p', 'fonte', 'credito aqr-credito', day['fonte'],
                         'margin-top:var(--espaco-2);max-width:100%', 'tinta-suave')
        content += '</div><div style="height:var(--espaco-3);flex:none"></div>'
    else:
        content = image + _text('p', 'credito', 'credito aqr-credito', day['obra']['credito'],
                                'margin-top:var(--espaco-3)', 'tinta-suave')
        content += _text('h1', 'nome', 'titulo-capa aqr-titulo', day['nome'],
                         'margin-top:var(--espaco-4);max-width:880px;text-align:center')
    post = montar_arte(_header(day) + content + assinatura('pergaminho'),
                       tema='pergaminho', cor_do_dia=color_token(day['cor']))
    return html_document(post, css, EXTRA_CSS, f'Santo do Dia · {day["data"]} · {day["nome"]}')


_CARD_JS = r"""() => {
 const root=document.querySelector('.aqr-post').getBoundingClientRect();
 const card=document.querySelector('.aqr-santinho');
 if(!card) return null;
 const s=getComputedStyle(card), r=card.getBoundingClientRect();
 const p=v=>parseFloat(v)||0, round=v=>+v.toFixed(6);
 const box=(x,y,w,h)=>({x:round(x-root.left),y:round(y-root.top),largura:round(w),altura:round(h)});
 const border={top:p(s.borderTopWidth),right:p(s.borderRightWidth),bottom:p(s.borderBottomWidth),left:p(s.borderLeftWidth)};
 const padding={top:p(s.paddingTop),right:p(s.paddingRight),bottom:p(s.paddingBottom),left:p(s.paddingLeft)};
 const inner=box(r.left+border.left+padding.left,r.top+border.top+padding.top,
   r.width-border.left-border.right-padding.left-padding.right,
   r.height-border.top-border.bottom-padding.top-padding.bottom);
 const a=getComputedStyle(card,'::before');
 const frame=box(r.left+border.left+p(a.left),r.top+border.top+p(a.top),p(a.width),p(a.height));
 const nodes=[...card.querySelectorAll('[data-element]')].map(n=>({elemento:n.dataset.element,
   caixa:box(n.getBoundingClientRect().left,n.getBoundingClientRect().top,n.getBoundingClientRect().width,n.getBoundingClientRect().height)}));
 return {caixa:box(r.left,r.top,r.width,r.height),area_interna:inner,filete_interno:frame,
  padding_px:padding,borda_px:border,cor_moldura:s.borderTopColor,cor_filete_interno:a.borderTopColor,
  filete_espessura_px:p(a.borderTopWidth),fundo:s.backgroundColor,
  scroll_width_px:card.scrollWidth,client_width_px:card.clientWidth,
  scroll_height_px:card.scrollHeight,client_height_px:card.clientHeight,elementos:nodes};
}"""


def _measure(page: Any, day: dict) -> dict:
    measured = measure_evangelho(page, 1, 1)
    measured.update({'tipo': day['tipo'], 'modelo': 'PostSanto' if day['tipo'] == 'santinho' else 'PostFesta',
                     'tema': 'pergaminho'})
    for text in measured['textos']:
        if text['campo'] == 'grau':
            text['alinhamento_canva'] = 'end'
    card = page.evaluate(_CARD_JS)
    measured['cartao'] = card
    measured['caixas'].update({'cartao': card['caixa'] if card else None,
                              'cartao_area_interna': card['area_interna'] if card else None,
                              'cartao_filete_interno': card['filete_interno'] if card else None})
    if card:
        for name, box in [('cartao-area-interna', card['area_interna']), ('cartao-filete-interno', card['filete_interno'])]:
            measured['elementos'].append({'element': name, 'kind': 'container' if name.endswith('area-interna') else 'pseudo',
                'x': box['x'], 'y': box['y'], 'width': box['largura'], 'height': box['altura'],
                'hex': color('ouro', 'pergaminho') if name.endswith('filete-interno') else None,
                'measurement': 'getComputedStyle + host.getBoundingClientRect'})
    return measured


def _inside(inner: dict, box: dict, tolerance=0.1) -> bool:
    return (box['x'] >= inner['x']-tolerance and box['y'] >= inner['y']-tolerance
            and box['x']+box['largura'] <= inner['x']+inner['largura']+tolerance
            and box['y']+box['altura'] <= inner['y']+inner['altura']+tolerance)


def _limits(day: dict) -> dict[str, int]:
    return {'nome': 1, 'titulo': 1, 'frase': 3, 'fonte': 1} if day['tipo'] == 'santinho' else {'nome': 2, 'credito': 1}


def _validate_layout(day: dict, measured: dict) -> dict:
    errors = []; distances = []; limits = _limits(day)
    art = {'x': 0, 'y': 0, 'largura': 1080, 'altura': 1350}
    logo = measured['caixas']['logo']
    for text in measured['textos']:
        field = text['campo']; limit = limits.get(field)
        if limit is not None and text['quantidade_linhas'] > limit:
            errors.append(f'{day["data"]}, {field}: {text["quantidade_linhas"]} linhas; limite {limit}.')
        if not _inside(art, text['caixa']):
            errors.append(f'{day["data"]}, {field}: caixa fora da arte.')
        for line, box in zip(text['linhas'], text['caixas_das_linhas']):
            if re.search(r'(?:^|\s)[aàeéoAÀEÉO][\W_]*$', line):
                errors.append(f'{day["data"]}, {field}: palavra de uma letra no fim de {line!r}.')
            if box['largura'] and (box['x'] < text['caixa']['x']-0.1 or box['x']+box['largura'] > text['caixa']['x']+text['caixa']['largura']+0.1):
                errors.append(f'{day["data"]}, {field}: linha transborda a largura do campo.')
            if not _inside(art, box):
                errors.append(f'{day["data"]}, {field}: linha fora da arte.')
            if measured['cartao'] and field in limits and not _inside(measured['cartao']['area_interna'], box):
                errors.append(f'{day["data"]}, {field}: linha fora da área interna do cartão descontado o padding.')
        distance = _distance(text['caixa'], logo)
        distances.append({'campo': field, 'logo_px': round(distance, 6)})
        if distance < 31.99:
            errors.append(f'{day["data"]}, {field}: distância ao logo {distance:.2f}px < 32px.')
    top = None
    if measured['caixas']['referencia']:
        top = _distance(measured['caixas']['selo'], measured['caixas']['referencia'])
        if top < 31.99: errors.append(f'{day["data"]}, grau: distância ao selo {top:.2f}px < 32px.')
    card_check = None
    if measured['cartao']:
        card = measured['cartao']; area = card['area_interna']; frame = card['filete_interno']
        gaps = []
        for element in card['elementos']:
            if not _inside(area, element['caixa']):
                errors.append(f'{day["data"]}, {element["elemento"]}: conteúdo fora da área interna do cartão descontado o padding.')
            box = element['caixa']
            margins = {'esquerda': box['x']-frame['x'], 'topo': box['y']-frame['y'],
                       'direita': frame['x']+frame['largura']-box['x']-box['largura'],
                       'base': frame['y']+frame['altura']-box['y']-box['altura']}
            if min(margins.values()) <= card['filete_espessura_px']:
                errors.append(f'{day["data"]}, {element["elemento"]}: conteúdo encosta no filete interno.')
            gaps.append({'elemento': element['elemento'], 'distancias_filete_interno_px': margins})
        if card['scroll_width_px'] > card['client_width_px'] or card['scroll_height_px'] > card['client_height_px']:
            errors.append(f'{day["data"]}: conteúdo transborda o cartão.')
        niche = measured['caixas']['nicho']
        # The sill projects 48 px to either side of the niche and 3 px below it.
        sill = {'x': niche['x']-48, 'y': niche['y']+niche['altura'], 'largura': niche['largura']+96, 'altura': 3}
        if not _inside(area, sill): errors.append(f'{day["data"]}: parapeito fora da área interna do cartão.')
        card_check = {'area_interna': area, 'padding_px': card['padding_px'], 'elementos': gaps,
                      'parapeito_na_area_interna': _inside(area, sill), 'sem_transbordamento': True}
    result = {'ok': not errors, 'limites': limits, 'distancias_ao_logo': distances,
              'selo_grau_px': top, 'cartao': card_check, 'errors': errors}
    if errors: raise ValueError('; '.join(errors))
    return result


def _pixels(path: Path, day: dict, measured: dict) -> dict:
    samples = []; errors = []
    with Image.open(path) as raw:
        image = raw.convert('RGB')
        def sample(name: str, x: float, y: float, expected: str):
            point = (int(x), int(y)); actual = image.getpixel(point); wanted = ImageColor.getrgb(expected)
            record = {'elemento': name, 'pixel': list(point), 'esperado': expected,
                      'rgb': list(actual), 'ok': actual == wanted}
            samples.append(record)
            if not record['ok']: errors.append(f'{day["data"]}, {name}: pixel {actual}, esperado {wanted}.')
        cross = measured['caixas']['cruz']; liturgy = color(color_token(day['cor']), 'pergaminho')
        sample('cruz do selo', cross['x']+9, cross['y']+18, liturgy)
        sample('fundo da arte', 8, 8, color('fundo', 'pergaminho'))
        if measured['cartao']:
            card = measured['cartao']; outer = card['caixa']; inner = card['filete_interno']; gold = color('ouro', 'pergaminho')
            for name, box, inset in [('moldura externa', outer, 1), ('filete interno', inner, 0)]:
                sample(name+' topo', box['x']+box['largura']/2, box['y']+inset, gold)
                sample(name+' base', box['x']+box['largura']/2, box['y']+box['altura']-1-inset, gold)
                sample(name+' esquerda', box['x']+inset, box['y']+box['altura']/2, gold)
                sample(name+' direita', box['x']+box['largura']-1-inset, box['y']+box['altura']/2, gold)
            sample('papel do cartão', outer['x']+24, outer['y']+24, color('papel', 'pergaminho'))
    box = measured['caixas']['nicho']
    niche = validate_niche_pixels(path, [{'name': 'nicho', 'x': box['x'], 'y': box['y'],
        'width': box['largura'], 'height': box['altura'], 'filete': liturgy,
        'background': color('papel' if measured['cartao'] else 'fundo', 'pergaminho')}])
    errors.extend(niche['errors'])
    result = {'ok': not errors, 'amostras': samples, 'nicho': niche, 'errors': errors}
    if errors: raise ValueError('; '.join(errors))
    return result


def _pdf_check(path: Path, day: dict, measured: dict) -> dict:
    import fitz
    errors = []; fonts = {}; pages = []; combined = ''
    required = {'CormorantGaramond-SemiBold', 'Lato-Bold', 'Lato-Regular'}
    if day['tipo'] == 'santinho': required.add('CormorantGaramond-MediumItalic')
    with fitz.open(path) as document:
        if len(document) != 1: errors.append(f'{day["data"]}: PDF deve ter uma página.')
        for page in document:
            text = page.get_text(); combined += ' '+text
            pages.append({'largura_pt': page.rect.width, 'altura_pt': page.rect.height, 'caracteres_extraidos': len(text)})
            if abs(page.rect.width-810) > .01 or abs(page.rect.height-1012.5) > .01:
                errors.append(f'{day["data"]}: formato PDF diferente de 810 × 1012,5 pt.')
            for info in page.get_fonts(full=True):
                xref, _, kind, name = info[:4]
                if xref in fonts: continue
                _, extension, _, data = document.extract_font(xref)
                name = re.sub(r'^[A-Z]{6}\+', '', name)
                embedded_ttf = bool(data) and extension.lower() in {'ttf','ttc'} and data[:4] in {b'\x00\x01\x00\x00', b'true', b'ttcf'}
                fonts[xref] = {'nome': name, 'tipo': kind, 'formato': extension,
                               'embutida': bool(data), 'truetype': embedded_ttf, 'bytes': len(data)}
                if not embedded_ttf: errors.append(f'{day["data"]}: fonte TTF não embutida: {name}.')
    normalize = lambda text: ' '.join(text.replace('\xa0', ' ').split())
    extracted = normalize(combined); fields = []
    for text in measured['textos']:
        expected = normalize(' '.join(text['linhas']))
        found = expected in extracted
        fields.append({'campo': text['campo'], 'conteudo': expected, 'extraivel': found})
        if not found: errors.append(f'{day["data"]}, {text["campo"]}: texto ausente na extração do PDF.')
    missing = required-{font['nome'] for font in fonts.values()}
    if missing: errors.append(f'{day["data"]}: fontes ausentes: '+', '.join(sorted(missing)))
    poppler = None
    if shutil.which('pdffonts'):
        process = subprocess.run(['pdffonts', str(path)], capture_output=True, text=True, check=False)
        poppler = process.stdout
        if process.returncode: errors.append('pdffonts falhou: '+process.stderr)
        for required_name in required:
            if required_name not in poppler: errors.append(f'pdffonts não lista {required_name}.')
        for line in poppler.splitlines()[2:]:
            match = re.search(r'\s(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$', line)
            if match and match.group(1) != 'yes': errors.append('pdffonts: fonte não embutida '+line)
    else: errors.append('pdffonts indisponível.')
    result = {'ok': not errors, 'paginas': pages, 'fontes': list(fonts.values()),
              'fontes_exigidas': sorted(required), 'textos': fields, 'pdffonts': poppler, 'errors': errors}
    if errors: raise ValueError('; '.join(errors))
    return result


def _board(target: Path) -> tuple[int, int]:
    records = [(path, json.loads(path.read_text(encoding='utf-8')))
               for path in sorted(target.glob('????-??-??/ficha.json'))]
    gap = 24; margin = 32; size = (margin*2+len(records)*360+(len(records)-1)*gap, 550)
    board = Image.new('RGB', size, color('fundo', 'pergaminho')); draw = ImageDraw.Draw(board)
    font = ImageFont.truetype(str(KIT/'fontes/Lato-Regular.ttf'), 20)
    for index, (path, record) in enumerate(records):
        x = margin+index*(360+gap)
        draw.text((x, 20), f'{record["data"]} · {record["tipo"]} · {record["cor"]}', font=font, fill=color('tinta','pergaminho'))
        if record['obra_pendente']:
            draw.text((x, 45), 'obra pendente', font=font, fill=color('tinta-suave','pergaminho'))
        with Image.open(path.parent/'card.png') as image:
            board.paste(image.convert('RGB').resize((360,450), Image.Resampling.LANCZOS), (x, 72))
    board.save(target/'prancha.png'); return size


def _regression_summary(output: Path) -> dict:
    path = output/'evangelho/conferencia-kit-v3.json'
    if not path.is_file():
        return {'verificado': False, 'arquivo': str(path.relative_to(PROJECT)),
                'resultado': 'A conferência de regressão do Evangelho deve ser consultada no relatório geral da etapa.'}
    return {'verificado': True, 'arquivo': str(path.relative_to(PROJECT)),
            'resultado': json.loads(path.read_text(encoding='utf-8'))}



def _regression_text(summary: dict) -> str:
    result = summary['resultado']
    if isinstance(result, str):
        return result
    rows = ['Conferência '+('aprovada.' if result.get('ok') else 'com diferenças a conferir.'),
            'Base: `'+result.get('baseline_commit','desconhecida')+'`.']
    components = result.get('componentes', {})
    images = components.get('pngs', [])
    if images:
        rows.append(f'Componentes: {sum(bool(image.get("pixels_identicos")) for image in images)}/{len(images)} PNGs com pixels idênticos.')
    for date, day in sorted(result.get('evangelho', {}).items()):
        cards = day.get('cards', [])
        identical = [str(card['card']) for card in cards if card.get('pixels_identicos')]
        cover = next((card for card in cards if card.get('card') == 1), {})
        content = 'textos, linhas, estilos e caixas '+('idênticos' if day.get('textos_linhas_estilos_caixas_identicos') else 'com diferenças')
        rows.append(f'{date}: {content}; cards '+', '.join(identical)+' com pixels idênticos; '
                    +('a capa mudou somente na área da obra real.' if cover.get('fora_da_obra_identico') else 'a capa deve ser consultada na conferência.'))
    if result.get('errors'):
        rows.append('Diferenças registradas: '+'; '.join(result['errors'])+'.')
    rows.append('Detalhes: [`CONFERENCIA-KIT-V3.md`](../evangelho/CONFERENCIA-KIT-V3.md) e '
                '[`conferencia-kit-v3.json`](../evangelho/conferencia-kit-v3.json).')
    return '\n\n'.join(rows)


def _report(target: Path, records: list[dict], checks: dict, command: str) -> Path:
    lines = ['# Santo do Dia', '', f'`{command}`', '', '## Decisões', '',
        '- Os dois modelos seguem os previews do kit v3: pergaminho, logo pergaminho, Nicho CSS com imagem trocável, foco do YAML e nenhuma sobreposição SVG.',
        '- Dentro do santinho, o conjunto obra e textos fica centralizado como no justify-content:center do kit. Frases de uma e três linhas mudam a altura do conjunto e, por isso, os nichos dos dois santos ficam em alturas diferentes.',
        '- Festa de santo permanece santinho, com Santo do Dia no selo e o grau à direita. A festa do Senhor ou de Nossa Senhora usa o grau como série, sem informação à direita.',
        '- A moldura dupla e o ornamento dos santinhos ficam em ouro, inclusive no mártir; só a cruz do selo e o filete do nicho seguem a cor litúrgica.',
        '- O crédito da obra dos santinhos fica na ficha e neste relatório para a legenda. Na festa, também aparece sob o nicho. As frases recebem aspas curvas sem modificar o YAML.',
        '- Quebras manuais viram <br>; as demais seguem o balanceamento do bundle.css. O espaço depois de a, à, e, é e o é inseparável. As linhas vazias forçadas também contam para os limites.',
        '- A ficha mantém o formato do Evangelho e acrescenta as caixas, o padding e os afastamentos da moldura do cartão. As linhas são medidas no DOM com Range, depois do carregamento das seis fontes locais.',
        '- A prancha usa miniaturas exatas de 360 × 450 px, lado a lado, e inclui todas as datas já geradas; --data preserva os arquivos das outras datas. HTMLs de apoio ficam em work/santo-do-dia.',
        '- Os PDFs mantêm texto extraível e as fontes usadas embutidas; a festa não recebe uma exigência artificial de fonte itálica.',
        '', '## Linhas medidas', '', '| Data | Campo | Estilo | Linhas | Limite |', '| --- | --- | --- | --- | --- |']
    for record in records:
        limits = _limits(record)
        for text in record['cards'][0]['textos']:
            lines.append(f'| {record["data"]} | {text["campo"]} | {text["estilo"]} | {text["quantidade_linhas"]} | {limits.get(text["campo"], "—")} |')
    lines += ['', '## Obras e legendas', '']
    pending = []
    for record in records:
        if record['obra_pendente']: pending.append(record['data'])
        state = 'obra pendente; provisória utilizada' if record['obra_pendente'] else 'obra real local; recorte.png gerado'
        lines += [f'- **{record["data"]} — {record["nome"]}:** {state}.',
                  f'  {record["obra"]["credito"]} — {record["obra"]["pagina"]}']
    lines += ['', 'Obras pendentes: '+(', '.join(pending) if pending else 'nenhuma')+'.',
        '', '## Conferências', '',
        'PNG 1080 × 1350; PDF de uma página em 810 × 1012,5 pt; textos extraíveis; TTF embutidos e pdffonts; limites de linhas e largura; palavras de uma letra; área interna e afastamento do filete; cruz, nicho e moldura por pixel. Os dados completos estão em verificacao.json e nas fichas.',
        '', '### Evangelho com o kit v3', '', _regression_text(checks['evangelho_kit_v3']),
        '', '### Limites da verificação', '',
        'A importação no editor do Canva não foi executada. A validação confere os arquivos produzidos, suas fontes, textos, cores e geometria. As obras foram usadas como entregues no repositório, sem downloads.',
        '', '## Árvore', '', '```text', 'saida/santo-do-dia/']
    names = {path.relative_to(target).as_posix() for path in target.rglob('*') if path.is_file()}; names.add('RELATORIO.md')
    lines += ['  '+name for name in sorted(names)] + ['```','']
    path = target/'RELATORIO.md'; path.write_text('\n'.join(lines),encoding='utf-8'); return path


def generate(output: Path, content_path: Path, date_filter: str | None = None) -> dict:
    output = Path(output).resolve(); target = output/'santo-do-dia'; target.mkdir(parents=True, exist_ok=True)
    days = load_saints(content_path)
    if date_filter is not None:
        days = [day for day in days if day['data'] == date_filter]
        if not days: raise ValueError(f'Nenhum conteúdo para --data {date_filter}.')
    kit = validate_kit(PROJECT)
    if not kit['ok']: raise ValueError('Kit inválido: '+'; '.join(kit['errors']))
    css = generate_tokens_css(output/'tokens.css'); placeholder = output/'obra-provisoria.png'
    if not placeholder.is_file(): placeholder = PROJECT/'saida/obra-provisoria.png'
    expected = {}; records = []; checks = {'kit': kit, 'dias': {}}; errors = []
    work = PROJECT/'work/santo-do-dia'
    with local_server() as base_url, sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=shutil.which('chromium') or '/usr/bin/chromium', headless=True, args=['--no-sandbox'])
        context = browser.new_context(device_scale_factor=1)
        context.route('**/*', lambda route: route.continue_() if urlsplit(route.request.url).netloc == urlsplit(base_url).netloc else route.abort())
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('console', lambda message: errors.append(message.text) if message.type == 'error' else None)
        page.on('response', lambda response: errors.append(f'HTTP {response.status}: {response.url}') if response.status >= 400 else None)
        for day in days:
            folder = target/day['data']; folder.mkdir(parents=True,exist_ok=True)
            artwork = local_artwork_path(day['obra']['arquivo']); pending = not artwork.is_file()
            if pending:
                if not placeholder.is_file(): raise FileNotFoundError('Obra provisória ausente; execute python gerar.py componentes.')
                artwork = placeholder
            temporary = work/day['data']/'card.png'; temporary_pdf = temporary.with_suffix('.pdf')
            render = render_arte(page, _document(day, css, artwork), temporary, pdf_path=temporary_pdf, base_url=base_url)
            measured = _measure(page, day); layout = _validate_layout(day, measured)
            pixels = _pixels(temporary, day, measured); pdfcheck = _pdf_check(temporary_pdf, day, measured)
            shutil.copyfile(temporary, folder/'card.png'); shutil.copyfile(temporary_pdf, folder/f'santo-{day["data"]}.pdf')
            expected[str(folder/'card.png')] = (1080,1350)
            if not pending:
                width, height = SIZES[day['tipo']]
                _crop_proof(artwork, folder/'recorte.png', day['obra']['foco'], niche_width=width, niche_height=height)
                with Image.open(folder/'recorte.png') as crop: expected[str(folder/'recorte.png')] = crop.size
            elif (folder/'recorte.png').exists(): (folder/'recorte.png').unlink()
            record = {key: day[key] for key in ('data','tipo','cor','grau','nome','obra')}
            record.update({'obra_pendente':pending,'obra_usada':artwork.relative_to(PROJECT).as_posix(),'cards':[measured]})
            (folder/'ficha.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            records.append(record); checks['dias'][day['data']] = {'layout':layout,'pixels':pixels,'pdf':pdfcheck,'fontes_render':render['fonts']}
        browser.close()
    if errors: raise RuntimeError('Erros de navegador: '+'; '.join(errors))
    expected[str(target/'prancha.png')] = _board(target)
    checks['pngs'] = validate_pngs(expected); checks['kit_final'] = validate_kit(PROJECT)
    checks['browser'] = {'ok':True,'errors':[],'fontes_locais_por_render':6,'recursos_externos':False}
    checks['obras_pendentes'] = [record['data'] for record in records if record['obra_pendente']]
    checks['evangelho_kit_v3'] = _regression_summary(output)
    checks['ok'] = all(checks[key]['ok'] for key in ('kit','kit_final','pngs'))
    if not checks['ok']: raise RuntimeError('Falha de validação de PNG ou kit.')
    command = 'python gerar.py santo' + (f' --data {date_filter}' if date_filter else '')
    checks['comando'] = command
    (target/'verificacao.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report = _report(target,records,checks,command)
    return {'dias':len(records),'cards':len(records),'pdfs':len(records),'pngs':len(expected),
            'obras_pendentes':checks['obras_pendentes'],'relatorio':str(report),
            'verificacoes':str(target/'verificacao.json')}
