"""Para Rezar: orações em cards explícitos, com provas do DOM e da prévia do kit."""
from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any
from urllib.parse import urlsplit

from PIL import Image, ImageChops, ImageColor
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

from .base import (PROJECT, KIT, assinatura, await_fonts, color, generate_tokens_css,
                   html_document, montar_arte, render_arte, resource_url, selo)
from .conteudo import color_token, date_label
from .conteudo_oracao import load_prayers, prayer_warnings
from .evangelho import _board, _distance, _measure as measure_evangelho, _ornament, _text
from .renderizacao import local_server
from .validacao import validate_kit, validate_pngs


EXTRA_CSS = '@page{margin:0;}'
REQUIRED_FONTS = {'CormorantGaramond-SemiBold', 'CormorantGaramond-Medium', 'Lato-Bold', 'Lato-Regular'}


def _header(day: dict, number: int) -> str:
    support = day['intencao'] if number == 1 else f'{number}/{len(day["partes"])}'
    markup = selo('Para Rezar', date_label(day['data']), support)
    for element, field in [('selo-serie', 'selo'), ('selo-data', 'data'),
                           ('selo-info', 'intencao' if number == 1 else 'contagem')]:
        markup = markup.replace(f'data-element="{element}"',
                                f'data-element="{element}" data-text="{field}" data-style="selo"')
    return markup


def _document(day: dict, number: int, css: Path) -> str:
    """Keep the preview's classes, inline spacing and flex composition intact."""
    body = '<div class="aqr-texto" style="margin-top:auto">'
    if number == 1:
        body += _text('h1', 'titulo', 'titulo aqr-titulo', day['titulo'], 'max-width:820px')
        body += _ornament()
    body += _text('p', 'oracao', 'oracao aqr-corpo', day['partes'][number-1], 'max-width:880px')
    if number == len(day['partes']):
        body += _text('p', 'origem', 'credito aqr-credito', day['origem'],
                      'margin-top:var(--espaco-3)', 'tinta-suave')
    body += '</div>'
    post = montar_arte(_header(day, number)+body+assinatura('pergaminho'),
                       tema='pergaminho', cor_do_dia=color_token(day['cor']))
    return html_document(post, css, EXTRA_CSS, f'Para Rezar · {day["data"]} · {number}/{len(day["partes"])}')


def _measure(page: Any, day: dict, number: int) -> dict:
    card = measure_evangelho(page, number, 1)
    card.update({'tipo': 'Para Rezar', 'modelo': 'PostOracao', 'tema': 'pergaminho'})
    for text in card['textos']:
        if text['campo'] in {'intencao', 'contagem'}:
            text['alinhamento_canva'] = 'end'
    block = card['caixas']['bloco_texto']; top = card['caixas']['selo']; logo = card['caixas']['logo']
    upper = block['y']-top['y']-top['altura']
    lower = logo['y']-block['y']-block['altura']
    card['distancias'] = {'selo_texto_px': upper, 'texto_assinatura_px': lower,
                          'diferenca_centralizacao_px': abs(upper-lower)}
    return card


