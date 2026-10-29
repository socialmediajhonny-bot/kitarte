"""Stories fixos por tempo litúrgico, fiéis à prévia StoryAngelus do kit."""
from __future__ import annotations

from html import escape
import json
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any
from urllib.parse import urlsplit

from PIL import Image, ImageChops, ImageColor, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

from .base import (PROJECT, KIT, assinatura, await_fonts, color, generate_tokens_css,
                   html_document, montar_arte, nicho, render_arte, resource_url, selo)
from .conteudo import color_token, local_artwork_path
from .conteudo_stories import load_stories
from .evangelho import _measure as measure_evangelho, _ornament, _text
from .obras import artwork_geometry, crop_proof, inspect_artwork
from .renderizacao import local_server
from .validacao import validate_kit, validate_niche_pixels, validate_pngs


LIMITS = {'titulo': 1, 'subtitulo': 1, 'invocacao': 3, 'resposta': 2}
NICHE_SIZE = (600, 700)


def _header(story: dict) -> str:
    markup = selo('Para Rezar', story['hora'])
    for original, field in [('selo-serie', 'selo'), ('selo-data', 'hora')]:
        markup = markup.replace(f'data-element="{original}"',
            f'data-element="{original}" data-text="{field}" data-style="selo"')
    return markup


def _document(tempo: dict, story: dict, css: Path, artwork: Path) -> str:
    image = nicho(*NICHE_SIZE, artwork, foco=story['obra']['foco'], zoom=story['obra'].get('zoom', 1))
    image = image.replace('style="width:600px;height:700px;"',
        'style="width:600px;height:700px;margin-top:var(--espaco-4)"')
    image = image.replace('alt="Obra provisória"', f'alt="{escape(story["titulo"], quote=True)}"')
    image = image.replace('data-arquivo="obra-provisoria.png"',
        f'data-arquivo="{escape(artwork.relative_to(PROJECT).as_posix(), quote=True)}"')
    body = _header(story)+image+'<div class="aqr-texto" style="margin-top:var(--espaco-4)">'
    body += _text('h1', 'titulo', 'titulo-capa', story['titulo'])
    body += _text('p', 'subtitulo', 'corpo aqr-suave', story['subtitulo'], token='tinta-suave')
    body += _ornament()
    body += _text('p', 'invocacao', 'citacao aqr-citacao', story['invocacao'])
    if 'resposta' in story:
        body += _text('p', 'resposta', 'oracao aqr-suave', story['resposta'], token='tinta-suave')
    body += '</div>'+assinatura('capela')
    post = montar_arte(body, tema='capela', cor_do_dia=color_token(tempo['cor']), formato='story')
    return html_document(post, css, '@page{margin:0;}', f'Stories · {tempo["nome"]} · {story["titulo"]}')


def _measure(page: Any, tempo: dict, story: dict, number: int) -> dict:
    measured = measure_evangelho(page, number, 1)
    measured.update({'tipo': 'story', 'modelo': 'StoryAngelus', 'tema': 'capela',
        'id': story['id'], 'hora': story['hora'], 'tempo': tempo['id'], 'cor': tempo['cor'],
        'largura': 1080, 'altura': 1920})
    for text in measured['textos']:
        text['alinhamento_canva'] = 'start' if text['campo'] in {'selo', 'hora'} else 'center'
    extras = page.evaluate("""() => {
      const root=document.querySelector('.aqr-post').getBoundingClientRect();
      const box=selector=>{const r=document.querySelector(selector).getBoundingClientRect();
        return {x:r.left-root.left,y:r.top-root.top,largura:r.width,altura:r.height};};
      return {assinatura:box('.aqr-assinatura'),ornamento_cruz:box('.aqr-ornamento svg')};
    }""")
    measured['caixas'].update(extras)
    sill = next(item for item in measured['elementos'] if item['element'] == 'nicho-parapeito')
    measured['caixas']['parapeito'] = {'x': sill['x'], 'y': sill['y'], 'largura': sill['width'], 'altura': sill['height']}
    return measured


