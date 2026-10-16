"""Verificações independentes dos arquivos entregues pelo gerador.

As funções apenas leem arquivos e retornam dicionários serializáveis em JSON.
``ok`` falso e ``errors`` descrevem um bloqueio de entrega; o chamador decide
onde salvar o relatório e como interromper a geração.
"""

from __future__ import annotations

from collections import defaultdict
from io import BytesIO
from math import cos, floor, isclose, isfinite, pi, sin
from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
import zipfile

from PIL import Image, ImageColor


_SVG_NS = "http://www.w3.org/2000/svg"
_SHAPES = {"path", "rect", "circle", "ellipse", "polygon", "polyline", "line"}
_ALLOWED_ELEMENTS = _SHAPES | {"svg", "g", "title", "desc", "metadata"}
_PATH_COMMANDS = frozenset("MLHVCAZmlhvcaz")
_MAX_SVG_BYTES = 3_000_000
_REQUIRED_PDF_FONTS = (
    "CormorantGaramond-SemiBold",
    "CormorantGaramond-MediumItalic",
    "Lato-Bold",
    "Lato-Regular",
)


def _local_name(name: str) -> str:
    return name.rsplit("}", 1)[-1]


def _number(value: str | None) -> float:
    """Accept SVG user units or explicit px, never physical or relative units."""
    if value is None:
        raise ValueError("medida ausente")
    value = value.strip()
    if value.endswith("px"):
        value = value[:-2]
    result = float(value)
    if not isfinite(result):
        raise ValueError("medida não finita")
    return result


def _canonical_color(value: str) -> str:
    try:
        rgb = ImageColor.getrgb(value)
        return "#" + "".join(f"{channel:02x}" for channel in rgb)
    except ValueError:
        return value.strip().lower()


