"""Prepare flat, editable SVG assets for Canva without changing ``kit/``.

The exported logo viewBoxes describe the complete painted drawing.  This fixes
the small whitespace/clipping in the source horizontal and vertical viewBoxes;
the original bounds are returned as metadata for a fair rendering comparison.
"""

from __future__ import annotations

from collections import OrderedDict
from copy import deepcopy
import json
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET

from picosvg.svg import SVG


ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "kit"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

# These are the six documented usages, in the order given in the brief.
NICHES = (
    (680, 760, "capela", "capela", "fundo", "liturgico-roxo"),
    (340, 420, "santinho", "pergaminho", "papel", "ouro"),
    (600, 680, "coragem", "pergaminho", "fundo", "liturgico-roxo"),
    (640, 760, "toda-bela", "capela", "fundo", "liturgico-roxo"),
    (720, 900, "status-coragem", "pergaminho", "fundo", "liturgico-roxo"),
    (600, 700, "angelus", "capela", "fundo", "liturgico-roxo"),
)


def _number(value: float) -> str:
    text = f"{float(value):.6f}".rstrip("0").rstrip(".")
    return "0" if text in {"", "-0"} else text


def _rectangle(rect) -> list[float]:
    return [float(rect.x), float(rect.y), float(rect.w), float(rect.h)]


def _document(width: float, height: float, viewbox, groups) -> str:
    root = ET.Element(
        f"{{{NS}}}svg",
        {
            "version": "1.1",
            "width": _number(width),
            "height": _number(height),
            "viewBox": " ".join(_number(n) for n in viewbox),
        },
    )
    for color, paths in groups.items():
        group = ET.SubElement(root, f"{{{NS}}}g")
        for path in paths:
            attrs = {"fill": color, "d": path["d"]}
            if path.get("fill-rule", "nonzero") != "nonzero":
                attrs["fill-rule"] = path["fill-rule"]
            ET.SubElement(group, f"{{{NS}}}path", attrs)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(
        root, encoding="unicode"
    ) + "\n"


def _canonical_path(path) -> str:
    """picosvg outlines strokes, then exact Q-to-C elevation removes quadratics."""
    path = deepcopy(path)

    def replace_quadratic(subpath_start, current, command, args, *_):
        if command == "Q":
            qx, qy, x, y = args
            return (("C", (
                current.x + (qx - current.x) * 2 / 3,
                current.y + (qy - current.y) * 2 / 3,
                x + (qx - x) * 2 / 3,
                y + (qy - y) * 2 / 3,
                x,
                y,
            )),)
        if command not in {"M", "L", "H", "V", "C", "A", "Z"}:
            raise ValueError(f"Unsupported Canva path command: {command}")
        return ((command, args),)

    path.walk(replace_quadratic)
    return " ".join(
        command + (" " + " ".join(_number(n) for n in args) if args else "")
        for command, args in path
    )


def niche_svg(largura: int, altura: int, fundo: str, filete: str) -> str:
    """Mask a rectangular image to the exact, concentric CSS niche geometry.

    The niche begins at x=48 in this SVG.  The inset artwork begins at (64,16)
    and touches y=altura. The three-pixel frame has no bottom edge; its parapet
    extends 48px beyond either side and occupies y=altura through altura+3.
    """
    w, h = float(largura), float(altura)
    if w <= 32 or h < w / 2:
        raise ValueError("Niche requires width > 32 and height >= width / 2")
    radius = w / 2
    artwork_radius = (w - 32) / 2
    f = _number
    # evenodd explicitly subtracts the artwork arch from the full rectangle.
    corners = (
        f"M 48 0 H {f(w+48)} V {f(h)} H 48 Z "
        f"M 64 {f(h)} V {f(radius)} "
        f"A {f(artwork_radius)} {f(artwork_radius)} 0 0 1 {f(w+32)} {f(radius)} "
        f"V {f(h)} Z"
    )
    frame = (
        f"M 48 {f(h)} V {f(radius)} "
        f"A {f(radius)} {f(radius)} 0 0 1 {f(w+48)} {f(radius)} "
        f"V {f(h)} H {f(w+45)} V {f(radius)} "
        f"A {f(radius-3)} {f(radius-3)} 0 0 0 51 {f(radius)} "
        f"V {f(h)} Z "
        f"M 0 {f(h)} H {f(w+96)} V {f(h+3)} H 0 Z"
    )
    groups = OrderedDict()
    groups.setdefault(fundo.lower(), []).append({"d": corners, "fill-rule": "evenodd"})
    groups.setdefault(filete.lower(), []).append({"d": frame})
    return _document(w + 96, h + 3, [0, 0, w + 96, h + 3], groups)