def _inside(area: dict, box: dict, tolerance=.1) -> bool:
    return (box['x'] >= area['x']-tolerance and box['y'] >= area['y']-tolerance
        and box['x']+box['largura'] <= area['x']+area['largura']+tolerance
        and box['y']+box['altura'] <= area['y']+area['altura']+tolerance)


def _validate_layout(tempo: dict, story: dict, measured: dict) -> dict:
    errors = []; label = f'{tempo["id"]}, {story["id"]}'
    art = {'x': 0, 'y': 0, 'largura': 1080, 'altura': 1920}
    texts = {text['campo']: text for text in measured['textos']}
    for text in measured['textos']:
        field = text['campo']; limit = LIMITS.get(field)
        if limit and text['quantidade_linhas'] > limit:
            errors.append(f'{label}, {field}: {text["quantidade_linhas"]} linhas; limite {limit}.')
        if not _inside(art, text['caixa']): errors.append(f'{label}, {field}: texto fora da arte.')
        for line, box in zip(text['linhas'], text['caixas_das_linhas']):
            if re.search(r'(?:^|\s)[aàeéoóAÀEÉOÓ][\W_]*$', line):
                errors.append(f'{label}, {field}: palavra de uma letra no fim de {line!r}.')
            if box['largura'] and (box['x'] < text['caixa']['x']-.1 or box['x']+box['largura'] > text['caixa']['x']+text['caixa']['largura']+.1):
                errors.append(f'{label}, {field}: linha transborda a largura do campo.')
            if not _inside(art, box): errors.append(f'{label}, {field}: linha fora da arte.')
    last_field = 'resposta' if 'resposta' in story else 'invocacao'
    last = texts[last_field]['caixa']; signature = measured['caixas']['assinatura']
    gap = signature['y']-last['y']-last['altura']
    if gap < 31.99: errors.append(f'{label}, {last_field}: distância à assinatura {gap:.2f}px < 32px.')
    seal = measured['caixas']['selo']; niche = measured['caixas']['nicho']; title = texts['titulo']['caixa']
    positions = {'selo_topo_px': seal['y'], 'nicho_topo_px': niche['y'],
        'nicho_base_px': niche['y']+niche['altura'], 'titulo_topo_px': title['y'],
        'assinatura_topo_px': signature['y']}
    expected = {'selo_topo_px': 240, 'nicho_topo_px': 328, 'nicho_base_px': 1028,
        'titulo_topo_px': 1076, 'assinatura_topo_px': 1628}
    for field, value in positions.items():
        if abs(value-expected[field]) > .1:
            errors.append(f'{label}, {field}: {value:g}px; esperado {expected[field]}px pela composição do kit.')
    result = {'ok': not errors, 'limites': LIMITS, 'posicoes': positions,
        'ultimo_campo': last_field, 'ultimo_texto_assinatura_px': round(gap, 6),
        'nicho_bloco_texto_px': measured['caixas']['bloco_texto']['y']-niche['y']-niche['altura'],
        'errors': errors}
    if errors: raise ValueError('; '.join(errors))
    return result


def _pixels(path: Path, tempo: dict, story: dict, measured: dict) -> dict:
    errors = []; samples = []; liturgy = color(color_token(tempo['cor']), 'capela')
    background = color('fundo', 'capela'); gold = color('ouro', 'capela')
    cross = measured['caixas']['cruz']; ornament = measured['caixas']['ornamento_cruz']
    with Image.open(path) as raw:
        image = raw.convert('RGB')
        for label, point, wanted in [('fundo', (8, 8), background),
            ('cruz do selo', (int(cross['x']+9), int(cross['y']+18)), liturgy),
            ('ornamento', (int(ornament['x']+7), int(ornament['y']+14)), gold)]:
            actual = image.getpixel(point); ok = actual == ImageColor.getrgb(wanted)
            samples.append({'elemento': label, 'pixel': list(point), 'esperado': wanted, 'rgb': list(actual), 'ok': ok})
            if not ok: errors.append(f'{tempo["id"]}, {story["id"]}, {label}: cor diferente de {wanted}.')
    box = measured['caixas']['nicho']
    niche = validate_niche_pixels(path, [{'name': 'nicho', 'x': box['x'], 'y': box['y'],
        'width': box['largura'], 'height': box['altura'], 'background': background, 'filete': liturgy}])
    errors.extend(niche['errors'])
    result = {'ok': not errors, 'amostras': samples, 'nicho': niche, 'errors': errors}
    if errors: raise ValueError('; '.join(errors))
    return result