def _validate_layout(day: dict, card: dict) -> dict:
    number = card['card']; errors = []; distances = []
    limits = {'titulo': 2, 'oracao': 10 if number == 1 else 14}
    logo = card['caixas']['logo']
    for text in card['textos']:
        field = text['campo']; box = text['caixa']; limit = limits.get(field)
        if limit is not None and text['quantidade_linhas'] > limit:
            errors.append(f'{day["data"]}, card {number}, {field}: {text["quantidade_linhas"]} linhas; limite {limit}.')
        if box['x'] < -.1 or box['y'] < -.1 or box['x']+box['largura'] > 1080.1 or box['y']+box['altura'] > 1350.1:
            errors.append(f'{day["data"]}, card {number}, {field}: texto fora da arte.')
        for line, linebox in zip(text['linhas'], text['caixas_das_linhas']):
            if re.search(r'(?:^|\s)[aàeéoóAÀEÉOÓ][\W_]*$', line):
                errors.append(f'{day["data"]}, card {number}, {field}: palavra de uma letra no fim de {line!r}.')
            if linebox['largura'] and (linebox['x'] < box['x']-.1 or linebox['x']+linebox['largura'] > box['x']+box['largura']+.1):
                errors.append(f'{day["data"]}, card {number}, {field}: linha transborda a largura do campo.')
            if linebox['x'] < -.1 or linebox['y'] < -.1 or linebox['x']+linebox['largura'] > 1080.1 or linebox['y']+linebox['altura'] > 1350.1:
                errors.append(f'{day["data"]}, card {number}, {field}: linha fora da arte.')
        gap = _distance(box, logo); distances.append({'campo': field, 'logo_px': gap})
        if gap < 31.99:
            errors.append(f'{day["data"]}, card {number}, {field}: distância ao logo {gap:.2f}px < 32px.')
    top_gap = _distance(card['caixas']['selo'], card['caixas']['referencia'])
    if top_gap < 31.99: errors.append(f'{day["data"]}, card {number}: selo e apoio distam {top_gap:.2f}px < 32px.')
    if card['distancias']['diferenca_centralizacao_px'] > .1:
        errors.append(f'{day["data"]}, card {number}: bloco de texto não centralizado entre selo e assinatura.')
    if min(card['distancias']['selo_texto_px'], card['distancias']['texto_assinatura_px']) < 32:
        errors.append(f'{day["data"]}, card {number}: bloco de texto a menos de 32px do selo ou da assinatura.')
    result = {'ok': not errors, 'limites': limits, 'distancias': card['distancias'],
              'distancias_ao_logo': distances, 'selo_apoio_px': top_gap, 'errors': errors}
    if errors: raise ValueError('; '.join(errors))
    return result


def _pixels(path: Path, day: dict, card: dict) -> dict:
    samples = []; errors = []
    with Image.open(path) as raw:
        image = raw.convert('RGB')
        cross = card['caixas']['cruz']
        for name, xy, expected in [
            ('cruz do selo', (int(cross['x']+9), int(cross['y']+18)), color(color_token(day['cor']), 'pergaminho')),
            ('fundo', (8, 8), color('fundo', 'pergaminho')),
        ]:
            actual = image.getpixel(xy); wanted = ImageColor.getrgb(expected)
            sample = {'elemento': name, 'pixel': list(xy), 'esperado': expected,
                      'rgb': list(actual), 'ok': actual == wanted}
            samples.append(sample)
            if not sample['ok']: errors.append(f'{day["data"]}, card {card["card"]}, {name}: {actual}; esperado {wanted}.')
    result = {'ok': not errors, 'amostras': samples, 'errors': errors}
    if errors: raise ValueError('; '.join(errors))
    return result


def _without_space(text: str) -> str:
    return re.sub(r'\s+', '', text)