def validate_svgs(elementos_dir: Path) -> dict:
    """Audita recursivamente SVGs Canva, incluindo geometria e grupos de cor.

    O limite é decimal (3.000.000 bytes), portanto também satisfaz o limite de
    3 MiB. Bounds são calculados dos preenchimentos pelo picosvg; uma folga
    máxima de 0,1 unidade acomoda o arredondamento decimal da exportação.
    """
    from picosvg.svg import SVG

    elementos_dir = Path(elementos_dir)
    files = sorted(elementos_dir.rglob("*.svg"))
    errors: list[str] = []
    records = []
    total_forbidden = {key: 0 for key in ("stroke", "text", "style", "class", "transform", "gradient", "Q", "T")}
    if not files:
        errors.append(f"Nenhum SVG encontrado em {elementos_dir}.")
    for path in files:
        relative = str(path.relative_to(elementos_dir))
        local_errors: list[str] = []
        record: dict = {"file": relative, "bytes": path.stat().st_size}
        forbidden_counts = {key: 0 for key in total_forbidden}
        if record["bytes"] >= _MAX_SVG_BYTES:
            local_errors.append("tamanho deve ser menor que 3 MB")
        try:
            contents = path.read_bytes()
            root = ET.fromstring(contents)
            if root.tag != f"{{{_SVG_NS}}}svg":
                local_errors.append("raiz deve ser svg no namespace SVG")
            if root.get("version") != "1.1":
                local_errors.append("version deve ser 1.1")
            try:
                width, height = _number(root.get("width")), _number(root.get("height"))
                if width <= 0 or height <= 0:
                    raise ValueError("width e height devem ser positivos")
                record["size"] = [width, height]
            except (ValueError, TypeError) as exc:
                local_errors.append(f"width/height inválidos: {exc}")
            try:
                viewbox = [float(value) for value in re.split(r"[\s,]+", root.get("viewBox", "").strip())]
                if len(viewbox) != 4 or not all(isfinite(value) for value in viewbox) or min(viewbox[2:]) <= 0:
                    raise ValueError("esperados quatro números finitos, largura e altura positivas")
                record["viewBox"] = viewbox
            except ValueError as exc:
                viewbox = None
                local_errors.append(f"viewBox inválido: {exc}")

            parents = {child: parent for parent in root.iter() for child in parent}
            color_groups: dict[str, set] = defaultdict(set)
            group_colors: dict[ET.Element, set[str]] = defaultdict(set)
            commands: set[str] = set()
            shapes = 0
            for element in root.iter():
                tag = _local_name(element.tag)
                if tag in {"text", "style"}:
                    forbidden_counts[tag] += 1
                if "gradient" in tag.lower():
                    forbidden_counts["gradient"] += 1
                if tag not in _ALLOWED_ELEMENTS:
                    local_errors.append(f"elemento não permitido: <{tag}>")
                for raw_name, value in element.attrib.items():
                    name = _local_name(raw_name)
                    if "stroke" in name.lower():
                        forbidden_counts["stroke"] += 1
                        local_errors.append(f"atributo de traço não permitido: {name}")
                    if name.lower() in {"style", "class", "transform"}:
                        forbidden_counts[name.lower()] += 1
                        local_errors.append(f"atributo não permitido: {name}")
                    if name.lower().startswith("on"):
                        local_errors.append(f"atributo de evento não permitido: {name}")
                    if "url(" in value.lower():
                        local_errors.append(f"referência CSS não permitida em {name}")
                if tag not in _SHAPES:
                    continue
                shapes += 1
                fill = element.get("fill")
                if not fill:
                    local_errors.append(f"<{tag}> sem fill explícito")
                elif fill.lower() in {"none", "currentcolor", "inherit", "context-fill", "context-stroke"} or "var(" in fill:
                    local_errors.append(f"<{tag}> sem cor concreta no fill: {fill}")
                else:
                    color = _canonical_color(fill)
                    parent = parents.get(element)
                    if parent is None or _local_name(parent.tag) != "g":
                        local_errors.append(f"forma {tag} ({color}) deve pertencer a um <g> de cor")
                    else:
                        color_groups[color].add(parent)
                        group_colors[parent].add(color)
                if tag == "path":
                    path_data = element.get("d", "")
                    # Exponents are numbers, not the e/E path command.
                    letters = set(re.findall(r"[A-Za-z]", re.sub(r"(?<=[\d.])[eE][+-]?\d+", "", path_data)))
                    for command in ("Q", "T"):
                        forbidden_counts[command] += sum(letter.upper() == command for letter in re.findall(r"[A-Za-z]", path_data))
                    commands.update(letters)
                    forbidden = sorted(letters - _PATH_COMMANDS)
                    if forbidden:
                        local_errors.append("comandos de path não permitidos: " + ", ".join(forbidden))
                    if not path_data.strip():
                        local_errors.append("path vazio")
            for color, groups in color_groups.items():
                if len(groups) != 1:
                    local_errors.append(f"cor {color} dividida em {len(groups)} grupos")
            for colors in group_colors.values():
                if len(colors) != 1:
                    local_errors.append("um grupo contém formas de cores diferentes: " + ", ".join(sorted(colors)))
            if not shapes:
                local_errors.append("SVG sem formas")
            record.update(shapes=shapes, colors=sorted(color_groups), path_commands=sorted(commands))

            try:
                svg = SVG.fromstring(contents.decode("utf-8"))
                bounds = svg.bounding_box()
                if bounds is None:
                    local_errors.append("não foi possível obter os bounds das formas")
                else:
                    actual = [bounds.x, bounds.y, bounds.w, bounds.h]
                    record["drawing_bounds"] = actual
                    if viewbox is not None and any(abs(a - b) > 0.1 for a, b in zip(actual, viewbox)):
                        local_errors.append(f"viewBox não justo: {viewbox}; desenho {actual}")
            except Exception as exc:
                local_errors.append(f"picosvg não conseguiu conferir os bounds: {type(exc).__name__}: {exc}")
        except (ET.ParseError, OSError, UnicodeError) as exc:
            local_errors.append(f"SVG ilegível: {exc}")
        record["ok"] = not local_errors
        record["forbidden_counts"] = forbidden_counts
        for key, count in forbidden_counts.items():
            total_forbidden[key] += count
        record["errors"] = list(dict.fromkeys(local_errors))
        records.append(record)
        errors.extend(f"{relative}: {error}" for error in record["errors"])
    return {"ok": not errors, "count": len(records), "forbidden_counts": total_forbidden, "files": records, "errors": errors}


