"""Coragem em feed e status, com obras locais e composição do kit v4."""
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
from .conteudo_coragem import load_courage
from .evangelho import _measure as measure_evangelho, _text
from .obras import artwork_geometry, crop_proof, inspect_artwork
from .renderizacao import local_server
from .validacao import validate_kit, validate_niche_pixels, validate_pngs


FORMATS = {'feed': {'height': 1350, 'niche': (600, 680), 'base': 'feed'},
           'status': {'height': 1920, 'niche': (720, 900), 'base': 'story'}}


def _header(day: dict) -> str:
    markup = selo('Coragem', date_label(day['data']))
    for original, field in [('selo-serie', 'selo'), ('selo-data', 'data')]:
        markup = markup.replace(f'data-element="{original}"',
            f'data-element="{original}" data-text="{field}" data-style="selo"')
    return markup


def _document(day: dict, css: Path, artwork: Path, format_name: str) -> str:
    config = FORMATS[format_name]
    width, height = config['niche']
    image = nicho(width, height, artwork, foco=day['obra']['foco'], zoom=day['obra'].get('zoom', 1))
    image = image.replace(f'style="width:{width}px;height:{height}px;"',
        f'style="width:{width}px;height:{height}px;margin-top:var(--espaco-4)"')
    image = image.replace('alt="Obra provisória"', 'alt="Obra de Coragem"')
    image = image.replace('data-arquivo="obra-provisoria.png"',
        f'data-arquivo="{escape(artwork.relative_to(PROJECT).as_posix(), quote=True)}"')
    body = _header(day) + image + '<div class="aqr-texto" style="margin-top:auto">'
    body += _text('p', 'frase', 'citacao-grande aqr-citacao', day['frase'])
    body += _text('p', 'referencia', 'referencia aqr-referencia', day['referencia'],
        'margin-top:var(--espaco-2)', token='ouro')
    body += '</div>'
    signature = assinatura('pergaminho', arroba=True).replace(
        'data-element="assinatura-arroba"',
        'data-element="assinatura-arroba" data-text="arroba" data-style="assinatura"')
    post = montar_arte(body+signature, tema='pergaminho',
        cor_do_dia=color_token(day['cor']), formato=config['base'])
    return html_document(post, css, '@page{margin:0;}',
        f'Coragem · {day["data"]} · {format_name}')


def _measure(page: Any, format_name: str) -> dict:
    measured = measure_evangelho(page, 1, 1)
    measured.update({'tipo': 'Coragem', 'modelo': 'PostCoragem', 'tema': 'pergaminho',
        'formato': format_name, 'largura': 1080, 'altura': FORMATS[format_name]['height']})
    for text in measured['textos']:
        if text['campo'] == 'referencia': text['alinhamento_canva'] = 'center'
    measured['caixas']['assinatura'] = page.locator('.aqr-assinatura').evaluate(
        """el => {const a=el.closest('.aqr-post').getBoundingClientRect(),r=el.getBoundingClientRect();
        return {x:r.left-a.left,y:r.top-a.top,largura:r.width,altura:r.height};}""")
    sill = next(item for item in measured['elementos'] if item['element'] == 'nicho-parapeito')
    measured['caixas']['parapeito'] = {'x': sill['x'], 'y': sill['y'],
        'largura': sill['width'], 'altura': sill['height']}
    return measured


def _inside(area: dict, box: dict, tolerance=0.1) -> bool:
    return (box['x'] >= area['x']-tolerance and box['y'] >= area['y']-tolerance
        and box['x']+box['largura'] <= area['x']+area['largura']+tolerance
        and box['y']+box['altura'] <= area['y']+area['altura']+tolerance)


