"""Auditoria independente dos PDFs de importação, sem usar o HTML gerador.

PyMuPDF mede texto, direções e pixels; pypdf inspeciona a árvore marcada e os
Form XObjects realmente invocados. Poppler dá uma segunda extração do texto e
das fontes. A ficha fornece os nomes dos campos, não as medidas do PDF.
"""
from __future__ import annotations

import json
from math import atan2, degrees, isclose
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any

import fitz
from PIL import Image, ImageChops
from pypdf import PdfReader
from pypdf.generic import ContentStream


VARIANTS = (
    ('controle', 0), ('camada', 0), ('giro', 0),
    ('respiro-32', 16), ('respiro-48', 32),
    ('respiro-80', 64), ('respiro-128', 112),
)
TARGETS = {2: ('trecho_ref', 'Mc 13,37'), 4: ('chamada_oracao', 'Para rezar hoje')}
PAIRS = {2: ('trecho', 'trecho_ref'), 4: ('chamada_oracao', 'pergunta')}


def compact(text: str) -> str:
    return re.sub(r'\s+', '', text)


def _deref(value: Any) -> Any:
    return value.get_object() if hasattr(value, 'get_object') else value


def _number_tree_keys(value: Any, seen: set[int] | None = None) -> set[int]:
    """Resolva o ParentTree; referências presentes mas vazias não bastam."""
    seen = seen if seen is not None else set()
    reference_id = getattr(value, 'idnum', id(value))
    if reference_id in seen: return set()
    seen.add(reference_id)
    node = _deref(value)
    if not isinstance(node, dict): return set()
    numbers = _deref(node.get('/Nums', []))
    keys = set()
    for index in range(0, len(numbers)-1, 2):
        children = _deref(numbers[index+1])
        if children: keys.add(int(numbers[index]))
    for child in _deref(node.get('/Kids', [])):
        keys.update(_number_tree_keys(child, seen))
    return keys


def inspect_tagging(path: Path) -> dict:
    """Confere a estrutura que sobreviveu à gravação final do PDF."""
    reader = PdfReader(path)
    root = reader.trailer['/Root']
    has_tree, has_info = '/StructTreeRoot' in root, '/MarkInfo' in root
    tree = _deref(root.get('/StructTreeRoot')) if has_tree else None
    info = _deref(root.get('/MarkInfo')) if has_info else None
    marked = _deref(info.get('/Marked')) if isinstance(info, dict) else None
    marked = getattr(marked, 'value', marked) is True
    tree_valid = (isinstance(tree, dict) and tree.get('/Type') == '/StructTreeRoot'
                  and tree.get('/K') is not None and tree.get('/ParentTree') is not None)
    page_keys = [int(page['/StructParents']) for page in reader.pages if '/StructParents' in page]
    parent_keys = _number_tree_keys(tree['/ParentTree']) if tree_valid else set()
    tree_valid = bool(tree_valid and _deref(tree['/K'])
                      and len(page_keys) == len(reader.pages) and set(page_keys) <= parent_keys)
    return {'struct_tree_root_presente': has_tree, 'mark_info_presente': has_info,
            'marked_true': marked, 'estrutura_preservada': tree_valid,
            'chaves_de_pagina': page_keys, 'chaves_parent_tree': sorted(parent_keys),
            'parent_tree_next_key': int(tree.get('/ParentTreeNextKey', 0)) if tree_valid else None,
            'sem_marcacao': not has_tree and not has_info,
            'marcado': bool(tree_valid and has_info and marked)}