def _font_name(name: str) -> str:
    return re.sub(r"^[A-Z]{6}\+", "", name)


def validate_pdf(path: Path) -> dict:
    """Confere páginas, texto extraível e os próprios programas TTF embutidos."""
    import fitz
    from fontTools.ttLib import TTFont

    path = Path(path)
    errors: list[str] = []
    pages = []
    fonts: dict[int, dict] = {}
    extracted = ""
    try:
        with fitz.open(path) as document:
            if document.page_count != 3:
                errors.append(f"PDF tem {document.page_count} páginas; esperado 3.")
            for number, page in enumerate(document, 1):
                width, height = page.rect.width, page.rect.height
                text = page.get_text("text")
                extracted += text + "\n"
                normalized_text = " ".join(text.split())
                pages.append({"page": number, "width_pt": width, "height_pt": height, "text_characters": len(text), "evangelho_do_dia": "Evangelho do Dia" in normalized_text})
                if not (isclose(width, 810, abs_tol=0.01) and isclose(height, 1012.5, abs_tol=0.01)):
                    errors.append(f"Página {number}: {width} × {height} pt; esperado 810 × 1012,5 pt.")
                if "Evangelho do Dia" not in normalized_text:
                    errors.append(f"Página {number}: selo não aparece como texto extraível.")
                expected_text = "Nem um pardal é esquecido por Deus" if number in {1, 2} else "Se Deus conta até os cabelos da minha cabeça, do que eu ainda tenho medo?"
                if expected_text not in normalized_text:
                    errors.append(f"Página {number}: título/citação não aparece como texto extraível.")
                for info in page.get_fonts(full=True):
                    xref, extension, font_type, basefont = info[:4]
                    if xref in fonts:
                        continue
                    record = {"name": _font_name(basefont), "pdf_name": basefont, "type": font_type, "extension": extension, "embedded": False, "truetype": False, "internal_postscript_names": []}
                    try:
                        _, ext, _, data = document.extract_font(xref)
                        record["embedded"] = bool(data)
                        record["bytes"] = len(data)
                        record["truetype"] = ext.lower() in {"ttf", "ttc"} and data[:4] in {b"\x00\x01\x00\x00", b"true", b"ttcf"}
                        if data:
                            with TTFont(BytesIO(data), lazy=True) as font:
                                record["internal_postscript_names"] = sorted({_font_name(name.toUnicode()) for name in font["name"].names if name.nameID == 6})
                    except Exception as exc:
                        errors.append(f"Não foi possível conferir a fonte {basefont}: {exc}")
                    if not record["embedded"]:
                        errors.append(f"Fonte não embutida: {basefont}.")
                    if not record["truetype"]:
                        errors.append(f"Fonte não é um TTF embutido: {basefont} ({font_type}/{extension}).")
                    if record["embedded"] and record["name"] not in record["internal_postscript_names"]:
                        errors.append(f"Nome PDF {basefont} não corresponde ao nome PostScript do TTF: {record['internal_postscript_names']}.")
                    fonts[xref] = record
    except Exception as exc:
        errors.append(f"PDF ilegível: {type(exc).__name__}: {exc}")
    names = {record["name"] for record in fonts.values()}
    for expected in _REQUIRED_PDF_FONTS:
        if expected not in names:
            errors.append(f"Fonte obrigatória ausente no PDF: {expected}.")
    contains_title = "Evangelho do Dia" in " ".join(extracted.split())
    if not contains_title:
        errors.append('Texto extraído não contém "Evangelho do Dia".')
    # Poppler oferece uma segunda leitura independente do dicionário de fontes.
    pdffonts_output = None
    if shutil.which("pdffonts"):
        result = subprocess.run(["pdffonts", str(path)], capture_output=True, text=True, check=False)
        if result.returncode:
            errors.append(f"pdffonts falhou: {result.stderr.strip()}")
        else:
            pdffonts_output = result.stdout.strip()
            for line in result.stdout.splitlines()[2:]:
                match = re.search(r"\s(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", line)
                if match and match.group(1) != "yes":
                    errors.append("pdffonts encontrou fonte não embutida: " + line.strip())
    return {"ok": not errors, "file": str(path), "page_count": len(pages), "pages": pages, "fonts": list(fonts.values()), "font_count": len(fonts), "required_fonts": list(_REQUIRED_PDF_FONTS), "contains_evangelho_do_dia": contains_title, "pdffonts": pdffonts_output, "errors": errors}


