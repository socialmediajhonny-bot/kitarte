"""Stories avulsos na composição fixa StoryAngelus, um PDF por grupo."""
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
from .conteudo_stories import _identifier
from .conteudo_stories_avulsos import load_stories_avulsos, validate_artwork_size
from .obras import crop_proof, inspect_artwork
from .renderizacao import local_server
from .stories import (_document, _measure, _pdf_check, _pixels, _source_warnings,
                      _validate_layout)
from .validacao import validate_kit, validate_pngs


APPROVAL_DATE = '2026-11-19'


def _json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def _adapt(story: dict) -> tuple[dict, dict]:
    """A composição usa hora só como nome interno do segundo texto do selo."""
    return ({'id': story['grupo'], 'nome': story['grupo'], 'cor': story['cor']},
            {**story, 'hora': story['apoio']})


def _records(target: Path) -> list[dict]:
    records = [json.loads(path.read_text(encoding='utf-8'))
               for path in target.glob('*/ficha.json')]
    return sorted(records, key=lambda record: (record['ordem_grupo'], record['grupo']))


def _visual_note(target: Path, story_id: str, pending: bool) -> dict:
    if pending:
        return {'inspecionada': False, 'nota': 'Obra pendente; usada a provisória, sem inspeção da obra original.'}
    path = target/'NOTAS-DAS-OBRAS.json'
    if path.is_file():
        notes = json.loads(path.read_text(encoding='utf-8'))
        if story_id in notes:
            note = notes[story_id]
            if not isinstance(note, dict) or not isinstance(note.get('nota'), str):
                raise ValueError(f'{path.name}, {story_id}: nota visual inválida.')
            return deepcopy(note)
    return {'inspecionada': False, 'nota': 'Obra e recorte registrados; conferir os elementos essenciais no arco.'}


def refresh_visual_notes(target: Path) -> list[dict]:
    """Atualize apenas fichas e notas, sem recompor PNGs ou PDFs."""
    target = Path(target)
    records = _records(target)
    for record in records:
        for card in record['cards']:
            card['nota_visual'] = _visual_note(target, card['id'], card['obra_pendente'])
        _json(target/record['grupo']/'ficha.json', record)
    return records


def _board(target: Path, records: list[dict]) -> tuple[int, int]:
    margin, gap, row_height = 32, 24, 740
    columns = max(len(record['cards']) for record in records)
    size = (2*margin+columns*360+(columns-1)*gap, 32+row_height*len(records))
    board = Image.new('RGB', size, color('fundo', 'pergaminho'))
    draw = ImageDraw.Draw(board)
    font = ImageFont.truetype(str(KIT/'fontes/Lato-Regular.ttf'), 22)
    for row, record in enumerate(records):
        y = 32+row*row_height
        draw.text((margin, y), record['grupo'], font=font, fill=color('tinta', 'pergaminho'))
        for column, card in enumerate(record['cards']):
            x = margin+column*(360+gap)
            draw.text((x, y+28), card['id'], font=font, fill=color('tinta-suave', 'pergaminho'))
            with Image.open(target/record['grupo']/(card['id']+'.png')) as image:
                board.paste(image.convert('RGB').resize((360, 640), Image.Resampling.LANCZOS), (x, y+60))
    board.save(target/'prancha.png')
    return size


