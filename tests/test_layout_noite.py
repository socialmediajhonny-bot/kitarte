"""Séries da noite: layout real, recortes e rejeição de artes inválidas."""

from copy import deepcopy
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from urllib.parse import urlsplit

from PIL import Image, ImageChops, JpegImagePlugin
from playwright.sync_api import sync_playwright

from gerar import ensure_kit
from arteque_reza.base import PROJECT, await_fonts, generate_tokens_css, render_arte, resource_url
from arteque_reza.conteudo_noite import LOADERS
from arteque_reza.noite import (
    _document, _measure, _pdf_check, _pixels, _validate_layout, artwork_window,
    crop_image, expand_cards, prepare_artworks,
)
from arteque_reza.renderizacao import local_server


@unittest.skipUnless(shutil.which("chromium"), "Chromium é necessário para medir o layout real")
class NightLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_kit()
        cls.temp = tempfile.TemporaryDirectory(dir=PROJECT / "work")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.folder = Path(cls.temp.name)
        cls.css = generate_tokens_css(cls.folder / "tokens.css")
        cls.server = local_server()
        cls.url = cls.server.__enter__()
        cls.addClassCleanup(cls.server.__exit__, None, None, None)
        cls.playwright = sync_playwright().start()
        cls.addClassCleanup(cls.playwright.stop)
        cls.browser = cls.playwright.chromium.launch(
            executable_path=shutil.which("chromium"), args=["--no-sandbox"])
        cls.addClassCleanup(cls.browser.close)
        cls.context = cls.browser.new_context(
            device_scale_factor=1, viewport={"width": 1080, "height": 1350})
        cls.addClassCleanup(cls.context.close)
        cls.context.route("**/*", lambda route: route.continue_()
            if urlsplit(route.request.url).netloc == urlsplit(cls.url).netloc else route.abort())
        cls.page = cls.context.new_page()
        cls.days = {series: reader(PROJECT / f"conteudo/{series}.yaml")
                    for series, reader in LOADERS.items()}
        cls.cards = {series: expand_cards(series, days) for series, days in cls.days.items()}
        cls.artworks = {series: prepare_artworks(series, days[0], cls.folder/series/days[0]["data"])
                        for series, days in cls.days.items()}

    def card(self, series, number=1):
        return self.cards[series][number-1]

    def markup(self, card, artworks=None, invocation_style="titulo-capa"):
        return _document(card, self.css,
                         self.artworks[card["serie"]] if artworks is None else artworks,
                         invocation_style=invocation_style)

    def render(self, card, artworks=None, invocation_style="titulo-capa"):
        path = self.folder/"card.html"
        path.write_text(self.markup(card, artworks, invocation_style), encoding="utf-8")
        self.page.goto(self.url+resource_url(path))
        await_fonts(self.page)
        return _measure(self.page, card)

    @staticmethod
    def field(measured, name):
        return next(text for text in measured["textos"] if text["campo"] == name)

    def geometry(self):
        return self.page.evaluate("""() => {
          const a=document.querySelector('.aqr-post').getBoundingClientRect();
          const rect=n=>{const r=n.getBoundingClientRect();return {x:r.x-a.x,y:r.y-a.y,w:r.width,h:r.height};};
          const box=sel=>{const n=document.querySelector(sel);return n?rect(n):null;};
          return {texts:Object.fromEntries([...document.querySelectorAll('[data-text]')].map(n=>[n.dataset.text,rect(n)])),
            seal:box('.aqr-selo'),block:box('.aqr-texto'),signature:box('.aqr-assinatura'),
            niches:[...document.querySelectorAll('.aqr-nicho')].map(rect)};
        }""")

    def assert_gap(self, first, second, expected):
        self.assertAlmostEqual(second["y"]-first["y"]-first["h"], expected, delta=.01)

    def assert_art_rejected(self, card, expression):
        with self.assertRaisesRegex(ValueError, expression):
            measured = _measure(self.page, card)
            _validate_layout(card, measured)
            path = self.folder/"invalid.png"
            self.page.screenshot(path=str(path), clip=self.page.locator('.aqr-post').bounding_box(),
                                 animations="disabled")
            _pixels(path, card, measured)

    def test_all_twelve_cards_have_required_gaps_centering_and_colors(self):
        self.assertEqual(sum(map(len, self.cards.values())), 12)
        for cards in self.cards.values():
            for card in cards:
                with self.subTest(series=card["serie"], number=card["numero"]):
                    measured = self.render(card)
                    self.assertTrue(_validate_layout(card, measured)["ok"])
                    g = self.geometry()
                    on_color = ((card["serie"] == "por-dentro-da-missa" and card["numero"] == 4)
                                or (card["serie"] == "toda-bela" and card["numero"] == 3))
                    theme = ('pergaminho' if on_color or card["serie"] in
                             {"por-dentro-da-missa", "rezo-por-voce"} else 'capela')
                    self.assertEqual(self.page.locator('.aqr-post').get_attribute('data-theme'), theme)
                    self.assertEqual('aqr-post--cor' in self.page.locator('.aqr-post').get_attribute('class'), on_color)
                    if card["serie"] == "rezo-por-voce":
                        self.assertEqual(self.page.locator('.aqr-topo__info').count(), 0)
                    else:
                        info = 'Ladainha 1' if card["serie"] == "toda-bela" and card["numero"] == 1 else f'{card["numero"]}/{card["total"]}'
                        self.assertEqual(self.page.locator('.aqr-topo__info').inner_text(), info)
                    high_art = ((card["serie"] == "olhe-de-novo" and card["numero"] <= 2)
                                or (card["serie"] == "toda-bela" and card["numero"] == 1))
                    if high_art:
                        self.assert_gap(g["seal"], g["niches"][0], 32)
                        last = g["texts"]["invocacao" if card["serie"] == "toda-bela" else "titulo"]
                        self.assertGreaterEqual(g["signature"]["y"]-last["y"]-last["h"], 31.99)
                    else:
                        above = g["block"]["y"]-g["seal"]["y"]-g["seal"]["h"]
                        below = g["signature"]["y"]-g["block"]["y"]-g["block"]["h"]
                        self.assertAlmostEqual(above, below, delta=.1)
                        self.assertGreaterEqual(min(above, below), 59.99)
                    if card["serie"] == "olhe-de-novo" and card["numero"] == 4:
                        first, second = g["niches"]
                        self.assertAlmostEqual(second["x"]-first["x"]-first["w"], 96, delta=.01)
                        self.assertAlmostEqual((first["x"]+second["x"]+second["w"])/2, 540, delta=.01)
                    path = self.folder/"valid.png"
                    self.page.screenshot(path=str(path), clip=self.page.locator('.aqr-post').bounding_box())
                    self.assertTrue(_pixels(path, card, measured)["ok"])
                    for image in self.page.locator('.aqr-nicho img').all():
                        self.assertEqual(image.evaluate('el=>getComputedStyle(el).objectPosition'), '50% 50%')
                        self.assertIn(image.evaluate('el=>getComputedStyle(el).transform'),
                                      ('none', 'matrix(1, 0, 0, 1, 0, 0)'))

    def test_16_pixel_label_title_gap_is_rejected(self):
        for series, number in (("olhe-de-novo", 3), ("por-dentro-da-missa", 2)):
            card = self.card(series, number)
            with self.subTest(series=series):
                self.assertTrue(_validate_layout(card, self.render(card))["ok"])
                self.page.locator('[data-text="rotulo"]').evaluate("el=>el.style.marginBottom='0px'")
                self.page.locator('[data-text="titulo"]').evaluate("el=>el.style.marginTop='0px'")
                g = self.geometry()["texts"]
                self.assert_gap(g["rotulo"], g["titulo"], 16)
                with self.assertRaisesRegex(ValueError, r"rotulo.*titulo.*16.*48"):
                    _validate_layout(card, _measure(self.page, card))

    def test_16_pixel_prayer_title_text_gap_is_rejected(self):
        card = self.card("rezo-por-voce")
        self.assertTrue(_validate_layout(card, self.render(card))["ok"])
        self.page.locator('[data-text="titulo"]').evaluate("el=>el.style.marginBottom='0px'")
        self.page.locator('[data-text="texto"]').evaluate("el=>el.style.marginTop='0px'")
        g = self.geometry()["texts"]
        self.assert_gap(g["titulo"], g["texto"], 16)
        with self.assertRaisesRegex(ValueError, r"titulo.*texto.*16.*32"):
            _validate_layout(card, _measure(self.page, card))

    def test_two_line_look_again_cover_title_is_rejected(self):
        card = self.card("olhe-de-novo")
        self.render(card)
        self.page.locator('[data-text="titulo"]').evaluate("el=>el.innerHTML='O lírio<br>da Anunciação'")
        measured = _measure(self.page, card)
        self.assertEqual(self.field(measured, "titulo")["quantidade_linhas"], 2)
        with self.assertRaisesRegex(ValueError, r"titulo.*2 linhas.*1"):
            _validate_layout(card, measured)

    def test_three_line_where_credit_is_rejected(self):
        card = self.card("olhe-de-novo", 4)
        self.render(card)
        self.page.locator('[data-text="credito_1"]').evaluate("el=>el.innerHTML='Jan van Eyck<br>A Anunciação<br>National Gallery of Art'")
        measured = _measure(self.page, card)
        self.assertEqual(self.field(measured, "credito_1")["quantidade_linhas"], 3)
        with self.assertRaisesRegex(ValueError, r"credito_1.*3 linhas.*2"):
            _validate_layout(card, measured)

    def test_five_line_closing_phrase_is_rejected(self):
        card = self.card("por-dentro-da-missa", 4)
        self.render(card)
        self.page.locator('[data-text="frase"]').evaluate("el=>el.innerHTML='Repare na cor<br>das vestes do padre<br>e na vela rosa<br>da coroa<br>do Advento.'")
        measured = _measure(self.page, card)
        self.assertEqual(self.field(measured, "frase")["quantidade_linhas"], 5)
        with self.assertRaisesRegex(ValueError, r"frase.*5 linhas.*4"):
            _validate_layout(card, measured)

    def test_line_ending_in_book_or_ordinal_is_rejected(self):
        card = self.card("olhe-de-novo", 3)
        for html, ending in (("Leiam Lc<br>1,27.", "Lc"), ("No 3º<br>Domingo do Advento.", "3º")):
            with self.subTest(ending=ending):
                self.render(card)
                self.page.locator('[data-text="texto"]').evaluate('(el,html)=>el.innerHTML=html', html)
                measured = _measure(self.page, card)
                self.assertTrue(any(line.endswith(ending) for line in self.field(measured, "texto")["linhas"]))
                with self.assertRaisesRegex(ValueError, r"bíblic|ordinal|Lc|3º"):
                    _validate_layout(card, measured)

    def test_broken_hyphenated_word_is_rejected(self):
        card = self.card("por-dentro-da-missa", 3)
        self.render(card)
        self.page.locator('[data-text="texto"]').evaluate("el=>el.innerHTML='Alegrai-<br>vos sempre no Senhor!'")
        measured = _measure(self.page, card)
        self.assertTrue(any(line.endswith('-') for line in self.field(measured, "texto")["linhas"]))
        with self.assertRaisesRegex(ValueError, r"hífen"):
            _validate_layout(card, measured)

    def test_biblical_reference_ordinal_and_hyphenated_word_keep_the_shared_protection(self):
        self.render(self.card("por-dentro-da-missa", 3))
        for kind, text in (("referencia", "Fl\u00a04,4"), ("ordinal", "3º\u00a0Domingo")):
            with self.subTest(kind=kind):
                protected = self.page.locator(f'[data-regra="{kind}"]').filter(has_text=text).first
                self.assertEqual(protected.inner_text(), text)
                self.assertEqual(protected.evaluate('el=>getComputedStyle(el).whiteSpace'), 'nowrap')
        self.render(self.card("por-dentro-da-missa", 2))
        word = self.page.locator('[data-regra="hifen"]').filter(has_text="345-346").first
        self.assertEqual(word.inner_text(), "345-346")
        self.assertEqual(word.evaluate('el=>getComputedStyle(el).whiteSpace'), 'nowrap')

    def test_closing_requires_the_whole_colored_card(self):
        for series, number in (("por-dentro-da-missa", 4), ("toda-bela", 3)):
            card = self.card(series, number)
            with self.subTest(series=series):
                self.render(card)
                self.page.locator('.aqr-post').evaluate("el=>el.classList.remove('aqr-post--cor')")
                self.assert_art_rejected(card, r"fundo|cor")

    def test_wrong_logo_variant_is_rejected(self):
        card = self.card("rezo-por-voce")
        self.render(card)
        self.page.locator('[data-element="logo"]').evaluate("el=>el.setAttribute('data-arquivo','logo-horizontal-capela.svg')")
        self.assert_art_rejected(card, r"logo|assinatura|variante")

    def test_second_where_niche_requires_the_color_of_the_day(self):
        card = self.card("olhe-de-novo", 4)
        self.render(card)
        frames = self.page.locator('[data-element="nicho-filete"]')
        self.assertEqual(frames.count(), 2)
        frames.nth(1).evaluate("el=>el.style.color='#000000'")
        self.assert_art_rejected(card, r"nicho|filete|cor")

    def test_pdf_preserves_text_and_both_vector_niches(self):
        card = self.card("olhe-de-novo", 4)
        path = self.folder/"where.pdf"
        render_arte(self.page, self.markup(card), path.with_suffix('.png'), pdf_path=path, base_url=self.url)
        measured = _measure(self.page, card)
        self.assertTrue(_pdf_check(path, [card], [measured])["ok"])

    def test_pdf_without_vector_niche_is_rejected(self):
        card = self.card("olhe-de-novo", 4)
        measured = self.render(card)
        markup = self.markup(card)
        altered, count = re.subn(r'<svg\b[^>]*data-element="nicho-filete"[^>]*>.*?</svg>', '', markup, flags=re.S)
        self.assertEqual(count, 2)
        path = self.folder/"no-vector.pdf"
        render_arte(self.page, altered, path.with_suffix('.png'), pdf_path=path, base_url=self.url)
        with self.assertRaisesRegex(ValueError, r"nicho|filete|vetorial|preenchimento"):
            _pdf_check(path, [card], [measured])

    def test_pdf_with_extra_text_is_rejected(self):
        card = self.card("rezo-por-voce")
        measured = self.render(card)
        extra = '<span style="position:absolute;left:80px;top:1280px;font:400 24px Lato">Texto extra</span>'
        markup = self.markup(card).replace('</article>', extra+'</article>')
        path = self.folder/"extra.pdf"
        render_arte(self.page, markup, path.with_suffix('.png'), pdf_path=path, base_url=self.url)
        with self.assertRaisesRegex(ValueError, r"texto|YAML"):
            _pdf_check(path, [card], [measured])

    def test_next_short_invocation_fits_in_cover_title_style(self):
        card = deepcopy(self.card("toda-bela"))
        card.update(data="2026-12-26", invocacao="Santa Mãe de Deus")
        measured = self.render(card)
        self.assertEqual(self.field(measured, "invocacao")["quantidade_linhas"], 1)
        self.assertEqual(self.field(measured, "invocacao")["estilo"], "titulo-capa")
        self.assertTrue(_validate_layout(card, measured)["ok"])

    def test_long_invocation_falls_back_to_two_title_lines(self):
        card = deepcopy(self.card("toda-bela"))
        card["invocacao"] = "Rainha concebida sem pecado original"
        first = self.render(card)
        self.assertGreater(self.field(first, "invocacao")["quantidade_linhas"], 1)
        measured = self.render(card, invocation_style="titulo")
        self.assertEqual(self.field(measured, "invocacao")["quantidade_linhas"], 2)
        self.assertEqual(self.field(measured, "invocacao")["estilo"], "titulo")
        self.assertTrue(_validate_layout(card, measured)["ok"])
        g = self.geometry(); title = g["texts"]["invocacao"]
        self.assertGreaterEqual(g["signature"]["y"]-title["y"]-title["h"], 31.99)

    def test_next_look_again_cover_title_fits_one_line(self):
        card = deepcopy(self.card("olhe-de-novo"))
        card.update(data="2026-12-30", titulo="O boi e o burro do presépio")
        measured = self.render(card)
        self.assertEqual(self.field(measured, "titulo")["quantidade_linhas"], 1)
        self.assertTrue(_validate_layout(card, measured)["ok"])

    def test_single_where_artwork_is_centered(self):
        day = deepcopy(self.days["olhe-de-novo"][0])
        day["onde"]["obras"] = day["onde"]["obras"][:1]
        card = expand_cards("olhe-de-novo", [day])[3]
        artworks = prepare_artworks("olhe-de-novo", day, self.folder/"one-artwork")
        measured = self.render(card, artworks)
        self.assertTrue(_validate_layout(card, measured)["ok"])
        niches = self.geometry()["niches"]
        self.assertEqual(len(niches), 1)
        self.assertAlmostEqual(niches[0]["x"]+niches[0]["w"]/2, 540, delta=.01)


