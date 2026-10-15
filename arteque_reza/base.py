"""Base reutilizável do gerador, fiel aos tokens e à composição do kit.

As funções de composição devolvem HTML. A renderização usa a API síncrona do
Playwright e recusa produzir arquivos se qualquer variante local estiver ausente.
"""

from __future__ import annotations

from html import escape
from io import BytesIO
import json
import os
from pathlib import Path
import re
from typing import Any
from urllib.parse import quote, urlparse


PROJECT = Path(__file__).resolve().parents[1]
KIT = PROJECT / "kit"
CRUZ_PATH = "M6.8 0h4.4v8.2H18v3.6h-6.8V30H6.8V11.8H0V8.2h6.8z"


def resource_url(path: Path | str) -> str:
    """URL local relativa à raiz do projeto servido por HTTP no loopback."""
    path = Path(path)
    if not path.is_absolute():
        path = PROJECT / path
    return "/" + quote(path.resolve().relative_to(PROJECT).as_posix(), safe="/")


def load_tokens() -> dict[str, Any]:
    """Leia a fonte da verdade sem alterar ou normalizar seus valores."""
    return json.loads((KIT / "design-system" / "tokens.json").read_text(encoding="utf-8"))


def _token_map(section: str) -> dict[str, Any]:
    return {item["name"]: item["value"] for item in load_tokens()[section]["tokens"]}


def _theme(tema: str) -> str:
    if tema not in {item["id"] for item in load_tokens()["color"]["themes"]}:
        raise ValueError(f"Tema desconhecido: {tema}")
    return tema


def color(token: str, tema: str = "pergaminho") -> str:
    """Resolva aliases de cor (inclusive aliases encadeados) para um hex."""
    _theme(tema)
    values = _token_map("color")
    name = token.strip().removeprefix("--")
    if name.startswith("{") and name.endswith("}"):
        name = name[1:-1]
    visited: set[str] = set()
    while True:
        if name in visited:
            raise ValueError(f"Alias circular de cor: {name}")
        visited.add(name)
        value = values[name]
        if isinstance(value, dict):
            value = value[tema]
        if value.startswith("{") and value.endswith("}"):
            name = value[1:-1]
            continue
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
            raise ValueError(f"Cor inválida no kit: {name} = {value!r}")
        return value


def dimension(token: str) -> int | float:
    """Leia uma medida em px dos espaços, raios ou formatos."""
    for section in ("spacing", "radius", "formato"):
        values = _token_map(section)
        if token in values:
            value = values[token]
            if not re.fullmatch(r"\d+(?:\.\d+)?px", value):
                raise ValueError(f"Medida não expressa em px: {token}")
            number = float(value[:-2])
            return int(number) if number.is_integer() else number
    raise KeyError(token)


def _font_entries() -> list[dict[str, Any]]:
    """Mapeie o basename dos WOFF2 descritos nos tokens aos TTF exportados."""
    entries = []
    for font in load_tokens()["type"]["fonts"]:
        font_file = KIT / "fontes" / (Path(font["file"]).stem + ".ttf")
        if not font_file.is_file():
            raise FileNotFoundError(f"Fonte obrigatória ausente: {font_file}")
        entries.append({**font, "path": font_file})
    if len(entries) != 6:
        raise ValueError("O kit precisa declarar exatamente seis variantes de fonte.")
    return entries


