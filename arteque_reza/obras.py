"""Enquadramento de obras locais: cover, foco, zoom e margens fotográficas.

O zoom usa a mesma origem do object-position, depois do object-fit: cover.
O cálculo em pixels originais também orienta a prova de recorte e a ficha.
"""
from __future__ import annotations

from math import cos, isfinite, pi, sin
from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageStat


def validate_zoom(value: int | float) -> float:
    if type(value) not in (int, float) or not 1 <= value <= 3 or not isfinite(value):
        raise ValueError('obra.zoom: use um número entre 1 e 3.')
    return float(value)


def _focus(value: str) -> tuple[float, float]:
    match = re.fullmatch(r'(\d+(?:\.\d+)?)%\s+(\d+(?:\.\d+)?)%', value) if isinstance(value, str) else None
    if match is None or any(not 0 <= float(item) <= 100 for item in match.groups()):
        raise ValueError('obra.foco: use duas porcentagens entre 0% e 100%.')
    return tuple(float(item) / 100 for item in match.groups())


def image_style(focus: str, zoom: float = 1) -> str:
    """CSS da imagem; a máscara continua no contêiner, fora do transform."""
    _focus(focus)
    zoom = validate_zoom(zoom)
    css = f'object-position:{focus}'
    if zoom != 1:
        css += f';transform:scale({zoom:g});transform-origin:{focus}'
    return css


def artwork_geometry(artwork: Path, focus: str, zoom: float = 1, *,
                     niche_width: float = 680, niche_height: float = 760) -> dict:
    """Janela retangular do arco em coordenadas da imagem original."""
    fx, fy = _focus(focus)
    zoom = validate_zoom(zoom)
    tw, th = niche_width - 32, niche_height - 16
    if tw <= 0 or th <= 0:
        raise ValueError('O nicho precisa comportar as margens internas de 16px.')
    with Image.open(artwork) as source:
        width, height = source.size
    cover = max(tw / width, th / height)
    scale = cover * zoom
    window_width, window_height = tw / scale, th / scale
    return {'foco': focus, 'zoom': zoom,
            'imagem_original': {'largura': width, 'altura': height},
            'nicho': {'largura': niche_width, 'altura': niche_height},
            'area_interna': {'largura': tw, 'altura': th},
            'escala_cover': cover, 'escala_com_zoom': scale,
            'janela_original': {'x': (width - window_width) * fx,
                                'y': (height - window_height) * fy,
                                'largura': window_width, 'altura': window_height}}


def uniform_margins(artwork: Path) -> dict[str, int]:
    """Bordas contíguas com >=4 linhas/colunas inteiras de σ cinza <6."""
    with Image.open(artwork) as source:
        image = source.convert('L')
        width, height = image.size
        margins = {}
        for side, count in (('topo', height), ('base', height),
                            ('esquerda', width), ('direita', width)):
            contiguous = 0
            for offset in range(count):
                if side == 'topo': box = (0, offset, width, offset + 1)
                elif side == 'base': box = (0, height - offset - 1, width, height - offset)
                elif side == 'esquerda': box = (offset, 0, offset + 1, height)
                else: box = (width - offset - 1, 0, width - offset, height)
                if ImageStat.Stat(image.crop(box)).stddev[0] >= 6:
                    break
                contiguous += 1
            margins[side] = contiguous if contiguous >= 4 else 0
    return margins


def inspect_artwork(artwork: Path, focus: str, zoom: float = 1, *,
                    niche_width: float = 680, niche_height: float = 760,
                    date: str | None = None) -> dict:
    geometry = artwork_geometry(artwork, focus, zoom, niche_width=niche_width, niche_height=niche_height)
    margins = uniform_margins(artwork)
    window, original = geometry['janela_original'], geometry['imagem_original']
    visible = []
    if margins['topo'] and window['y'] < margins['topo'] - 1e-9: visible.append('topo')
    if margins['base'] and window['y'] + window['altura'] > original['altura'] - margins['base'] + 1e-9: visible.append('base')
    if margins['esquerda'] and window['x'] < margins['esquerda'] - 1e-9: visible.append('esquerda')
    if margins['direita'] and window['x'] + window['largura'] > original['largura'] - margins['direita'] + 1e-9: visible.append('direita')
    warnings = []
    if visible:
        labels = {'topo': 'no topo', 'base': 'na base', 'esquerda': 'à esquerda', 'direita': 'à direita'}
        sides = [labels[side] for side in visible]
        label = sides[0] if len(sides) == 1 else ', '.join(sides[:-1]) + ' e ' + sides[-1]
        warnings.append(f'{date or Path(artwork).name}: margem da foto visível {label}; aumente o zoom')
    geometry.update({'margens_detectadas': margins, 'margens_visiveis': visible, 'avisos': warnings})
    return geometry


def crop_proof(artwork: Path, output: Path, focus: str, *, zoom: float = 1,
               niche_width: float = 680, niche_height: float = 760,
               date: str | None = None) -> dict:
    """Obra inteira a 1080px com o contorno da janela ampliada em arco."""
    geometry = inspect_artwork(artwork, focus, zoom, niche_width=niche_width, niche_height=niche_height, date=date)
    with Image.open(artwork) as raw:
        raw.load()
        source = raw.convert('RGB')
        width, height = source.size
        full = source.resize((1080, round(height * 1080 / width)), Image.Resampling.LANCZOS)
    window = geometry['janela_original']
    tw, th = geometry['area_interna']['largura'], geometry['area_interna']['altura']
    scale = geometry['escala_com_zoom']
    def inverse(x, y):
        return ((window['x'] + x / scale) * 1080 / width,
                (window['y'] + y / scale) * 1080 / width)
    curve = [inverse(tw / 2 + tw / 2 * cos(pi + i * pi / 240),
                     tw / 2 + tw / 2 * sin(pi + i * pi / 240)) for i in range(241)]
    curve += [inverse(tw, th), inverse(0, th), curve[0]]
    draw = ImageDraw.Draw(full)
    draw.line(curve, fill='#faf6ee', width=9, joint='curve')
    draw.line(curve, fill='#5b2e70', width=4, joint='curve')
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    full.save(output)
    return geometry
