"""Conteúdo estrito dos carrosséis de Igreja Doméstica aprovados pela página."""

from __future__ import annotations

from pathlib import Path

import yaml

from .conteudo import _UniqueKeyLoader, _date, _mapping, _text, _work, color_token


DAY_FIELDS = {"data", "cor", "cards"}
CARD_REQUIRED_FIELDS = {
    "capa": {"tipo", "titulo", "apoio", "obra"},
    "passos": {"tipo", "rotulo", "titulo", "itens", "fonte"},
    "oracao": {"tipo", "rotulo", "titulo", "falas"},
    "conversa": {"tipo", "rotulo", "pergunta", "convite"},
}
CARD_FIELDS = {kind: fields | ({"origem"} if kind == "oracao" else set())
               for kind, fields in CARD_REQUIRED_FIELDS.items()}
SPEECH_FIELDS = {"rubrica", "oracao", "aclamacao"}


def _card(value: object, context: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{context}: esperado um mapa de campos.")
    kind = value.get("tipo")
    if not isinstance(kind, str) or kind not in CARD_FIELDS:
        raise ValueError(f"{context}.tipo: use capa, passos, oracao ou conversa.")
    item = _mapping(value, CARD_FIELDS[kind], CARD_REQUIRED_FIELDS[kind], context)
    result = dict(item)
    for field in CARD_FIELDS[kind] - {"tipo", "obra", "itens", "falas"}:
        if field in item:
            _text(item[field], f"{context}.{field}")
    if kind == "capa":
        result["obra"] = _work(item["obra"], f"{context}.obra")
    if kind == "passos":
        items = item["itens"]
        if not isinstance(items, list) or not 2 <= len(items) <= 5:
            raise ValueError(f"{context}.itens: use uma lista de 2 a 5 textos.")
        for index, text in enumerate(items, 1):
            _text(text, f"{context}.itens[{index}]")
        result["itens"] = list(items)
    if kind == "oracao":
        speeches = item["falas"]
        if not isinstance(speeches, list) or not speeches:
            raise ValueError(f"{context}.falas: use uma lista não vazia de falas.")
        validated = []
        for index, speech in enumerate(speeches, 1):
            speech_context = f"{context}.falas[{index}]"
            speech = _mapping(speech, SPEECH_FIELDS, set(), speech_context)
            if len(speech) != 1:
                raise ValueError(f"{speech_context}: use uma única chave: rubrica, oracao ou aclamacao.")
            field, text = next(iter(speech.items()))
            _text(text, f"{speech_context}.{field}")
            validated.append(dict(speech))
        if not any("oracao" in speech for speech in validated):
            raise ValueError(f"{context}.falas: precisa haver pelo menos uma oracao.")
        result["falas"] = validated
    return result


def load_domestic_church(path: Path | str) -> list[dict]:
    """Preserve a ordem e as quebras do YAML; normalize somente as datas ISO."""
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
        item = _mapping(value, DAY_FIELDS, DAY_FIELDS, f"dia {index}")
        day = _date(item["data"], f"dia {index}.data")
        context = day.isoformat()
        if context in dates:
            raise ValueError(f"{context}: data repetida no conteúdo.")
        dates.add(context)
        if day.weekday() != 6:
            raise ValueError(f"{context}: Igreja Doméstica exige data de domingo.")
        color_token(item["cor"])
        cards = item["cards"]
        if not isinstance(cards, list) or not 2 <= len(cards) <= 5:
            raise ValueError(f"{context}.cards: use uma lista de 2 a 5 cards.")
        cards = [_card(card, f"{context}.cards[{number}]")
                 for number, card in enumerate(cards, 1)]
        if cards[0]["tipo"] != "capa" or any(card["tipo"] == "capa" for card in cards[1:]):
            raise ValueError(f"{context}: a capa precisa ser o primeiro e único card desse tipo.")
        if any(card["tipo"] == "conversa" for card in cards[:-1]):
            raise ValueError(f"{context}: conversa só pode ser o último card.")
        result.append({**item, "data": context, "cards": cards})
    return result