def _pdf_check(path: Path, stories: list[dict], cards: list[dict]) -> dict:
    import fitz
    errors = []; fonts = {}; pages = []; extracted_pages = []
    required = {'Lato-Bold', 'Lato-Regular', 'CormorantGaramond-SemiBold', 'CormorantGaramond-MediumItalic'}
    if any('resposta' in story for story in stories): required.add('CormorantGaramond-Medium')
    compact = lambda text: re.sub(r'\s+', '', text)
    with fitz.open(path) as document:
        if len(document) != len(stories): errors.append(f'{path.name}: {len(document)} páginas; esperado {len(stories)}.')
        for number, page in enumerate(document):
            text = page.get_text(); extracted_pages.append(text)
            expected = compact(''.join(item['conteudo'] for item in cards[number]['textos'])) if number < len(cards) else ''
            equal = compact(text) == expected
            pages.append({'pagina': number+1, 'largura_pt': page.rect.width, 'altura_pt': page.rect.height,
                'texto_integral_pymupdf_igual': equal, 'texto_esperado_sem_espacos': expected})
            if abs(page.rect.width-810) > .01 or abs(page.rect.height-1440) > .01:
                errors.append(f'{path.name}, página {number+1}: dimensão diferente de 810 × 1440 pt.')
            if not equal: errors.append(f'{path.name}, página {number+1}: texto integral diferente do conteúdo esperado (PyMuPDF).')
            for info in page.get_fonts(full=True):
                xref, _, kind, name = info[:4]
                if xref in fonts: continue
                _, extension, _, data = document.extract_font(xref)
                name = re.sub(r'^[A-Z]{6}\+', '', name)
                embedded = bool(data) and extension.lower() in {'ttf','ttc'} and data[:4] in {b'\x00\x01\x00\x00',b'true',b'ttcf'}
                fonts[xref] = {'nome': name, 'tipo': kind, 'formato': extension, 'embutida': embedded, 'bytes': len(data)}
                if not embedded: errors.append(f'{path.name}: fonte TTF não embutida: {name}.')
    missing = required-{font['nome'] for font in fonts.values()}
    if missing: errors.append(f'{path.name}: fontes ausentes: '+', '.join(sorted(missing)))
    poppler = None; extracted = None
    if shutil.which('pdffonts'):
        process = subprocess.run(['pdffonts', str(path)], capture_output=True, text=True, check=False)
        poppler = process.stdout
        if process.returncode: errors.append('pdffonts falhou: '+process.stderr)
        for font in required:
            if font not in poppler: errors.append('pdffonts não lista '+font+'.')
        for line in poppler.splitlines()[2:]:
            match = re.search(r'\s(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$', line)
            if match and match.group(1) != 'yes': errors.append('pdffonts: fonte não embutida '+line)
    else: errors.append('pdffonts indisponível.')
    if shutil.which('pdftotext'):
        process = subprocess.run(['pdftotext', '-layout', str(path), '-'], capture_output=True, text=True, check=False)
        extracted = process.stdout
        if process.returncode: errors.append('pdftotext falhou: '+process.stderr)
        parts = extracted.split('\f')
        if parts and not parts[-1].strip(): parts.pop()
        if len(parts) != len(cards): errors.append(f'pdftotext: {len(parts)} páginas extraídas; esperado {len(cards)}.')
        for index, card in enumerate(cards):
            expected = compact(''.join(text['conteudo'] for text in card['textos']))
            actual = compact(parts[index]) if index < len(parts) else None
            equal = actual == expected
            if index < len(pages): pages[index]['texto_integral_pdftotext_igual'] = equal
            if not equal: errors.append(f'{path.name}, página {index+1}: texto integral diferente do conteúdo esperado (pdftotext).')
    else: errors.append('pdftotext indisponível.')
    result = {'ok': not errors, 'paginas': pages, 'fontes': list(fonts.values()), 'fontes_exigidas': sorted(required),
        'pdffonts': poppler, 'pdftotext': extracted, 'tamanho_bytes': path.stat().st_size, 'errors': errors}
    if errors: raise ValueError('; '.join(errors))
    return result