def _report(target: Path, records: list[dict], checks: dict, command: str) -> Path:
    lines = ['# Stories avulsos', '', f'`{command}`', '', '## Composição', '',
        '- Textos e obras aprovados pela página em 19/11/2026. Os seis stories usam StoryAngelus, capela, 1080 × 1920, sem laço por tempo litúrgico.',
        '- O selo é serie · apoio; o nicho tem 600 × 700 px. A cruz e o filete seguem a cor do YAML; ornamento ouro e assinatura capela sem @.',
        '- Posições fixas: selo y=240; nicho y=328, base=1028; título y=1076; ornamento y=1286; assinatura y=1628.',
        '- 48 px entre título e subtítulo e, havendo resposta, entre invocação e resposta; mínimo de 32 px do último texto à assinatura. As margens inline mantêm o gap de 16 px do kit.',
        '- Limites: título e subtítulo em uma linha, invocação até três e resposta até duas. Só o nome fixo Antífonas do Ó no selo de uma linha é isento da regra de palavra de uma letra no fim.',
        '- O grupo recebe um PDF com as páginas na ordem do YAML. --grupo preserva os outros grupos e a prancha reúne todos os já gerados.',
        '', '## Medidas no navegador', '',
        '| Grupo | Story | Título / subtítulo / invocação / resposta: linhas | Título → subtítulo | Invocação → resposta | Último texto → assinatura | Assinatura y |',
        '| --- | --- | --- | --- | --- | --- | --- |']
    warnings = []
    pending = []
    for record in records:
        for card in record['cards']:
            fields = {text['campo']: text['quantidade_linhas'] for text in card['textos']}
            counts = ' / '.join(str(fields.get(field, '—')) for field in ('titulo','subtitulo','invocacao','resposta'))
            layout = card['distancias']
            response = f'{layout["invocacao_resposta_px"]:g}' if 'invocacao_resposta_px' in layout else '—'
            lines.append(f'| {record["grupo"]} | {card["id"]} | {counts} | {layout["titulo_subtitulo_px"]:g} | {response} | {layout["ultimo_texto_assinatura_px"]:g} | {layout["posicoes"]["assinatura_topo_px"]:g} |')
            warnings.extend(card['avisos'])
            if card['obra_pendente']:
                pending.append(card['id'])
    lines += ['', '## Obras, janelas e notas visuais', '']
    for record in records:
        for card in record['cards']:
            work = card['obra']; framing = card['enquadramento']; window = framing['janela_original']
            note = _visual_note(target, card['id'], card['obra_pendente'])
            lines += [f'### {card["id"]}', '', f'{work["credito"]} — {work["pagina"]}', '',
                f'Original: `{work["arquivo"]}`; foco `{work["foco"]}`, zoom `{work.get("zoom",1)}`. '
                f'Janela x={window["x"]:.6f}, y={window["y"]:.6f}, largura={window["largura"]:.6f}, altura={window["altura"]:.6f} px; '
                f'ampliação={framing["escala_com_zoom"]:.6f}.',
                'Provisória usada; obra pendente.' if card['obra_pendente'] else f'Prova do recorte: `{record["grupo"]}/recorte-{card["id"]}.png`.',
                'Margens: `'+json.dumps(framing['margens_detectadas'], ensure_ascii=False)+'`; '
                'faixas descartadas: `'+json.dumps(framing['faixas_descartadas'], ensure_ascii=False)+'`; '
                'margens visíveis: `'+json.dumps(framing['margens_visiveis'], ensure_ascii=False)+'`.',
                '', note['nota']]
            if note.get('sugestao'):
                lines += ['', 'Sugestão somente no relatório, sem mudar o YAML: '+json.dumps(note['sugestao'], ensure_ascii=False)]
    lines += ['', '## Avisos e pendências', '']
    lines += ['- '+warning for warning in dict.fromkeys(warnings)] if warnings else ['Nenhum aviso geométrico.']
    lines.append('Obras pendentes: '+(', '.join(pending) if pending else 'nenhuma')+'.')
    visual_pending = [card['id'] for record in records for card in record['cards']
                      if not _visual_note(target,card['id'],card['obra_pendente']).get('inspecionada')]
    if visual_pending:
        lines.append('Inspeção visual pendente: '+', '.join(visual_pending)+'.')
    lines += ['', '## PDF e Canva', '',
        'Cada página tem 810 × 1440 pt. PyMuPDF, pdffonts e pdftotext verificam texto integral e fontes TTF embutidas; o filete em U e o parapeito de cada nicho são vetoriais e validados.',
        'A importação no Canva permanece manual: conferir cada texto em sua caixa, a obra dentro do arco, o filete e o parapeito como formas e nenhuma caixa solta ou contendo só um espaço.',
        '', '## Árvore', '', '```text', 'saida/stories-avulsos/']
    paths = {path.relative_to(target).as_posix() for path in target.rglob('*') if path.is_file()}
    paths.add('RELATORIO.md')
    lines += ['  '+name for name in sorted(paths)]+['```','']
    path = target/'RELATORIO.md'
    path.write_text('\n'.join(lines), encoding='utf-8')
    return path


