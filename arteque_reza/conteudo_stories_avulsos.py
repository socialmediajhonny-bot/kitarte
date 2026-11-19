"""Leitura estrita dos stories avulsos, sem datas/tempos implícitos."""
from __future__ import annotations

from pathlib import Path

from PIL import Image
import yaml

from .conteudo import _UniqueKeyLoader, _mapping, _text, _work, color_token, local_artwork_path
from .conteudo_stories import _identifier


REQUIRED_FIELDS = {'id', 'grupo', 'cor', 'serie', 'apoio', 'titulo', 'subtitulo', 'invocacao', 'obra'}
FIELDS = REQUIRED_FIELDS | {'resposta'}
ARTWORK_DIMENSIONS = {
    'obras/stories/terco.jpg': (1822, 2717),
    'obras/stories/chave-de-davi.jpg': (2536, 2811),
    'obras/stories/comece-aqui-1.jpg': (1941, 2401),
    'obras/stories/comece-aqui-2.jpg': (7053, 5864),
    'obras/stories/comece-aqui-3.jpg': (3459, 4001),
}


def validate_artwork_size(work: dict) -> None:
    """As janelas aprovadas dependem dos tamanhos dos originais da rodada."""
    path = local_artwork_path(work['arquivo'])
    expected = ARTWORK_DIMENSIONS.get(work['arquivo'])
    if not path.is_file() or expected is None:
        return
    with Image.open(path) as image:
        actual = image.size
    if actual != expected:
        raise ValueError(f'{work["arquivo"]}: tamanho {actual[0]} × {actual[1]}; '
                         f'esperado {expected[0]} × {expected[1]} px.')


def load_stories_avulsos(path: Path | str) -> list[dict]:
    """Preserve ordem e quebras; IDs são únicos em toda a lista e grupos são seguros."""
    source = Path(path)
    try:
        document = yaml.load(source.read_text(encoding='utf-8'), Loader=_UniqueKeyLoader)
    except (yaml.YAMLError, ValueError) as error:
        raise ValueError(f'YAML inválido em {source}: {error}') from error
    if not isinstance(document, list) or not document:
        raise ValueError('O conteúdo deve ser uma lista não vazia de stories avulsos.')
    result = []
    identifiers = set()
    for number, value in enumerate(document, 1):
        context = f'story {number}'
        item = _mapping(value, FIELDS, REQUIRED_FIELDS, context)
        identifier = _identifier(item['id'], f'{context}.id')
        if identifier in identifiers:
            raise ValueError(f'{context}.id: id de story repetido: {identifier!r}.')
        identifiers.add(identifier)
        _identifier(item['grupo'], f'{context}.grupo')
        color_token(item['cor'])
        for field in ('serie', 'apoio', 'titulo', 'subtitulo', 'invocacao'):
            _text(item[field], f'{context}.{field}')
        if 'resposta' in item:
            _text(item['resposta'], f'{context}.resposta')
        work = _work(item['obra'], f'{context}.obra')
        validate_artwork_size(work)
        result.append({**item, 'obra': work})
    return result
