"""Leitura estrita das novenas aprovadas, sem recompor seus textos."""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path
import re

import yaml

from .conteudo import _UniqueKeyLoader, _date, _mapping, _text, color_token


NOVENA_FIELDS = {"id", "nome", "cor", "refrao", "dias", "encerramento"}
DAY_FIELDS = {"data", "titulo", "fonte", "oracao"}
CLOSING_REQUIRED_FIELDS = {"data", "cor", "titulo", "oracao"}
CLOSING_FIELDS = CLOSING_REQUIRED_FIELDS | {"fonte", "final"}


def _prayer(value: object, context: str) -> str:
    prayer = _text(value, context)
    if len(prayer) > 240:
        raise ValueError(
            f"{context}: oração com {len(prayer)} caracteres; limite 240, "
            "sem contar o refrão."
        )
    return prayer


def load_novenas(path: Path | str) -> list[dict]:
    """Preserve a ordem, os campos e as quebras; normalize só as datas ISO.

    Os nove números dos dias vêm da posição na lista, sem acrescentar campos
    ao conteúdo. A data do encerramento deve seguir imediatamente o nono dia.
    """
    source = Path(path)
    try:
        document = yaml.load(source.read_text(encoding="utf-8"), Loader=_UniqueKeyLoader)
    except (yaml.YAMLError, ValueError) as error:
        raise ValueError(f"YAML inválido em {source}: {error}") from error
    if not isinstance(document, list) or not document:
        raise ValueError("O conteúdo deve ser uma lista não vazia de novenas.")

    result = []
    identifiers = set()
    for index, value in enumerate(document, 1):
        context = f"novena {index}"
        item = _mapping(value, NOVENA_FIELDS, NOVENA_FIELDS, context)
        identifier = _text(item["id"], f"{context}.id")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", identifier):
            raise ValueError(
                f"{context}.id: id inválido; comece com letra ou número ASCII "
                "e use somente letras, números, hífen ou sublinhado."
            )
        if identifier in identifiers:
            raise ValueError(f"{context}.id: id de novena repetido: {identifier!r}.")
        identifiers.add(identifier)
        context = identifier
        _text(item["nome"], f"{context}.nome")
        _text(item["refrao"], f"{context}.refrao")
        color_token(item["cor"])

        days = item["dias"]
        if not isinstance(days, list) or len(days) != 9:
            raise ValueError(f"{context}.dias: use exatamente 9 dias em uma lista.")
        normalized_days = []
        previous_date = None
        for number, day in enumerate(days, 1):
            day_context = f"{context}.dias[{number}]"
            entry = _mapping(day, DAY_FIELDS, DAY_FIELDS, day_context)
            day_date = _date(entry["data"], f"{day_context}.data")
            if previous_date is not None and day_date - previous_date != timedelta(days=1):
                raise ValueError(
                    f"{day_context}.data: os 9 dias precisam ter datas consecutivas "
                    "na ordem da lista."
                )
            previous_date = day_date
            _text(entry["titulo"], f"{day_context}.titulo")
            _text(entry["fonte"], f"{day_context}.fonte")
            _prayer(entry["oracao"], f"{day_context}.oracao")
            normalized_days.append({**entry, "data": day_date.isoformat()})

        closing_context = f"{context}.encerramento"
        closing = _mapping(item["encerramento"], CLOSING_FIELDS,
                           CLOSING_REQUIRED_FIELDS, closing_context)
        closing_date = _date(closing["data"], f"{closing_context}.data")
        if closing_date - previous_date != timedelta(days=1):
            raise ValueError(
                f"{closing_context}.data: o encerramento precisa cair no dia "
                "seguinte ao 9º dia."
            )
        color_token(closing["cor"])
        _text(closing["titulo"], f"{closing_context}.titulo")
        _prayer(closing["oracao"], f"{closing_context}.oracao")
        for field in ("fonte", "final"):
            if field in closing:
                _text(closing[field], f"{closing_context}.{field}")
        result.append({**item, "dias": normalized_days,
                       "encerramento": {**closing, "data": closing_date.isoformat()}})
    return result