def generate(output: Path, content_path: Path, grupo_filter: str | None = None) -> dict:
    stories = load_stories_avulsos(content_path)
    order = {group: index for index, group in enumerate(dict.fromkeys(story['grupo'] for story in stories))}
    groups = list(order)
    if grupo_filter is not None:
        _identifier(grupo_filter, '--grupo')
        groups = [group for group in groups if group == grupo_filter]
        if not groups:
            raise ValueError(f'Nenhum grupo para --grupo {grupo_filter}.')
    output = Path(output).resolve()
    target = output/'stories-avulsos'
    kit = validate_kit(PROJECT)
    if not kit['ok']:
        raise ValueError('Kit inválido: '+'; '.join(kit['errors']))
    target.mkdir(parents=True, exist_ok=True)
    css = generate_tokens_css(PROJECT/'work/stories-avulsos/tokens.css')
    work = PROJECT/'work/stories-avulsos'
    placeholder = output/'obra-provisoria.png'
    if not placeholder.is_file():
        placeholder = PROJECT/'saida/obra-provisoria.png'
    previous = target/'verificacao.json'
    group_checks = json.loads(previous.read_text(encoding='utf-8')).get('grupos', {}) if previous.is_file() else {}
    errors = []
    generated = 0
    with local_server() as base_url, sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=shutil.which('chromium') or '/usr/bin/chromium',
                                             headless=True, args=['--no-sandbox'])
        context = browser.new_context(device_scale_factor=1)
        context.route('**/*', lambda route: route.continue_()
                      if urlsplit(route.request.url).netloc == urlsplit(base_url).netloc else route.abort())
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('console', lambda message: errors.append(message.text) if message.type == 'error' else None)
        page.on('response', lambda response: errors.append(f'HTTP {response.status}: {response.url}') if response.status >= 400 else None)
        for group in groups:
            selected = [story for story in stories if story['grupo'] == group]
            folder = target/group
            folder.mkdir(parents=True, exist_ok=True)
            cards, parts, card_checks = [], [], []
            for number, original in enumerate(selected, 1):
                validate_artwork_size(original['obra'])
                tempo, story = _adapt(original)
                artwork = local_artwork_path(story['obra']['arquivo'])
                pending = not artwork.is_file()
                warnings = []
                if pending:
                    if not placeholder.is_file():
                        raise FileNotFoundError('Obra provisória ausente; execute python gerar.py componentes.')
                    artwork = placeholder
                    warnings.append(f'{story["id"]}: obra pendente; utilizada a provisória.')
                framing = inspect_artwork(artwork, story['obra']['foco'], story['obra'].get('zoom',1),
                                          niche_width=600, niche_height=700, date=story['id'])
                proof = folder/f'recorte-{story["id"]}.png'
                if not pending:
                    warnings.extend(_source_warnings(story, artwork))
                    warnings.extend(framing['avisos'])
                    crop_proof(artwork, proof, story['obra']['foco'], zoom=story['obra'].get('zoom',1),
                               niche_width=600, niche_height=700, date=story['id'])
                elif proof.exists():
                    proof.unlink()
                png = work/group/f'{story["id"]}.png'
                pdf = png.with_suffix('.pdf')
                rendered = render_arte(page, _document(tempo,story,css,artwork), png,
                                       formato='story', pdf_path=pdf, base_url=base_url)
                card = _measure(page,tempo,story,number)
                layout = _validate_layout(tempo,story,card)
                pixels = _pixels(png,tempo,story,card)
                card.update({'grupo':group, 'serie':story['serie'], 'apoio':story['apoio'],
                             'textos_aprovados_em':APPROVAL_DATE, 'obra':original['obra'],
                             'obra_usada':artwork.relative_to(PROJECT).as_posix(), 'obra_pendente':pending,
                             'enquadramento':framing, 'ampliacao':framing['escala_com_zoom'],
                             'prova_recorte':proof.relative_to(PROJECT).as_posix() if not pending else None,
                             'nota_visual':_visual_note(target,story['id'],pending),
                             'avisos':warnings, 'distancias':layout})
                shutil.copyfile(png,folder/png.name)
                cards.append(card); parts.append(pdf)
                card_checks.append({'story':story['id'],'layout':layout,'pixels':pixels,'fontes_render':rendered['fonts']})
                generated += 1
            destination = folder/f'{group}.pdf'
            writer = PdfWriter()
            for part in parts:
                for pdf_page in PdfReader(part).pages:
                    writer.add_page(pdf_page)
            with destination.open('wb') as stream:
                writer.write(stream)
            pdf_check = _pdf_check(destination,selected,cards)
            record = {'modelo':'StoryAngelus','grupo':group,'ordem_grupo':order[group],
                      'textos_aprovados_em':APPROVAL_DATE,'cards':cards}
            _json(folder/'ficha.json',record)
            group_checks[group] = {'cards':card_checks,'pdf':pdf_check}
        browser.close()
    if errors:
        raise RuntimeError('Erros de navegador: '+'; '.join(errors))
    records = _records(target)
    expected = {}
    for record in records:
        for card in record['cards']:
            expected[str(target/record['grupo']/(card['id']+'.png'))] = (1080,1920)
            if card['prova_recorte']:
                proof = PROJECT/card['prova_recorte']
                with Image.open(proof) as image:
                    expected[str(proof)] = image.size
    expected[str(target/'prancha.png')] = _board(target,records)
    checks = {'kit':kit,'kit_final':validate_kit(PROJECT),
              'grupos':{record['grupo']:group_checks[record['grupo']] for record in records if record['grupo'] in group_checks},
              'pngs':validate_pngs(expected),'browser':{'ok':True,'errors':[],'fontes_locais_por_render':6,'recursos_externos':False},
              'obras_pendentes':[card['id'] for record in records for card in record['cards'] if card['obra_pendente']],
              'avisos':[warning for record in records for card in record['cards'] for warning in card['avisos']]}
    checks['ok'] = all(checks[key]['ok'] for key in ('kit','kit_final','pngs','browser'))
    if not checks['ok']:
        raise RuntimeError('Falha de validação dos PNGs, kit ou navegador.')
    command = 'python gerar.py stories-avulsos'+(f' --grupo {grupo_filter}' if grupo_filter else '')
    checks['comando'] = command
    _json(target/'verificacao.json',checks)
    report = _report(target,records,checks,command)
    return {'grupos':len(groups),'cards':generated,'pdfs':len(groups),'pngs':len(expected),
            'obras_pendentes':checks['obras_pendentes'],'avisos':checks['avisos'],
            'relatorio':str(report),'verificacoes':str(target/'verificacao.json')}
