"""Leitura estrita das quatro séries da noite aprovadas pela página."""
from __future__ import annotations

from pathlib import Path
from typing import Callable

from PIL import Image
import yaml

from .conteudo import (
    _UniqueKeyLoader, _date, _mapping, _reference, _text, _work,
    color_token, local_artwork_path,
)
from .igreja_domestica import BOOKS


LOOK_FIELDS = {"data", "cor", "titulo", "obra", "detalhe", "significado", "onde"}
MASS_FIELDS = {"data", "cor", "capa", "explicacoes", "fecho"}
PRAY_FIELDS = {"data", "cor", "titulo", "texto"}
FAIR_FIELDS = {"data", "cor", "info", "invocacao", "obra", "raiz", "oracao"}
EXPLANATION_FIELDS = {"rotulo", "titulo", "texto", "fonte"}
WINDOW_WORK_FIELDS = {"arquivo", "credito", "pagina", "janela", "tamanho"}


def _texts(value: object, fields: set[str], context: str) -> dict:
    item = _mapping(value, fields, fields, context)
    for field in fields:
        _text(item[field], f"{context}.{field}")
    return dict(item)


def _integers(value: object, length: int, context: str, *, positive: bool) -> list[int]:
    if not isinstance(value, list) or len(value) != length or any(type(n) is not int for n in value):
        raise ValueError(f"{context}: use uma lista de {length} inteiros.")
    if any(n < (1 if positive else 0) for n in value):
        qualifier = "positivos" if positive else "não negativos"
        raise ValueError(f"{context}: use inteiros {qualifier}.")
    return list(value)


def _window(value: object, size: object, artwork: str, area: tuple[int, int], context: str) -> tuple[list[int], list[int]]:
    window = _integers(value, 3, f"{context}.janela", positive=False)
    if window[2] == 0:
        raise ValueError(f"{context}.janela: a largura precisa ser positiva.")
    expected = _integers(size, 2, f"{context}.tamanho", positive=True)
    path = local_artwork_path(artwork)
    if not path.is_file():
        raise ValueError(f"{context}.arquivo: a obra local não foi encontrada: {artwork}.")
    with Image.open(path) as image:
        actual = image.size
    if tuple(expected) != actual:
        raise ValueError(f"{context}.tamanho: arquivo real tem {actual[0]} × {actual[1]}, não {expected}.")
    x, y, width = window
    height = round(width * area[1] / area[0])
    if height < 1 or x + width > actual[0] or y + height > actual[1]:
        raise ValueError(f"{context}.janela: a janela precisa caber inteira no arquivo.")
    if area[0] / width > 1.2:
        raise ValueError(f"{context}.janela: ampliação acima de 1,2 não é permitida.")
    return window, expected


def _window_work(value: object, context: str) -> dict:
    item = _mapping(value, WINDOW_WORK_FIELDS, WINDOW_WORK_FIELDS, context)
    # _work mantém as mesmas regras de caminho, crédito e página, sem aceitar
    # foco/zoom neste esquema de janela explícita.
    _work({field: item[field] for field in ("arquivo", "credito", "pagina")} | {"foco": "50% 50%"}, context)
    window, size = _window(item["janela"], item["tamanho"], item["arquivo"], (308, 404), context)
    return {**item, "janela": window, "tamanho": size}


def _look(item: dict, context: str) -> dict:
    _text(item["titulo"], f"{context}.titulo")
    work = _work(item["obra"], f"{context}.obra")
    detail = _mapping(item["detalhe"], {"titulo", "janela", "tamanho"}, {"titulo", "janela", "tamanho"}, f"{context}.detalhe")
    _text(detail["titulo"], f"{context}.detalhe.titulo")
    window, size = _window(detail["janela"], detail["tamanho"], work["arquivo"], (608, 824), f"{context}.detalhe")
    explanation = _texts(item["significado"], EXPLANATION_FIELDS, f"{context}.significado")
    where = _mapping(item["onde"], {"rotulo", "obras", "texto", "fonte"}, {"rotulo", "obras", "texto", "fonte"}, f"{context}.onde")
    for field in ("rotulo", "texto", "fonte"):
        _text(where[field], f"{context}.onde.{field}")
    works = where["obras"]
    if not isinstance(works, list) or not 1 <= len(works) <= 2:
        raise ValueError(f"{context}.onde.obras: use uma lista de 1 ou 2 obras.")
    works = [_window_work(value, f"{context}.onde.obras[{i}]") for i, value in enumerate(works, 1)]
    return {**item, "obra": work, "detalhe": {**detail, "janela": window, "tamanho": size},
            "significado": explanation, "onde": {**where, "obras": works}}