def _validate_layout(day: dict, measured: dict) -> dict:
    errors = []; values = {t['campo']: t for t in measured['textos']}
    art = {'x': 0, 'y': 0, 'largura': 1080, 'altura': measured['altura']}
    label = f'{day["data"]}, {measured["formato"]}'
    for text in measured['textos']:
        field = text['campo']; limit = {'frase': 2, 'referencia': 1}.get(field)
        if limit and text['quantidade_linhas'] > limit:
            errors.append(f'{label}, {field}: {text["quantidade_linhas"]} linhas; limite {limit}.')
        if not _inside(art, text['caixa']): errors.append(f'{label}, {field}: texto fora da arte.')
        for line, box in zip(text['linhas'], text['caixas_das_linhas']):
            if re.search(r'(?:^|\s)[aàeéoóAÀEÉOÓ][\W_]*$', line):
                errors.append(f'{label}, {field}: palavra de uma letra no fim de {line!r}.')
            if box['largura'] and (box['x'] < text['caixa']['x']-.1 or box['x']+box['largura'] > text['caixa']['x']+text['caixa']['largura']+.1):
                errors.append(f'{label}, {field}: linha transborda a largura do campo.')
            if not _inside(art, box): errors.append(f'{label}, {field}: linha fora da arte.')
    sill = measured['caixas']['parapeito']; signature = measured['caixas']['assinatura']
    quote = values['frase']['caixa']; reference = values['referencia']['caixa']
    pair_gap = reference['y']-quote['y']-quote['altura']
    if abs(pair_gap-32) > .01:
        errors.append(f'{label}, frase → referencia: distância {pair_gap:.2f}px; esperado 32px (±0,01).')
    above = quote['y']-sill['y']-sill['altura']
    below = signature['y']-reference['y']-reference['altura']
    if above < 31.99: errors.append(f'{label}, frase: distância ao parapeito {above:.2f}px < 32px.')
    if below < 31.99: errors.append(f'{label}, referencia: distância à assinatura {below:.2f}px < 32px.')
    block = measured['caixas']['bloco_texto']; niche = measured['caixas']['nicho']
    upper = block['y']-niche['y']-niche['altura']
    lower = signature['y']-block['y']-block['altura']
    if abs(upper-lower) > .1: errors.append(f'{label}: texto não centralizado entre nicho e assinatura.')
    result = {'ok': not errors, 'limites': {'frase': 2, 'referencia': 1},
        'frase_referencia_px': round(pair_gap, 6),
        'parapeito_frase_px': round(above, 6), 'referencia_assinatura_px': round(below, 6),
        'respiro_bloco_superior_px': round(upper, 6), 'respiro_bloco_inferior_px': round(lower, 6),
        'errors': errors}
    if errors: raise ValueError('; '.join(errors))
    return result


def _pixels(path: Path, day: dict, measured: dict) -> dict:
    samples = []; errors = []
    liturgy = color(color_token(day['cor']), 'pergaminho')
    background = color('fundo', 'pergaminho')
    with Image.open(path) as raw:
        image = raw.convert('RGB')
        for label, point, wanted in [('fundo', (8, 8), background),
            ('cruz do selo', (int(measured['caixas']['cruz']['x']+9), int(measured['caixas']['cruz']['y']+18)), liturgy)]:
            actual = image.getpixel(point); ok = actual == ImageColor.getrgb(wanted)
            samples.append({'elemento': label, 'pixel': list(point), 'esperado': wanted,
                'rgb': list(actual), 'ok': ok})
            if not ok: errors.append(f'{day["data"]}, {measured["formato"]}, {label}: cor diferente de {wanted}.')
    box = measured['caixas']['nicho']
    niche = validate_niche_pixels(path, [{'name': 'nicho', 'x': box['x'], 'y': box['y'],
        'width': box['largura'], 'height': box['altura'], 'filete': liturgy, 'background': background}])
    errors.extend(niche['errors'])
    result = {'ok': not errors, 'amostras': samples, 'nicho': niche, 'errors': errors}
    if errors: raise ValueError('; '.join(errors))
    return result