def transparency_forms(reader: PdfReader, page_number: int) -> list[dict]:
    """Lista apenas Forms chamados por Do, inclusive os aninhados.

    Conta BT/ET no próprio stream, extrai seu texto e registra a opacidade do
    estado gráfico no qual o Form foi chamado. Recursos não usados não valem
    como evidência de isolamento do elemento.
    """
    page = reader.pages[page_number-1]
    found: list[dict] = []

    def walk(stream, resources, prefix: str, inherited_alpha=1.0, parents=()):
        stack = []; alpha = inherited_alpha
        for args, operator in ContentStream(stream, reader).operations:
            if operator == b'q':
                stack.append(alpha)
            elif operator == b'Q':
                alpha = stack.pop() if stack else inherited_alpha
            elif operator == b'gs':
                states = _deref(resources.get('/ExtGState', {}))
                state = _deref(states.get(args[0], {}))
                if '/ca' in state: alpha = float(state['/ca'])
            elif operator == b'Do':
                objects = _deref(resources.get('/XObject', {}))
                reference = objects.get(args[0])
                if reference is None: continue
                obj = _deref(reference)
                if obj.get('/Subtype') != '/Form': continue
                identity = getattr(reference, 'idnum', id(obj))
                if identity in parents: raise ValueError('Ciclo de Form XObjects no PDF.')
                operators = ContentStream(obj, reader).operations
                group = _deref(obj.get('/Group', {}))
                text = page.extract_xform_text(obj, orientations=(0, 90, 180, 270))
                child_resources = _deref(obj.get('/Resources', resources))
                painted_images = 0
                child_objects = _deref(child_resources.get('/XObject', {}))
                for operands, op in operators:
                    if op == b'Do':
                        child = _deref(child_objects.get(operands[0], {}))
                        painted_images += child.get('/Subtype') == '/Image'
                found.append({'recurso': prefix+str(args[0]),
                              'grupo_transparencia': group.get('/S') == '/Transparency',
                              'opacidade_invocacao': alpha,
                              'blocos_bt': sum(op == b'BT' for _, op in operators),
                              'blocos_et': sum(op == b'ET' for _, op in operators),
                              'imagens_pintadas': painted_images,
                              'pinturas_nao_textuais': sum(op in {b'Do', b'S', b's', b'f', b'F', b'f*', b'B', b'B*', b'b', b'b*', b'sh'}
                                                          for _, op in operators),
                              'texto': text, 'texto_sem_espacos': compact(text)})
                walk(obj, child_resources, prefix+str(args[0])+'/', alpha, (*parents, identity))

    walk(page.get_contents(), _deref(page['/Resources']), '')
    return found


def inspect_layer(path: Path, page_number: int, target_text: str) -> dict:
    forms = transparency_forms(PdfReader(path), page_number)
    target = compact(target_text)
    candidates = [form for form in forms if form['texto_sem_espacos'] == target]
    good = [form for form in candidates if form['grupo_transparencia']
            and form['blocos_bt'] == form['blocos_et'] == 1
            and form['imagens_pintadas'] == 0
            and form['pinturas_nao_textuais'] == 0
            and isclose(form['opacidade_invocacao'], .999, abs_tol=.00001)]
    return {'ok': len(good) == 1, 'pagina': page_number, 'alvo': target_text,
            'forms': forms, 'forms_alvo': len(candidates), 'forms_alvo_validos': len(good)}


def text_lines(page: fitz.Page) -> list[dict]:
    lines = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            text = ''.join(span['text'] for span in line['spans'])
            if not compact(text): continue
            direction = line['dir']
            lines.append({'texto': text, 'texto_sem_espacos': compact(text),
                          'caixa_pt': list(line['bbox']), 'direcao': list(direction),
                          'angulo_graus': degrees(atan2(direction[1], direction[0]))})
    return lines


def inspect_rotation(path: Path, page_number: int, target_text: str,
                     target_angle: float = .5) -> dict:
    with fitz.open(path) as document:
        lines = text_lines(document[page_number-1])
    targets = [line for line in lines if line['texto_sem_espacos'] == compact(target_text)]
    others = [line for line in lines if line['texto_sem_espacos'] != compact(target_text)]
    ok = (len(targets) == 1
          and abs(targets[0]['angulo_graus']-target_angle) <= (.05 if target_angle else .01)
          and all(abs(line['angulo_graus']) <= .01 for line in others))
    return {'ok': ok, 'pagina': page_number, 'alvo': target_text,
            'angulo_esperado': target_angle, 'linhas': lines}


def _field_lines(meta: dict, field: str) -> list[str]:
    fields = [text for text in meta['textos'] if text['campo'] == field]
    if len(fields) != 1: raise ValueError(f'Ficha: campo {field} ausente ou duplicado.')
    return fields[0]['linhas']


def _find_lines(page: fitz.Page, expected: list[str]) -> list[dict]:
    lines = text_lines(page); found = []
    for text in expected:
        matches = [line for line in lines if line['texto_sem_espacos'] == compact(text)]
        if len(matches) != 1:
            raise ValueError(f'PDF: linha {text!r} não foi encontrada uma única vez.')
        found.append(matches[0])
    return found