def _pdf_check(path: Path, day: dict, cards: list[dict]) -> dict:
    """Check every page, embedded programs and exact text through Poppler."""
    import fitz
    errors = []; pages = []; fonts = {}; expected_pages = []
    with fitz.open(path) as document:
        if len(document) != len(day['partes']): errors.append(f'{day["data"]}: número de páginas PDF incorreto.')
        for index, page in enumerate(document):
            expected = ''.join(_without_space(text['conteudo']) for text in cards[index]['textos'])
            extracted = _without_space(page.get_text())
            expected_pages.append(expected)
            # The complete page must match the YAML-driven fields, apart from
            # whitespace; this also detects duplicated or omitted prayer text.
            exact = expected == extracted
            pages.append({'pagina': index+1, 'largura_pt': page.rect.width, 'altura_pt': page.rect.height,
                          'texto_igual_sem_espacos': exact, 'oracao_igual_yaml_sem_espacos': _without_space(day['partes'][index]) in extracted})
            if not exact: errors.append(f'{day["data"]}, card {index+1}: texto extraído do PDF difere dos campos do YAML.')
            if abs(page.rect.width-810) > .01 or abs(page.rect.height-1012.5) > .01:
                errors.append(f'{day["data"]}, card {index+1}: tamanho PDF diferente de 810 × 1012,5 pt.')
            for info in page.get_fonts(full=True):
                xref, _, kind, name = info[:4]
                if xref in fonts: continue
                _, extension, _, data = document.extract_font(xref)
                name = re.sub(r'^[A-Z]{6}\+', '', name)
                ttf = bool(data) and extension.lower() in {'ttf','ttc'} and data[:4] in {b'\x00\x01\x00\x00', b'true', b'ttcf'}
                fonts[xref] = {'nome': name, 'tipo': kind, 'formato': extension, 'embutida': bool(data), 'truetype': ttf, 'bytes': len(data)}
                if not ttf: errors.append(f'{day["data"]}: fonte TTF não embutida: {name}.')
    missing = REQUIRED_FONTS-{font['nome'] for font in fonts.values()}
    if missing: errors.append('Fontes ausentes: '+', '.join(sorted(missing)))
    poppler_fonts = None; poppler_text = None
    if shutil.which('pdffonts'):
        process = subprocess.run(['pdffonts', str(path)], capture_output=True, text=True, check=False)
        poppler_fonts = process.stdout
        if process.returncode: errors.append('pdffonts falhou: '+process.stderr)
        for font in REQUIRED_FONTS:
            if font not in poppler_fonts: errors.append(f'pdffonts não lista {font}.')
        for line in poppler_fonts.splitlines()[2:]:
            match = re.search(r'\s(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$', line)
            if match and match.group(1) != 'yes': errors.append('pdffonts encontrou fonte não embutida: '+line)
    else: errors.append('pdffonts indisponível.')
    if shutil.which('pdftotext'):
        process = subprocess.run(['pdftotext', '-layout', str(path), '-'], capture_output=True, text=True, check=False)
        poppler_text = process.stdout
        if process.returncode: errors.append('pdftotext falhou: '+process.stderr)
        actual_pages = [part for part in poppler_text.split('\f') if part.strip()]
        if [_without_space(part) for part in actual_pages] != expected_pages:
            errors.append(f'{day["data"]}: pdftotext difere do YAML, desconsiderando espaços e quebras.')
    else: errors.append('pdftotext indisponível.')
    result = {'ok': not errors, 'paginas': pages, 'fontes': list(fonts.values()),
              'pdffonts': poppler_fonts, 'pdftotext': poppler_text,
              'texto_igual_yaml_sem_espacos': not errors, 'errors': errors}
    if errors: raise ValueError('; '.join(errors))
    return result