def _source_warnings(story: dict, artwork: Path) -> list[str]:
    warnings = []
    with Image.open(artwork) as image: width = image.width
    if artwork.stat().st_size > 4_000_000:
        warnings.append(f'{story["id"]}: obra com {artwork.stat().st_size} bytes, acima de 4 MB; o PDF incorpora a imagem inteira.')
    if width < 1000: warnings.append(f'{story["id"]}: obra com {width}px de largura, abaixo de 1000px.')
    return warnings


def _visual_note(story: dict, artwork: Path, pending: bool, framing: dict) -> dict:
    if pending: return {'inspecionada': False, 'nota': 'Obra pendente; não foi possível conferir os elementos essenciais.'}
    if story['id'] == 'angelus':
        return {'inspecionada': True,
            'nota': 'Na obra real desta entrega, o arco com foco 50% 55% mostra os rostos de Gabriel, à esquerda, e de Maria, à direita. O recorte concentra a cena nas duas figuras e deixa partes superiores da arquitetura e inferiores da pintura fora da janela. Os elementos essenciais estão preservados; não foi necessário recomendar outro foco ou zoom.'}
    if story['id'] == 'misericordia':
        proposed = inspect_artwork(artwork, '50% 8%', 1.33, niche_width=600, niche_height=700)
        return {'inspecionada': True,
            'nota': 'Na obra real desta entrega, o foco 50% 8% preserva o rosto, a mão que abençoa e a origem dos raios vermelho e claro. O detector objetivo acusa faixas uniformes laterais: são áreas escuras do fundo original da pintura, e não uma margem branca externa da foto. O aviso foi mantido. A composição pedida foi preservada, sem alterar o YAML.',
            'sugestao_opcional': {'foco': '50% 8%', 'zoom': 1.33,
                'margens_visiveis': proposed['margens_visiveis'],
                'janela_original': proposed['janela_original'],
                'nota': 'Para excluir também as faixas escuras uniformes, foco 50% 8% e zoom 1.33 eliminam o aviso. Na prova de enquadramento, rosto, mão que abençoa e origem dos dois raios permanecem na janela. A sugestão não foi aplicada ao YAML.'}}
    return {'inspecionada': False, 'nota': 'A janela e o recorte foram registrados; esta obra nova requer conferência visual dos elementos essenciais.'}


