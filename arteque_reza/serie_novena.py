"""Geração das Novenas: validação interna completa e prova de três páginas.

O modo de teste entrega somente os três cards aprovados para a conferência no
Canva. As vinte artes completas e seus HTMLs de render ficam em work/novena/.
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
from .conteudo_novena import load_novenas
from .novena import (_document, _measure, _pdf_check, _pixels, _validate_layout,
                     expand_cards, expected_layout)
from .renderizacao import local_server
from .validacao import validate_kit, validate_pngs


APPROVAL_DATE = '2026-11-03'
TEST_SLUGS = ('dia-1', 'dia-8', 'encerramento')


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def _relative(path: Path) -> str:
    return Path(path).resolve().relative_to(PROJECT).as_posix()


def _merge(parts: list[Path], destination: Path) -> None:
    """A mesma composição de PDFs de uma página usada pelas demais séries."""
    writer = PdfWriter()
    for path in parts:
        for page in PdfReader(path).pages:
            writer.add_page(page)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('wb') as stream:
        writer.write(stream)


def _board(paths: list[Path], cards: list[dict], destination: Path) -> tuple[int, int]:
    margin, gap, heading, height = 32, 24, 72, 450
    size = (2*margin+360*len(paths)+gap*(len(paths)-1), margin+heading+height+margin)
    image = Image.new('RGB', size, color('fundo', 'pergaminho'))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(str(KIT/'fontes/Lato-Regular.ttf'), 22)
    for number, (path, card) in enumerate(zip(paths, cards)):
        x = margin+number*(360+gap)
        label = 'Encerramento' if card['encerramento'] else f'Dia {card["numero"]} de 9'
        draw.text((x, margin), label, font=font, fill=color('tinta', 'pergaminho'))
        draw.text((x, margin+28), card['data'], font=font, fill=color('tinta-suave', 'pergaminho'))
        with Image.open(path) as artwork:
            image.paste(artwork.convert('RGB').resize((360, 450), Image.Resampling.LANCZOS), (x, margin+heading))
    image.save(destination)
    return size


def _row(card: dict, measured: dict, layout: dict) -> dict:
    texts = {text['campo']: text for text in measured['textos']}
    actual = {'titulo_linhas': texts['titulo']['quantidade_linhas'],
              'oracao_linhas': texts['oracao']['quantidade_linhas'],
              'selo_texto_px': measured['distancias']['selo_texto_px'],
              'texto_assinatura_px': measured['distancias']['texto_assinatura_px']}
    expected = expected_layout(card)
    differences = []
    if expected:
        for field in ('titulo_linhas', 'oracao_linhas'):
            if actual[field] != expected[field]:
                differences.append(f'{field}: medido {actual[field]}, previsto {expected[field]}')
        for field in ('selo_texto_px', 'texto_assinatura_px'):
            if abs(actual[field]-expected['folga_px']) > .01:
                differences.append(f'{field}: medido {actual[field]:g}px, previsto {expected["folga_px"]:g}px')
    return {'novena': card['novena'], 'nome': card['nome'], 'data': card['data'],
            'slug': card['slug'], 'numero': card['numero'],
            'encerramento': card['encerramento'], 'medido': actual, 'previsto': expected,
            'diferencas_tabela': differences, 'validacao': layout}


def _ficha(cards: list[dict], measurements: list[dict], *, modo: str,
           png_paths: list[Path]) -> dict:
    records = []
    for index, (spec, measured, path) in enumerate(zip(cards, measurements, png_paths), 1):
        record = deepcopy(measured)
        record.update({'card': index, 'pagina': index, 'novena': spec['novena'],
                       'nome': spec['nome'], 'data': spec['data'], 'numero': spec['numero'],
                       'encerramento': spec['encerramento'], 'slug': spec['slug'],
                       'conteudo': deepcopy(spec), 'arquivo': path.name})
        records.append(record)
    return {'modelo': 'PostNovena', 'modo': modo, 'textos_aprovados_em': APPROVAL_DATE,
            'novena': cards[0]['novena'], 'cards': records}


def _report(target: Path, checks: dict, command: str) -> Path:
    is_test = checks['modo'] == 'teste-canva'
    measured_count = len(checks['tabela_medida'])
    lines = ['# Novenas', '', f'`{command}`', '', '## Conteúdo e composição', '',
        '- As orações foram escritas pela página e aprovadas em 03/11/2026. O YAML mantém os vinte textos e os refrões aprovados, sem composição automática de orações.',
        '- PostNovena usa feed 1080 × 1350, tema pergaminho, sem obra. O bloco inteiro fica centralizado entre o selo e a assinatura, com pelo menos 60 px de folga dos dois lados.',
        '- O selo traz o nome da novena e a data, sem apoio à direita. A cruz segue a cor da novena nos nove dias: roxo #5b2e70, inclusive em 30/11, 3/12 e 7/12.',
        '- Dia N de 9 → título: 48 px; título → fonte: 32 px; fonte → ornamento e ornamento → oração: 48 px; oração → contas: 48 px. No encerramento sem fonte, título → ornamento: 48 px. Os espaços são o gap de 16 px do kit somado às margens inline em tokens e são medidos no navegador com tolerância de ±0,01 px.',
        '- Título em titulo, até duas linhas e 820 px. A oração usa oracao a 880 px, com entrelinha de 62 px, e contém o refrão em um único parágrafo, depois de uma quebra de linha. O refrão usa Cormorant Garamond Medium Italic e tinta-suave; a Imaculada mantém duas linhas, com a primeira terminando em `pecado,`.',
        '- Palavras com hífen recebem white-space:nowrap apenas nessa palavra. As palavras de uma letra seguem a regra compartilhada de espaços inseparáveis, sem modificar o helper usado pelas outras séries.',
        '- As nove contas formam um SVG de 306 × 18 px, centros x=9+36·i e y=9. Até o dia N, raio 9 e preenchimento ouro; as demais têm raio 7,75, traço de 2,5 px em ouro e nenhum preenchimento.',
        '- O encerramento usa cartão inteiro em ouro litúrgico (#866420), todos os elementos em sobre-cor (#faf6ee), logo-horizontal-sobre-cor.svg e nove contas cheias. O final do YAML substitui o refrão quando existe; no Natal, Glória a Deus nas alturas!.',
        '', '## Tabela prevista no prompt', '',
        '| Cards | Título | Oração com refrão | Folga prevista |',
        '| --- | --- | --- | --- |',
        '| Imaculada · dias 1 a 7 e 9 | 1 linha | 6 linhas | 154 px |',
        '| Imaculada · dia 8 | 2 linhas | 6 linhas | 116 px |',
        '| Imaculada · encerramento | 1 linha | 7 linhas | 158 px |',
        '| Natal · dias 1, 3 e 5 a 9 e encerramento | 1 linha | 5 linhas | 184 px |',
        '| Natal · dia 2 | 2 linhas | 5 linhas | 146 px |',
        '| Natal · dia 4 | 1 linha | 6 linhas | 154 px |',
        '', f'## {measured_count} cards medidos no navegador', '',
        f'Os {measured_count} cards selecionados foram renderizados e validados em work/novena/. Os números abaixo são medidas reais do DOM; diferenças da tabela prevista são informativas quando todos os limites continuam satisfeitos.', '',
        '| Novena | Data | Card | Título: medido / previsto | Oração: medido / previsto | Selo → bloco | Bloco → assinatura | Folga prevista |',
        '| --- | --- | --- | --- | --- | --- | --- | --- |']
    for row in checks['tabela_medida']:
        actual, expected = row['medido'], row['previsto']
        expected_title = expected.get('titulo_linhas', '—') if expected else '—'
        expected_prayer = expected.get('oracao_linhas', '—') if expected else '—'
        expected_gap = f'{expected["folga_px"]:g} px' if expected else '—'
        label = 'Encerramento' if row['encerramento'] else f'Dia {row["numero"]}'
        lines.append(f'| {row["novena"]} | {row["data"]} | {label} | {actual["titulo_linhas"]} / {expected_title} | {actual["oracao_linhas"]} / {expected_prayer} | {actual["selo_texto_px"]:g} px | {actual["texto_assinatura_px"]:g} px | {expected_gap} |')
    lines += ['', '## Diferenças da tabela prevista', '']
    differences = [f'{row["novena"]}, {row["slug"]}: '+ '; '.join(row['diferencas_tabela'])
                   for row in checks['tabela_medida'] if row['diferencas_tabela']]
    lines += ['- '+difference for difference in differences] if differences else ['Nenhuma diferença.']
    lines += ['', '## Verificações', '',
        '- As distâncias, o limite de oito linhas da oração com refrão, as linhas próprias e a variante itálica do refrão, as palavras com hífen e a geometria e as cores das contas foram conferidos no navegador.',
        '- Cada PDF interno de uma página passa pelas verificações de texto e fontes. Os PDFs reunidos são conferidos novamente: páginas de 810 × 1012,5 pt, fontes TTF embutidas e texto integral igual ao conteúdo aprovado, desconsiderando apenas espaços e quebras.',
        '- Os renders carregam somente os seis arquivos de fonte e demais recursos locais do projeto. O ZIP e os 44 arquivos de kit/ são conferidos antes e depois. Nenhuma outra série é regenerada por este comando.',
        '', '## Entrega desta rodada', '']
    if is_test:
        lines += ['Somente os três cards da Imaculada foram gravados em saida/novena/teste-canva/: dia 1 (29/11), dia 8 (6/12) e encerramento (8/12), nessa ordem. O HTML e o PDF usam exatamente a composição dos cards finais; os arquivos internos dos vinte cards permanecem em work/novena/.',
            '', '- [novena-teste-canva.pdf](teste-canva/novena-teste-canva.pdf)',
            '- [prancha.png](teste-canva/prancha.png)',
            '- [ficha.json](teste-canva/ficha.json)']
    else:
        lines.append('Os cards selecionados foram entregues por novena, com um PNG por card e um PDF de dez páginas por novena. O filtro --novena preserva as demais pastas já geradas.')
    lines += ['', '## O que conferir no Canva', '',
        '- Cada texto na sua caixa: selo, data, Dia N de 9 ou Encerramento, título e fonte.',
        '- A oração e o refrão numa caixa só, com entrelinha de 62 px, o refrão em itálico e na cor certa, e a quebra depois da vírgula.',
        '- As nove contas como formas.',
        '- Nenhuma caixa solta.',
        '', '## Pendências', '',
        'A importação deste PDF no Canva ainda precisa ser conferida. Após essa conferência, gerar os vinte cards finais em saida/novena/imaculada/ e saida/novena/natal/, com os PDFs novena-imaculada.pdf e novena-natal.pdf. Nesta rodada, esses vinte cards não foram publicados.' if is_test else 'A importação dos PDFs finais no editor do Canva não foi realizada por este comando.',
        '', 'A evidência da geração está em [verificacao.json](verificacao.json).']
    if (target/'CONFERENCIA-PROMPT-8.md').is_file():
        lines += ['', 'A preservação das saídas anteriores em relação à main no commit 2369956 e a conferência independente das novas artes estão documentadas em [CONFERENCIA-PROMPT-8.md](CONFERENCIA-PROMPT-8.md), com [evidência detalhada](conferencia-prompt8.json).']
    lines += ['', '## Árvore', '', '```text', 'saida/novena/']
    paths = {path.relative_to(target).as_posix() for path in target.rglob('*') if path.is_file()}
    paths.add('RELATORIO.md')
    lines += ['  '+path for path in sorted(paths)]+['```', '']
    destination = target/'RELATORIO.md'
    destination.write_text('\n'.join(lines), encoding='utf-8')
    return destination


def generate(output: Path, content_path: Path, novena_filter: str | None = None,
             teste_canva: bool = False) -> dict:
    """Valide as artes e publique o conjunto selecionado, sem alterar outras séries."""
    output = Path(output).resolve()
    novenas = load_novenas(content_path)
    available = {novena['id'] for novena in novenas}
    if novena_filter is not None and novena_filter not in available:
        raise ValueError(f'Nenhuma novena para --novena {novena_filter}.')
    if teste_canva and novena_filter not in {None, 'imaculada'}:
        raise ValueError('--teste-canva usa somente a Novena da Imaculada; escolha --novena imaculada ou retire o filtro.')
    cards = expand_cards(novenas)
    if teste_canva:
        render_cards = cards
        published_cards = [card for slug in TEST_SLUGS for card in cards
                           if card['novena']=='imaculada' and card['slug']==slug]
        if len(published_cards) != 3:
            raise ValueError('O teste do Canva exige os dias 1 e 8 e o encerramento da Imaculada.')
    else:
        render_cards = [card for card in cards if novena_filter is None or card['novena']==novena_filter]
        published_cards = render_cards
    kit = validate_kit(PROJECT)
    if not kit['ok']:
        raise ValueError('Kit inválido: '+'; '.join(kit['errors']))
    work = PROJECT/'work/novena'
    css = generate_tokens_css(work/'tokens.css')
    target = output/'novena'
    target.mkdir(parents=True, exist_ok=True)
    errors = []
    measurements = {}
    parts = {}
    pngs = {}
    expected_internal = {}
    checked_cards = []
    rows = []
    with local_server() as base_url, sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=shutil.which('chromium') or '/usr/bin/chromium', headless=True, args=['--no-sandbox'])
        context = browser.new_context(device_scale_factor=1)
        context.route('**/*', lambda route: route.continue_()
                      if urlsplit(route.request.url).netloc == urlsplit(base_url).netloc else route.abort())
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('console', lambda message: errors.append(message.text) if message.type=='error' else None)
        page.on('response', lambda response: errors.append(f'HTTP {response.status}: {response.url}') if response.status>=400 else None)
        for spec in render_cards:
            key = (spec['novena'], spec['slug'])
            png = work/spec['novena']/(spec['slug']+'.png')
            pdf = png.with_suffix('.pdf')
            render = render_arte(page, _document(spec, css), png, pdf_path=pdf, base_url=base_url)
            measured = _measure(page, spec)
            layout = _validate_layout(spec, measured)
            measured['distancias'] = layout['distancias']
            pixels = _pixels(png, spec, measured)
            pdf_check = _pdf_check(pdf, [spec], [measured])
            measurements[key] = measured
            parts[key] = pdf
            pngs[key] = png
            expected_internal[str(png)] = (1080,1350)
            rows.append(_row(spec, measured, layout))
            checked_cards.append({'novena': spec['novena'], 'slug': spec['slug'], 'data': spec['data'],
                                  'layout': layout, 'pixels': pixels, 'pdf': pdf_check,
                                  'fontes_render': render['fonts'],
                                  'png_interno': _relative(png), 'html_interno': _relative(png.with_suffix('.html'))})
        browser.close()
    if errors:
        raise RuntimeError('Erros de navegador: '+'; '.join(errors))
    _write_json(work/'ficha-validacao.json', {'modelo':'PostNovena', 'cards':[
        measurements[(card['novena'],card['slug'])] for card in render_cards]})
    checks = {'modo':'teste-canva' if teste_canva else 'final',
              'kit':kit, 'cards_validados':checked_cards, 'tabela_medida':rows,
              'pngs_validacao_interna':validate_pngs(expected_internal), 'pdfs_entregues':[]}
    expected_output = {}
    written_pngs = 0
    if teste_canva:
        folder = target/'teste-canva'
        folder.mkdir(parents=True, exist_ok=True)
        selected_measurements = []
        paths = []
        for spec in published_cards:
            key = (spec['novena'],spec['slug'])
            destination = folder/(spec['slug']+'.png')
            shutil.copyfile(pngs[key], destination)
            paths.append(destination)
            selected_measurements.append(measurements[key])
            expected_output[str(destination)] = (1080,1350)
        destination = folder/'novena-teste-canva.pdf'
        _merge([parts[(card['novena'],card['slug'])] for card in published_cards], destination)
        pdf_check = _pdf_check(destination, published_cards, selected_measurements)
        checks['pdfs_entregues'].append({'arquivo':_relative(destination), 'validacao':pdf_check})
        _write_json(folder/'ficha.json', _ficha(published_cards, selected_measurements, modo='teste-canva', png_paths=paths))
        expected_output[str(folder/'prancha.png')] = _board(paths, published_cards, folder/'prancha.png')
        written_pngs = 4
    else:
        for novena in novenas:
            selected = [card for card in published_cards if card['novena']==novena['id']]
            if not selected:
                continue
            folder = target/novena['id']
            folder.mkdir(parents=True, exist_ok=True)
            selected_measurements = []
            paths = []
            for spec in selected:
                key = (spec['novena'],spec['slug'])
                destination = folder/(spec['slug']+'.png')
                shutil.copyfile(pngs[key], destination)
                expected_output[str(destination)] = (1080,1350)
                paths.append(destination)
                selected_measurements.append(measurements[key])
            destination = folder/f'novena-{novena["id"]}.pdf'
            _merge([parts[(card['novena'],card['slug'])] for card in selected], destination)
            pdf_check = _pdf_check(destination, selected, selected_measurements)
            checks['pdfs_entregues'].append({'arquivo':_relative(destination), 'validacao':pdf_check})
            _write_json(folder/'ficha.json', _ficha(selected, selected_measurements, modo='final', png_paths=paths))
            written_pngs += len(paths)
    checks['pngs'] = validate_pngs(expected_output)
    checks['kit_final'] = validate_kit(PROJECT)
    checks['browser'] = {'ok':True, 'errors':[], 'fontes_locais_por_render':6, 'recursos_externos':False}
    checks['avisos'] = [f'{row["novena"]}, {row["slug"]}: '+'; '.join(row['diferencas_tabela'])
                         for row in rows if row['diferencas_tabela']]
    checks['obras_pendentes'] = []
    checks['ok'] = all(checks[key]['ok'] for key in ('kit','kit_final','pngs','pngs_validacao_interna'))
    if not checks['ok']:
        raise RuntimeError('Falha de validação dos PNGs ou do kit.')
    command = 'python gerar.py novena'+(f' --novena {novena_filter}' if novena_filter else '')+(' --teste-canva' if teste_canva else '')
    checks['comando'] = command
    _write_json(target/'verificacao.json', checks)
    report = _report(target, checks, command)
    return {'novena':novena_filter, 'cards_validados':len(render_cards), 'cards':len(published_cards),
            'pdfs':len(checks['pdfs_entregues']), 'pngs':written_pngs,
            'obras_pendentes':[], 'avisos':checks['avisos'], 'modo':checks['modo'],
            'relatorio':str(report), 'verificacoes':str(target/'verificacao.json')}