def validate_pngs(expected: dict[Path | str, tuple[int, int]]) -> dict:
    """Lê cada PNG inteiro e compara sua dimensão ao contrato do chamador."""
    errors: list[str] = []
    records = []
    if not expected:
        errors.append("Nenhum PNG foi informado para validação.")
    for filename, dimensions in expected.items():
        path = Path(filename)
        record = {"file": str(path), "expected": list(dimensions), "ok": False}
        try:
            with Image.open(path) as image:
                image.load()
                record["actual"] = list(image.size)
                record["format"] = image.format
                record["ok"] = image.format == "PNG" and image.size == tuple(dimensions)
                if not record["ok"]:
                    errors.append(f"{path}: {image.format} {image.size}; esperado PNG {dimensions}.")
        except (OSError, ValueError) as exc:
            errors.append(f"{path}: {exc}")
        records.append(record)
    return {"ok": not errors, "count": len(records), "files": records, "errors": errors}


def validate_kit(project: Path) -> dict:
    """Confere o contrato v2 e compara kit/ byte a byte com o ZIP do commit."""
    project = Path(project)
    errors: list[str] = []
    missing, modified, extra = [], [], []
    logo_count = 0
    archive_name = "kit-arte-que-reza.zip"
    try:
        result = subprocess.run(["git", "show", f"HEAD:{archive_name}"], cwd=project, capture_output=True, check=False)
        if result.returncode:
            raise ValueError("não foi possível ler o ZIP rastreado no commit atual")
        baseline: dict[str, bytes] = {}
        with zipfile.ZipFile(BytesIO(result.stdout)) as archive:
            for info in archive.infolist():
                if info.is_dir() or not info.filename.startswith("kit/"):
                    continue
                relative = info.filename[len("kit/"):]
                if not relative or ".." in Path(relative).parts:
                    raise ValueError("caminho inválido no ZIP")
                baseline[relative] = archive.read(info)
        if not baseline:
            raise ValueError("o ZIP rastreado não contém kit/")
        if len(baseline) != 42:
            errors.append(f"Kit tem {len(baseline)} arquivos; a versão 2 exige 42.")
        logo_names = [name for name in baseline if Path(name).parent == Path("logos") and Path(name).suffix.lower() in {".svg", ".png"}]
        logo_count = len(logo_names)
        if logo_count != 11:
            errors.append(f"Kit tem {logo_count} ativos de logo; a versão 2 exige 11.")
        if "logos/logo-horizontal-sobre-cor.svg" not in baseline:
            errors.append("Logo horizontal sobre cor da versão 2 ausente.")
        if not baseline.get("LEIA-ME.md", b"").decode("utf-8").startswith("# Kit Arte que Reza · versão 2"):
            errors.append("LEIA-ME.md não identifica o kit como versão 2.")
        present = {str(path.relative_to(project / "kit")): path for path in (project / "kit").rglob("*") if path.is_file()}
        for name, data in baseline.items():
            if name not in present:
                missing.append(name)
            elif present[name].read_bytes() != data:
                modified.append(name)
        extra = sorted(set(present) - set(baseline))
        if missing:
            errors.append(f"{len(missing)} arquivo(s) do kit ausente(s).")
        if modified:
            errors.append(f"{len(modified)} arquivo(s) do kit alterado(s).")
        if extra:
            errors.append(f"{len(extra)} arquivo(s) extra(s) em kit/.")
        count = len(baseline)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        errors.append(f"Não foi possível conferir kit/: {exc}.")
        count = 0
    return {"ok": not errors, "version": 2, "baseline": f"git HEAD:{archive_name}", "count": count, "logo_count": logo_count, "missing": sorted(missing), "modified": sorted(modified), "extra": extra, "errors": errors}


