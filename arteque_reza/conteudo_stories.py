"""Schema estrito dos stories fixos e das suas versões por tempo litúrgico."""

from __future__ import annotations

from pathlib import Path
import re

import yaml

from .conteudo import _UniqueKeyLoader, _mapping, _text, _work, color_token


ROOT_FIELDS = {"tempos", "stories"}
SEASON_FIELDS = {"id", "nome", "cor"}
STORY_REQUIRED_FIELDS = {"id", "hora", "titulo", "subtitulo", "invocacao", "obra"}
STORY_FIELDS = STORY_REQUIRED_FIELDS | {"resposta"}


def _items(value: object, context: str) -> list:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{context}: use uma lista não vazia.")
    return value


def _identifier(value: object, context: str) -> str:
    identifier = _text(value, context)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", identifier):
        raise ValueError(
            f"{context}: id inválido; comece com uma letra ou número ASCII "
            "e use somente letras, números, hífen ou sublinhado."
        )
    return identifier


def load_stories(path: Path | str) -> dict:
    """Preserve campos, textos e ordem sem introduzir datas ou padrões no YAML.

    Os ids são também nomes de diretórios e arquivos; por isso não aceitam
    separadores de caminho. A ausência de obra local é permitida pelo schema.
    """
    source = Path(path)
    try:
        document = yaml.load(source.read_text(encoding="utf-8"), Loader=_UniqueKeyLoader)
    except (yaml.YAMLError, ValueError) as error:
        raise ValueError(f"YAML inválido em {source}: {error}") from error
    root = _mapping(document, ROOT_FIELDS, ROOT_FIELDS, "raiz")

    seasons = []
    season_ids = set()
    for index, value in enumerate(_items(root["tempos"], "tempos"), 1):
        context = f"tempos[{index}]"
        item = _mapping(value, SEASON_FIELDS, SEASON_FIELDS, context)
        identifier = _identifier(item["id"], f"{context}.id")
        if identifier in season_ids:
            raise ValueError(f"{context}.id: id de tempo repetido: {identifier!r}.")
        season_ids.add(identifier)
        _text(item["nome"], f"{context}.nome")
        color_token(item["cor"])
        seasons.append(dict(item))

    stories = []
    story_ids = set()
    for index, value in enumerate(_items(root["stories"], "stories"), 1):
        context = f"stories[{index}]"
        item = _mapping(value, STORY_FIELDS, STORY_REQUIRED_FIELDS, context)
        identifier = _identifier(item["id"], f"{context}.id")
        if identifier in story_ids:
            raise ValueError(f"{context}.id: id de story repetido: {identifier!r}.")
        story_ids.add(identifier)
        for field in ("hora", "titulo", "subtitulo", "invocacao"):
            _text(item[field], f"{context}.{field}")
        if not re.fullmatch(r"(?:[0-9]|1[0-9]|2[0-3])h", item["hora"]):
            raise ValueError(f"{context}.hora: use de 0h a 23h, por exemplo 12h.")
        if "resposta" in item:
            _text(item["resposta"], f"{context}.resposta")
        work = _work(item["obra"], f"{context}.obra")
        stories.append({**item, "obra": work})
    return {"tempos": seasons, "stories": stories}