def _mass(item: dict, context: str) -> dict:
    cover = _texts(item["capa"], {"pergunta", "resposta"}, f"{context}.capa")
    explanations = item["explicacoes"]
    if not isinstance(explanations, list) or not 1 <= len(explanations) <= 3:
        raise ValueError(f"{context}.explicacoes: use uma lista de 1 a 3 explicações.")
    explanations = [_texts(value, EXPLANATION_FIELDS, f"{context}.explicacoes[{i}]")
                    for i, value in enumerate(explanations, 1)]
    closing = _texts(item["fecho"], {"rotulo", "frase", "convite"}, f"{context}.fecho")
    return {**item, "capa": cover, "explicacoes": explanations, "fecho": closing}


def _pray(item: dict, context: str) -> dict:
    for field in ("titulo", "texto"):
        _text(item[field], f"{context}.{field}")
    return dict(item)


def _fair(item: dict, context: str) -> dict:
    info = _text(item["info"], f"{context}.info")
    if len(info) > 16:
        raise ValueError(f"{context}.info: use no máximo 16 caracteres.")
    _text(item["invocacao"], f"{context}.invocacao")
    work = _work(item["obra"], f"{context}.obra")
    root = _texts(item["raiz"], {"rotulo", "versiculo", "referencia", "texto", "fonte"}, f"{context}.raiz")
    book, separator, verses = root["referencia"].partition(" ")
    if not separator or book not in BOOKS:
        raise ValueError(f"{context}.raiz.referencia: livro bíblico fora da lista permitida.")
    _reference("Lc " + verses, f"{context}.raiz.referencia")
    prayer = _texts(item["oracao"], {"rotulo", "frase", "convite"}, f"{context}.oracao")
    return {**item, "obra": work, "raiz": root, "oracao": prayer}


def _load(path: Path | str, fields: set[str], validate: Callable[[dict, str], dict]) -> list[dict]:
    source = Path(path)
    try:
        document = yaml.load(source.read_text(encoding="utf-8"), Loader=_UniqueKeyLoader)
    except (yaml.YAMLError, ValueError) as error:
        raise ValueError(f"YAML inválido em {source}: {error}") from error
    if not isinstance(document, list) or not document:
        raise ValueError("O conteúdo deve ser uma lista não vazia de dias.")
    result = []
    dates = set()
    for index, value in enumerate(document, 1):
        item = _mapping(value, fields, fields, f"dia {index}")
        day = _date(item["data"], f"dia {index}.data").isoformat()
        if day in dates:
            raise ValueError(f"{day}: data repetida no conteúdo.")
        dates.add(day)
        color_token(item["cor"])
        result.append({**validate(item, day), "data": day})
    return result


def load_look_again(path: Path | str) -> list[dict]:
    return _load(path, LOOK_FIELDS, _look)


def load_inside_mass(path: Path | str) -> list[dict]:
    return _load(path, MASS_FIELDS, _mass)


def load_pray_for_you(path: Path | str) -> list[dict]:
    return _load(path, PRAY_FIELDS, _pray)


def load_all_fair(path: Path | str) -> list[dict]:
    return _load(path, FAIR_FIELDS, _fair)


LOADERS = {
    "olhe-de-novo": load_look_again,
    "por-dentro-da-missa": load_inside_mass,
    "rezo-por-voce": load_pray_for_you,
    "toda-bela": load_all_fair,
}
