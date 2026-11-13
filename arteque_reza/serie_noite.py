"""Geração das quatro séries da noite, com recortes locais para o Canva.

Os modelos vivem no gerador. O kit e os módulos das outras séries permanecem
como fontes compartilhadas, sem serem regravados por estes comandos.
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
from .canva import niche_svg, validate_svg
from .conteudo_noite import LOADERS
from .noite import (_document, _measure, _pdf_check, _pixels, _validate_layout,
                    expand_cards, expected_layout, prepare_artworks)
from .renderizacao import local_server
from .validacao import validate_kit, validate_pngs


APPROVAL_DATE = '2026-11-12'
SERIES = {
    'olhe-de-novo': ('Olhe de Novo', 'PostOlheDeNovo'),
    'por-dentro-da-missa': ('Por Dentro da Missa', 'PostPorDentroDaMissa'),
    'rezo-por-voce': ('Rezo por Você', 'PostRezoPorVoce'),
    'toda-bela': ('Toda Bela', 'PostTodaBela'),
}


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


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


def _artwork_key(artwork: dict) -> str:
    key = f'card-{artwork["card"]}'
    return key+f'-{artwork["indice"]}' if artwork['card'] == 4 else key


def _visual_note(target: Path, date: str, artwork: dict) -> dict:
    path = target/'NOTAS-DAS-OBRAS.json'
    if path.is_file():
        notes = json.loads(path.read_text(encoding='utf-8'))
        value = notes.get(date, {}).get(_artwork_key(artwork))
        if value is not None:
            if not isinstance(value, dict) or not isinstance(value.get('nota'), str):
                raise ValueError(f'{path.name}, {date}, {_artwork_key(artwork)}: nota visual inválida.')
            return deepcopy(value)
    return {'inspecionada': False,
            'nota': 'Capa/detalhe e prova de recorte ainda precisam de inspeção visual antes da publicação.'}


def refresh_visual_notes(target: Path) -> list[dict]:
    """Atualize as notas persistidas nas fichas sem renderizar os cards de novo."""
    target = Path(target)
    records = _records(target)
    for record in records:
        for artwork in record['obras']:
            artwork['nota_visual'] = _visual_note(target, record['data'], artwork)
        for card in record['cards']:
            card['obras'] = [deepcopy(artwork) for artwork in record['obras']
                             if artwork['card'] == card['card']]
        _write_json(target/record['data']/'ficha.json', record)
    return records


def _row(card: dict, measured: dict, layout: dict) -> dict:
    counts = {text['campo']: text['quantidade_linhas'] for text in measured['textos']
              if text['campo'] not in {'selo', 'data', 'contagem', 'info'}}
    expected = expected_layout(card)
    distances = layout['distancias']
    differences = []
    for field, wanted in expected.get('linhas', {}).items():
        if counts.get(field) != wanted:
            differences.append(f'{field}: {counts.get(field, "ausente")} linhas; previsto {wanted}')
    if 'folga_px' in expected:
        for field in ('selo_texto_px', 'texto_assinatura_px'):
            if abs(distances[field]-expected['folga_px']) > .01:
                differences.append(f'{field}: {distances[field]:g}px; previsto {expected["folga_px"]:g}px')
    for field in ('selo_nicho_px', 'titulo_assinatura_px', 'invocacao_assinatura_px'):
        if field in expected and abs(distances[field]-expected[field]) > .01:
            differences.append(f'{field}: {distances[field]:g}px; previsto {expected[field]:g}px')
    return {'data': card['data'], 'card': card['numero'], 'tipo': card['tipo'],
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
            with Image.open(target/record['data']/card['arquivo']) as image:
                board.paste(image.convert('RGB').resize((360, 450), Image.Resampling.LANCZOS),
                            (left+column*(360+gap), y+top))
    board.save(target/'prancha.png')
    return size


def _elements(target: Path) -> dict:
    folder = target/'elementos'
    folder.mkdir(parents=True, exist_ok=True)
    records = []
    for width, height in ((640, 840), (340, 420)):
        path = folder/f'nicho-{width}x{height}-olhe-de-novo.svg'
        path.write_text(niche_svg(width, height, color('fundo', 'capela'),
                                  color('liturgico-roxo', 'capela')), encoding='utf-8')
        records.append(validate_svg(path))
    return {'ok': True, 'svgs': records}


def _rules(series: str) -> list[str]:
    common = [
        '- Os textos foram escritos pela página e aprovados em 12/11/2026. O YAML preserva pontuação, aspas, acentos e quebras manuais; nenhum texto é gerado automaticamente.',
        '- Feed de 1080 × 1350. Os modelos existem apenas no gerador, sem prévia equivalente no kit v4. Nenhum módulo compartilhado ou arquivo do kit é modificado.',
        '- O helper igreja_text_html é importado intacto: protege palavras de uma letra, referências bíblicas inteiras, ordinais ligados à palavra seguinte e palavras com hífen. As quebras do YAML são mantidas.',
        '- O gap de 16 px do aqr-texto recebe margens inline em tokens: 48 px entre rótulo e texto e em volta do ornamento; 32 px entre texto e fonte/referência e entre nicho e crédito. Cada par é medido no navegador com tolerância de ±0,01 px.',
        '- Os cards com obra no alto seguem o selo e deixam pelo menos 32 px entre o último texto e a assinatura. Os demais centralizam o bloco entre selo e assinatura, com pelo menos 60 px de cada lado e diferença de centralização até 0,1 px.',
        '- A cruz e o filete recebem a cor do dia; o ornamento usa ouro. Nos cartões inteiros na cor do dia, fundo na cor litúrgica e textos, cruz, ornamento e logo em sobre-cor.',
        '- A assinatura usa a variante do tema, ou sobre-cor no cartão inteiro na cor. Cores, fontes, caixas, limites de linhas e trechos protegidos são validados no DOM e por pixels.',
    ]
    specific = {
        'olhe-de-novo': [
            '- PostOlheDeNovo: quatro cards no tema capela, com contagem 1/4 a 4/4 em todos eles. Os dois primeiros têm nichos 640 × 840, crédito em uma linha e título em uma linha; o card 3 apresenta o significado e o card 4 mostra uma ou duas obras.',
            '- No card 4, cada figura tem 380 px e o intervalo entre figuras é 56 px. Os nichos medem 340 × 420; com duas obras, ficam a 96 px um do outro e os parapeitos de 48 px se encostam sem sobrepor. Os créditos usam até duas linhas e text-wrap:balance.',
            '- Os SVGs de nicho para o Canva ficam somente em elementos/ desta série, com fundo e filete do tema capela em liturgico-roxo; saida/canva/ permanece intacta.',
        ],
        'por-dentro-da-missa': [
            '- PostPorDentroDaMissa: tema pergaminho, de três a cinco cards, com contagem em todos eles. Capa com pergunta e resposta; uma a três explicações na ordem do YAML; fecho em cartão inteiro na cor do dia.',
            '- A capa limita a pergunta a duas linhas e a resposta a três; explicações limitam título a duas, corpo a seis e fonte a duas; o fecho limita a frase a quatro linhas e o convite a uma.',
        ],
        'rezo-por-voce': [
            '- PostRezoPorVoce: card único no tema pergaminho, sem informação à direita do selo. Ornamento, título em titulo-capa de até duas linhas e texto em corpo/tinta-suave de até duas linhas.',
            '- Ornamento → título: 48 px; título → texto: 32 px. O bloco inteiro permanece centralizado entre selo e assinatura.',
        ],
        'toda-bela': [
            '- PostTodaBela: três cards. Capa e raiz no tema capela; oração em cartão inteiro na cor do dia. A capa traz o info do YAML e os outros cards a contagem 2/3 e 3/3.',
            '- A capa usa nicho 640 × 760, crédito em uma linha e invocação em titulo-capa. Se a invocação quebrar, é renderizada em titulo com até duas linhas; a assinatura continua a pelo menos 32 px. Não há apoio na capa.',
            '- A raiz traz versículo de até três linhas, referência em uma linha, texto de até cinco e fonte em uma. A oração usa citacao-grande em até três linhas, com as quebras manuais do YAML, e convite em uma.',
        ],
    }
    if series in {'olhe-de-novo', 'toda-bela'}:
        common += [
            '- Cada nicho recebe um JPEG já recortado na janela visível, qualidade 95 e sem subamostragem de cor, usando LANCZOS e Image.resize com box fracionária. O card e o PDF usam esse arquivo com foco 50% 50% e zoom 1. Isso evita a ampliação que borrou a obra de 25/12 na importação do Canva.',
            '- O recorte mantém a dimensão nativa, limitado a 2× a área interna do nicho, sem ampliar o arquivo. As janelas explícitas exigem dimensão original exata, contenção completa e ampliação de até 1,2. Nenhuma obra original é alterada ou baixada.',
            '- Cada obra recebe uma prova da imagem inteira a 1080 px com o contorno da janela do arco. Margens fotográficas visíveis geram aviso e nunca alteram o YAML.',
        ]
    return common+specific[series]


def _report(target: Path, records: list[dict], checks: dict, command: str) -> Path:
    series = checks['serie']
    lines = ['# '+SERIES[series][0], '', f'`{command}`', '', '## Conteúdo e composição', '',
             *_rules(series), '', '## Tabela medida no navegador', '',
             '| Data | Card | Tipo | Linhas medidas | Distâncias e folgas medidas | Previsto |',
             '| --- | --- | --- | --- | --- | --- |']
    rows = [row for record in records for row in record['tabela_medida']]
    for row in rows:
        counts = '; '.join(f'{name}: {count}' for name, count in row['linhas'].items())
        distances = '; '.join(f'{name}: {value:g} px' for name, value in row['distancias'].items())
        expected = row['previsto']
        wanted = '; '.join(f'{name}: {count} linhas' for name, count in expected.get('linhas', {}).items())
        wanted += '; '+'; '.join(f'{name}: {value:g} px' for name, value in expected.items() if name!='linhas')
        lines.append(f'| {row["data"]} | {row["card"]} | {row["tipo"]} | {counts} | {distances} | {wanted} |')
    differences = [f'{row["data"]}, card {row["card"]}: '+'; '.join(row['diferencas_tabela'])
                   for row in rows if row['diferencas_tabela']]
    lines += ['', '## Diferenças da tabela prevista', '']
    lines += ['- '+note for note in differences] if differences else ['Nenhuma diferença.']
    lines += ['', '## Obras, janelas e recortes', '']
    pending = []
    for record in records:
        for artwork in record['obras']:
            key = _artwork_key(artwork)
            note = _visual_note(target, record['data'], artwork)
            if not note['inspecionada']:
                pending.append(f'{record["data"]} · {key}')
            window = artwork['janela_original']
            lines += [f'### {record["data"]} · {key}', '',
                f'{artwork["credito"]} — {artwork["pagina"]}', '',
                f'Original local: `{artwork["arquivo"]}`. '+
                (f'Foco `{artwork["foco"]}`, zoom `{artwork.get("zoom", 1)}`.' if 'foco' in artwork else
                 f'Janela aprovada `{artwork["janela"]}`, tamanho original `{artwork["tamanho"]}`.'), '',
                f'Janela original x={window["x"]:.6f}, y={window["y"]:.6f}, largura={window["largura"]:.6f}, altura={window["altura"]:.6f} px; ampliação={artwork["ampliacao"]:.6f}.',
                f'Arquivo recortado: `{artwork["arquivo_recortado"]}`. Prova: `{artwork["prova_recorte"]}`.']
            with Image.open(PROJECT/artwork['arquivo_recortado']) as image:
                lines.append(f'Dimensão do JPEG recortado: {image.width} × {image.height} px.')
            lines += ['', 'Margens e faixas detectadas: `'+json.dumps(artwork.get('margens', artwork.get('geometria', {})), ensure_ascii=False)+'`.',
                      '', note['nota']]
            suggestion = note.get('sugestao')
            if suggestion:
                lines += ['', 'Sugestão somente para avaliação, sem alterar o YAML: '+
                          (suggestion if isinstance(suggestion, str) else json.dumps(suggestion, ensure_ascii=False))]
    if not any(record['obras'] for record in records):
        lines.append('Esta série não usa obras nem nichos.')
    warnings = [warning for record in records for warning in record['avisos']]+differences
    lines += ['', '## Avisos e pendências', '']
    lines += ['- '+warning for warning in warnings] if warnings else ['Nenhum aviso.']
    if pending:
        lines.append('Inspeção visual pendente: '+', '.join(pending)+'.')
    lines += ['', '## PDF e conferências', '',
        'Um PDF por data, com todos os cards na ordem do YAML e páginas de 810 × 1012,5 pt. PyMuPDF, pdffonts e pdftotext verificam fontes TTF embutidas e texto integral igual ao YAML. Cada nicho tem o filete em U e o parapeito vetoriais conferidos, inclusive os dois nichos do card 4 do Olhe de Novo.',
        'As fichas registram caixas de cada linha de texto, tema, cores, conteúdos aprovados, janela original, ampliação e arquivo recortado de cada obra. Os renders usam somente recursos e seis fontes locais.',
        '', '## O que conferir no Canva', '',
        '- Cada texto na sua caixa: selo, data, contagem ou info, rótulo, título ou pergunta, crédito, texto, fonte, versículo, referência, frase e convite.',
        '- A obra dentro do arco, sem borrão, usando o arquivo já recortado.',
        '- O filete, o parapeito e o ornamento como formas.',
        '- No card 4 de 9/12, os dois nichos lado a lado, com os parapeitos encostados.',
        '- Nenhuma caixa solta, nem contendo só um espaço; conferir que dois textos não foram fundidos.',
        '', 'A importação destes PDFs no editor do Canva permanece uma conferência manual.',
        'A evidência da geração está em [verificacao.json](verificacao.json).',
        '', '## Árvore', '', '```text', 'saida/'+series+'/']
    names = {path.relative_to(target).as_posix() for path in target.rglob('*') if path.is_file()}
    names.add('RELATORIO.md')
    lines += ['  '+name for name in sorted(names)]+['```', '']
    destination = target/'RELATORIO.md'
    destination.write_text('\n'.join(lines), encoding='utf-8')
    return destination


def generate(output: Path, content_path: Path, series: str,
             date_filter: str | None = None) -> dict:
    """Gere a série selecionada e preserve as demais datas e séries."""
    if series not in SERIES:
        raise ValueError('Série da noite desconhecida: '+str(series))
    days = LOADERS[series](content_path)
    if date_filter is not None:
        days = [day for day in days if day['data'] == date_filter]
        if not days:
            raise ValueError(f'Nenhum conteúdo para --data {date_filter}.')
    kit = validate_kit(PROJECT)
    if not kit['ok']:
        raise ValueError('Kit inválido: '+'; '.join(kit['errors']))
    target = Path(output).resolve()/series
    target.mkdir(parents=True, exist_ok=True)
    work = PROJECT/'work'/series
    css = generate_tokens_css(work/'tokens.css')
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
            cards = expand_cards(series, [day])
            folder = target/day['data']
            folder.mkdir(parents=True, exist_ok=True)
            artworks = prepare_artworks(series, day, folder)
            for artwork in artworks:
                artwork['nota_visual'] = _visual_note(target, day['data'], artwork)
            generated_crops += len(artworks)
            warnings = [warning for artwork in artworks for warning in artwork.get('avisos', [])]
            measurements, parts, card_checks, rows = [], [], [], []
            for original in cards:
                card = deepcopy(original)
                png = work/day['data']/f'card-{card["numero"]}.png'
                pdf = png.with_suffix('.pdf')
                rendered = render_arte(page, _document(card, css, artworks), png, pdf_path=pdf, base_url=base_url)
                measured = _measure(page, card)
                if series == 'toda-bela' and card['tipo'] == 'capa':
                    invocation = next(text for text in measured['textos'] if text['campo']=='invocacao')
                    if invocation['quantidade_linhas'] > 1:
                        card['invocation_style'] = 'titulo'
                        rendered = render_arte(page, _document(card, css, artworks, invocation_style='titulo'),
                                               png, pdf_path=pdf, base_url=base_url)
                        measured = _measure(page, card)
                layout = _validate_layout(card, measured)
                measured['distancias'] = layout['distancias']
                pixels = _pixels(png, card, measured)
                measured.update({'card':card['numero'], 'pagina':card['numero'], 'arquivo':png.name,
                                 'conteudo':deepcopy(card),
                                 'obras':[deepcopy(artwork) for artwork in artworks if artwork['card']==card['numero']]})
                shutil.copyfile(png, folder/png.name)
                measurements.append(measured)
                parts.append(pdf)
                rows.append(_row(card, measured, layout))
                card_checks.append({'card':card['numero'], 'tipo':card['tipo'], 'layout':layout,
                                    'pixels':pixels, 'fontes_render':rendered['fonts']})
                generated_cards += 1
            destination = folder/f'{series}-{day["data"]}.pdf'
            _merge(parts, destination)
            pdf_check = _pdf_check(destination, [entry['conteudo'] for entry in measurements], measurements)
            record = {'modelo':SERIES[series][1], 'serie':series, 'textos_aprovados_em':APPROVAL_DATE,
                      'data':day['data'], 'cor':day['cor'], 'cards':measurements,
                      'obras':artworks, 'avisos':warnings, 'tabela_medida':rows}
            _write_json(folder/'ficha.json', record)
            for old in folder.glob('card-*.png'):
                if int(old.stem.split('-')[-1]) > len(cards):
                    old.unlink()
            day_checks[day['data']] = {'cards':card_checks, 'pdf':pdf_check}
        browser.close()
    if errors:
        raise RuntimeError('Erros de navegador: '+'; '.join(errors))
    records = _records(target)
    expected_pngs = {}
    for record in records:
        folder = target/record['data']
        for card in record['cards']:
            expected_pngs[str(folder/card['arquivo'])] = (1080,1350)
        for artwork in record['obras']:
            path = PROJECT/artwork['prova_recorte']
            with Image.open(path) as image:
                expected_pngs[str(path)] = image.size
    expected_pngs[str(target/'prancha.png')] = _board(target, records)
    elements = _elements(target) if series == 'olhe-de-novo' else {'ok':True, 'svgs':[]}
    checks = {'serie':series, 'kit':kit, 'kit_final':validate_kit(PROJECT), 'elementos':elements,
              'dias':{record['data']:day_checks[record['data']] for record in records if record['data'] in day_checks},
              'pngs':validate_pngs(expected_pngs),
              'browser':{'ok':True, 'errors':[], 'fontes_locais_por_render':6, 'recursos_externos':False},
              'obras_pendentes':[],
              'avisos':[warning for record in records for warning in record['avisos']]
                       +[f'{row["data"]}, card {row["card"]}: '+'; '.join(row['diferencas_tabela'])
                         for record in records for row in record['tabela_medida'] if row['diferencas_tabela']],
              'tabela_medida':[row for record in records for row in record['tabela_medida']]}
    checks['ok'] = all(checks[key]['ok'] for key in ('kit','kit_final','pngs','elementos'))
    if not checks['ok']:
        raise RuntimeError('Falha de validação dos PNGs, SVGs ou do kit.')
    command = 'python3 gerar.py '+series+(f' --data {date_filter}' if date_filter else '')
    checks['comando'] = command
    _write_json(target/'verificacao.json', checks)
    report = _report(target, records, checks, command)
    return {'dias':len(days), 'cards':generated_cards, 'pdfs':len(days),
            'pngs':generated_cards+generated_crops+1, 'obras_pendentes':[],
            'avisos':checks['avisos'], 'relatorio':str(report), 'verificacoes':str(target/'verificacao.json')}