def pair_gap(page: fitz.Page, meta: dict, card: int) -> dict:
    upper, lower = PAIRS[card]
    a = _find_lines(page, _field_lines(meta, upper))
    b = _find_lines(page, _field_lines(meta, lower))
    upper_bottom = max(line['caixa_pt'][3] for line in a)
    lower_top = min(line['caixa_pt'][1] for line in b)
    gap_pt = lower_top-upper_bottom
    return {'superior': upper, 'inferior': lower,
            'caixas_superiores_pt': [line['caixa_pt'] for line in a],
            'caixas_inferiores_pt': [line['caixa_pt'] for line in b],
            'distancia_pt': gap_pt, 'distancia_px': gap_pt*96/72}


def _raster(page: fitz.Page) -> Image.Image:
    scale = 1080/page.rect.width
    pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale), colorspace=fitz.csRGB, alpha=False)
    return Image.frombytes('RGB', (pixmap.width, pixmap.height), pixmap.samples)


def _image_difference(a: Image.Image, b: Image.Image) -> dict:
    if a.size != b.size:
        return {'dimensoes_iguais': False, 'antes': list(a.size), 'depois': list(b.size),
                'identicos': False, 'maior_diferenca_por_canal': None}
    difference = ImageChops.difference(a, b)
    maxima = [extent[1] for extent in difference.getextrema()]
    return {'dimensoes_iguais': True, 'dimensao_px': list(a.size),
            'identicos': difference.getbbox() is None, 'maior_diferenca_por_canal': maxima,
            'limites_da_diferenca': list(difference.getbbox()) if difference.getbbox() else None}


def _poppler_text(path: Path) -> list[str]:
    result = subprocess.run(['pdftotext', '-layout', str(path), '-'],
                            capture_output=True, text=True, check=False)
    if result.returncode: raise ValueError('pdftotext falhou: '+result.stderr.strip())
    pages = result.stdout.split('\f')
    if pages and not pages[-1].strip(): pages.pop()
    return pages


def _font_check(document: fitz.Document, path: Path) -> dict:
    fonts = {}; errors = []
    for page in document:
        for info in page.get_fonts(full=True):
            xref = info[0]
            if xref in fonts: continue
            name = re.sub(r'^[A-Z]{6}\+', '', info[3])
            try:
                _, extension, _, program = document.extract_font(xref)
                embedded = bool(program)
                valid_ttf = (extension.lower() in {'ttf','ttc'}
                             and program[:4] in {b'\x00\x01\x00\x00', b'true', b'ttcf'})
            except Exception as error:
                program = b''; embedded = valid_ttf = False
                errors.append(f'{path.name}: não foi possível extrair {name}: {error}')
            fonts[xref] = {'nome': name, 'embutida': embedded, 'truetype': valid_ttf,
                           'bytes': len(program)}
            if not embedded or not valid_ttf: errors.append(f'{path.name}: TTF não embutido: {name}.')
    process = subprocess.run(['pdffonts', str(path)], capture_output=True, text=True, check=False)
    if process.returncode: errors.append('pdffonts falhou: '+process.stderr.strip())
    rows = process.stdout.splitlines()[2:]
    if not rows: errors.append(f'{path.name}: pdffonts não encontrou fontes.')
    for row in rows:
        match = re.search(r'\s(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$', row)
        if not match or match.group(1) != 'yes': errors.append('pdffonts: fonte não embutida: '+row.strip())
    return {'ok': not errors, 'fontes': list(fonts.values()), 'pdffonts': process.stdout.strip(), 'errors': errors}


def _style(variant: str, card: int, increment: int) -> dict:
    if variant == 'camada': return {'opacity': '0.999'}
    if variant == 'giro': return {'transform': 'rotate(0.5deg)'}
    if increment: return {'margin-top' if card == 2 else 'margin-bottom': f'{increment}px'}
    return {}


