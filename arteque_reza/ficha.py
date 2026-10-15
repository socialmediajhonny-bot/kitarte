"""Medições do DOM renderizado e ficha técnica em tabelas.

As coordenadas são relativas à arte, nunca à janela do navegador. Os
pseudo-elementos não têm ``getBoundingClientRect``: seus retângulos são
calculados a partir do retângulo medido do bloco e dos valores CSS resolvidos.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import unquote, urlparse
import xml.etree.ElementTree as ET

from .base import PROJECT, await_fonts, color, load_tokens


_MEASURE_JS = r"""tokenNames => {
  const article = document.querySelector('.aqr-post');
  if (!article) throw new Error('A arte .aqr-post não foi encontrada.');
  const rootRect = article.getBoundingClientRect();
  const rootStyle = getComputedStyle(article);
  const round = value => Math.round(value * 1000000) / 1000000;
  const number = value => Number.isFinite(parseFloat(value)) ? parseFloat(value) : null;
  const hex = value => {
    if (!value || value === 'none' || value === 'transparent') return null;
    value = value.trim().toLowerCase();
    if (/^#[0-9a-f]{6}$/.test(value)) return value;
    if (/^#[0-9a-f]{3}$/.test(value)) return '#' + [...value.slice(1)].map(c => c+c).join('');
    const values = value.match(/^rgba?\(([^)]+)\)$/);
    if (!values) return value;
    const channels = values[1].split(/[, /]+/).map(Number);
    if (channels.length > 3 && channels[3] === 0) return null;
    const result = '#' + channels.slice(0,3).map(n => Math.round(n).toString(16).padStart(2,'0')).join('');
    return channels.length > 3 && channels[3] < 1 ? result + Math.round(channels[3]*255).toString(16).padStart(2,'0') : result;
  };
  const palette = Object.fromEntries(tokenNames.map(token => [token, hex(rootStyle.getPropertyValue('--'+token))]));
  const colorToken = (actual, hint, isColorCard) => {
    if (!actual) return null;
    if (isColorCard && ['tinta','tinta-suave','cor-do-dia'].includes(hint)
        && actual === palette['sobre-cor']) return 'sobre-cor';
    if (hint && actual === palette[hint]) return hint;
    return tokenNames.find(token => palette[token] === actual) || null;
  };
  const rect = value => ({x:round(value.left-rootRect.left), y:round(value.top-rootRect.top),
    width:round(value.width), height:round(value.height)});
  const actualRadius = (style, width, height) => {
    const pair = (value, horizontal, vertical) => {
      const pieces = value.trim().split(/\s+/);
      const resolve = (part, extent) => part.endsWith('%') ? parseFloat(part)*extent/100 : parseFloat(part);
      return [resolve(pieces[0],horizontal), resolve(pieces[1] || pieces[0],vertical)];
    };
    const [tl,tr,br,bl] = [style.borderTopLeftRadius,style.borderTopRightRadius,
      style.borderBottomRightRadius,style.borderBottomLeftRadius].map(value => pair(value,width,height));
    const ratio = (size,sum) => sum ? size/sum : 1;
    const scale = Math.min(1, ratio(width,tl[0]+tr[0]),ratio(width,bl[0]+br[0]),
      ratio(height,tl[1]+bl[1]),ratio(height,tr[1]+br[1]));
    return {top_left:tl.map(n=>round(n*scale)),top_right:tr.map(n=>round(n*scale)),
      bottom_right:br.map(n=>round(n*scale)),bottom_left:bl.map(n=>round(n*scale))};
  };
  const items = [];
  const background = hex(rootStyle.backgroundColor);
  items.push({element:'arte-fundo', kind:'background', ...rect(rootRect),
    text:null, arquivo:null, token:article.classList.contains('aqr-post--cor')?'cor-do-dia':'fundo',
    hex:background, background_hex:background, measurement:'getBoundingClientRect'});
  for (const node of article.querySelectorAll('[data-element]')) {
    const bounds = node.getBoundingClientRect(), style = getComputedStyle(node);
    const ownText = [...node.childNodes].some(child => child.nodeType === Node.TEXT_NODE && child.textContent.trim());
    const isText = ownText && !['svg','path'].includes(node.tagName.toLowerCase());
    const isImage = node.tagName.toLowerCase() === 'img';
    const isSVG = node.tagName.toLowerCase() === 'svg';
    const background = hex(style.backgroundColor);
    let actual = isText || isSVG ? hex(style.color) : background;
    if (isSVG) {
      const shape = node.querySelector('path,rect,circle,ellipse,polygon,polyline,line');
      const fill = shape ? getComputedStyle(shape).fill : '';
      if (fill && fill !== 'none') actual = hex(fill);
    }
    const hint = node.dataset.corToken || null;
    const isColorCard = Boolean(node.closest('.aqr-post--cor'));
    const size = isText ? number(style.fontSize) : null;
    const leading = isText ? number(style.lineHeight) : null;
    const tracking = isText ? (style.letterSpacing === 'normal' ? 0 : number(style.letterSpacing)) : null;
    const item = {
      element:node.dataset.element, kind:isText?'text':isImage?'image':isSVG?'svg':'container',
      ...rect(bounds), text:isText?(node.innerText || node.textContent).replace(/\s+/g,' ').trim():null,
      arquivo:node.dataset.arquivo || (isImage ? new URL(node.currentSrc || node.src,location.href).pathname.replace(/^\//,'') : null),
      source:isImage?(node.currentSrc || node.src):null,
      font_family:isText?style.fontFamily.split(',')[0].trim().replace(/^["']|["']$/g,''):null,
      font_weight:isText?style.fontWeight:null, font_style:isText?style.fontStyle:null,
      font_size_px:size, line_height_px:leading,
      line_height_multiple:size && leading !== null?round(leading/size):null,
      letter_spacing_px:tracking, letter_spacing_em:size && tracking !== null?round(tracking/size):null,
      letter_spacing_thousandths_em:size && tracking !== null?round(1000*tracking/size):null,
      token:colorToken(actual,hint,isColorCard), hex:actual, background_hex:background,
      measurement:'getBoundingClientRect',
      border_radius_px:actualRadius(style,bounds.width,bounds.height),
    };
    if (isImage) {
      item.source_width_px=node.naturalWidth; item.source_height_px=node.naturalHeight;
      item.object_fit=style.objectFit; item.object_position=style.objectPosition;
    }
    items.push(item);
    if (!node.matches('.aqr-nicho, .aqr-ornamento')) continue;
    for (const pseudo of ['::before','::after']) {
      const resolved = getComputedStyle(node,pseudo);
      if (resolved.content === 'none' || resolved.content === 'normal' || resolved.display === 'none') continue;
      // The nicho's containing block is its padding box. Used CSS width/height
      // include the border because the kit sets box-sizing:border-box.
      let width=number(resolved.width), height=number(resolved.height);
      let left=number(resolved.left), top=number(resolved.top);
      const right=number(resolved.right), bottom=number(resolved.bottom);
      const cbWidth=node.clientWidth, cbHeight=node.clientHeight;
      if (width === null && left !== null && right !== null) width=cbWidth-left-right;
      if (height === null && top !== null && bottom !== null) height=cbHeight-top-bottom;
      if (node.matches('.aqr-ornamento')) {
        // These pseudos are the two flex items around the measured central SVG.
        const cross=node.querySelector('svg');
        if (!cross) continue;
        const crossBounds=cross.getBoundingClientRect();
        const gap=number(style.columnGap) || 0;
        left=pseudo==='::before'?crossBounds.left-bounds.left-gap-width:crossBounds.right-bounds.left+gap;
        top=(bounds.height-height)/2;
      } else {
        if (left === null && right !== null && width !== null) left=cbWidth-right-width;
        if (top === null && bottom !== null && height !== null) top=cbHeight-bottom-height;
      }
      if ([left,top,width,height].some(value => value === null || !Number.isFinite(value)))
        throw new Error('Pseudo-elemento sem geometria resolvida: '+node.dataset.element+pseudo);
      const stroke=hex(resolved.borderTopColor), fill=hex(resolved.backgroundColor);
      const actual=fill || (number(resolved.borderTopWidth)>0 ? stroke : null);
      const token=style.getPropertyValue('--moldura').trim() ?
        tokenNames.find(name=>palette[name]===actual) : 'cor-do-dia';
      const name=node.matches('.aqr-nicho') ?
        (pseudo==='::before'?'nicho-filete':'nicho-parapeito') :
        (pseudo==='::before'?'ornamento-filete-esquerdo':'ornamento-filete-direito');
      items.push({element:name,kind:'pseudo',pseudo,host:node.dataset.element,
        x:round(bounds.left-rootRect.left+node.clientLeft+left),
        y:round(bounds.top-rootRect.top+node.clientTop+top),width:round(width),height:round(height),
        text:null,arquivo:null,token:colorToken(actual,token,isColorCard),hex:actual,
        background_hex:fill,border_top_px:number(resolved.borderTopWidth),
        border_right_px:number(resolved.borderRightWidth),border_bottom_px:number(resolved.borderBottomWidth),
        border_left_px:number(resolved.borderLeftWidth),border_radius_px:actualRadius(resolved,width,height),
        measurement:'getComputedStyle('+pseudo+') + host.getBoundingClientRect',
      });
    }
  }
  return {theme:article.dataset.theme,width:round(rootRect.width),height:round(rootRect.height),
    color_card:article.classList.contains('aqr-post--cor'),palette,
    cor_do_dia_css:article.style.getPropertyValue('--cor-do-dia').trim(),elements:items};
}"""


def _asset_path(source: str | None) -> Path | None:
    """Mapeie apenas arquivos no checkout; nunca busque recursos externos."""
    if not source:
        return None
    parsed = urlparse(source)
    if parsed.scheme not in {"", "http", "https"}:
        return None
    if parsed.netloc and parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
        return None
    path = (PROJECT / unquote(parsed.path).lstrip("/")).resolve()
    try:
        path.relative_to(PROJECT)
    except ValueError:
        return None
    return path if path.is_file() else None


def _svg_colors(path: Path) -> list[str]:
    """Cores pintadas, inclusive traços herdados dos logos originais."""
    from PIL import ImageColor

    root = ET.fromstring(path.read_bytes())
    result: set[str] = set()
    shapes = {"path", "rect", "circle", "ellipse", "polygon", "polyline", "line"}

    def walk(node: ET.Element, inherited: dict[str, str], opacity: float = 1) -> None:
        current = dict(inherited)
        for attribute in ("fill", "stroke", "color", "fill-opacity", "stroke-opacity", "display", "visibility"):
            if attribute in node.attrib:
                current[attribute] = node.attrib[attribute]
        for declaration in node.get("style", "").split(";"):
            if ":" in declaration:
                key, value = declaration.split(":", 1)
                current[key.strip()] = value.strip()
        opacity *= float(node.get("opacity", "1"))
        if current.get("display") == "none" or current.get("visibility") == "hidden" or opacity == 0:
            return
        if node.tag.rsplit("}", 1)[-1] in shapes:
            for paint in ("fill", "stroke"):
                value = current.get(paint, "#000000" if paint == "fill" else "none")
                if value == "currentColor":
                    value = current.get("color", "#000000")
                if value == "none" or float(current.get(paint + "-opacity", "1")) == 0:
                    continue
                channels = ImageColor.getrgb(value)
                result.add("#" + "".join(f"{channel:02x}" for channel in channels[:3]))
        for child in node:
            walk(child, current, opacity)

    walk(root, {})
    return sorted(result)


def measure_page(page: Any, page_number: int, name: str) -> dict[str, Any]:
    """Meça elementos marcados depois de confirmar todas as fontes locais."""
    await_fonts(page)
    tokens = load_tokens()
    token_names = [item["name"] for item in tokens["color"]["tokens"]]
    result = page.evaluate(_MEASURE_JS, token_names)
    result.update({"page_n": page_number, "name": name})
    for element in result["elements"]:
        if element["kind"] != "image":
            continue
        path = _asset_path(element.get("source"))
        if path is None or path.suffix.lower() != ".svg":
            continue
        asset_theme = re.search(r"-(pergaminho|capela)\.svg$", path.name)
        theme = asset_theme.group(1) if asset_theme else result["theme"]
        records = []
        for value in _svg_colors(path):
            candidates = [token for token in token_names if color(token, theme).lower() == value]
            records.append({"hex": value, "token": candidates[0] if candidates else None, "theme": theme})
        element["svg_colors"] = records
        # An SVG image can paint more than one colour; inherited CSS color is
        # unrelated to its internal artwork.
        element["token"] = None
        element["hex"] = None
        element["source"] = path.relative_to(PROJECT).as_posix()
    return result


def _palette_rows(colors: dict[str, Any] | None) -> list[dict[str, str]]:
    section: Any = colors or load_tokens()["color"]
    if "color" in section:
        section = section["color"]
    if "tokens" in section:
        values = {item["name"]: item["value"] for item in section["tokens"]}
    elif {"pergaminho", "capela"}.issubset(section):
        names = dict.fromkeys([*section["pergaminho"], *section["capela"]])
        values = {name: {theme: section[theme][name] for theme in ("pergaminho", "capela")} for name in names}
    else:
        values = section

    def resolve(name: str, theme: str, visited: frozenset[str] = frozenset()) -> str:
        if name in visited:
            raise ValueError(f"Alias circular na ficha: {name}")
        value = values[name]
        if isinstance(value, dict):
            value = value[theme]
        if value.startswith("{") and value.endswith("}"):
            return resolve(value[1:-1], theme, visited | {name})
        return value.lower()

    rows = []
    for name, value in values.items():
        alias = value[1:-1] if isinstance(value, str) and value.startswith("{") and value.endswith("}") else "—"
        rows.append({"token": name, "pergaminho": resolve(name, "pergaminho"), "capela": resolve(name, "capela"), "alias": alias})
    return rows


def _value(value: Any) -> str:
    if value is None or value == "":
        return "—"
    if isinstance(value, float):
        value = int(value) if value.is_integer() else f"{value:.6f}".rstrip("0").rstrip(".")
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def _paint(element: dict[str, Any]) -> str:
    if element.get("svg_colors"):
        return "; ".join(
            f"{item.get('token') or '—'} [{item['theme']}] / {item['hex']}"
            for item in element["svg_colors"]
        )
    return f"{element.get('token') or '—'} / {element['hex']}" if element.get("hex") else "—"


def _table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    return ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |",
            *("| " + " | ".join(_value(value) for value in row) + " |" for row in rows)]


def write_ficha(output: Path, pages: list[dict[str, Any]], colors: dict[str, Any] | None = None) -> Path:
    """Salve somente valores e tabelas de geometria, tipografia e paleta."""
    output = Path(output)
    if output.suffix.lower() != ".md":
        output = output / "FICHA.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Ficha técnica", ""]
    lines += _table(["Token", "Pergaminho", "Capela", "Alias"], [
        [row["token"], row["pergaminho"], row["capela"], row["alias"]] for row in _palette_rows(colors)
    ])
    for page in pages:
        lines += ["", f"## Página {page['page_n']} · {page['name']}", ""]
        lines += _table(["Tema", "Largura (px)", "Altura (px)", "Cor do dia"], [[
            page["theme"], page["width"], page["height"], page["cor_do_dia_css"]
        ]])
        lines.append("")
        rows = []
        for item in page["elements"]:
            font = " / ".join(str(item[key]) for key in ("font_family", "font_weight", "font_style") if item.get(key)) or None
            rows.append([item["element"], item.get("arquivo"), item.get("text"), font,
                         item["x"], item["y"], item["width"], item["height"], item.get("font_size_px"),
                         item.get("line_height_px"), item.get("line_height_multiple"),
                         item.get("letter_spacing_em"), item.get("letter_spacing_thousandths_em"), _paint(item)])
        lines += _table(["Elemento", "Arquivo", "Texto", "Fonte / peso / estilo", "x (px)", "y (px)",
                         "Largura (px)", "Altura (px)", "Texto (px)", "Entrelinha (px)", "Entrelinha (×)",
                         "Letras (em)", "Letras (‰ de em)", "Cor: token / hex"], rows)
        details = []
        for item in page["elements"]:
            for key, label in (("background_hex", "Fundo"), ("source", "Origem"),
                               ("source_width_px", "Imagem: largura original (px)"),
                               ("source_height_px", "Imagem: altura original (px)"),
                               ("object_fit", "object-fit"), ("object_position", "object-position")):
                if item.get(key) is not None:
                    details.append([item["element"], label, item[key]])
            radii = item.get("border_radius_px")
            if radii and any(any(pair) for pair in radii.values()):
                for corner, value in radii.items():
                    details.append([item["element"], "Raio " + corner + " (rx, ry; px)", value])
            if item["kind"] == "pseudo":
                details.append([item["element"], "Medição", item["measurement"]])
                for side in ("top", "right", "bottom", "left"):
                    details.append([item["element"], f"Borda {side} (px)", item[f"border_{side}_px"]])
        if details:
            lines += ["", *_table(["Elemento", "Propriedade", "Valor"], details)]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output