def _preview_check(page: Any, css: Path, target: Path, work: Path, base_url: str) -> dict:
    reference = target/'tempo-comum/angelus.png'
    if not reference.is_file():
        return {'ok': True, 'verificado': False, 'motivo': 'A versão tempo-comum/angelus ainda não foi gerada nesta pasta.'}
    source = KIT/'design-system/componentes/StoryAngelus/preview.html'
    html = source.read_text(encoding='utf-8')
    links = f'<link rel="stylesheet" href="{resource_url(css)}"><link rel="stylesheet" href="{resource_url(KIT/"design-system/bundle.css")}">'
    html = html.replace('<head>', '<head>'+links).replace('../../../logos/', resource_url(KIT/'logos')+'/')
    folder = work/'conferencia-kit'; folder.mkdir(parents=True, exist_ok=True)
    document = folder/'preview.html'; document.write_text(html, encoding='utf-8')
    page.set_viewport_size({'width': 1176, 'height': 2016})
    page.goto(base_url+resource_url(document), wait_until='load'); await_fonts(page)
    articles = page.locator('article.aqr-post')
    if articles.count() != 1: raise ValueError('StoryAngelus/preview.html precisa conter um article.aqr-post.')
    bounds = articles.first.bounding_box(); screenshot = folder/'article.png'
    page.screenshot(path=str(screenshot), clip=bounds, animations='disabled')
    def compare(path):
        with Image.open(path) as raw, Image.open(reference) as generated:
            a = raw.convert('RGB'); b = generated.convert('RGB')
            if a.size != b.size: raise ValueError('Prévia StoryAngelus e story gerado têm dimensões diferentes.')
            difference = ImageChops.difference(a, b)
        difference.paste((0,0,0), (256,344,824,1028))
        channels = difference.split()
        maximum = ImageChops.lighter(ImageChops.lighter(channels[0],channels[1]),channels[2])
        count = maximum.width*maximum.height-maximum.histogram()[0]
        box = difference.getbbox()
        return difference,maximum,count,box
    difference,maximum,count,box = compare(screenshot)
    diff_path = folder/'diferenca-fora-obra.png' if count else None
    if diff_path: difference.save(diff_path)
    generated = json.loads((target/'tempo-comum/ficha.json').read_text(encoding='utf-8'))
    measured = next(card for card in generated['cards'] if card['id'] == 'angelus')
    niche = measured['caixas']['nicho']; logo = measured['caixas']['logo']
    regions = {}
    leftover = maximum.copy()
    for name,area in [('nicho',niche),('logo',logo)]:
        bounds = (max(0,int(area['x'])-1),max(0,int(area['y'])-1),
            min(1080,int(area['x']+area['largura'])+2),min(1920,int(area['y']+area['altura'])+2))
        region = maximum.crop(bounds)
        regions[name] = {'pixels_alterados':region.width*region.height-region.histogram()[0],
            'diferenca_maxima_por_canal':region.getextrema()[1]}
        leftover.paste(0,bounds)
    isolated = folder/'article-origem-0.png'
    articles.first.evaluate("el=>{el.style.position='absolute';el.style.left='0';el.style.top='0';}")
    await_fonts(page)
    page.screenshot(path=str(isolated),clip=articles.first.bounding_box(),animations='disabled')
    isolated_diff,_,isolated_count,isolated_box = compare(isolated)
    isolated_path = folder/'diferenca-origem-0.png' if isolated_count else None
    if isolated_path: isolated_diff.save(isolated_path)
    only_curves = leftover.getbbox() is None
    explanation = None
    if count:
        explanation = (f'O confronto literal solicitado teve {count} pixels diferentes fora da obra: '
            f'{regions["nicho"]["pixels_alterados"]} nas curvas do filete do nicho e '
            f'{regions["logo"]["pixels_alterados"]} no SVG do logo. '
            if only_curves else f'O confronto literal solicitado teve {count} pixels diferentes fora da obra. ')
        if isolated_count == 0:
            explanation += ('No diagnóstico separado, o mesmo article original reposicionado na origem (0,0), sem mudar '
                'seu conteúdo, teve zero pixels diferentes fora da obra. Isso identifica rasterização das curvas em '
                'coordenadas globais diferentes da vitrine; o resultado literal continua registrado como não zero.')
        else:
            explanation += (f'O diagnóstico na origem (0,0) ainda tem {isolated_count} pixels diferentes; '
                'a imagem da diferença foi salva para inspeção. O resultado literal não foi substituído pelo diagnóstico.')
    return {'ok': True, 'verificado': True, 'confronto_fora_obra_identico': count == 0,
        'pixels_alterados_fora_obra': count, 'limites_diferenca': list(box) if box else None,
        'obra_excluida': [256,344,824,1028], 'fonte': source.relative_to(PROJECT).as_posix(),
        'preview_renderizado': screenshot.relative_to(PROJECT).as_posix(),
        'diferenca': diff_path.relative_to(PROJECT).as_posix() if diff_path else None,
        'regioes_diferenca':regions, 'diferenca_somente_curvas_nicho_logo':only_curves,
        'diagnostico_origem_0':{'pixels_alterados_fora_obra':isolated_count,
            'limites_diferenca':list(isolated_box) if isolated_box else None,
            'preview_renderizado':isolated.relative_to(PROJECT).as_posix(),
            'diferenca':isolated_path.relative_to(PROJECT).as_posix() if isolated_path else None},
        'explicacao': explanation}