def generate_tokens_css(output: Path) -> Path:
    """Gere variáveis e estilos; os aliases CSS continuam apontando aos tokens."""
    output = Path(output)
    if output.suffix != ".css":
        output = output / "tokens.css"
    output.parent.mkdir(parents=True, exist_ok=True)
    tokens = load_tokens()
    lines = ["/* Gerado de kit/design-system/tokens.json; não edite manualmente. */"]
    for font in _font_entries():
        lines.append(
            "@font-face { "
            f"font-family: {json.dumps(font['family'])}; "
            f"src: url({json.dumps(resource_url(font['path']))}) format('truetype'); "
            f"font-weight: {font['weight']}; font-style: {font['style']}; "
            "font-display: block; }"
        )
    lines.append(":root {")
    for name, family in tokens["type"]["families"].items():
        lines.append(f"  --font-{name}: {family};")
    for section in ("spacing", "radius", "formato"):
        for item in tokens[section]["tokens"]:
            lines.append(f"  --{item['name']}: {item['value']};")
    lines.append("}")
    for theme in tokens["color"]["themes"]:
        theme_id = theme["id"]
        lines.append(f'[data-theme="{theme_id}"] {{')
        for item in tokens["color"]["tokens"]:
            value = item["value"]
            if isinstance(value, dict):
                value = value[theme_id]
            if value.startswith("{") and value.endswith("}"):
                value = f"var(--{value[1:-1]})"
            lines.append(f"  --{item['name']}: {value};")
        lines.append("}")
    for group in tokens["type"]["groups"]:
        for style in group["styles"]:
            lines.append(
                f".{style['name']} {{ "
                f"font-family: var(--font-{group['family']}); "
                f"font-size: {style['fontSize']}; line-height: {style['lineHeight']}; "
                f"font-weight: {style['fontWeight']}; "
                f"font-style: {style.get('fontStyle', 'normal')}; "
                f"letter-spacing: {style.get('letterSpacing', '0em')}; }}"
            )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def cruz() -> str:
    """O path original do Selo/preview.html, sem redesenho."""
    return (
        '<svg class="aqr-selo__cruz" data-element="selo-cruz" '
        'data-cor-token="cor-do-dia" viewBox="0 0 18 30" aria-hidden="true">'
        f'<path d="{CRUZ_PATH}" fill="currentColor"/></svg>'
    )


def selo(serie: str, data: str, info: str | None = None) -> str:
    """Topo completo: selo à esquerda e apoio opcional à direita."""
    support = (
        '<span class="selo aqr-topo__info" data-element="selo-info" '
        f'data-cor-token="tinta-suave">{escape(info)}</span>'
        if info is not None else ""
    )
    return (
        '<header class="aqr-topo" data-element="topo">'
        '<div class="aqr-selo selo">' + cruz() + '<span>'
        f'<span data-element="selo-serie" data-cor-token="tinta">{escape(serie)}</span> '
        '<span class="aqr-selo__data" data-element="selo-data" '
        f'data-cor-token="tinta-suave">· {escape(data)}</span></span></div>'
        + support + '</header>'
    )


def _image_uri(obra: str | Path) -> str:
    if isinstance(obra, Path):
        return resource_url(obra)
    if urlparse(obra).scheme:
        return obra
    if obra.startswith("/") and not obra.startswith(str(PROJECT)):
        return obra
    return resource_url(obra)


def nicho(largura: int | float, altura: int | float, obra: str | Path) -> str:
    """Nicho CSS original, com uma imagem real no recorte em arco."""
    if largura <= 32 or altura <= 16:
        raise ValueError("O nicho precisa comportar as margens de 16 px da obra.")
    src = escape(_image_uri(obra), quote=True)
    return (
        '<div class="aqr-nicho" data-element="nicho" '
        f'style="width:{largura:g}px;height:{altura:g}px;">'
        '<div class="aqr-nicho__obra" data-element="nicho-recorte">'
        f'<img src="{src}" alt="Obra provisória" data-element="nicho-obra" '
        'data-arquivo="obra-provisoria.png"></div></div>'
    )


