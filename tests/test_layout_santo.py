"""Limites dos dois modelos medidos no Chromium, incluindo falhas de geometria."""

from copy import deepcopy
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

from gerar import ensure_kit
from arteque_reza.base import PROJECT, await_fonts, generate_tokens_css, resource_url
from arteque_reza.conteudo import local_artwork_path
from arteque_reza.conteudo_santo import load_saints
from arteque_reza.renderizacao import local_server
from arteque_reza.santo import _document, _measure, _validate_layout


@unittest.skipUnless(shutil.which("chromium"), "Chromium é necessário para medir o layout real")
class SaintLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_kit()
        work = PROJECT / "work"
        work.mkdir(exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(dir=work)
        cls.addClassCleanup(cls.temp.cleanup)
        cls.folder = Path(cls.temp.name)
        cls.css = generate_tokens_css(cls.folder / "tokens.css")
        cls.server = local_server()
        cls.url = cls.server.__enter__()
        cls.addClassCleanup(cls.server.__exit__, None, None, None)
        cls.playwright = sync_playwright().start()
        cls.addClassCleanup(cls.playwright.stop)
        cls.browser = cls.playwright.chromium.launch(
            executable_path=shutil.which("chromium"), args=["--no-sandbox"]
        )
        cls.addClassCleanup(cls.browser.close)
        cls.context = cls.browser.new_context(
            device_scale_factor=1, viewport={"width": 1080, "height": 1350}
        )
        cls.addClassCleanup(cls.context.close)
        cls.context.route(
            "**/*",
            lambda route: route.continue_()
            if urlsplit(route.request.url).netloc == urlsplit(cls.url).netloc
            else route.abort(),
        )
        cls.page = cls.context.new_page()
        cls.days = load_saints(PROJECT / "conteudo/santo-do-dia.yaml")
        cls.saint = cls.days[0]
        cls.feast = cls.days[2]

    def render(self, day):
        artwork = local_artwork_path(day["obra"]["arquivo"])
        if not artwork.is_file():
            artwork = PROJECT / "saida/obra-provisoria.png"
        path = self.folder / "card.html"
        path.write_text(_document(day, self.css, artwork), encoding="utf-8")
        self.page.goto(self.url + resource_url(path))
        await_fonts(self.page)
        return _measure(self.page, day)

    @staticmethod
    def field(card, name):
        return next(text for text in card["textos"] if text["campo"] == name)

    def test_supplied_days_fit_their_real_rendered_models(self):
        for day in self.days:
            with self.subTest(date=day["data"], kind=day["tipo"]):
                self.assertTrue(_validate_layout(day, self.render(day))["ok"])

    def test_each_editorial_line_limit_reports_its_date_and_field(self):
        cases = (
            (self.saint, "nome", 1),
            (self.saint, "titulo", 1),
            (self.saint, "frase", 3),
            (self.saint, "fonte", 1),
            (self.feast, "nome", 2),
            (self.feast, "credito", 1),
        )
        for example, field, limit in cases:
            with self.subTest(date=example["data"], field=field):
                day = deepcopy(example)
                target = day["obra"] if field == "credito" else day
                target[field] = "\n".join(["Linha de texto"] * (limit + 1))
                card = self.render(day)
                self.assertEqual(self.field(card, field)["quantidade_linhas"], limit + 1)
                expected = f'{day["data"]}, {field}: {limit + 1} linhas; limite {limit}'
                with self.assertRaisesRegex(ValueError, re.escape(expected)):
                    _validate_layout(day, card)

    def test_blank_forced_lines_also_count_toward_the_quote_limit(self):
        day = deepcopy(self.saint)
        day["frase"] = "Primeira frase\n\nOutra frase\nÚltima frase"
        card = self.render(day)
        quote = self.field(card, "frase")
        self.assertEqual(quote["quantidade_linhas"], 4)
        self.assertEqual(quote["linhas"][1], "")
        with self.assertRaisesRegex(ValueError, r"2026-11-30, frase: 4 linhas; limite 3"):
            _validate_layout(day, card)

    def test_unbroken_words_cannot_escape_either_model(self):
        for example, field in ((self.saint, "frase"), (self.feast, "nome")):
            with self.subTest(kind=example["tipo"], field=field):
                day = deepcopy(example)
                day[field] = "Amém" * 60
                card = self.render(day)
                text = self.field(card, field)
                self.assertGreater(text["caixas_das_linhas"][0]["largura"], text["caixa"]["largura"])
                expected = f'{day["data"]}, {field}: linha transborda a largura do campo'
                with self.assertRaisesRegex(ValueError, re.escape(expected)):
                    _validate_layout(day, card)

    def test_a_manual_break_cannot_leave_a_one_letter_word_at_line_end(self):
        day = deepcopy(self.saint)
        day["frase"] = "Vigiai e\nrezai sempre"
        card = self.render(day)
        self.assertEqual(self.field(card, "frase")["linhas"][0], "“Vigiai e")
        with self.assertRaisesRegex(ValueError, r"2026-11-30, frase: palavra de uma letra no fim"):
            _validate_layout(day, card)

    def test_content_cannot_enter_the_padding_or_touch_the_inner_frame(self):
        for boundary, diagnostic in (
            ("padding", "conteúdo fora da área interna do cartão descontado o padding"),
            ("frame", "conteúdo encosta no filete interno"),
        ):
            with self.subTest(boundary=boundary):
                day = deepcopy(self.saint)
                self.assertTrue(_validate_layout(day, self.render(day))["ok"])
                # Move the actual niche on the page. Keep the text content and
                # measurement routine intact so the validator sees real bounds.
                observed = self.page.evaluate("""boundary => {
                    const card = document.querySelector('.aqr-santinho');
                    const niche = card.querySelector('.aqr-nicho');
                    const c = card.getBoundingClientRect(), n = niche.getBoundingClientRect();
                    const s = getComputedStyle(card), frame = getComputedStyle(card, '::before');
                    const innerLeft = c.left + parseFloat(s.borderLeftWidth) + parseFloat(s.paddingLeft);
                    const frameLeft = c.left + parseFloat(s.borderLeftWidth) + parseFloat(frame.left);
                    const target = boundary === 'padding' ? innerLeft - 8 : frameLeft;
                    niche.style.transform = `translateX(${target - n.left}px)`;
                    return {left:niche.getBoundingClientRect().left, innerLeft, frameLeft};
                }""", boundary)
                self.assertLess(observed["left"], observed["innerLeft"])
                if boundary == "frame":
                    self.assertAlmostEqual(observed["left"], observed["frameLeft"], places=3)
                else:
                    self.assertGreater(observed["left"], observed["frameLeft"] + 1)
                expected = f'{day["data"]}, nicho: {diagnostic}'
                with self.assertRaisesRegex(ValueError, re.escape(expected)):
                    _validate_layout(day, _measure(self.page, day))

    def test_feast_name_must_keep_at_least_32_pixels_from_the_logo(self):
        day = deepcopy(self.feast)
        self.assertTrue(_validate_layout(day, self.render(day))["ok"])
        gap = self.page.evaluate("""() => {
            const name = document.querySelector('[data-text="nome"]').getBoundingClientRect();
            const logo = document.querySelector('[data-element="logo"]');
            const before = logo.getBoundingClientRect();
            logo.style.transform = `translateY(${name.bottom + 16 - before.top}px)`;
            return logo.getBoundingClientRect().top - name.bottom;
        }""")
        self.assertAlmostEqual(gap, 16, places=3)
        with self.assertRaisesRegex(ValueError, r"2026-12-08, nome: distância ao logo 16\.00px < 32px"):
            _validate_layout(day, _measure(self.page, day))


if __name__ == "__main__":
    unittest.main()
