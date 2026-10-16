"""Leitura estrita do conteúdo local dos carrosséis do Evangelho do Dia."""

from __future__ import annotations

from datetime import date
from html import escape
from pathlib import Path, PurePosixPath
import re
from typing import Any
from urllib.parse import urlsplit
import warnings

import yaml

from .base import PROJECT


COLOR_TOKENS = {
    "verde": "liturgico-verde",
    "roxo": "liturgico-roxo",
    "ouro": "liturgico-branco",
    "branco": "liturgico-branco",
    "vermelho": "liturgico-vermelho",
    "rosa": "liturgico-rosa",
}
GOSPELS = {"Mt": "Mateus", "Mc": "Marcos", "Lc": "Lucas", "Jo": "João"}
WEEKDAYS = ("seg", "ter", "qua", "qui", "sex", "sáb", "dom")
MONTHS = ("jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez")
ROOT_FIELDS = {
    "data", "celebracao", "cor", "referencia", "titulo", "obra", "trecho",
    "trecho_ref", "reflexao", "pergunta",
}
WORK_FIELDS = {"arquivo", "credito", "pagina", "foco"}
REFLECTION_FIELDS = {"titulo", "texto"}
REFERENCE_PATTERN = re.compile(
    r"(?:Mt|Mc|Lc|Jo) [1-9]\d*,[1-9]\d*[a-d]?"
    r"(?:[-.][1-9]\d*(?:,[1-9]\d*)?[a-d]?)*"
    r"(?:;\s*[1-9]\d*,[1-9]\d*[a-d]?(?:[-.][1-9]\d*(?:,[1-9]\d*)?[a-d]?)*)*"
)


class ContentWarning(UserWarning):
    """Conteúdo permitido que merece atenção no relatório."""


class _UniqueKeyLoader(yaml.SafeLoader):
    """Evite que uma chave repetida descarte texto silenciosamente."""


def _unique_mapping(loader: _UniqueKeyLoader, node: Any, deep: bool = False) -> dict:
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            repeated = key in result
        except TypeError as error:
            raise ValueError("As chaves do YAML precisam ser nomes de campos.") from error
        if repeated:
            raise ValueError(f"Campo repetido no YAML: {key!r}.")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping
)


def _mapping(value: Any, fields: set[str], required: set[str], context: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{context}: esperado um mapa de campos.")
    unknown = set(value) - fields
    if unknown:
        names = ", ".join(sorted(map(str, unknown)))
        raise ValueError(f"{context}: campo desconhecido: {names}.")
    missing = required - set(value)
    if missing:
        raise ValueError(f"{context}: campo obrigatório ausente: {', '.join(sorted(missing))}.")
    return value


def _text(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{context}: esperado texto não vazio.")
    return value


def _date(value: Any, context: str = "data") -> date:
    # PyYAML converte datas ISO sem aspas em date; timestamps não são datas.
    if type(value) is date:
        return value
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"{context}: use uma data válida no formato AAAA-MM-DD.")
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"{context}: data inválida: {value!r}.") from error


def color_token(value: str) -> str:
    """Resolva a cor editorial para o token litúrgico, sem alterar o YAML."""
    if not isinstance(value, str) or value not in COLOR_TOKENS:
        raise ValueError(f"Cor desconhecida: {value!r}; use {', '.join(COLOR_TOKENS)}.")
    return COLOR_TOKENS[value]


def _reference(value: Any, context: str) -> str:
    value = _text(value, context)
    if not REFERENCE_PATTERN.fullmatch(value):
        raise ValueError(
            f"{context}: referência inválida: {value!r}; "
            "use Mt, Mc, Lc ou Jo, capítulo e versículos (por exemplo Mc 13,33-37)."
        )
    return value