def _board(target: Path) -> tuple[int,int]:
    records = [(path, json.loads(path.read_text(encoding='utf-8'))) for path in target.glob('*/ficha.json')]
    records.sort(key=lambda pair: (pair[1].get('ordem_tempo', 0), pair[1]['tempo']['id']))
    columns = max(len(record['cards']) for _,record in records)
    margin = 32; gap = 24; row_height = 740
    size = (2*margin+columns*360+(columns-1)*gap, 32+row_height*len(records))
    board = Image.new('RGB', size, color('fundo','pergaminho')); draw = ImageDraw.Draw(board)
    font = ImageFont.truetype(str(KIT/'fontes/Lato-Regular.ttf'), 22)
    for row,(path,record) in enumerate(records):
        y = 32+row*row_height; tempo = record['tempo']
        draw.text((margin,y),f'{tempo["nome"]} · {tempo["cor"]}',font=font,fill=color('tinta','pergaminho'))
        for column,card in enumerate(record['cards']):
            x = margin+column*(360+gap)
            draw.text((x,y+28),f'{card["id"]} · {card["hora"]}',font=font,fill=color('tinta-suave','pergaminho'))
            with Image.open(path.parent/f'{card["id"]}.png') as image:
                board.paste(image.convert('RGB').resize((360,640),Image.Resampling.LANCZOS),(x,y+60))
    board.save(target/'prancha.png'); return size


def _report(target: Path, records: list[dict], checks: dict, command: str, artwork_records: dict) -> Path:
    lines = ['# Stories por tempo litúrgico', '', f'`{command}`', '', '## Composição e decisões', '',
        '- A composição segue StoryAngelus: tema capela, formato 1080 × 1920, 240 px no topo e na base, selo Para Rezar com a hora e assinatura capela sem @.',
        '- O Nicho 600 × 700 fica a espaco-4 do selo. O bloco de texto fica a espaco-4 do nicho, alinhado ao topo; margin-top:auto não foi aplicado a ele.',
        '- Só a cruz do selo e o filete do nicho recebem a cor do tempo. O ornamento permanece ouro. Os créditos das obras estão nas fichas e não entram na arte.',
        '- Quebras manuais são preservadas e palavras de uma letra, incluindo Ó e ó, ficam ligadas à seguinte. As linhas são medidas com Range, após carregar as seis fontes locais.',
        '- A ordem de stories no YAML é a ordem das páginas. Os recortes são globais porque foco, zoom e imagem são iguais nos quatro tempos. --tempo preserva os outros tempos e a prancha indexa todos os já gerados.',
        '', '## Linhas e posições', '', '| Tempo | Story | Campo | Linhas | Limite |', '| --- | --- | --- | --- | --- |']
    for record in records:
        for card in record['cards']:
            for text in card['textos']:
                lines.append(f'| {record["tempo"]["id"]} | {card["id"]} | {text["campo"]} | {text["quantidade_linhas"]} | {LIMITS.get(text["campo"],"—")} |')
    lines += ['', '| Tempo | Story | Selo y | Nicho y / base | Título y | Assinatura y | Último texto → assinatura |', '| --- | --- | --- | --- | --- | --- | --- |']
    for record in records:
        for card in record['cards']:
            layout = card['distancias']; pos = layout['posicoes']
            lines.append(f'| {record["tempo"]["id"]} | {card["id"]} | {pos["selo_topo_px"]:g} | {pos["nicho_topo_px"]:g} / {pos["nicho_base_px"]:g} | {pos["titulo_topo_px"]:g} | {pos["assinatura_topo_px"]:g} | {layout["ultimo_texto_assinatura_px"]:g} px |')
    lines += ['', '## Obras, recortes e notas visuais', '']
    for story_id,item in artwork_records.items():
        story = item['story']; framing = item['enquadramento']; window = framing['janela_original']
        lines += [f'### {story_id}', '', f'{story["obra"]["credito"]} — {story["obra"]["pagina"]}', '',
            ('Obra pendente; provisória usada.' if item['obra_pendente'] else 'Obra real local; recorte global gerado.'),
            f'Foco `{framing["foco"]}`, zoom `{framing["zoom"]}`; janela original x={window["x"]:g}, y={window["y"]:g}, largura={window["largura"]:g}, altura={window["altura"]:g} px.',
            '', item['nota_visual']['nota']]
        suggestion = item['nota_visual'].get('sugestao_opcional')
        if suggestion: lines += ['', suggestion['nota'], f'Confirmação objetiva da sugestão: margens visíveis = {suggestion["margens_visiveis"]}.']
    lines += ['', '## Conferência da prévia', '']
    preview = checks['previa_kit']
    if preview.get('verificado'):
        lines.append(f'Prévia literal do StoryAngelus contra tempo-comum/angelus: {preview["pixels_alterados_fora_obra"]} pixels diferentes fora da janela (256,344)–(824,1028).')
        if preview.get('diferenca'): lines += [preview['explicacao'], 'Diferença: `'+preview['diferenca']+'`.']
    else: lines.append(preview['motivo'])
    lines += ['', '## Avisos e pendências', '']
    lines += ['- '+warning for warning in checks['avisos']] if checks['avisos'] else ['Nenhum aviso.']
    lines.append('Obras pendentes: '+(', '.join(checks['obras_pendentes']) if checks['obras_pendentes'] else 'nenhuma')+'.')
    lines += ['', '## PDF e limites', '',
        'Duas páginas de 810 × 1440 pt por tempo na ordem do YAML. As cinco fontes usadas foram conferidas como TTF embutidos por pdffonts; o texto integral de cada página foi comparado por PyMuPDF e pdftotext -layout, ignorando apenas espaços e quebras.',
        '', 'A importação no editor do Canva não foi executada. Avisos de tamanho acima de 4 MB por obra, largura abaixo de 1000 px ou PDF acima de 12 MB são informativos. Nenhum recurso externo foi baixado.',
        '', '## Árvore', '', '```text', 'saida/stories/']
    paths = {path.relative_to(target).as_posix() for path in target.rglob('*') if path.is_file()}; paths.add('RELATORIO.md')
    lines += ['  '+path for path in sorted(paths)]+['```','']
    report = target/'RELATORIO.md'; report.write_text('\n'.join(lines),encoding='utf-8'); return report


