"""Conteúdo estrito dos santinhos e cards de festa, com o leitor já usado no Evangelho."""

from __future__ import annotations

from pathlib import Path

import yaml

from .conteudo import _UniqueKeyLoader, _date, _mapping, _text, _work, color_token


COMMON_FIELDS = {"data", "tipo", "cor", "grau", "nome", "obra"}
TYPE_FIELDS = {
    "santinho": COMMON_FIELDS | {"titulo", "frase", "fonte"},
    "festa": COMMON_FIELDS,
}


def load_saints(path: Path | str) -> list[dict]:
    """Valide cada modelo e devolva os campos originais com ``data`` ISO.

    Frases ficam sem aspas no conteúdo: o renderer acrescenta as aspas curvas.
    A obra pode estar ausente no disco e não é baixada por este leitor.
    """
    source = Path(path)
    try:
        document = yaml.load(source.read_text(encoding="utf-8"), Loader=_UniqueKeyLoader)
    except (yaml.YAMLError, ValueError) as error:
        raise ValueError(f"YAML inválido em {source}: {error}") from error
    if not isinstance(document, list) or not document:
        raise ValueError("O conteúdo deve ser uma lista não vazia de dias.")

    result = []
    dates = set()
    all_fields = set().union(*TYPE_FIELDS.values())
    for index, value in enumerate(document, 1):
        context = f"dia {index}"
        item = _mapping(value, all_fields, COMMON_FIELDS, context)
        kind = _text(item["tipo"], f"{context}.tipo")
        if kind not in TYPE_FIELDS:
            raise ValueError(f"{context}.tipo: use santinho ou festa; recebido {kind!r}.")
        day = _date(item["data"], f"{context}.data")
        context = day.isoformat()
        fields = TYPE_FIELDS[kind]
        _mapping(item, fields, fields, context)
        if day.weekday() == 6:
            raise ValueError(f"{context}: domingo não tem Santo do Dia.")
        if context in dates:
            raise ValueError(f"{context}: data repetida no conteúdo.")
        dates.add(context)
        for field in fields - {"data", "obra"}:
            _text(item[field], f"{context}.{field}")
        color_token(item["cor"])
        work = _work(item["obra"], f"{context}.obra")
        result.append({**item, "data": context, "obra": work})
    return result