def local_artwork_path(arquivo: str, project_root: Path = PROJECT) -> Path:
    """Resolva somente arquivo relativo local; a ausência permite a provisória.

    Não abre URLs nem baixa obras. Também impede escape por '..' e por links
    simbólicos, mantendo as imagens dentro do projeto servido no loopback.
    """
    value = _text(arquivo, "obra.arquivo")
    source = PurePosixPath(value)
    if (
        value != value.strip() or "\\" in value or ":" in value
        or "?" in value or "#" in value or any(ord(char) < 32 for char in value)
        or source.is_absolute() or ".." in source.parts
        or value.startswith("//") or not source.name or source == PurePosixPath(".")
    ):
        raise ValueError("obra.arquivo: use um caminho relativo local dentro do projeto.")
    root = Path(project_root).resolve()
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise ValueError("obra.arquivo: o caminho ou link simbólico sai do projeto.")
    if path.exists() and not path.is_file():
        raise ValueError("obra.arquivo: o caminho precisa apontar para um arquivo.")
    return path


def _work(value: Any, context: str) -> dict:
    work = _mapping(value, WORK_FIELDS, WORK_FIELDS, context)
    for field in WORK_FIELDS:
        _text(work[field], f"{context}.{field}")
    local_artwork_path(work["arquivo"])
    page = urlsplit(work["pagina"])
    if page.scheme not in {"https", "http"} or not page.netloc or any(
        char.isspace() for char in work["pagina"]
    ):
        raise ValueError(f"{context}.pagina: use uma URL http ou https válida.")
    focus = re.fullmatch(r"(\d+(?:\.\d+)?)%\s+(\d+(?:\.\d+)?)%", work["foco"])
    if focus is None or any(not 0 <= float(item) <= 100 for item in focus.groups()):
        raise ValueError(f"{context}.foco: use duas porcentagens entre 0% e 100%.")
    return dict(work)


def load_content(path: Path | str) -> list[dict]:
    """Leia e valide todos os dias, preservando textos e quebras manuais.

    O resultado mantém os campos originais e normaliza apenas ``data`` para
    string ISO. A imagem não precisa existir: o renderer usará a provisória.
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
    for index, value in enumerate(document, 1):
        context = f"dia {index}"
        item = _mapping(value, ROOT_FIELDS, ROOT_FIELDS - {"reflexao"}, context)
        day = _date(item["data"], f"{context}.data")
        context = day.isoformat()
        if context in dates:
            raise ValueError(f"{context}: data repetida no conteúdo.")
        dates.add(context)
        for field in ("celebracao", "titulo", "trecho", "pergunta"):
            _text(item[field], f"{context}.{field}")
        color_token(item["cor"])
        _reference(item["referencia"], f"{context}.referencia")
        _reference(item["trecho_ref"], f"{context}.trecho_ref")
        validated = {**item, "data": context, "obra": _work(item["obra"], f"{context}.obra")}
        if "reflexao" in item:
            reflection = _mapping(
                item["reflexao"], REFLECTION_FIELDS, REFLECTION_FIELDS,
                f"{context}.reflexao",
            )
            for field in REFLECTION_FIELDS:
                _text(reflection[field], f"{context}.reflexao.{field}")
            validated["reflexao"] = dict(reflection)
            if day.weekday() != 6:
                warnings.warn(
                    f"{context}: dia de semana com reflexão; permitido para solenidades.",
                    ContentWarning, stacklevel=2,
                )
        elif day.weekday() == 6:
            raise ValueError(f"{context}: domingo sem reflexão; inclua reflexao.titulo e reflexao.texto.")
        result.append(validated)
    return result


def date_label(value: date | str) -> str:
    """Data curta editorial, independente do locale do sistema operacional."""
    day = _date(value)
    return f"{WEEKDAYS[day.weekday()]}, {day.day} {MONTHS[day.month - 1]}"


def expanded_reference(reference: str) -> str:
    """Expanda só o livro; mantenha capítulos, versículos e separadores."""
    _reference(reference, "referencia")
    book, remainder = reference.split(" ", 1)
    return f"{GOSPELS[book]} {remainder}"


def text_html(value: str) -> str:
    """Escape conteúdo, preserve quebras e una as palavras de uma letra."""
    value = _text(value, "texto").replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(
        r"(?<!\w)([aàeéoAÀEÉO])[ \t]+(?=\S)",
        lambda match: match.group(1) + "\N{NO-BREAK SPACE}", value,
    )
    return escape(value).replace("\n", "<br>")