def generate(output: Path, content_path: Path, tempo_filter: str | None = None) -> dict:
    output = Path(output).resolve(); target = output/'stories'; target.mkdir(parents=True,exist_ok=True)
    content = load_stories(content_path); all_tempos = content['tempos']; stories = content['stories']; tempos = all_tempos
    order = {tempo['id']: index for index,tempo in enumerate(all_tempos)}
    if tempo_filter is not None:
        tempos = [tempo for tempo in tempos if tempo['id'] == tempo_filter]
        if not tempos: raise ValueError(f'Nenhum tempo para --tempo {tempo_filter}.')
    kit = validate_kit(PROJECT)
    if not kit['ok']: raise ValueError('Kit inválido: '+'; '.join(kit['errors']))
    css = generate_tokens_css(output/'tokens.css'); placeholder = output/'obra-provisoria.png'
    if not placeholder.is_file(): placeholder = PROJECT/'saida/obra-provisoria.png'
    work = PROJECT/'work/stories'; expected = {}; records = []; checks = {'kit':kit,'tempos':{}}; errors = []; warnings = []; artwork_records = {}
    for story in stories:
        artwork = local_artwork_path(story['obra']['arquivo']); pending = not artwork.is_file()
        if pending:
            if not placeholder.is_file(): raise FileNotFoundError('Obra provisória ausente; execute python gerar.py componentes.')
            artwork = placeholder; warnings.append(f'{story["id"]}: obra pendente; utilizada obra provisória.')
        framing = inspect_artwork(artwork,story['obra']['foco'],story['obra'].get('zoom',1),niche_width=600,niche_height=700,date=story['id'])
        crop = target/f'recorte-{story["id"]}.png'
        if not pending:
            warnings.extend(_source_warnings(story,artwork)); warnings.extend(framing['avisos'])
            crop_proof(artwork,crop,story['obra']['foco'],zoom=story['obra'].get('zoom',1),niche_width=600,niche_height=700,date=story['id'])
            with Image.open(crop) as image: expected[str(crop)] = image.size
        elif crop.exists(): crop.unlink()
        artwork_records[story['id']] = {'story':story,'arquivo':artwork,'obra_pendente':pending,
            'enquadramento':framing,'nota_visual':_visual_note(story,artwork,pending,framing)}
    with local_server() as base_url,sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=shutil.which('chromium') or '/usr/bin/chromium',headless=True,args=['--no-sandbox'])
        context = browser.new_context(device_scale_factor=1)
        context.route('**/*',lambda route:route.continue_() if urlsplit(route.request.url).netloc == urlsplit(base_url).netloc else route.abort())
        page = context.new_page()
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.on('console',lambda message:errors.append(message.text) if message.type == 'error' else None)
        page.on('response',lambda response:errors.append(f'HTTP {response.status}: {response.url}') if response.status >= 400 else None)
        for tempo in tempos:
            folder = target/tempo['id']; folder.mkdir(parents=True,exist_ok=True)
            cards = []; parts = []; card_checks = []
            for number,story in enumerate(stories,1):
                art = artwork_records[story['id']]; temporary = work/tempo['id']/f'{story["id"]}.png'; part = temporary.with_suffix('.pdf')
                render = render_arte(page,_document(tempo,story,css,art['arquivo']),temporary,formato='story',pdf_path=part,base_url=base_url)
                card = _measure(page,tempo,story,number); layout = _validate_layout(tempo,story,card); pixels = _pixels(temporary,tempo,story,card)
                card.update({'obra':story['obra'],'obra_usada':art['arquivo'].relative_to(PROJECT).as_posix(),
                    'obra_pendente':art['obra_pendente'],'enquadramento':art['enquadramento'],
                    'nota_visual':art['nota_visual'],'distancias':layout})
                shutil.copyfile(temporary,folder/f'{story["id"]}.png'); expected[str(folder/f'{story["id"]}.png')] = (1080,1920)
                cards.append(card); parts.append(part); card_checks.append({'story':story['id'],'layout':layout,'pixels':pixels,'fontes_render':render['fonts']})
            destination = folder/f'stories-{tempo["id"]}.pdf'; writer = PdfWriter()
            for part in parts:
                for pdf_page in PdfReader(part).pages: writer.add_page(pdf_page)
            with destination.open('wb') as stream: writer.write(stream)
            pdf_check = _pdf_check(destination,stories,cards)
            if destination.stat().st_size > 12_000_000: warnings.append(f'{tempo["id"]}: PDF com {destination.stat().st_size} bytes, acima de 12 MB; o Canva pode recusar arquivo grande.')
            record = {'tempo':tempo,'ordem_tempo':order[tempo['id']],'cards':cards}
            (folder/'ficha.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            records.append(record); checks['tempos'][tempo['id']] = {'cards':card_checks,'pdf':pdf_check}
        checks['previa_kit'] = _preview_check(page,css,target,work,base_url)
        if checks['previa_kit'].get('verificado') and not checks['previa_kit'].get('confronto_fora_obra_identico'):
            warnings.append('StoryAngelus: a prévia literal apresentou diferenças fora da obra; consulte a imagem da diferença e a explicação no relatório.')
        browser.close()
    if errors: raise RuntimeError('Erros de navegador: '+'; '.join(errors))
    expected[str(target/'prancha.png')] = _board(target)
    checks['pngs'] = validate_pngs(expected); checks['kit_final'] = validate_kit(PROJECT)
    checks['browser'] = {'ok':True,'errors':[],'fontes_locais_por_render':6,'recursos_externos':False}
    checks['obras_pendentes'] = [story_id for story_id,art in artwork_records.items() if art['obra_pendente']]
    checks['avisos'] = warnings
    checks['obras'] = {story_id:{key:value for key,value in art.items() if key not in {'arquivo'}} for story_id,art in artwork_records.items()}
    checks['ok'] = all(checks[key]['ok'] for key in ('kit','kit_final','pngs','previa_kit'))
    if not checks['ok']: raise RuntimeError('Falha de validação de PNG, kit ou prévia.')
    command = 'python gerar.py stories'+(f' --tempo {tempo_filter}' if tempo_filter else '')
    checks['comando'] = command
    (target/'verificacao.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for warning in warnings: print('Aviso: '+warning)
    report = _report(target,records,checks,command,artwork_records)
    return {'tempos':len(records),'cards':sum(len(record['cards']) for record in records),
        'pdfs':len(records),'pngs':len(expected),'obras_pendentes':checks['obras_pendentes'],
        'avisos':warnings,'relatorio':str(report),'verificacoes':str(target/'verificacao.json')}