def _pdf_check(path: Path, day: dict, measured: dict) -> dict:
    import fitz
    errors = []; fonts = {}; pages = []; combined = ''
    required = {'CormorantGaramond-MediumItalic', 'Lato-Bold', 'Lato-Regular'}
    expected_height = measured['altura']*.75
    with fitz.open(path) as document:
        if len(document) != 1: errors.append(f'{path.name}: esperado PDF de uma página.')
        for page in document:
            combined += ' '+page.get_text()
            pages.append({'largura_pt': page.rect.width, 'altura_pt': page.rect.height})
            if abs(page.rect.width-810) > .01 or abs(page.rect.height-expected_height) > .01:
                errors.append(f'{path.name}: formato diferente de 810 × {expected_height:g} pt.')
            for info in page.get_fonts(full=True):
                xref, _, kind, name = info[:4]
                if xref in fonts: continue
                _, extension, _, data = document.extract_font(xref)
                name = re.sub(r'^[A-Z]{6}\+', '', name)
                embedded = bool(data) and extension.lower() in {'ttf', 'ttc'} and data[:4] in {b'\x00\x01\x00\x00', b'true', b'ttcf'}
                fonts[xref] = {'nome': name, 'tipo': kind, 'formato': extension, 'embutida': embedded, 'bytes': len(data)}
                if not embedded: errors.append(f'{path.name}: fonte TTF não embutida: {name}.')
    missing = required-{font['nome'] for font in fonts.values()}
    if missing: errors.append(f'{path.name}: fontes ausentes: '+', '.join(sorted(missing)))
    compact = lambda value: re.sub(r'\s+', '', value)
    expected_text = compact(''.join(text['conteudo'] for text in measured['textos']))
    pymupdf_text = compact(combined)
    pymupdf_equal = pymupdf_text == expected_text
    if not pymupdf_equal:
        errors.append(f'{path.name}: texto integral do PDF difere do conteúdo esperado (PyMuPDF).')
    text_checks = []
    for text in measured['textos']:
        wanted = compact(text['conteudo']); found = wanted in compact(combined)
        text_checks.append({'campo': text['campo'], 'extraivel': found})
        if not found: errors.append(f'{path.name}: texto {text["campo"]} não extraível.')
    poppler = None; extracted = None; pdftotext_equal = False
    if shutil.which('pdffonts'):
        process = subprocess.run(['pdffonts', str(path)], capture_output=True, text=True, check=False)
        poppler = process.stdout
        if process.returncode: errors.append('pdffonts falhou: '+process.stderr)
        for name in required:
            if name not in poppler: errors.append(f'pdffonts não lista {name}.')
        for line in poppler.splitlines()[2:]:
            match = re.search(r'\s(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$', line)
            if match and match.group(1) != 'yes': errors.append('pdffonts: fonte não embutida '+line)
    else: errors.append('pdffonts indisponível.')
    if shutil.which('pdftotext'):
        process = subprocess.run(['pdftotext', '-layout', str(path), '-'], capture_output=True, text=True, check=False)
        extracted = process.stdout
        if process.returncode: errors.append('pdftotext falhou: '+process.stderr)
        pdftotext_equal = compact(extracted) == expected_text
        if not pdftotext_equal:
            errors.append(f'{path.name}: texto integral do PDF difere do conteúdo esperado (pdftotext).')
        for field in ('frase', 'referencia'):
            if compact(day[field]) not in compact(extracted): errors.append(f'pdftotext: {field} diferente do YAML.')
    else: errors.append('pdftotext indisponível.')
    result = {'ok': not errors, 'paginas': pages, 'fontes': list(fonts.values()),
        'textos': text_checks, 'pdffonts': poppler, 'pdftotext': extracted,
        'igualdade_texto_integral': {'pymupdf': pymupdf_equal, 'pdftotext': pdftotext_equal,
            'esperado_sem_espacos': expected_text, 'pymupdf_sem_espacos': pymupdf_text,
            'pdftotext_sem_espacos': compact(extracted) if extracted is not None else None},
        'errors': errors}
    if errors: raise ValueError('; '.join(errors))
    return result


def _recommendation(artwork: Path, focus: str, zoom: float, size: tuple[int, int], analysis: dict) -> dict | None:
    """Recommend a crop without changing YAML or its rendered composition."""
    if not analysis['margens_visiveis']: return None
    margins = analysis['margens_detectadas']
    width = analysis['imagem_original']['largura']; height = analysis['imagem_original']['altura']
    left, right = margins.get('esquerda', 0), width-margins.get('direita', 0)
    top, bottom = margins.get('topo', 0), height-margins.get('base', 0)
    def safe(g):
        box = g['janela_original']
        return (box['x'] >= left-1e-6 and box['y'] >= top-1e-6
            and box['x']+box['largura'] <= right+1e-6
            and box['y']+box['altura'] <= bottom+1e-6)
    # The first acceptable zoom keeps the requested focus whenever possible.
    for integer in range(max(100, round(zoom*100)), 301):
        candidate = integer/100
        geometry = artwork_geometry(artwork, focus, candidate, niche_width=size[0], niche_height=size[1])
        if safe(geometry):
            verified = inspect_artwork(artwork, focus, candidate, niche_width=size[0], niche_height=size[1])
            if not verified['margens_visiveis']:
                return {'foco': focus, 'zoom': candidate, 'janela_original': geometry['janela_original'], 'margens_visiveis': []}
    # If the painting is off-centre, centre the window within the detected paint.
    for integer in range(100, 301):
        candidate = integer/100
        geometry = artwork_geometry(artwork, '50% 50%', candidate, niche_width=size[0], niche_height=size[1])
        box = geometry['janela_original']; vw, vh = box['largura'], box['altura']
        if vw > right-left or vh > bottom-top: continue
        fx = ((left+right-vw)/2)/(width-vw) if width > vw else .5
        fy = ((top+bottom-vh)/2)/(height-vh) if height > vh else .5
        proposed = f'{min(100,max(0,fx*100)):.6f}% {min(100,max(0,fy*100)):.6f}%'
        geometry = artwork_geometry(artwork, proposed, candidate, niche_width=size[0], niche_height=size[1])
        if safe(geometry):
            verified = inspect_artwork(artwork, proposed, candidate, niche_width=size[0], niche_height=size[1])
            if not verified['margens_visiveis']:
                return {'foco': proposed, 'zoom': candidate, 'janela_original': geometry['janela_original'], 'margens_visiveis': []}
    return {'foco': None, 'zoom': None, 'resolvido': False,
        'observacao': 'Nenhum foco e zoom até 3 elimina as margens detectadas desta foto.'}


