"""Conteúdo estrito de Para Rezar, com partes definidas pelo autor no YAML."""

from __future__ import annotations

from pathlib import Path
import warnings

import yaml

from .conteudo import ContentWarning, _UniqueKeyLoader, _date, _mapping, _text, color_token


PRAYER_FIELDS = {"data", "cor", "titulo", "intencao", "origem", "partes"}


def prayer_warnings(day: dict) -> list[str]:
    """Avisos editoriais para terminal e relatório, sem mudar os dados originais."""
    parts = day["partes"]
    if len(parts) == 1 and len(parts[0]) > 400:
        return [
            f'{day["data"]}: card único com {len(parts[0])} caracteres; '
            "acima de 400; considere dividir em partes."
        ]
    return []


def load_prayers(path: Path | str) -> list[dict]:
    """Leia orações sem dividir, recompor ou remover quebras dos seus textos."""
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
        item = _mapping(value, PRAYER_FIELDS, PRAYER_FIELDS, f"dia {index}")
        day = _date(item["data"], f"dia {index}.data")
        context = day.isoformat()
        if context in dates:
            raise ValueError(f"{context}: data repetida no conteúdo.")
        dates.add(context)
        for field in ("titulo", "intencao", "origem"):
            _text(item[field], f"{context}.{field}")
        color_token(item["cor"])
        parts = item["partes"]
        if not isinstance(parts, list) or not parts:
            raise ValueError(f"{context}.partes: use uma lista não vazia de textos.")
        for number, part in enumerate(parts, 1):
            _text(part, f"{context}.partes[{number}]")
            if number < len(parts) and not part.rstrip().endswith((".", ";", "!", "?")):
                raise ValueError(
                    f"{context}.partes[{number}]: parte que não é a última "
                    "deve terminar com '.', ';', '!' ou '?'."
                )
        validated = {**item, "data": context, "partes": list(parts)}
        for message in prayer_warnings(validated):
            warnings.warn(message, ContentWarning, stacklevel=2)
        result.append(validated)
    return result