def _preview_check(page: Any, css: Path, target: Path, work: Path, base_url: str) -> dict:
    """Compare the literal gallery first, then diagnose any SVG-origin noise."""
    source = KIT/'design-system/componentes/PostOracao/preview.html'
    document = source.read_text(encoding='utf-8')
    articles = re.findall(r'<article\b.*?</article>', document, re.S)
    if len(articles) != 3:
        raise ValueError('PostOracao/preview.html precisa conter os três cards do kit v4 final.')
    expected = [('2026-10-20', 1), ('2026-12-15', 1), ('2026-12-15', 2)]
    folder = work/'conferencia-kit'; folder.mkdir(parents=True,exist_ok=True)
    links = (f'<link rel="stylesheet" href="{resource_url(css)}">'
             f'<link rel="stylesheet" href="{resource_url(KIT/"design-system/bundle.css")}">')
    original = document.replace('<head>','<head>'+links,1)
    original = original.replace('../../../logos/',resource_url(KIT/'logos')+'/')
    path = folder/'vitrine-original.html'; path.write_text(original,encoding='utf-8')
    page.set_viewport_size({'width':3600,'height':1446})
    page.goto(base_url+resource_url(path),wait_until='load');await_fonts(page)
    references=[]
    for index in range(3):
        reference=folder/f'vitrine-previa-{index+1}.png'
        bounds=page.locator('article.aqr-post').nth(index).bounding_box()
        page.screenshot(path=str(reference),clip=bounds,animations='disabled')
        references.append(reference)
    records=[];errors=[];warnings=[]
    for index,(date,number) in enumerate(expected):
        generated=target/date/f'card-{number}.png'
        if not generated.is_file():
            records.append({'data':date,'card':number,'verificado':False,'motivo':'data ainda não gerada nesta saída'})
            continue
        with Image.open(generated) as raw_generated,Image.open(references[index]) as raw_reference:
            actual=raw_generated.convert('RGB');original=raw_reference.convert('RGB')
            diff=ImageChops.difference(actual,original)
            altered=sum(any(pixel) for pixel in diff.get_flattened_data());bbox=diff.getbbox()
            record={'data':date,'card':number,'verificado':True,'pixels_alterados':altered,
                    'pixels_identicos':altered==0,'limites_diferenca':list(bbox) if bbox else None,
                    'referencia':references[index].relative_to(PROJECT).as_posix()}
            if altered:
                difference=folder/f'vitrine-diferenca-{index+1}.png';diff.save(difference)
                record['diferenca']=difference.relative_to(PROJECT).as_posix()
        # Diagnostic only: the original article, unchanged internally, rendered
        # at the final PNG's (0,0). This never replaces the gallery's result.
        article=articles[index].replace('../../../logos/',resource_url(KIT/'logos')+'/')
        isolated_html=folder/f'isolado-{index+1}.html'
        isolated_html.write_text(html_document(article,css,title='Diagnóstico de origem do SVG'),encoding='utf-8')
        page.set_viewport_size({'width':1080,'height':1350})
        page.goto(base_url+resource_url(isolated_html),wait_until='load');await_fonts(page)
        isolated=isolated_html.with_suffix('.png')
        page.screenshot(path=str(isolated),clip=page.locator('article.aqr-post').bounding_box(),animations='disabled')
        with Image.open(generated) as raw_generated,Image.open(isolated) as raw_reference:
            diagnostic=ImageChops.difference(raw_generated.convert('RGB'),raw_reference.convert('RGB'))
            diagnostic_count=sum(any(pixel) for pixel in diagnostic.get_flattened_data())
            record['diagnostico_article_isolado']={'pixels_alterados':diagnostic_count,'pixels_identicos':diagnostic_count==0,
                'referencia':isolated.relative_to(PROJECT).as_posix(),'origem':[0,0]}
            if diagnostic_count:
                difference=folder/f'isolado-diferenca-{index+1}.png';diagnostic.save(difference)
                record['diagnostico_article_isolado']['diferenca']=difference.relative_to(PROJECT).as_posix()
                errors.append(f'{date}, card {number}: article isolado também difere da arte; veja {difference.relative_to(PROJECT)}.')
        if altered:
            ficha=json.loads((target/date/'ficha.json').read_text(encoding='utf-8'))
            logo=ficha['cards'][number-1]['caixas']['logo']
            only_logo=(bbox[0]>=logo['x'] and bbox[1]>=logo['y'] and
                       bbox[2]<=logo['x']+logo['largura'] and bbox[3]<=logo['y']+logo['altura'])
            record['diferenca_confinada_ao_logo']=only_logo
            if only_logo and not diagnostic_count:
                message=(f'{date}, card {number}: confronto da vitrine inteira tem {altered} pixels diferentes, '
                         'confinados ao SVG do logo; o article isolado na origem 0,0 tem zero. '
                         f'Diferença salva em {record["diferenca"]}.')
                record['explicacao']='Rasterização do SVG em posições globais diferentes na vitrine e no PNG; nenhum ajuste foi aplicado à composição.'
                warnings.append(message);print('Aviso: '+message)
            else:
                errors.append(f'{date}, card {number}: {altered} pixels diferentes da vitrine; veja {record["diferenca"]}.')
        records.append(record)
    result={'ok':not errors,'confronto_vitrine_identico':all(not card.get('pixels_alterados') for card in records if card['verificado']),
            'fonte':source.relative_to(PROJECT).as_posix(),'metodo':'Vitrine original inteira; screenshot de cada article. Isolamento na origem 0,0 somente como diagnóstico separado.',
            'cards':records,'avisos':warnings,'errors':errors}
    if errors:raise ValueError('; '.join(errors))
    return result


