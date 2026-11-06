"""Confere as formas vetoriais do nicho no PDF destinado ao Canva.

As medidas recebidas vêm do DOM em pixels CSS. O Chromium exporta cada pixel
como 0,75 ponto; as três verificações usam os desenhos extraídos pelo PyMuPDF.
"""
from __future__ import annotations

from math import isfinite
from pathlib import Path
import re

import fitz

from .base import dimension


PX_TO_PT = .75
BBOX_TOLERANCE_PT = .5
COLOR_TOLERANCE = .5 / 255 + 1e-6


def _box(value: dict) -> dict:
    if not isinstance(value, dict):
        raise ValueError('Caixa do nicho precisa ser um objeto.')
    try:
        box = {key: float(value[key]) for key in ('x', 'y', 'width', 'height')}
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError('Caixa do nicho precisa conter x, y, width e height numéricos.') from exc
    if not all(isfinite(number) for number in box.values()):
        raise ValueError('Caixa do nicho contém medida não finita.')
    if box['width'] <= 0 or box['height'] <= 0:
        raise ValueError('Caixa do nicho precisa ter largura e altura positivas.')
    return box


def _hex(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', value):
        raise ValueError('Cor do filete precisa ser um hexadecimal RGB de seis dígitos.')
    return value.lower()


def _page_number(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError('Página do nicho precisa ser um inteiro a partir de 1.')
    return value


def niches_from_elements(elements: list[dict], page: int = 1) -> list[dict]:
    """Associe cada filete ao parapeito medido na mesma base e centro.

    Uma página de texto sem nicho devolve lista vazia. Uma ficha incompleta ou
    ambígua interrompe a geração, em vez de omitir uma forma da conferência.
    """
    page = _page_number(page)
    filets = [item for item in elements if item.get('element') == 'nicho-filete']
    sills = [item for item in elements if item.get('element') == 'nicho-parapeito']
    result = []
    used = set()
    for filet in filets:
        box = _box(filet)
        color = _hex(filet.get('hex'))
        center = box['x'] + box['width'] / 2
        base = box['y'] + box['height']
        matches = []
        for index, sill in enumerate(sills):
            candidate = _box(sill)
            if (abs(candidate['x'] + candidate['width'] / 2 - center) <= .01
                    and abs(candidate['y'] - base) <= .01):
                matches.append((index, sill, candidate))
        if len(matches) != 1 or matches[0][0] in used:
            raise ValueError(f'Página {page}: parapeito ausente ou ambíguo para o filete do nicho.')
        index, sill, candidate = matches[0]
        if _hex(sill.get('hex')) != color:
            raise ValueError(f'Página {page}: filete e parapeito têm cores diferentes.')
        used.add(index)
        result.append({'page': page, **box, 'hex': color, 'parapeito': candidate})
    if len(used) != len(sills):
        raise ValueError(f'Página {page}: parapeito sem filete correspondente.')
    return result


def _rect_pt(box: dict) -> tuple[float, float, float, float]:
    return tuple(number * PX_TO_PT for number in
                 (box['x'], box['y'], box['x'] + box['width'], box['y'] + box['height']))


def _same_rect(actual, expected) -> bool:
    return all(abs(a - b) <= BBOX_TOLERANCE_PT for a, b in zip(actual, expected))


def _same_color(actual, expected) -> bool:
    return (actual is not None and len(actual) == 3
            and all(abs(a - b) <= COLOR_TOLERANCE for a, b in zip(actual, expected)))


def validate_niche_pdf(path: Path, niches: list[dict]) -> dict:
    """Exija um filete curvo, nenhuma borda CSS antiga e um parapeito simples.

    Devolve uma prova JSON, inclusive quando o PDF ou uma especificação falha.
    O gerador deve interromper a geração se ``ok`` for falso.
    """
    path = Path(path)
    errors = []
    records = []
    result = {'ok': False, 'arquivo': str(path), 'escala_px_para_pt': PX_TO_PT,
              'tolerancia_caixa_pt': BBOX_TOLERANCE_PT, 'nichos': records, 'errors': errors}
    try:
        document = fitz.open(path)
    except (OSError, RuntimeError, ValueError) as exc:
        errors.append(f'{path.name}: PDF não pôde ser aberto: {exc}')
        return result
    with document:
        drawings_by_page = {}
        for index, raw in enumerate(niches, 1):
            record = {'indice': index, 'filete_vetorial': False,
                      'borda_antiga_ausente': False, 'parapeito_vetorial': False}
            records.append(record)
            try:
                page_number = _page_number(raw.get('page', 1))
                box = _box(raw)
                color_hex = _hex(raw.get('hex'))
                # A caixa explícita usa a medição do ::after. O padrão também
                # aceita specs externos, com o avanço lateral do token do kit.
                margin = dimension('espaco-4')
                sill = _box(raw.get('parapeito', {
                    'x': box['x'] - margin, 'y': box['y'] + box['height'],
                    'width': box['width'] + 2 * margin, 'height': 3,
                }))
                if (abs(sill['height'] - 3) > .01
                        or abs(sill['y'] - box['y'] - box['height']) > .01):
                    raise ValueError('Parapeito deve ter 3 px e começar na base do nicho.')
            except (AttributeError, TypeError, ValueError) as exc:
                errors.append(f'{path.name}, nicho {index}: {exc}')
                continue
            record.update(pagina=page_number, hex=color_hex,
                          caixa_nicho_pt=list(_rect_pt(box)), caixa_parapeito_pt=list(_rect_pt(sill)))
            if page_number > len(document):
                errors.append(f'{path.name}, nicho {index}: página {page_number} não existe.')
                continue
            if page_number not in drawings_by_page:
                drawings_by_page[page_number] = document[page_number - 1].get_drawings()
            color_rgb = tuple(channel / 255 for channel in bytes.fromhex(color_hex[1:]))
            fills = [drawing for drawing in drawings_by_page[page_number]
                     if 'f' in drawing.get('type', '') and _same_color(drawing.get('fill'), color_rgb)]
            niche_fills = [drawing for drawing in fills if _same_rect(drawing['rect'], _rect_pt(box))]
            curved = [drawing for drawing in niche_fills
                      if any(item[0] == 'c' for item in drawing['items'])]
            old_border = [drawing for drawing in niche_fills
                          if drawing['items'] and all(item[0] == 're' for item in drawing['items'])]
            sill_fills = [drawing for drawing in fills
                          if _same_rect(drawing['rect'], _rect_pt(sill))
                          and abs(drawing['rect'].height - 3 * PX_TO_PT) <= .01
                          and abs(drawing['rect'].width - sill['width'] * PX_TO_PT) <= .01
                          and len(drawing['items']) == 1 and drawing['items'][0][0] == 're']
            record.update(filete_vetorial=len(curved) == 1,
                          borda_antiga_ausente=not old_border,
                          parapeito_vetorial=len(sill_fills) == 1,
                          preenchimentos_curvos=len(curved),
                          assinaturas_antigas_re=len(old_border), parapeitos_re=len(sill_fills))
            for key, message in (
                    ('filete_vetorial', 'esperado exatamente um preenchimento curvo na caixa e cor do filete'),
                    ('borda_antiga_ausente', 'detectada a borda CSS antiga feita de retângulos na caixa do nicho'),
                    ('parapeito_vetorial', 'esperado exatamente um parapeito retangular separado de 3 px')):
                if not record[key]:
                    errors.append(f'{path.name}, página {page_number}, nicho {index}: {message}.')
    result['ok'] = not errors
    return result