def validate_canva(output: Path, gospel_pdf: Path, ficha: dict | None = None) -> dict:
    """Retorne evidências serializáveis e bloqueios; não altera os PDFs auditados."""
    output, gospel_pdf = Path(output), Path(gospel_pdf)
    result: dict = {'ok': False, 'checks': {}, 'errors': []}
    errors = result['errors']

    def check(ok: bool, message: str):
        if not ok: errors.append(message)
        return ok

    try:
        if ficha is None: ficha = json.loads((output/'ficha.json').read_text(encoding='utf-8'))
        for tool in ('pdffonts', 'pdftotext'):
            if not shutil.which(tool): raise ValueError(f'{tool} indisponível.')
        paths = {key: output/f'teste-canva-{key}.pdf' for key in ('a','b')}
        source = fitz.open(gospel_pdf)
        documents = {key: fitz.open(path) for key,path in paths.items()}
        try:
            if len(source) < 4: raise ValueError('PDF do Evangelho precisa conter os cards 2 e 4.')
            # Um Form pode ser pintado por último e ainda estar visualmente
            # acima da pergunta. Compare a ordem de leitura geométrica, como
            # pdftotext -layout, e registre essa escolha explicitamente.
            expected_text = {card: compact(source[card-1].get_text(sort=True)) for card in (2,4)}
            expected_fonts = {re.sub(r'^[A-Z]{6}\+', '', font[3])
                              for card in (2,4) for font in source[card-1].get_fonts(full=True)}
            reference_poppler = _poppler_text(gospel_pdf)
            for card in (2,4):
                check(compact(reference_poppler[card-1]) == expected_text[card],
                      f'Evangelho card {card}: extrações PyMuPDF e pdftotext divergentes.')
            result['origem'] = {'arquivo': str(gospel_pdf), 'paginas': {str(c): c for c in (2,4)},
                                'extracao_pymupdf': 'get_text(sort=True), ordem geométrica de leitura',
                                'extracao_poppler': 'pdftotext -layout'}
            for key, expected_count in [('a',14),('b',2)]:
                document = documents[key]; path=paths[key]
                metadata = ficha['documentos'][key]
                pages_meta = metadata['paginas']
                tag = inspect_tagging(path)
                correct_tagging = tag['sem_marcacao'] if key == 'a' else tag['marcado']
                check(correct_tagging, f'PDF {key.upper()}: marcação incorreta: {tag}.')
                count_ok = len(document) == expected_count and len(pages_meta) == expected_count
                check(count_ok, f'PDF {key.upper()}: esperado {expected_count} páginas no PDF e na ficha.')
                production = {'documentos_html': metadata.get('documentos_html'),
                              'chamadas_page_pdf': metadata.get('chamadas_page_pdf'),
                              'paginas_pdf': metadata.get('paginas_pdf')}
                production_ok = production == {'documentos_html':1, 'chamadas_page_pdf':1,
                                                'paginas_pdf':expected_count}
                check(production_ok, f'PDF {key.upper()}: ficha não declara um HTML e uma chamada page.pdf.')
                font_check = _font_check(document,path)
                errors.extend(font_check['errors'])
                actual_fonts = {font['nome'] for font in font_check['fontes']}
                check(expected_fonts <= actual_fonts, f'PDF {key.upper()}: faltam fontes do card original: {sorted(expected_fonts-actual_fonts)}.')
                poppler = _poppler_text(path)
                check(len(poppler)==expected_count, f'PDF {key.upper()}: pdftotext não retornou {expected_count} páginas.')
                pages=[]
                for index,page in enumerate(document):
                    card=2 if index%2==0 else 4
                    size_ok=isclose(page.rect.width,810,abs_tol=.01) and isclose(page.rect.height,1012.5,abs_tol=.01)
                    check(size_ok,f'PDF {key.upper()} página {index+1}: tamanho diferente de 810 × 1012,5 pt.')
                    text_ok=compact(page.get_text(sort=True))==expected_text[card]
                    poppler_ok=index<len(poppler) and compact(poppler[index])==expected_text[card]
                    check(text_ok and poppler_ok,f'PDF {key.upper()} página {index+1}: texto difere do card {card}.')
                    page_record={'pagina':index+1,'card_origem':card,'dimensao_pt':[page.rect.width,page.rect.height],
                                 'tamanho_ok':size_ok,'texto_pymupdf_igual':text_ok,'texto_pdftotext_igual':poppler_ok}
                    if index<len(pages_meta):
                        meta=pages_meta[index]
                        variant,increment=VARIANTS[index//2] if key=='a' and index<14 else ('controle',0)
                        meta_ok=(meta.get('pagina')==index+1 and meta.get('card_origem')==card
                                 and meta.get('variante')==variant and meta.get('elemento_alvo')==TARGETS[card][0]
                                 and compact(meta.get('elemento_alvo_texto',''))==compact(TARGETS[card][1])
                                 and meta.get('estilo_acrescentado')==_style(variant,card,increment)
                                 and meta.get('incremento_px')==increment)
                        check(meta_ok,f'PDF {key.upper()} página {index+1}: ficha não corresponde à variante especificada.')
                        page_record['ficha_variante_ok']=meta_ok
                        computed = meta.get('estilo_computado_alvo')
                        if computed and increment:
                            computed_ok=(computed.get('position')=='static'
                                         and str(computed.get('opacity'))=='1'
                                         and computed.get('transform')=='none')
                            check(computed_ok,f'PDF {key.upper()} página {index+1}: respiro usa position, opacity ou transform.')
                            page_record['respiro_estilo_computado_ok']=computed_ok
                        target=TARGETS[card][1]
                        rotation=inspect_rotation(path,index+1,target,.5 if variant=='giro' else 0)
                        check(rotation['ok'],f'PDF {key.upper()} página {index+1}: direção das linhas incorreta.')
                        page_record['rotacao']=rotation
                    pages.append(page_record)
                result['checks'][key]={'arquivo':path.name,'paginas':pages,'contagem_ok':count_ok,
                                       'marcacao':tag,'marcacao_ok':correct_tagging,'fontes':font_check,
                                       'producao_declarada':production,'producao_declarada_ok':production_ok}

            a,b=documents['a'],documents['b']
            if len(a)>=14 and len(b)>=2:
                raster=[]
                for index,card in [(0,2),(1,4)]:
                    reference=_raster(source[card-1]);image_a=_raster(a[index]);image_b=_raster(b[index])
                    for name,image in [(f'A{index+1}',image_a),(f'B{index+1}',image_b)]:
                        diff=_image_difference(reference,image)
                        check(diff['identicos'],f'{name}: raster difere do Evangelho card {card}.')
                        raster.append({'pagina':name,'referencia':f'Evangelho card {card}',**diff})
                    diff=_image_difference(image_a,_raster(a[index+2]))
                    maximum=diff['maior_diferenca_por_canal']
                    opacity_ok=diff['dimensoes_iguais'] and maximum is not None and max(maximum)<=2
                    check(opacity_ok,f'A{index+3}: camada muda mais de 2 níveis RGB em relação ao controle.')
                    raster.append({'pagina':f'A{index+3}','referencia':f'A{index+1}',**diff,'limite_rgb':2,'ok':opacity_ok})
                result['checks']['raster']=raster
                layers=[inspect_layer(paths['a'],index,TARGETS[2 if index==3 else 4][1]) for index in (3,4)]
                for layer in layers:
                    check(layer['ok'],f'A{layer["pagina"]}: elemento não está sozinho em Form XObject /Group /Transparency com um BT/ET.')
                result['checks']['camadas']=layers
                gaps=[]
                for index in range(6,14):
                    card=2 if index%2==0 else 4;meta=ficha['documentos']['a']['paginas'][index]
                    increment=VARIANTS[index//2][1];wanted=16+increment
                    pair=meta.get('par',{});upper,lower=PAIRS[card]
                    dom=float(meta.get('distancia_par_px',-1))
                    box_a,box_b=pair['caixa_superior'],pair['caixa_inferior']
                    independent_dom=box_b['y']-box_a['y']-box_a['altura']
                    dom_ok=(pair.get('superior')==upper and pair.get('inferior')==lower
                            and abs(dom-wanted)<=.01 and abs(independent_dom-wanted)<=.01)
                    check(dom_ok,f'A{index+1}: respiro DOM não é {wanted}px.')
                    current=pair_gap(a[index],meta,card)
                    control_meta=ficha['documentos']['a']['paginas'][card//2-1]
                    control=pair_gap(a[card//2-1],control_meta,card)
                    delta=current['distancia_px']-control['distancia_px']
                    pdf_ok=abs(delta-increment)<=.5
                    check(pdf_ok,f'A{index+1}: respiro PDF cresceu {delta:.4f}px; esperado {increment}px ±0,5.')
                    gaps.append({'pagina':index+1,'card_origem':card,'esperado_dom_px':wanted,
                                 'distancia_dom_px':dom,'distancia_calculada_das_caixas_dom_px':independent_dom,
                                 'dom_ok':dom_ok,'pdf':current,'controle_pdf':control,
                                 'incremento_pdf_px':delta,'incremento_esperado_px':increment,'pdf_ok':pdf_ok})
                result['checks']['respiros']=gaps
        finally:
            for document in documents.values(): document.close()
            source.close()
    except Exception as error:
        errors.append(f'{type(error).__name__}: {error}')
    result['ok']=not errors
    return result