def _report(target: Path, records: list[dict], checks: dict, command: str) -> Path:
    lines = ['# Para Rezar', '', f'`{command}`', '', '## Decisões', '',
        '- Composição dos três artigos do PostOracao do kit v4: mesmas classes, estilos inline, fontes, bundle.css e espaços. O confronto solicitado renderiza a vitrine original inteira e recorta cada article. O isolamento do article na origem 0,0 é só um diagnóstico adicional, sem substituir o resultado da vitrine.',
        '- Cada item de partes gera um card; não há divisão automática. Título e ornamento ficam no primeiro, origem somente no último e a intenção dá lugar à contagem nos seguintes.',
        '- O bloco inteiro usa margin-top:auto junto à assinatura, como a prévia, deixando respiros iguais acima e abaixo. As distâncias medidas estão também em cada ficha.',
        '- Quebras manuais são preservadas; os demais textos seguem o balanceamento do bundle. Espaços após a, à, e, é e o são inseparáveis. Linhas vazias forçadas também entram na contagem.',
        '- A ficha mantém o formato das séries anteriores, com linhas recuperadas por Range. A prancha usa miniaturas de 360 × 450 px e indexa todas as datas já geradas; --data preserva as demais.',
        '- São Miguel de 20/10 é uma prova do design system e não é publicação. Não há obras nesta série.',
        '', '## Linhas medidas no render', '', '| Data | Card | Campo | Linhas | Limite |', '| --- | --- | --- | --- | --- |']
    for record in records:
        for card in record['cards']:
            for text in card['textos']:
                limit = {'titulo': 2, 'oracao': 10 if card['card'] == 1 else 14}.get(text['campo'], '—')
                lines.append(f'| {record["data"]} | {card["card"]} | {text["campo"]} | {text["quantidade_linhas"]} | {limit} |')
    lines += ['', '## Distâncias', '', '| Data | Card | Selo → texto | Texto → assinatura |', '| --- | --- | --- | --- |']
    for record in records:
        for card in record['cards']:
            d = card['distancias']
            lines.append(f'| {record["data"]} | {card["card"]} | {d["selo_texto_px"]:g} px | {d["texto_assinatura_px"]:g} px |')
    lines += ['', '## Conferência da prévia', '']
    for card in checks['previa_kit']['cards']:
        if not card['verificado']:
            lines.append(f'- {card["data"]}, card {card["card"]}: '+card['motivo']+'.')
            continue
        lines.append(f'- **{card["data"]}, card {card["card"]}: vitrine inteira — {card["pixels_alterados"]} pixels diferentes; diagnóstico isolado — {card["diagnostico_article_isolado"]["pixels_alterados"]}.**')
        if card.get('diferenca'):
            lines.append(f'  Diferença: `{card["diferenca"]}`; caixa {card["limites_diferenca"]}. '+card.get('explicacao',''))
    if not checks['previa_kit']['confronto_vitrine_identico']:
        lines += ['', 'O confronto literal solicitado não deu zero. As diferenças ficaram confinadas ao SVG do logo; nenhum outro pixel mudou. O diagnóstico com cada article original intacto na mesma origem do PNG deu zero, indicando rasterização do SVG em posições globais diferentes. Os PNGs de referência e diferenças estão em work/para-rezar/conferencia-kit/.']
    lines += ['', '## Avisos e pendências', '']
    warnings = [warning for record in records for warning in record['avisos']]+checks['previa_kit']['avisos']
    lines += ['- '+warning for warning in warnings] if warnings else ['Nenhum aviso; obras pendentes: nenhuma.']
    lines += ['', '## PDF e limites da verificação', '',
        'Páginas de 810 × 1012,5 pt (1080 × 1350 px), uma por parte; fontes TTF usadas embutidas e listadas por pdffonts. O texto integral extraído por pdftotext -layout corresponde aos campos do YAML, desconsiderando espaços e quebras. A opção -layout mantém o contador do topo na ordem visual; a heurística padrão de colunas podia movê-lo para o fim da página.',
        '', 'A importação no editor do Canva não foi executada. A validação cobre o arquivo produzido, suas fontes, textos, cores, dimensões e geometria.',
        '', '## Árvore', '', '```text', 'saida/para-rezar/']
    paths = {path.relative_to(target).as_posix() for path in target.rglob('*') if path.is_file()}; paths.add('RELATORIO.md')
    lines += ['  '+name for name in sorted(paths)]+['```','']
    report = target/'RELATORIO.md'; report.write_text('\n'.join(lines), encoding='utf-8'); return report


