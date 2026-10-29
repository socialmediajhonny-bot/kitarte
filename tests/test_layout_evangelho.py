"""Regressões de limites visuais medidos no Chromium, inclusive linhas vazias."""

from copy import deepcopy
from pathlib import Path
import shutil
import tempfile
import unittest

from playwright.sync_api import sync_playwright

from gerar import ensure_kit
from arteque_reza.base import PROJECT, await_fonts, generate_tokens_css, render_arte, resource_url
from arteque_reza.conteudo import load_content
from arteque_reza.evangelho import _document, _measure, _validate_layout
from arteque_reza.renderizacao import local_server


@unittest.skipUnless(shutil.which("chromium"), "Chromium é necessário para medir as linhas reais")
class LayoutTests(unittest.TestCase):
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
        cls.page = cls.browser.new_page(viewport={"width": 1080, "height": 1350})
        cls.days = load_content(PROJECT / "conteudo/evangelho.yaml")
        cls.base = cls.days[0]

    def measure(self, day, kind):
        path = self.folder / "card.html"
        path.write_text(_document(day, kind, self.css, PROJECT / "saida/obra-provisoria.png"))
        self.page.goto(self.url + resource_url(path))
        await_fonts(self.page)
        return _measure(self.page, kind, kind)

    def measure_reflection(self, day):
        return self.measure(day, 3)

    def test_canva_pairs_and_centered_blocks_on_both_dates(self):
        for day in self.days:
            for kind, expected in ((2, 32), (3, 48), (4, 48)):
                with self.subTest(data=day['data'], card=kind):
                    result = _validate_layout(day, self.measure(day, kind))
                    self.assertAlmostEqual(result['par_canva']['distancia_px'], expected, places=2)
                    self.assertLessEqual(result['centralizacao_vertical']['diferenca_px'], 0.1)

    def assert_old_gap_rejected(self, kind, field, margin):
        self.measure(self.base, kind)
        self.page.locator(f'[data-text="{field}"]').evaluate(
            '(node, margin) => node.style[margin] = "0px"', margin)
        card = _measure(self.page, kind, kind)
        with self.assertRaisesRegex(ValueError, rf'card {kind}: distância entre .* 16\.00px; esperado'):
            _validate_layout(self.base, card)

    def test_card_2_rejects_old_16px_pair(self):
        self.assert_old_gap_rejected(2, 'trecho_ref', 'marginTop')

    def test_card_3_rejects_old_16px_pair(self):
        self.assert_old_gap_rejected(3, 'chamada_reflexao', 'marginBottom')

    def test_card_4_rejects_old_16px_pair(self):
        self.assert_old_gap_rejected(4, 'chamada_oracao', 'marginBottom')

    def test_empty_forced_line_counts_toward_title_limit(self):
        day = deepcopy(self.base)
        day["reflexao"]["titulo"] = "A Igreja\n\nespera"
        card = self.measure_reflection(day)
        title = next(text for text in card["textos"] if text["campo"] == "reflexao.titulo")
        self.assertEqual(title["linhas"], ["A\u00a0Igreja", "", "espera"])
        with self.assertRaisesRegex(ValueError, r"2026-11-29, card 3, reflexao.titulo: 3 linhas; limite 2"):
            _validate_layout(day, card)

    def test_unbroken_word_cannot_escape_body_width(self):
        day = deepcopy(self.base)
        day["reflexao"]["texto"] = "Amém" * 60
        with self.assertRaisesRegex(ValueError, r"2026-11-29, card 3, reflexao.texto: linha transborda"):
            _validate_layout(day, self.measure_reflection(day))

    def test_same_path_rerender_uses_smaller_verse_style(self):
        day = deepcopy(self.base)
        day["trecho"] = "Primeira frase\nSegunda frase\nTerceira frase\nQuarta frase"
        for style in ("citacao-grande", "citacao"):
            render_arte(
                self.page,
                _document(day, 2, self.css, PROJECT / "saida/obra-provisoria.png", style),
                self.folder / "verse.png", base_url=self.url,
            )
            card = _measure(self.page, 2, 2)
            verse = next(text for text in card["textos"] if text["campo"] == "trecho")
            self.assertEqual(verse["estilo"], style)
            self.assertEqual(verse["quantidade_linhas"], 4)
        self.assertTrue(_validate_layout(day, card)["ok"])