def _colors() -> dict[str, dict[str, str]]:
    data = json.loads((KIT / "design-system/tokens.json").read_text())
    tokens = {item["name"]: item["value"] for item in data["color"]["tokens"]}

    def resolve(name, theme):
        value = tokens[name]
        if isinstance(value, str) and value.startswith("{"):
            return resolve(value[1:-1], theme)
        return value[theme].lower()

    return {
        theme["id"]: {name: resolve(name, theme["id"]) for name in tokens}
        for theme in data["color"]["themes"]
    }


def _export_logo(source: Path, destination: Path) -> dict:
    original = ET.parse(source).getroot()
    converted = SVG.parse(str(source)).topicosvg(ndigits=6)
    bounds = converted.bounding_box()
    if bounds is None:
        raise ValueError(f"Logo has no drawing: {source}")
    box = _rectangle(bounds)
    groups = OrderedDict()
    for shape in converted.shapes():
        if shape.opacity != 1 or shape.fill_opacity != 1:
            raise ValueError(f"Unexpected opacity in source logo: {source}")
        groups.setdefault(shape.fill.lower(), []).append(
            {"d": _canonical_path(shape), "fill-rule": shape.fill_rule}
        )
    if source.name.startswith("logo-horizontal"):
        height = 52.0
        usage = "assinatura horizontal: desenho justo com 52 px de altura"
    elif source.name.startswith("simbolo-reduzido"):
        height = 40.0
        usage = "assinatura curta: símbolo com 40 px de altura"
    else:
        height = float(original.attrib["height"])
        usage = "altura nominal do arquivo de origem; proporção ajustada ao desenho justo"
    width = height * bounds.w / bounds.h
    destination.write_text(_document(width, height, box, groups), encoding="utf-8")
    return {
        "source": str(source.relative_to(ROOT)),
        "file": str(destination.relative_to(ROOT)) if destination.is_relative_to(ROOT) else str(destination),
        "source_view_box": [float(n) for n in original.attrib["viewBox"].split()],
        "source_width": float(original.attrib["width"]),
        "source_height": float(original.attrib["height"]),
        "view_box": box,
        "drawing_bounds": box,
        "width": width,
        "height": height,
        "usage": usage,
        "comparison": "normalize original viewBox to drawing_bounds, then render both at equal dimensions",
    }


def _protection_area(logo_metadata: dict) -> dict:
    source = KIT / "logos/logo-horizontal-pergaminho.svg"
    original = ET.parse(source).getroot()
    symbol_group = original.find(f"{{{NS}}}g")
    scale_match = re.search(r"scale\(([-.\d]+)\)", symbol_group.attrib["transform"])
    if not scale_match:
        raise ValueError("Expected explicit uniform scale on horizontal logo symbol")
    scale = float(scale_match.group(1))
    # The crossbar is the horizontal path in the symbol, before the parapet.
    horizontal = []
    for path in symbol_group.findall(f"{{{NS}}}path"):
        match = re.fullmatch(r"M\s*([-.\d]+)\s+([-.\d]+)\s*H\s*([-.\d]+)", path.attrib["d"].strip())
        if match:
            x1, y, x2 = map(float, match.groups())
            horizontal.append((abs(x2 - x1), y))
    if len(horizontal) != 2:
        raise ValueError("Expected one symbol crossbar and one parapet")
    native_width, _ = min(horizontal, key=lambda item: item[1])
    source_width = native_width * scale
    return {
        "source": "kit/logos/logo-horizontal-pergaminho.svg",
        "crossbar_native_units": native_width,
        "symbol_scale": scale,
        "crossbar_svg_units": source_width,
        "source_logo_52px": source_width / logo_metadata["source_view_box"][3] * 52,
        "canva_tight_logo_52px": source_width / logo_metadata["drawing_bounds"][3] * 52,
        "rule": "comprimento da travessa da cruz em todos os lados do logo",
    }


def validate_svg(path: Path) -> dict:
    """Reject prohibited SVG constructs and noncanonical path commands."""
    text = path.read_text(encoding="utf-8")
    root = ET.fromstring(text)
    if root.attrib.get("version") != "1.1":
        raise ValueError(f"SVG must declare version 1.1: {path}")
    if path.stat().st_size >= 3_000_000:
        raise ValueError(f"SVG exceeds 3 MB: {path}")
    groups = {}
    for child in root:
        if child.tag != f"{{{NS}}}g":
            raise ValueError(f"SVG shapes must be grouped by color: {path}")
        for shape in child:
            if shape.tag != f"{{{NS}}}path" or "fill" not in shape.attrib:
                raise ValueError(f"Only explicitly filled paths are allowed: {path}")
            fill = shape.attrib["fill"]
            if fill in groups and groups[fill] is not child:
                raise ValueError(f"A color appears in multiple groups: {path}")
            groups[fill] = child
            commands = set(re.findall(r"[A-Za-z]", shape.attrib["d"]))
            if commands - set("MLHVCAZ"):
                raise ValueError(f"Forbidden path commands {commands}: {path}")
    for node in root.iter():
        local = node.tag.rsplit("}", 1)[-1]
        if local in {"text", "style", "linearGradient", "radialGradient"}:
            raise ValueError(f"Forbidden SVG element {local}: {path}")
        for attr in node.attrib:
            if attr in {"class", "style", "transform"} or attr.startswith("stroke"):
                raise ValueError(f"Forbidden SVG attribute {attr}: {path}")
    return {"file": str(path), "bytes": path.stat().st_size, "colors": list(groups)}