def validate_niche_pixels(image: Path, boxes: list[dict]) -> dict:
    """Confere máscara, filete, parapeito e arco externo nos pixels renderizados.

    Cada caixa fornece x/y/width/height em pixels do PNG, ``background`` e
    ``filete`` (ou ``filet``) como cor CSS. ``name`` é opcional. Além dos pontos
    cardeais, três amostras no semicírculo verificam raio W/2 na imagem real.
    Não usa apenas o valor declarado no CSS para aprovar a geometria.
    """
    errors: list[str] = []
    records = []
    try:
        with Image.open(image) as source:
            pixels = source.convert("RGB")
            pixels.load()
        for index, box in enumerate(boxes):
            name = str(box.get("name", f"nicho-{index + 1}"))
            local_errors = []
            samples = []
            try:
                x, y, width, height = (float(box[key]) for key in ("x", "y", "width", "height"))
                if width <= 32 or height <= width / 2:
                    raise ValueError("dimensões incompatíveis com um nicho em arco pleno")
                background = ImageColor.getrgb(box["background"])[:3]
                filete = ImageColor.getrgb(box.get("filete", box.get("filet")))[:3]
                radius = width / 2
                if "outer_radius" in box and not isclose(float(box["outer_radius"]), radius, abs_tol=0.1):
                    local_errors.append(f"raio externo declarado {box['outer_radius']}; esperado {radius}")

                def sample(label: str, sx: float, sy: float, color: tuple, tolerance: int = 3):
                    point = (floor(sx), floor(sy))
                    item = {"name": label, "xy": list(point), "expected_rgb": list(color)}
                    if not (0 <= point[0] < pixels.width and 0 <= point[1] < pixels.height):
                        item["ok"] = False
                        local_errors.append(f"{label}: amostra fora da imagem em {point}")
                    else:
                        actual = pixels.getpixel(point)
                        delta = max(abs(a - b) for a, b in zip(actual, color))
                        item.update(actual_rgb=list(actual), max_channel_delta=delta, ok=delta <= tolerance)
                        if not item["ok"]:
                            local_errors.append(f"{label} em {point}: pixel {actual}; esperado {color} (tolerância {tolerance})")
                    samples.append(item)

                sample("canto da obra fora do arco", x + 16.5, y + 16.5, background)
                sample("topo do filete", x + width / 2, y + 1, filete)
                sample("lateral do filete", x + 1, y + radius + 20, filete)
                sample("parapeito", x - 20, y + height + 1, filete)
                for degrees in (-135, -90, -45):
                    angle = degrees * pi / 180
                    sample(f"arco externo W/2: {degrees} graus", x + radius + (radius - 1.5) * cos(angle), y + radius + (radius - 1.5) * sin(angle), filete)
                    sample(f"fora do arco W/2: {degrees} graus", x + radius + (radius + 4) * cos(angle), y + radius + (radius + 4) * sin(angle), background)
                records.append({"name": name, "ok": not local_errors, "outer_radius": radius, "samples": samples, "errors": local_errors})
            except (KeyError, ValueError, TypeError) as exc:
                local_errors.append(f"metadados inválidos: {exc}")
                records.append({"name": name, "ok": False, "samples": samples, "errors": local_errors})
            errors.extend(f"{name}: {message}" for message in local_errors)
        if not boxes:
            errors.append("Nenhum nicho foi informado para conferir os pixels.")
    except (OSError, ValueError) as exc:
        errors.append(f"Não foi possível ler {image}: {exc}")
    return {"ok": not errors, "file": str(image), "count": len(records), "niches": records, "tolerance_rgb": 3, "errors": errors}
