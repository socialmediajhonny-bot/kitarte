"""Conteúdo estrito de Coragem, compartilhando a validação local das obras."""

from __future__ import annotations

from pathlib import Path

import yaml

from .conteudo import _UniqueKeyLoader, _date, _mapping, _text, _work, color_token


COURAGE_FIELDS = {"data", "cor", "frase", "referencia", "obra"}


def load_courage(path: Path | str) -> list[dict]:
    """Preserve frase e referência livres; normalize somente a data para ISO."""
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
        item = _mapping(value, COURAGE_FIELDS, COURAGE_FIELDS, f"dia {index}")
        day = _date(item["data"], f"dia {index}.data")
        context = day.isoformat()
        if context in dates:
            raise ValueError(f"{context}: data repetida no conteúdo.")
        dates.add(context)
        for field in ("frase", "referencia"):
            _text(item[field], f"{context}.{field}")
        color_token(item["cor"])
        work = _work(item["obra"], f"{context}.obra")
        result.append({**item, "data": context, "obra": work})
    return result