def assinatura(tema: str, arroba: bool = False, curta: bool = False) -> str:
    """Assinatura horizontal ou reduzida, com dimensões do uso final."""
    _theme(tema)
    filename = f"{'simbolo-reduzido' if curta else 'logo-horizontal'}-{tema}.svg"
    source = resource_url(KIT / "logos" / filename)
    classes = "aqr-assinatura aqr-assinatura--curta" if curta else "aqr-assinatura"
    # A curta é sempre símbolo + @; os 40/16 px vêm do pedido e do preview.
    image_style = ' style="height:40px"' if curta else ""
    wrapper_style = ' style="gap:var(--espaco-2)"' if curta else ""
    handle = (
        '<span class="assinatura aqr-arroba" data-element="assinatura-arroba" '
        'data-cor-token="tinta-suave">@artequereza.oficial</span>'
        if arroba or curta else ""
    )
    return (
        f'<footer class="{classes}" data-element="assinatura"{wrapper_style}>'
        f'<img src="{source}" alt="Arte que Reza" '
        f'data-element="logo" data-arquivo="kit/logos/{filename}"'
        f'{image_style}>' + handle + '</footer>'
    )


def montar_arte(
    conteudo: str,
    tema: str = "pergaminho",
    cor_do_dia: str = "liturgico-verde",
    formato: str = "feed",
    cartao_cor: bool = False,
) -> str:
    """Monte a tela 1080 × 1350/1920 sem acrescentar um modelo de série."""
    _theme(tema)
    if formato not in {"feed", "story"}:
        raise ValueError("Formato precisa ser 'feed' ou 'story'.")
    if cor_do_dia not in _token_map("color"):
        raise ValueError(f"Token de cor desconhecido: {cor_do_dia}")
    classes = ["aqr-post"]
    if formato == "story":
        classes.append("aqr-post--story")
    if cartao_cor:
        classes.append("aqr-post--cor")
        # O cartão litúrgico usa a versão clara do logo, mesmo no pergaminho.
        conteudo = re.sub(
            r"((?:logo-horizontal|simbolo-reduzido)-)pergaminho(\.svg)",
            r"\1capela\2",
            conteudo,
        )
    return (
        f'<article class="{" ".join(classes)}" data-theme="{tema}" '
        f'data-formato="{formato}" style="--cor-do-dia:var(--{cor_do_dia})">'
        + conteudo + '</article>'
    )


def html_document(
    body: str,
    css_path: Path,
    extra_css: str = "",
    title: str = "Arte que Reza",
) -> str:
    """Documento autônomo com fontes locais e o bundle original por referência."""
    css_uri = resource_url(css_path)
    bundle_uri = resource_url(KIT / "design-system" / "bundle.css")
    return (
        '<!doctype html>\n<html lang="pt-BR" data-theme="pergaminho"><head>'
        '<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{escape(title)}</title><link rel="stylesheet" href="{css_uri}">'
        f'<link rel="stylesheet" href="{bundle_uri}">'
        '<style>*,*::before,*::after{box-sizing:border-box;}html,body{margin:0;padding:0;}'
        'body{font-family:var(--font-sem-serifa);background:var(--fundo);color:var(--tinta);}'
        + extra_css + '</style></head><body>' + body + '</body></html>'
    )


def await_fonts(page: Any) -> list[dict[str, Any]]:
    """Carregue e confira as seis variantes antes de qualquer PNG ou PDF.

    ``document.fonts.check`` isoladamente pode aceitar fallback quando não há
    FontFace correspondente. A lista devolvida por ``load`` também é verificada.
    """
    variants = [
        {"family": font["family"], "weight": str(font["weight"]), "style": font["style"]}
        for font in _font_entries()
    ]
    result = page.evaluate(
        """async variants => {
          const results = [];
          for (const variant of variants) {
            const shorthand = `${variant.style} ${variant.weight} 32px "${variant.family}"`;
            const faces = await document.fonts.load(shorthand, 'Arte que Reza Ávila');
            const match = face => face.family.replace(/^["']|["']$/g, '') === variant.family
              && face.weight === variant.weight && face.style === variant.style
              && face.status === 'loaded';
            results.push({...variant, checked: document.fonts.check(shorthand, 'Arte que Reza Ávila'),
              loaded: faces.some(match)});
          }
          await document.fonts.ready;
          await Promise.all(Array.from(document.images, async image => {
            if (!image.complete) await new Promise((resolve, reject) => {
              image.addEventListener('load', resolve, {once:true});
              image.addEventListener('error', () => reject(new Error('Imagem ausente: '+image.src)), {once:true});
            });
            if (!image.naturalWidth) throw new Error('Imagem inválida: '+image.src);
            await image.decode();
          }));
          return results;
        }""",
        variants,
    )
    failed = [item for item in result if not item["checked"] or not item["loaded"]]
    if failed:
        raise RuntimeError("Fonte substituta ou ausente; render interrompido: " + repr(failed))
    return result