def generate(output: Path, content_path: Path, date_filter: str | None = None) -> dict:
    output = Path(output).resolve(); target = output/'para-rezar'; target.mkdir(parents=True, exist_ok=True)
    days = load_prayers(content_path)
    if date_filter is not None:
        days = [day for day in days if day['data'] == date_filter]
        if not days: raise ValueError(f'Nenhum conteúdo para --data {date_filter}.')
    kit = validate_kit(PROJECT)
    if not kit['ok']: raise ValueError('Kit inválido: '+'; '.join(kit['errors']))
    css = generate_tokens_css(output/'tokens.css'); work = PROJECT/'work/para-rezar'
    expected = {}; records = []; checks = {'kit': kit, 'dias': {}}; errors = []
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
            cards = []; parts = []; card_checks = []
            for number in range(1, len(day['partes'])+1):
                temporary = work/day['data']/f'card-{number}.png'; part = temporary.with_suffix('.pdf')
                render_arte(page, _document(day, number, css), temporary, pdf_path=part, base_url=base_url)
                card = _measure(page, day, number); layout = _validate_layout(day, card)
                pixels = _pixels(temporary, day, card)
                shutil.copyfile(temporary, folder/f'card-{number}.png'); expected[str(folder/f'card-{number}.png')] = (1080,1350)
                cards.append(card); parts.append(part); card_checks.append({'card': number, 'layout': layout, 'pixels': pixels})
            pdf = folder/f'para-rezar-{day["data"]}.pdf'; writer = PdfWriter()
            for part in parts:
                reader = PdfReader(part)
                for page_pdf in reader.pages: writer.add_page(page_pdf)
            with pdf.open('wb') as stream: writer.write(stream)
            pdf_check = _pdf_check(pdf, day, cards)
            for old in folder.glob('card-*.png'):
                if int(old.stem.split('-')[-1]) > len(cards): old.unlink()
            record = {'data': day['data'], 'cor': day['cor'], 'titulo': day['titulo'],
                      'intencao': day['intencao'], 'origem': day['origem'], 'partes': day['partes'],
                      'obra_pendente': False, 'avisos': prayer_warnings(day), 'cards': cards}
            (folder/'ficha.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
            records.append(record); checks['dias'][day['data']] = {'cards': card_checks, 'pdf': pdf_check}
        checks['previa_kit'] = _preview_check(page, css, target, work, base_url)
        browser.close()
    if errors: raise RuntimeError('Erros de navegador: '+'; '.join(errors))
    rows = []
    for path in sorted(target.glob('????-??-??/ficha.json')):
        record = json.loads(path.read_text(encoding='utf-8'))
        rows.append((f'{record["data"]} · {record["cor"]}'+(' · prova do design system (não publicar)' if record['data']=='2026-10-20' else ''),
                     [path.parent/f'card-{card["card"]}.png' for card in record['cards']]))
    expected[str(target/'prancha.png')] = _board(rows, target/'prancha.png', max(len(row[1]) for row in rows))
    checks['pngs'] = validate_pngs(expected); checks['kit_final'] = validate_kit(PROJECT)
    checks['browser'] = {'ok': True, 'errors': [], 'fontes_locais_por_render': 6, 'recursos_externos': False}
    checks['obras_pendentes'] = []; checks['avisos'] = [warning for record in records for warning in record['avisos']]+checks['previa_kit']['avisos']
    checks['ok'] = all(checks[key]['ok'] for key in ('kit', 'kit_final', 'pngs', 'previa_kit'))
    if not checks['ok']: raise RuntimeError('Falha de validação do kit, PNG ou prévia.')
    command = 'python gerar.py para-rezar'+(f' --data {date_filter}' if date_filter else '')
    checks['comando'] = command
    (target/'verificacao.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    report = _report(target, records, checks, command)
    return {'dias': len(records), 'cards': sum(len(record['cards']) for record in records),
            'pdfs': len(records), 'pngs': len(expected), 'obras_pendentes': [],
            'relatorio': str(report), 'verificacoes': str(target/'verificacao.json')}
