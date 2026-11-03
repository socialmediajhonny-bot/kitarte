"""Carrosséis Igreja Doméstica, com obras locais e provas por data.

Somente esta série recebe arquivos novos. Os tokens de renderização e os
arquivos intermediários ficam em work/igreja-domestica/.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import shutil
from urllib.parse import urlsplit

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

from .base import PROJECT, KIT, color, generate_tokens_css, render_arte
from .conteudo import local_artwork_path
from .conteudo_igreja_domestica import load_domestic_church
from .igreja_domestica import (_document, _measure, _pdf_check, _pixels,
                              _validate_layout, expand_cards, expected_layout)
from .obras import crop_proof, inspect_artwork
from .renderizacao import local_server
from .validacao import validate_kit, validate_pngs


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def _relative(path: Path) -> str:
    return Path(path).resolve().relative_to(PROJECT).as_posix()


def _merge(parts: list[Path], destination: Path) -> None:
    writer = PdfWriter()
    for part in parts:
        for page in PdfReader(part).pages:
            writer.add_page(page)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('wb') as stream:
        writer.write(stream)


def _records(target: Path) -> list[dict]:
    return [json.loads(path.read_text(encoding='utf-8'))
            for path in sorted(target.glob('????-??-??/ficha.json'))]


def _visual_note(target: Path, date: str, pending: bool) -> dict:
    """Leia as notas visuais persistidas sem presumir detecção de rostos."""
    if pending:
        return {'inspecionada': False, 'nota': 'Obra pendente; usada a imagem provisória. Rostos e vela não puderam ser conferidos.'}
    path = target/'NOTAS-DAS-OBRAS.json'
    if path.is_file():
        notes = json.loads(path.read_text(encoding='utf-8'))
        if date in notes:
            value = notes[date]
            if not isinstance(value, dict) or not isinstance(value.get('nota'), str):
                raise ValueError(f'{path.name}, {date}: a nota visual precisa conter texto em nota.')
            return deepcopy(value)
    return {'inspecionada': False,
            'nota': 'Obra real local e janela de recorte registradas; conferir visualmente os rostos e a vela antes de publicar.'}


def refresh_visual_notes(target: Path) -> list[dict]:
    """Atualize somente metadados depois de inspecionar os recortes e capas."""
    target = Path(target)
    records = _records(target)
    for record in records:
        note = _visual_note(target, record['data'], record['obra_pendente'])
        record['nota_visual'] = note
        record['cards'][0]['nota_visual'] = note
        _write_json(target/record['data']/'ficha.json', record)
    return records


def _margin_recommendation(artwork: Path, work: dict, framing: dict) -> dict | None:
    if not framing['margens_visiveis']:
        return None
    start = max(1, work.get('zoom', 1))
    for step in range(1, 41):
        zoom = round(start+step*.05, 6)
        if zoom > 3:
            break
        proposed = inspect_artwork(artwork, work['foco'], zoom,
                                  niche_width=600, niche_height=680)
        if not proposed['margens_visiveis']:
            return {'foco': work['foco'], 'zoom': zoom,
                    'janela_original': proposed['janela_original'],
                    'nota': 'Sugestão geométrica para retirar as margens detectadas; conferir os rostos e a vela antes de adotar. O YAML não foi alterado.'}
    return {'nota': 'Não foi encontrada correção de margem até zoom 3 mantendo o foco; rever foco e zoom visualmente. O YAML não foi alterado.'}


def _row(spec: dict, measured: dict, layout: dict) -> dict:
    counts = {text['campo']: text['quantidade_linhas'] for text in measured['textos']
              if text['campo'] not in {'selo', 'data', 'contagem', 'rotulo'}
              and not text['campo'].startswith('numero_')}
    expected = expected_layout(spec)
    distances = layout['distancias']
    differences = []
    for field, wanted in expected.get('linhas', {}).items():
        if counts.get(field) != wanted:
            differences.append(f'{field}: {counts.get(field, "ausente")} linhas; previsto {wanted}')
    if 'folga_px' in expected:
        for field in ('selo_texto_px', 'texto_assinatura_px'):
            if abs(distances[field]-expected['folga_px']) > .01:
                differences.append(f'{field}: {distances[field]:g}px; previsto {expected["folga_px"]:g}px')
    for field in ('selo_nicho_px', 'apoio_assinatura_px'):
        if field in expected and abs(distances[field]-expected[field]) > .01:
            differences.append(f'{field}: {distances[field]:g}px; previsto {expected[field]:g}px')
    return {'data': spec['data'], 'card': spec['numero'], 'tipo': spec['tipo'],
            'linhas': counts, 'distancias': distances, 'previsto': expected,
            'diferencas_tabela': differences}


def _board(target: Path, records: list[dict]) -> tuple[int, int]:
    columns = max(len(record['cards']) for record in records)
    left, top, gap, row_height = 32, 52, 24, 530
    size = (2*left+columns*360+(columns-1)*gap, 32+row_height*len(records))
    board = Image.new('RGB', size, color('fundo', 'pergaminho'))
    draw = ImageDraw.Draw(board)
    font = ImageFont.truetype(str(KIT/'fontes/Lato-Regular.ttf'), 22)
    for row, record in enumerate(records):
        y = 32+row*row_height
        draw.text((left, y), f'{record["data"]} · {len(record["cards"])} cards · {record["cor"]}',
                  font=font, fill=color('tinta', 'pergaminho'))
        for column, card in enumerate(record['cards']):
            path = target/record['data']/card['arquivo']
            with Image.open(path) as image:
                board.paste(image.convert('RGB').resize((360, 450), Image.Resampling.LANCZOS),
                            (left+column*(360+gap), y+top))
    board.save(target/'prancha.png')
    return size


def _report(target: Path, records: list[dict], checks: dict, command: str) -> Path:
    lines = ['# Igreja Doméstica', '', f'`{command}`', '', '## Conteúdo e composição', '',
        '- Os textos foram escritos pela página e aprovados em 03/11/2026. O YAML mantém as quebras manuais e a ordem dos cards, itens e falas.',
        '- PostIgrejaDomestica usa feed 1080 × 1350 e tema pergaminho. O selo traz a série e a data; do segundo card em diante aparece a contagem à direita.',
        '- A capa segue o fluxo abaixo do selo: Nicho 600 × 680 com foco e zoom do YAML, crédito, título e apoio. A imagem entra dentro do arco; o crédito aparece na capa, e a página da obra fica somente na ficha e neste relatório.',
        '- Passos, oração e conversa mantêm o bloco centralizado entre selo e assinatura, com pelo menos 60 px de folga e diferença de centralização até 0,1 px. Na capa, o apoio fica a pelo menos 32 px da assinatura.',
        '- O gap de 16 px do kit recebe margens inline em tokens: 48 px do rótulo ou da instrução ao texto seguinte e 32 px de um texto à sua fonte. Todos os pares são medidos no navegador com tolerância de ±0,01 px.',
        '- A lista usa 820 px, coluna de número de 24 px, intervalo de 20 px e texto em corpo alinhado à esquerda com text-wrap:pretty. Cada número em Lato Bold fica na linha de base da primeira linha do item; entre itens há 32 px.',
        '- Rubricas usam corpo/tinta-suave e até duas linhas; oração usa oracao/tinta e até seis; aclamação usa citacao, Cormorant Garamond Medium Italic, em uma linha. Há 48 px entre falas e 32 px antes da origem opcional.',
        '- A cruz e o filete seguem a cor do YAML; números e ornamento são ouro. A conversa ocupa o cartão inteiro nessa cor, com todos os textos, cruz, ornamento e logo em sobre-cor.',
        '- As palavras de uma letra seguem o helper compartilhado intacto. Só esta série protege palavras com hífen, referências bíblicas inteiras com espaço inseparável entre livro e capítulo e ordinais unidos à palavra seguinte, como 3º domingo.',
        '- O modelo existe apenas no gerador, sem prévia equivalente no kit. Nenhum arquivo do kit ou recurso das novenas e dos stories foi alterado.',
        '', '## Tabela prevista no prompt', '',
        '| Data · card | Linhas previstas | Folgas previstas |', '| --- | --- | --- |',
        '| 29/11 · 1 · capa | crédito 1, título 1, apoio 1 | selo → nicho 32 px; apoio → assinatura 116 px |',
        '| 29/11 · 2 · passos | título 1; itens 2, 2, 2 e 2; fonte 1 | 128,5 px acima e abaixo |',
        '| 29/11 · 3 · oração | título 1; rubricas 2 e 1; oração 4; aclamação 1 | 103,5 px acima e abaixo |',
        '| 29/11 · 4 · conversa | pergunta 2; convite 1 | 353,5 px acima e abaixo |',
        '| 6/12 · 1 · capa | crédito 1, título 1, apoio 1 | selo → nicho 32 px; apoio → assinatura 116 px |',
        '| 6/12 · 2 · oração | título 1; rubricas 2 e 1; oração 4; aclamação 1 | 103,5 px acima e abaixo |',
        '| 6/12 · 3 · conversa | pergunta 2; convite 1 | 353,5 px acima e abaixo |',
        '', '## Valores medidos no navegador', '',
        '| Data | Card | Tipo | Linhas | Distâncias e folgas |', '| --- | --- | --- | --- | --- |']
    rows = [row for record in records for row in record['tabela_medida']]
    for row in rows:
        counts = '; '.join(f'{field}: {count}' for field, count in row['linhas'].items())
        distances = '; '.join(f'{field}: {value:g}px' for field, value in row['distancias'].items())
        lines.append(f'| {row["data"]} | {row["card"]} | {row["tipo"]} | {counts} | {distances} |')
    lines += ['', '## Diferenças da tabela prevista', '']
    differences = [f'{row["data"]}, card {row["card"]}: '+ '; '.join(row['diferencas_tabela'])
                   for row in rows if row['diferencas_tabela']]
    lines += ['- '+value for value in differences] if differences else ['Nenhuma diferença.']
    lines += ['', '## Obras, enquadramentos e recortes', '']
    for record in records:
        work = record['obra']; framing = record['enquadramento']; window = framing['janela_original']
        note = _visual_note(target, record['data'], record['obra_pendente'])
        lines += [f'### {record["data"]}', '', f'{work["credito"]} — {work["pagina"]}', '',
            'Obra pendente; imagem provisória usada, sem recorte real.' if record['obra_pendente'] else 'Obra real local, sem novo download. Recorte gerado com a pintura inteira e o contorno da janela do arco.',
            f'Foco `{framing["foco"]}`, zoom `{framing["zoom"]}`; janela original x={window["x"]:g}, y={window["y"]:g}, largura={window["largura"]:g}, altura={window["altura"]:g} px.', '', note['nota']]
        recommendation = record.get('recomendacao_margem')
        if recommendation:
            lines += ['', recommendation['nota']]
            if 'foco' in recommendation:
                lines.append(f'Sugestão para a margem: foco `{recommendation["foco"]}`, zoom `{recommendation["zoom"]}`.')
        suggestion = note.get('sugestao')
        if isinstance(suggestion, dict):
            lines += ['', f'Sugestão visual: foco `{suggestion["foco"]}`, zoom `{suggestion["zoom"]}`. '+suggestion.get('nota', '')]
    lines += ['', '## Avisos e pendências', '']
    warnings = [warning for record in records for warning in record['avisos']]+differences
    lines += ['- '+warning for warning in warnings] if warnings else ['Nenhum aviso.']
    pending = [record['data'] for record in records if record['obra_pendente']]
    lines.append('Obras pendentes: '+(', '.join(pending) if pending else 'nenhuma')+'.')
    visual_pending = [record['data'] for record in records if not _visual_note(target, record['data'], record['obra_pendente']).get('inspecionada')]
    if visual_pending:
        lines.append('Inspeção visual dos rostos e da vela pendente: '+', '.join(visual_pending)+'.')
    lines += ['', '## PDF e conferências', '',
        'Cada data recebe um PDF com os cards na ordem do YAML, páginas de 810 × 1012,5 pt e texto e fontes embutidas conferidos por PyMuPDF, pdffonts e pdftotext. A ficha preserva as caixas de cada linha, as falas, as posições da lista e os dados do enquadramento.',
        '', 'A importação destes PDFs no editor do Canva ainda não foi executada.',
        '', '## O que conferir no Canva', '',
        '- Cada texto na sua caixa: selo, contagem, rótulo, título, apoio, crédito, cada rubrica, a oração, a aclamação, cada número e cada item, a fonte, a pergunta e o convite.',
        '- A obra dentro do arco.',
        '- O filete, o parapeito e o ornamento como formas.',
        '- Nenhuma caixa solta.',
        '', 'A evidência da geração está em [verificacao.json](verificacao.json).']
    if (target/'CONFERENCIA-PROMPT-10.md').is_file():
        lines += ['', 'A preservação das saídas anteriores e a conferência independente desta série estão registradas em [CONFERENCIA-PROMPT-10.md](CONFERENCIA-PROMPT-10.md), com [evidência detalhada](conferencia-prompt10.json).']
    lines += ['', '## Árvore', '', '```text', 'saida/igreja-domestica/']
    names = {path.relative_to(target).as_posix() for path in target.rglob('*') if path.is_file()}
    names.add('RELATORIO.md')
    lines += ['  '+name for name in sorted(names)]+['```', '']
    report = target/'RELATORIO.md'
    report.write_text('\n'.join(lines), encoding='utf-8')
    return report


def generate(output: Path, content_path: Path, date_filter: str | None = None) -> dict:
    output = Path(output).resolve()
    days = load_domestic_church(content_path)
    if date_filter is not None:
        days = [day for day in days if day['data'] == date_filter]
        if not days:
            raise ValueError(f'Nenhum conteúdo para --data {date_filter}.')
    kit = validate_kit(PROJECT)
    if not kit['ok']:
        raise ValueError('Kit inválido: '+'; '.join(kit['errors']))
    target = output/'igreja-domestica'
    target.mkdir(parents=True, exist_ok=True)
    work = PROJECT/'work/igreja-domestica'
    css = generate_tokens_css(work/'tokens.css')
    placeholder = output/'obra-provisoria.png'
    if not placeholder.is_file():
        placeholder = PROJECT/'saida/obra-provisoria.png'
    previous = target/'verificacao.json'
    day_checks = json.loads(previous.read_text(encoding='utf-8')).get('dias', {}) if previous.is_file() else {}
    errors = []
    generated_cards = 0
    generated_crops = 0
    with local_server() as base_url, sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=shutil.which('chromium') or '/usr/bin/chromium', headless=True, args=['--no-sandbox'])
        context = browser.new_context(device_scale_factor=1)
        context.route('**/*', lambda route: route.continue_()
                      if urlsplit(route.request.url).netloc == urlsplit(base_url).netloc else route.abort())
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('console', lambda message: errors.append(message.text) if message.type=='error' else None)
        page.on('response', lambda response: errors.append(f'HTTP {response.status}: {response.url}') if response.status>=400 else None)
        for day in days:
            cards = expand_cards([day])
            cover = cards[0]
            artwork = local_artwork_path(cover['obra']['arquivo'])
            pending = not artwork.is_file()
            if pending:
                if not placeholder.is_file():
                    raise FileNotFoundError('Imagem provisória ausente; execute python gerar.py componentes.')
                artwork = placeholder
            folder = target/day['data']
            folder.mkdir(parents=True, exist_ok=True)
            framing = inspect_artwork(artwork, cover['obra']['foco'], cover['obra'].get('zoom', 1),
                                      niche_width=600, niche_height=680, date=day['data'])
            warnings = ([f'{day["data"]}: obra pendente; imagem provisória usada.'] if pending else framing['avisos'])
            crop = folder/'recorte.png'
            if pending:
                if crop.exists():
                    crop.unlink()
            else:
                crop_proof(artwork, crop, cover['obra']['foco'], zoom=cover['obra'].get('zoom', 1),
                           niche_width=600, niche_height=680, date=day['data'])
                generated_crops += 1
            note = _visual_note(target, day['data'], pending)
            measurements = []
            parts = []
            checks = []
            rows = []
            for spec in cards:
                png = work/day['data']/f'card-{spec["numero"]}.png'
                pdf = png.with_suffix('.pdf')
                rendered = render_arte(page, _document(spec, css, artwork if spec['tipo']=='capa' else None),
                                       png, pdf_path=pdf, base_url=base_url)
                measured = _measure(page, spec)
                layout = _validate_layout(spec, measured)
                measured['distancias'] = layout['distancias']
                pixels = _pixels(png, spec, measured)
                measured.update({'card':spec['numero'], 'pagina':spec['numero'],
                                 'arquivo':png.name, 'conteudo':deepcopy(spec)})
                if spec['tipo']=='capa':
                    measured.update({'obra':deepcopy(cover['obra']), 'obra_usada':_relative(artwork),
                                     'obra_pendente':pending, 'enquadramento':framing, 'nota_visual':note})
                shutil.copyfile(png, folder/png.name)
                measurements.append(measured)
                parts.append(pdf)
                rows.append(_row(spec, measured, layout))
                checks.append({'card':spec['numero'], 'tipo':spec['tipo'], 'layout':layout,
                               'pixels':pixels, 'fontes_render':rendered['fonts']})
                generated_cards += 1
            destination = folder/f'igreja-domestica-{day["data"]}.pdf'
            _merge(parts, destination)
            pdf_check = _pdf_check(destination, cards, measurements)
            record = {'modelo':'PostIgrejaDomestica', 'textos_aprovados_em':'2026-11-03',
                      'data':day['data'], 'cor':day['cor'], 'cards':measurements,
                      'obra':deepcopy(cover['obra']), 'obra_usada':_relative(artwork),
                      'obra_pendente':pending, 'enquadramento':framing, 'nota_visual':note,
                      'recomendacao_margem':_margin_recommendation(artwork, cover['obra'], framing) if not pending else None,
                      'avisos':warnings, 'tabela_medida':rows}
            _write_json(folder/'ficha.json', record)
            for old in folder.glob('card-*.png'):
                if int(old.stem.split('-')[-1]) > len(cards):
                    old.unlink()
            day_checks[day['data']] = {'cards':checks, 'pdf':pdf_check}
        browser.close()
    if errors:
        raise RuntimeError('Erros de navegador: '+'; '.join(errors))
    records = _records(target)
    expected_pngs = {}
    for record in records:
        folder = target/record['data']
        for card in record['cards']:
            expected_pngs[str(folder/card['arquivo'])] = (1080,1350)
        if not record['obra_pendente']:
            with Image.open(folder/'recorte.png') as image:
                expected_pngs[str(folder/'recorte.png')] = image.size
    expected_pngs[str(target/'prancha.png')] = _board(target, records)
    checks = {'kit':kit, 'kit_final':validate_kit(PROJECT), 'dias':{
        record['data']:day_checks[record['data']] for record in records if record['data'] in day_checks},
        'pngs':validate_pngs(expected_pngs),
        'browser':{'ok':True, 'errors':[], 'fontes_locais_por_render':6, 'recursos_externos':False},
        'obras_pendentes':[record['data'] for record in records if record['obra_pendente']],
        'avisos':[warning for record in records for warning in record['avisos']]
                 +[f'{row["data"]}, card {row["card"]}: '+'; '.join(row['diferencas_tabela'])
                   for record in records for row in record['tabela_medida'] if row['diferencas_tabela']],
        'tabela_medida':[row for record in records for row in record['tabela_medida']]}
    checks['ok'] = all(checks[key]['ok'] for key in ('kit','kit_final','pngs'))
    if not checks['ok']:
        raise RuntimeError('Falha de validação dos PNGs ou do kit.')
    command = 'python gerar.py igreja-domestica'+(f' --data {date_filter}' if date_filter else '')
    checks['comando'] = command
    _write_json(target/'verificacao.json', checks)
    report = _report(target, records, checks, command)
    return {'dias':len(days), 'cards':generated_cards, 'pdfs':len(days),
            'pngs':generated_cards+generated_crops+1, 'obras_pendentes':checks['obras_pendentes'],
            'avisos':checks['avisos'], 'relatorio':str(report), 'verificacoes':str(target/'verificacao.json')}