def _board(target: Path) -> tuple[int, int]:
    records = [(path, json.loads(path.read_text(encoding='utf-8')))
        for path in sorted(target.glob('????-??-??/ficha.json'))]
    margin = 32; gap = 24; row_height = 730
    size = (margin*2+360*2+gap, 32+row_height*len(records))
    board = Image.new('RGB', size, color('fundo', 'pergaminho')); draw = ImageDraw.Draw(board)
    font = ImageFont.truetype(str(KIT/'fontes/Lato-Regular.ttf'), 22)
    for index, (path, record) in enumerate(records):
        y = 32+index*row_height
        label = f'{record["data"]} · {record["cor"]}'+(' · obra pendente' if record['obra_pendente'] else '')
        draw.text((margin, y), label, font=font, fill=color('tinta', 'pergaminho'))
        for column, name in enumerate(FORMATS):
            draw.text((margin+column*(360+gap), y+30), name, font=font, fill=color('tinta-suave', 'pergaminho'))
            with Image.open(path.parent/f'{name}.png') as image:
                board.paste(image.convert('RGB').resize((360, FORMATS[name]['height']//3), Image.Resampling.LANCZOS),
                    (margin+column*(360+gap), y+62))
    board.save(target/'prancha.png'); return size


def _report(target: Path, records: list[dict], checks: dict, command: str) -> Path:
    lines = ['# Coragem', '', f'`{command}`', '', '## Composição e decisões', '',
        '- Tema pergaminho; o feed segue PostCoragem e o status usa a mesma composição com aqr-post--story, sem substituir os 240 px de padding superior e inferior do kit.',
        '- Nichos de 600 × 680 no feed e 720 × 900 no status, com img dentro do arco, object-fit:cover, foco e zoom depois do cover. O crédito da obra permanece somente na ficha para uso na legenda.',
        '- Frase em citacao-grande e referência livre em referencia/ouro, centralizadas entre nicho e assinatura; a assinatura inclui @artequereza.oficial nos dois formatos.',
        '- 32 px entre o texto e a referência e 48 px entre o rótulo e o texto, para o Canva importar cada um em sua caixa (teste de 29/10/2026). No Coragem, a referência recebe margin-top:var(--espaco-2) sobre o gap de 16 px do kit.',
        '- Quebras manuais são preservadas; as demais linhas são equilibradas pelo CSS do kit. Palavras de uma letra ficam ligadas à seguinte. As linhas vazias também contam para o limite.',
        '- Cada formato recebe seu PDF, porque os designs do Canva têm um tamanho único. Os recortes mostram a obra inteira a 1080 px de largura com a janela do arco, já considerando o zoom.',
        '- As obras reais fornecidas no repositório foram usadas sem downloads. Avisos e recomendações abaixo não alteram coragem.yaml nem o enquadramento pedido.',
        '', '## Linhas e distâncias', '',
        '| Data | Formato | Frase (limite 2) | Referência (limite 1) | Frase → referência | Parapeito → frase | Referência → assinatura |',
        '| --- | --- | --- | --- | --- | --- | --- |']
    pending = []
    for record in records:
        if record['obra_pendente']: pending.append(record['data'])
        for card in record['cards']:
            texts = {text['campo']: text for text in card['textos']}
            layout = checks['dias'][record['data']]['formatos'][card['formato']]['layout']
            lines.append(f'| {record["data"]} | {card["formato"]} | {texts["frase"]["quantidade_linhas"]} | {texts["referencia"]["quantidade_linhas"]} | {layout["frase_referencia_px"]:g} px | {layout["parapeito_frase_px"]:g} px | {layout["referencia_assinatura_px"]:g} px |')
    lines += ['', '## Obras, foco e zoom', '']
    for record in records:
        lines += [f'- **{record["data"]}:** '+('obra pendente; provisória utilizada.' if record['obra_pendente'] else 'obra real local; recortes de feed e status gerados.'),
            f'  {record["obra"]["credito"]} — {record["obra"]["pagina"]}']
        for card in record['cards']:
            framing = card['enquadramento']; window = framing['janela_original']
            lines.append(f'  - {card["formato"]}: foco `{framing["foco"]}`, zoom `{framing["zoom"]}`; janela original x={window["x"]:g}, y={window["y"]:g}, largura={window["largura"]:g}, altura={window["altura"]:g} px.')
            for warning in framing.get('avisos', []): lines.append('    - Aviso: '+warning)
            recommendation = card.get('recomendacao_margem')
            if recommendation:
                if recommendation.get('foco'):
                    lines.append(f'    - Para eliminar a margem neste formato, use foco `{recommendation["foco"]}` e zoom `{recommendation["zoom"]}`. Recomendação conferida sem margem; valores não aplicados ao YAML.')
                else: lines.append('    - '+recommendation['observacao'])
    visual_notes = target/'NOTAS-DE-ENQUADRAMENTO.md'
    if visual_notes.is_file():
        lines += ['', '## Revisão visual das obras', '', visual_notes.read_text(encoding='utf-8').strip()]
    lines += ['', 'Obras pendentes: '+(', '.join(pending) if pending else 'nenhuma')+'.',
        'Avisos de margem: '+(str(len(checks['avisos']))+'; recomendações por formato acima.' if checks['avisos'] else 'nenhum nos dois formatos das obras reais fornecidas.'),
        '', '## Conferências e limites', '',
        'Foram conferidos dimensões dos PNGs, cores da cruz e do filete por pixel, linhas reais com Range, limites e distâncias. PDFs com uma página em 810 × 1012,5 pt no feed e 810 × 1440 pt no status; fontes TTF usadas embutidas por pdffonts e texto do YAML verificado por pdftotext desconsiderando espaços e quebras.',
        '', 'A regra dos espaços foi aprovada no teste do Canva de 29/10/2026; os PDFs desta geração não foram reimportados. As margens são diagnosticadas por linhas/colunas uniformes com contraste de pelo menos 10 níveis de cinza em relação às 16 linhas/colunas seguintes; faixas sem esse contraste ficam registradas como descartadas. A recomendação conserva a arte gerada e serve para ajuste posterior.',
        '', '## Árvore', '', '```text', 'saida/coragem/']
    names = {path.relative_to(target).as_posix() for path in target.rglob('*') if path.is_file()}; names.add('RELATORIO.md')
    lines += ['  '+name for name in sorted(names)] + ['```', '']
    path = target/'RELATORIO.md'; path.write_text('\n'.join(lines), encoding='utf-8'); return path


def generate(output: Path, content_path: Path, date_filter: str | None = None) -> dict:
    output = Path(output).resolve(); target = output/'coragem'; target.mkdir(parents=True, exist_ok=True)
    days = load_courage(content_path)
    if date_filter is not None:
        days = [day for day in days if day['data'] == date_filter]
        if not days: raise ValueError(f'Nenhum conteúdo para --data {date_filter}.')
    kit = validate_kit(PROJECT)
    if not kit['ok']: raise ValueError('Kit inválido: '+'; '.join(kit['errors']))
    css = generate_tokens_css(output/'tokens.css'); placeholder = output/'obra-provisoria.png'
    if not placeholder.is_file(): placeholder = PROJECT/'saida/obra-provisoria.png'
    work = PROJECT/'work/coragem'; expected = {}; records = []; checks = {'kit': kit, 'dias': {}}; errors = []; warnings = []
    with local_server() as base_url, sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=shutil.which('chromium') or '/usr/bin/chromium', headless=True, args=['--no-sandbox'])
        context = browser.new_context(device_scale_factor=1)
        context.route('**/*', lambda route: route.continue_() if urlsplit(route.request.url).netloc == urlsplit(base_url).netloc else route.abort())
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('console', lambda message: errors.append(message.text) if message.type == 'error' else None)
        page.on('response', lambda response: errors.append(f'HTTP {response.status}: {response.url}') if response.status >= 400 else None)
        for day in days:
            folder = target/day['data']; folder.mkdir(parents=True, exist_ok=True)
            artwork = local_artwork_path(day['obra']['arquivo']); pending = not artwork.is_file()
            if pending:
                if not placeholder.is_file(): raise FileNotFoundError('Obra provisória ausente; execute python gerar.py componentes.')
                artwork = placeholder
                warning = f'{day["data"]}: obra pendente; utilizada obra provisória.'
                warnings.append(warning); print('Aviso: '+warning)
            cards = []; formats = {}
            for format_name, config in FORMATS.items():
                png = work/day['data']/f'{format_name}.png'; pdf = png.with_suffix('.pdf')
                render = render_arte(page, _document(day, css, artwork, format_name), png,
                    formato=config['base'], pdf_path=pdf, base_url=base_url)
                card = _measure(page, format_name); layout = _validate_layout(day, card)
                pixels = _pixels(png, day, card); pdfcheck = _pdf_check(pdf, day, card)
                width, height = config['niche']; focus = day['obra']['foco']; zoom = day['obra'].get('zoom', 1)
                framing = inspect_artwork(artwork, focus, zoom, niche_width=width, niche_height=height, date=day['data'])
                if pending: framing['avisos'] = []; framing['margens_visiveis'] = []
                card['enquadramento'] = framing
                for warning in framing['avisos']:
                    message = f'{format_name}: {warning}'; warnings.append(message); print('Aviso: '+message)
                recommendation = _recommendation(artwork, focus, zoom, config['niche'], framing) if not pending else None
                if recommendation: card['recomendacao_margem'] = recommendation
                shutil.copyfile(png, folder/f'{format_name}.png')
                shutil.copyfile(pdf, folder/f'coragem-{day["data"]}-{format_name}.pdf')
                expected[str(folder/f'{format_name}.png')] = (1080, config['height'])
                crop = folder/f'recorte-{format_name}.png'
                if not pending:
                    crop_proof(artwork, crop, focus, zoom=zoom, niche_width=width, niche_height=height, date=day['data'])
                    with Image.open(crop) as image: expected[str(crop)] = image.size
                elif crop.exists(): crop.unlink()
                cards.append(card); formats[format_name] = {'layout': layout, 'pixels': pixels, 'pdf': pdfcheck, 'fontes_render': render['fonts'], 'enquadramento': framing, 'recomendacao_margem': recommendation}
            record = {key: day[key] for key in ('data', 'cor', 'frase', 'referencia', 'obra')}
            record.update({'obra_pendente': pending, 'obra_usada': artwork.relative_to(PROJECT).as_posix(), 'cards': cards})
            (folder/'ficha.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
            records.append(record); checks['dias'][day['data']] = {'formatos': formats}
        browser.close()
    if errors: raise RuntimeError('Erros de navegador: '+'; '.join(errors))
    expected[str(target/'prancha.png')] = _board(target)
    checks['pngs'] = validate_pngs(expected); checks['kit_final'] = validate_kit(PROJECT)
    checks['browser'] = {'ok': True, 'errors': [], 'fontes_locais_por_render': 6, 'recursos_externos': False}
    checks['obras_pendentes'] = [record['data'] for record in records if record['obra_pendente']]
    checks['avisos'] = warnings
    checks['ok'] = all(checks[key]['ok'] for key in ('kit', 'kit_final', 'pngs'))
    if not checks['ok']: raise RuntimeError('Falha de validação de PNG ou kit.')
    command = 'python gerar.py coragem'+(f' --data {date_filter}' if date_filter else '')
    checks['comando'] = command
    (target/'verificacao.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    report = _report(target, records, checks, command)
    return {'dias': len(records), 'cards': len(records)*2, 'pdfs': len(records)*2, 'pngs': len(expected),
        'obras_pendentes': checks['obras_pendentes'], 'avisos': warnings, 'relatorio': str(report), 'verificacoes': str(target/'verificacao.json')}