class NightCropTests(unittest.TestCase):
    def test_detail_is_pixel_identical_to_original_crop_before_jpeg(self):
        day = LOADERS["olhe-de-novo"](PROJECT/"conteudo/olhe-de-novo.yaml")[0]
        original = PROJECT/day["obra"]["arquivo"]
        geometry = artwork_window(original, day["detalhe"], 640, 840)
        cropped = crop_image(original, geometry)
        self.assertEqual(cropped.size, (608, 824))
        with Image.open(original) as source:
            expected = source.convert('RGB').crop((396, 2440, 1004, 3264))
        self.assertIsNone(ImageChops.difference(expected, cropped.convert('RGB')).getbbox())

    def test_cover_crop_is_capped_at_twice_the_internal_area(self):
        day = LOADERS["olhe-de-novo"](PROJECT/"conteudo/olhe-de-novo.yaml")[0]
        original = PROJECT/day["obra"]["arquivo"]
        geometry = artwork_window(original, day["obra"], 640, 840)
        cropped = crop_image(original, geometry)
        self.assertEqual(cropped.size, (1216, 1648))

    def test_prepared_jpegs_keep_the_required_dimensions_without_chroma_subsampling(self):
        day = LOADERS["olhe-de-novo"](PROJECT/"conteudo/olhe-de-novo.yaml")[0]
        with tempfile.TemporaryDirectory(dir=PROJECT/"work") as temporary:
            artworks = prepare_artworks("olhe-de-novo", day, Path(temporary))
            by_card = {(item["card"], item["indice"]): item for item in artworks}
            for key, size in (((1, 1), (1216, 1648)), ((2, 1), (608, 824))):
                with self.subTest(card=key[0]), Image.open(PROJECT/by_card[key]["arquivo_recortado"]) as image:
                    self.assertEqual(image.format, 'JPEG')
                    self.assertEqual(image.size, size)
                    self.assertEqual(JpegImagePlugin.get_sampling(image), 0)


if __name__ == "__main__":
    unittest.main()