def export_elements(output_dir: Path) -> dict:
    """Export all Canva assets and return reproducible geometry/source metadata."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    palette = _colors()
    metadata = {"crosses": [], "niches": [], "logos": [], "fonts": [], "licenses": []}
    preview = (KIT / "design-system/componentes/Selo/preview.html").read_text()
    match = re.search(r'<svg\b[^>]*class="aqr-selo__cruz"[^>]*>\s*<path\b[^>]*d="([^"]+)"', preview)
    if not match:
        raise ValueError("Unable to find source seal cross path")
    for theme in ("pergaminho", "capela"):
        color = palette[theme]["liturgico-roxo"]
        source = SVG.fromstring(f'<svg xmlns="{NS}" viewBox="0 0 18 30"><path fill="{color}" d="{match.group(1)}"/></svg>')
        shapes = source.topicosvg(ndigits=6).shapes()
        path = output_dir / f"cruz-{theme}.svg"
        path.write_text(_document(18, 30, [0, 0, 18, 30], {color: [{"d": _canonical_path(p)} for p in shapes]}), encoding="utf-8")
        metadata["crosses"].append({"file": str(path), "theme": theme, "width": 18, "height": 30, "color_token": "liturgico-roxo", "color": color})
    for w, h, usage, theme, background_token, frame_token in NICHES:
        path = output_dir / f"nicho-{w}x{h}-{usage}.svg"
        background, frame = palette[theme][background_token], palette[theme][frame_token]
        path.write_text(niche_svg(w, h, background, frame), encoding="utf-8")
        metadata["niches"].append({
            "file": str(path), "usage": usage, "theme": theme,
            "niche_width": w, "niche_height": h, "width": w+96, "height": h+3,
            "position_offset_x": -48, "position_offset_y": 0,
            "outer_radius": w/2, "artwork_radius": (w-32)/2,
            "artwork_bounds": [64, 16, w-32, h-16],
            "background_token": background_token, "background": background,
            "frame_token": frame_token, "frame": frame, "frame_width": 3,
        })
    variants = output_dir / "variantes"
    variants.mkdir(exist_ok=True)
    green = variants / "nicho-680x760-capela-verde.svg"
    green.write_text(niche_svg(680, 760, palette["capela"]["fundo"], palette["capela"]["liturgico-verde"]), encoding="utf-8")
    metadata["green_test_niche"] = str(green)
    logos = output_dir / "logos"
    logos.mkdir(exist_ok=True)
    logo_sources = sorted((KIT / "logos").glob("*.svg"))
    if len(logo_sources) != 10 or not any(source.name == "logo-horizontal-sobre-cor.svg" for source in logo_sources):
        raise ValueError("O kit v2 precisa conter dez logos SVG, incluindo o horizontal sobre cor.")
    for source in logo_sources:
        metadata["logos"].append(_export_logo(source, logos / source.name))
    shutil.copy2(KIT / "logos/avatar-perfil.png", logos / "avatar-perfil.png")
    metadata["avatar_png"] = str(logos / "avatar-perfil.png")
    fonts = output_dir / "fontes"
    fonts.mkdir(exist_ok=True)
    for source in sorted((KIT / "fontes").glob("*.ttf")):
        shutil.copy2(source, fonts / source.name)
        metadata["fonts"].append(str(fonts / source.name))
    licenses = fonts / "licencas"
    licenses.mkdir(exist_ok=True)
    for source in sorted((KIT / "fontes/licencas").iterdir()):
        if source.is_file():
            shutil.copy2(source, licenses / source.name)
            metadata["licenses"].append(str(licenses / source.name))
    horizontal = next(item for item in metadata["logos"] if item["source"].endswith("logo-horizontal-pergaminho.svg"))
    metadata["protection_area"] = _protection_area(horizontal)
    metadata["validation"] = [validate_svg(path) for path in sorted(output_dir.rglob("*.svg"))]
    return metadata