def render_arte(
    page: Any,
    html: str,
    png_path: Path,
    formato: str = "feed",
    pdf_path: Path | None = None,
    *,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Renderize uma arte, com verificação de dimensões, fontes e imagens."""
    if formato not in {"feed", "story"}:
        raise ValueError("Formato precisa ser 'feed' ou 'story'.")
    width = dimension("post-largura")
    height = dimension("story-altura" if formato == "story" else "post-altura")
    page.set_viewport_size({"width": width, "height": height})
    # HTTP de loopback é compatível com a política do Chromium do ambiente.
    # Os arquivos TTF, SVG e CSS continuam vindo exclusivamente deste checkout.
    png_path = Path(png_path)
    png_path.parent.mkdir(parents=True, exist_ok=True)
    html_path = png_path.with_suffix(".html")
    html_path.write_text(html, encoding="utf-8")
    base_url = base_url or os.environ.get("ARTEQUE_REZA_BASE_URL")
    if not base_url:
        raise RuntimeError(
            "Informe base_url do servidor HTTP local que serve PROJECT, "
            "ou configure ARTEQUE_REZA_BASE_URL."
        )
    page.goto(base_url.rstrip("/") + resource_url(html_path), wait_until="load")
    fonts = await_fonts(page)
    bounds = page.locator(".aqr-post").first.bounding_box()
    if not bounds or bounds["width"] != width or bounds["height"] != height:
        raise RuntimeError(f"Tela com dimensão incorreta: {bounds}; esperado {width} × {height}.")
    # A arte, e não eventuais anotações ao redor dela, define o PNG exportado.
    page.screenshot(path=str(png_path), clip=bounds, animations="disabled")
    if pdf_path is not None:
        pdf_path = Path(pdf_path)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        await_fonts(page)
        raw_pdf = page.pdf(
            width=f"{width}px", height=f"{height}px",
            print_background=True, margin={"top":"0", "right":"0", "bottom":"0", "left":"0"},
            prefer_css_page_size=False,
        )
        from pypdf import PdfReader, PdfWriter, Transformation
        from pypdf.generic import RectangleObject

        reader = PdfReader(BytesIO(raw_pdf))
        if len(reader.pages) != 1:
            raise RuntimeError(f"Uma arte deve gerar uma página PDF; recebidas {len(reader.pages)}.")
        pdf_page = reader.pages[0]
        pdf_width, pdf_height = width * 0.75, height * 0.75
        # O Chromium arredonda o papel para unidades internas. Corrigir a caixa
        # e deslocar o conteúdo mantém a origem superior, o texto e os vetores.
        pdf_page.add_transformation(
            Transformation().translate(ty=pdf_height - float(pdf_page.mediabox.height))
        )
        pdf_page.mediabox = RectangleObject([0, 0, pdf_width, pdf_height])
        pdf_page.cropbox = RectangleObject([0, 0, pdf_width, pdf_height])
        writer = PdfWriter()
        writer.add_page(pdf_page)
        with pdf_path.open("wb") as stream:
            writer.write(stream)
    return {"width": width, "height": height, "fonts": fonts, "html": str(html_path)}
