"""Renderização local, galerias de componentes e prova de importação do Canva."""
from __future__ import annotations

from contextlib import contextmanager
from functools import partial
from html import escape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
from typing import Any
from urllib.parse import urlsplit

from PIL import Image, ImageChops, ImageStat
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject

from .base import KIT, PROJECT, CRUZ_PATH, assinatura, await_fonts, color, dimension, generate_tokens_css, html_document, load_tokens, montar_arte, nicho, selo
from .canva import export_elements
from .ficha import measure_page, write_ficha
from .validacao import validate_kit, validate_niche_pixels, validate_pdf, validate_pngs, validate_svgs


COLORS = ["verde", "roxo", "branco", "vermelho", "rosa"]
NICHES = [
    (680, 760, "capela", "capela", "fundo", "liturgico-roxo"),
    (340, 420, "santinho", "pergaminho", "papel", "ouro"),
    (600, 680, "coragem", "pergaminho", "fundo", "liturgico-roxo"),
    (640, 760, "toda-bela", "capela", "fundo", "liturgico-roxo"),
    (720, 900, "status-coragem", "pergaminho", "fundo", "liturgico-roxo"),
    (600, 700, "angelus", "capela", "fundo", "liturgico-roxo"),
]


def url(path: Path) -> str:
    return "/" + path.resolve().relative_to(PROJECT).as_posix()


class LocalHandler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        # HTML may be rewritten twice in one second when the verse changes
        # from citacao-grande to citacao. A cached Last-Modified response must
        # never reuse the first layout during the second measurement.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *_: Any) -> None:
        pass


@contextmanager
def local_server():
    """Apenas arquivos locais; não depende de file:// nem de navegação externa."""
    handler = partial(LocalHandler, directory=str(PROJECT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def check(result: dict[str, Any], name: str) -> None:
    if not result.get("ok"):
        raise RuntimeError(f"{name}: " + "; ".join(result.get("errors", [str(result)])))


def load(page, document: str, path: Path, base_url: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(document, encoding="utf-8")
    page.goto(base_url + url(path), wait_until="networkidle")
    return await_fonts(page)


def snapshot(page, path: Path, expected: dict, *, clip=None, full_page=False):
    await_fonts(page)
    path.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(path), clip=clip, full_page=full_page, animations="disabled")
    with Image.open(path) as image:
        expected[str(path)] = image.size


GALLERY_CSS = """
.gallery {display:grid;grid-template-columns:repeat(2,1080px);width:2160px;gap:0;}
.case {margin:0;width:1080px;overflow:hidden;}
.case-label {height:40px;padding:12px 32px 8px;font:400 14px/20px var(--font-sem-serifa);color:var(--tinta-suave);}
.case-panel {position:relative;width:1080px;background:var(--fundo);color:var(--tinta);}
.seal-panel {height:160px;}
.seal-panel>.aqr-topo {position:absolute;left:var(--espaco-5);top:var(--espaco-5);width:calc(100% - 2*var(--espaco-5));}
.signature-panel {height:180px;}
.signature-panel>.aqr-assinatura {position:absolute;bottom:var(--espaco-5);left:0;width:100%;}
.niche-panel {height:1080px;display:flex;justify-content:center;align-items:flex-start;padding-top:var(--espaco-5);}
.case-panel.aqr-post--cor {background:var(--cor-do-dia);color:var(--sobre-cor);}
"""


def case(label, content, kind, tema="pergaminho", liturgy="verde", card=False, background=None):
    classes = f"case-panel {kind}-panel" + (" aqr-post--cor" if card else "")
    style = f"--cor-do-dia:var(--liturgico-{liturgy});"
    if background:
        style += f"background:var(--{background});"
    return f'<section class="case"><div class="case-label">{escape(label)}</div><div class="{classes}" data-theme="{tema}" style="{style}">{content}</div></section>'


def galleries(page, output, css, artwork, base_url, expected):
    examples = {
        "verde": ("Evangelho do Dia", "sex, 16 out"),
        "roxo": ("Evangelho do Dia", "dom, 29 nov"),
        "branco": ("Santo do Dia", "qui, 15 out"),
        "vermelho": ("Santo do Dia", "sáb, 17 out"),
        "rosa": ("Evangelho do Dia", "dom, 13 dez"),
    }
    cases = []
    for tema in ["pergaminho", "capela"]:
        for name in COLORS:
            serie, data = examples[name]
            cases.append(case(f"{tema} · {'ouro' if name == 'branco' else name}", selo(serie, data, "Lc 12,1-7" if name == "verde" else None), "seal", tema, name))
    for name in COLORS:
        serie, data = examples[name]
        cases.append(case(f"Cartão · {'ouro' if name == 'branco' else name}", selo(serie, data), "seal", "pergaminho", name, True))
    page.set_viewport_size({"width": 2160, "height": 1600})
    load(page, html_document('<div class="gallery">' + ''.join(cases) + '</div>', css, GALLERY_CSS, "Selos"), output / "html/selos.html", base_url)
    snapshot(page, output / "previas/selos.png", expected, full_page=True)
    expected[str(output / "previas/selos.png")] = (2160, 1600)

    cases = []
    for width, height, use, tema, background, frame in NICHES:
        piece = nicho(width, height, artwork)
        if frame == "ouro":
            piece = piece.replace('style="width:', 'style="--moldura:var(--ouro);width:', 1)
        cases.append(case(f"{width} × {height} · {use}", piece, "niche", tema, "roxo", background=background))
    page.set_viewport_size({"width": 2160, "height": 3360})
    load(page, html_document('<div class="gallery">' + ''.join(cases) + '</div>', css, GALLERY_CSS, "Nichos"), output / "html/nichos.html", base_url)
    boxes = page.locator('.niche-panel .aqr-nicho').evaluate_all("""els => els.map(el => {
      const r=el.getBoundingClientRect(), panel=el.closest('.niche-panel'), style=getComputedStyle(el);
      return {x:r.x,y:r.y,width:r.width,height:r.height,background:getComputedStyle(panel).backgroundColor,
        filete:style.getPropertyValue('--moldura').trim() || style.getPropertyValue('--cor-do-dia').trim(),outer_radius:r.width/2};
    })""")
    # Resolve actual pseudo-element paint (aliases may remain in custom properties).
    for i, box in enumerate(boxes):
        box['filete'] = page.locator('.niche-panel .aqr-nicho').nth(i).evaluate("el => getComputedStyle(el,'::before').borderTopColor")
    snapshot(page, output / "previas/nichos.png", expected, full_page=True)
    expected[str(output / "previas/nichos.png")] = (2160, 3360)

    cases = []
    for tema in ["pergaminho", "capela"]:
        for label, handle, short in [("Horizontal", False, False), ("Horizontal com @", True, False), ("Curta com @", True, True)]:
            cases.append(case(f"{label} · {tema}", assinatura(tema, handle, short), "signature", tema))
    for name in COLORS:
        cases.append(case(f"Cartão · {'ouro' if name == 'branco' else name}", assinatura("pergaminho", sobre_cor=True), "signature", "pergaminho", name, True))
    page.set_viewport_size({"width": 2160, "height": 1320})
    load(page, html_document('<div class="gallery">' + ''.join(cases) + '</div>', css, GALLERY_CSS, "Assinaturas"), output / "html/assinaturas.html", base_url)
    snapshot(page, output / "previas/assinaturas.png", expected, full_page=True)
    expected[str(output / "previas/assinaturas.png")] = (2160, 1320)
    return boxes


def cover(artwork: Path, overlay: Path | None = None):
    header = selo("Evangelho do Dia", "sex, 16 out", "Lc 12,1-7")
    if overlay is None:
        work = nicho(680, 760, artwork).replace('style="width:', 'style="margin-top:var(--espaco-3);width:', 1)
    else:
        # Same inner image rectangle as CSS version, no CSS clipping or gradients.
        work = f'''<div class="canva-nicho" data-element="nicho-canva" style="position:relative;flex:none;width:680px;height:760px;margin-top:var(--espaco-3)">
<img data-element="nicho-obra-retangular" data-arquivo="obra-provisoria.png" src="{url(artwork)}" alt="Obra provisória" style="position:absolute;left:16px;top:16px;width:648px;height:744px;object-fit:cover;display:block">
<img data-element="nicho-mascara" data-arquivo="canva/elementos/variantes/nicho-680x760-capela-verde.svg" src="{url(overlay)}" alt="Nicho para Canva" style="position:absolute;left:-48px;top:0;width:776px;height:763px;display:block">
</div>'''
    text = '<p class="credito aqr-credito" data-element="credito-obra" data-cor-token="tinta-suave" style="margin-top:var(--espaco-3)">Artista · Título da obra · Museu</p><h1 class="titulo aqr-titulo" data-element="titulo" data-cor-token="tinta" style="margin-top:var(--espaco-4);max-width:880px;text-align:center">Nem um pardal é esquecido por Deus</h1>'
    return montar_arte(header + work + text + assinatura("capela"), "capela")


def prayer_card():
    header = selo("Evangelho do Dia", "sex, 16 out", "Lc 12,1-7")
    content = f'''<div class="aqr-texto" style="margin-top:auto">
<p class="selo" data-element="convite-oracao" data-cor-token="sobre-cor">Para rezar hoje</p>
<p class="citacao aqr-citacao" data-element="pergunta" data-cor-token="sobre-cor" style="max-width:860px">Se Deus conta até os cabelos da minha cabeça, do que eu ainda tenho medo?</p>
<div class="aqr-ornamento" data-element="ornamento" data-cor-token="sobre-cor" style="color:var(--sobre-cor);margin-block:var(--espaco-3)"><svg data-element="ornamento-cruz" data-cor-token="sobre-cor" viewBox="0 0 18 30" aria-hidden="true"><path d="{CRUZ_PATH}" fill="currentColor"/></svg></div>
<p class="corpo"><span data-element="convite-biblia" data-cor-token="sobre-cor">Abra sua Bíblia em </span><strong data-element="referencia-biblia" data-cor-token="sobre-cor">Lucas 12,1-7</strong></p></div>'''
    return montar_arte(header + content + assinatura("pergaminho", sobre_cor=True), "pergaminho", cartao_cor=True)


def import_proof(page, output, css, artwork, base_url, expected):
    overlay = output / "canva/elementos/variantes/nicho-680x760-capela-verde.svg"
    bodies = [cover(artwork), cover(artwork, overlay), prayer_card()]
    names = ["Capa CSS", "Capa Canva", "Cartão final"]
    page.set_viewport_size({"width": 1080, "height": 1350})
    writer = PdfWriter()
    measurements = []
    font_checks = []
    for index, (body, name) in enumerate(zip(bodies, names), 1):
        html_path = output / f"html/pagina-{index}.html"
        font_checks.append(load(page, html_document(body, css, "@page{size:1080px 1350px;margin:0;}html,body{width:1080px;height:1350px;}body{-webkit-print-color-adjust:exact;print-color-adjust:exact;}", name), html_path, base_url))
        measurements.append(measure_page(page, index, name))
        image = output / f"canva/pagina-{index}.png"
        snapshot(page, image, expected)
        expected[str(image)] = (1080, 1350)
        await_fonts(page)
        pdf = page.pdf(width="1080px", height="1350px", print_background=True, margin={"top":"0","bottom":"0","left":"0","right":"0"}, prefer_css_page_size=True)
        import io
        reader = PdfReader(io.BytesIO(pdf))
        if len(reader.pages) != 1:
            raise RuntimeError(f"Página {index} criou {len(reader.pages)} páginas no PDF.")
        pdf_page = reader.pages[0]
        # Chromium rounds its paper size to device units. Preserve the CSS top
        # origin and remove the extra bottom sliver, without rasterizing text.
        desired_width, desired_height = 1080 * 72 / 96, 1350 * 72 / 96
        actual_height = float(pdf_page.mediabox.height)
        pdf_page.add_transformation(Transformation().translate(ty=desired_height - actual_height))
        pdf_page.mediabox = RectangleObject([0,0,desired_width,desired_height])
        pdf_page.cropbox = RectangleObject([0,0,desired_width,desired_height])
        writer.add_page(pdf_page)
    destination = output / "canva/teste-importacao.pdf"
    writer.write(destination)
    (output / "canva/medicoes.json").write_text(json.dumps(measurements, ensure_ascii=False, indent=2) + '\n', encoding="utf-8")
    write_ficha(output / "canva/FICHA.md", measurements)
    return font_checks


def logo_comparisons(page, metadata, output, css, base_url, expected):
    """Compare vector conversion at identical drawing bounds, without whitespace shifts."""
    import xml.etree.ElementTree as ET
    comparisons = []
    work = output / "verificacao/logos"
    work.mkdir(parents=True, exist_ok=True)
    for entry in metadata['logos']:
        source = Path(entry['source'])
        converted = Path(entry['file'])
        if not source.is_absolute():
            source = PROJECT / source
        if not converted.is_absolute():
            converted = PROJECT / converted
        if source.suffix.lower() != '.svg':
            continue
        tree = ET.fromstring(source.read_text())
        bounds = entry['drawing_bounds']
        if isinstance(bounds, dict):
            box = [bounds.get('x',0), bounds.get('y',0), bounds['width'], bounds['height']]
        else:
            box = list(bounds)
        tree.set('viewBox', ' '.join(str(v) for v in box))
        tree.set('width', str(entry['width']))
        tree.set('height', str(entry['height']))
        normalized = work / source.name
        normalized.write_text(ET.tostring(tree, encoding='unicode'), encoding='utf-8')
        # Supersample small marks; large assets are already readable at 1080 px.
        scale = min(4.0, 1080 / max(float(entry['width']),float(entry['height'])))
        width = float(entry['width']) * scale
        height = float(entry['height']) * scale
        render_width = max(1, round(width))
        render_height = max(1, round(height))
        images = []
        for variant, path in [('original', normalized), ('convertido', converted)]:
            markup = f'<img id="logo" src="{url(path)}" style="display:block;width:{render_width}px;height:{render_height}px">'
            page.set_viewport_size({'width': render_width, 'height': render_height})
            load(page, html_document(markup, css, 'html,body{background:transparent;}'), work / 'comparacao.html', base_url)
            await_fonts(page)
            image_path = work / f'{source.stem}-{variant}.png'
            page.screenshot(path=str(image_path), omit_background=True, animations='disabled')
            expected[str(image_path)] = (render_width, render_height)
            images.append(Image.open(image_path).convert('RGBA'))
        # Composite on both brand backgrounds, because alpha is part of appearance.
        metrics = []
        for background in [color('fundo','pergaminho'), color('fundo','capela')]:
            a = Image.new('RGBA', images[0].size, background)
            b = Image.new('RGBA', images[1].size, background)
            a.alpha_composite(images[0]); b.alpha_composite(images[1])
            diff = ImageChops.difference(a.convert('RGB'), b.convert('RGB'))
            mean = sum(ImageStat.Stat(diff).mean) / 3
            channels = diff.split()
            largest = ImageChops.lighter(ImageChops.lighter(channels[0],channels[1]),channels[2])
            histogram = largest.histogram()
            severe = sum(histogram[33:]) / (diff.width * diff.height)
            metrics.append({'background': background, 'mean_channel_difference': round(mean,6), 'pixels_over_32_fraction':round(severe,6)})
            if mean > 1.5 or severe > 0.015:
                raise RuntimeError(f'Diferença visual não desprezível no logo {source.name}: {metrics[-1]}')
        comparisons.append({'file': source.name, 'comparison_size': [render_width,render_height], 'metrics':metrics})
    return comparisons


def generate(output: Path):
    output.mkdir(parents=True, exist_ok=True)
    css = generate_tokens_css(output / 'tokens.css')
    metadata = export_elements(output / 'canva/elementos')
    checks = {'kit': validate_kit(PROJECT), 'svgs': validate_svgs(output / 'canva/elementos')}
    for name,result in checks.items(): check(result,name)
    expected = {}
    expected[str(output / 'canva/elementos/logos/avatar-perfil.png')] = (1080,1080)
    errors = []
    with local_server() as base_url, sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
        context = browser.new_context(device_scale_factor=1)
        context.route('**/*', lambda route: route.continue_() if urlsplit(route.request.url).netloc == urlsplit(base_url).netloc else route.abort())
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
        page.on('response', lambda response: errors.append(f'HTTP {response.status}: {response.url}') if response.status >= 400 else None)
        artwork = output / 'obra-provisoria.png'
        page.set_viewport_size({'width':1080,'height':1350})
        load(page, html_document('<div class="aqr-obra--luz" style="width:1080px;height:1350px"></div>', css), output / 'html/obra-provisoria.html', base_url)
        snapshot(page, artwork, expected)
        expected[str(artwork)] = (1080,1350)
        boxes = galleries(page,output,css,artwork,base_url,expected)
        fonts = import_proof(page,output,css,artwork,base_url,expected)
        comparisons = logo_comparisons(page,metadata,output,css,base_url,expected)
        browser.close()
    if errors:
        raise RuntimeError('Erros de navegador: ' + '; '.join(errors))
    checks['pngs'] = validate_pngs(expected)
    checks['pdf'] = validate_pdf(output / 'canva/teste-importacao.pdf')
    checks['nicho_pixels'] = validate_niche_pixels(output / 'previas/nichos.png', boxes)
    checks['kit_final'] = validate_kit(PROJECT)
    for name,result in checks.items(): check(result,name)
    checks['browser'] = {'ok':True,'errors':[],'font_variants_per_render':6}
    checks['logos'] = {'ok':True,'comparisons':comparisons}
    manifest = {'checks':checks,'expected_pngs':{str(Path(path).relative_to(output)):list(size) for path,size in expected.items()},'elementos':metadata,'fonts':fonts}
    (output / 'verificacao').mkdir(exist_ok=True)
    (output / 'verificacao/resultados.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    from .relatorio import write_report
    write_report(output,manifest)
    return {'pngs':len(expected),'svgs':len(list((output/'canva/elementos').rglob('*.svg')))}
