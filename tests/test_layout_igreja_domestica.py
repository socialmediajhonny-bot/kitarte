"""Igreja Doméstica: geometria real e rejeição de artes que quebram as regras."""

from copy import deepcopy
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from urllib.parse import urlsplit

import fitz
from playwright.sync_api import sync_playwright

from gerar import ensure_kit
from arteque_reza.base import PROJECT, await_fonts, generate_tokens_css, render_arte, resource_url
from arteque_reza.conteudo import text_html
from arteque_reza.conteudo_igreja_domestica import load_domestic_church
from arteque_reza.igreja_domestica import (
    _document, _measure, _pdf_check, _pixels, _validate_layout, expand_cards,
)
from arteque_reza.renderizacao import local_server


def compact(value):
    return re.sub(r"\s+", "", value)


@unittest.skipUnless(shutil.which("chromium"), "Chromium é necessário para medir o layout real")
class DomesticChurchLayoutTests(unittest.TestCase):
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
        cls.days = load_domestic_church(PROJECT / "conteudo/igreja-domestica.yaml")
        cls.cards = expand_cards(cls.days)

    def card(self, kind, date="2026-11-29"):
        return next(card for card in self.cards if card["tipo"] == kind and card["data"] == date)

    def markup(self, card):
        artwork = PROJECT / card["obra"]["arquivo"] if card["tipo"] == "capa" else None
        return _document(card, self.css, artwork)

    def render(self, card):
        path = self.folder / "card.html"
        path.write_text(self.markup(card), encoding="utf-8")
        self.page.goto(self.url + resource_url(path))
        await_fonts(self.page)
        return _measure(self.page, card)

    @staticmethod
    def field(measured, name):
        return next(text for text in measured["textos"] if text["campo"] == name)

    def geometry(self):
        return self.page.evaluate("""() => {
          const a=document.querySelector('.aqr-post').getBoundingClientRect();
          const box=sel=>{const n=document.querySelector(sel);if(!n)return null;
            const r=n.getBoundingClientRect();return {x:r.x-a.x,y:r.y-a.y,w:r.width,h:r.height};};
          const texts={};for(const n of document.querySelectorAll('[data-text]'))
            texts[n.dataset.text]=box('[data-text="'+n.dataset.text+'"]');
          return {texts,seal:box('.aqr-selo'),block:box('.aqr-texto'),niche:box('.aqr-nicho'),
            signature:box('.aqr-assinatura'),ornament:box('.aqr-ornamento'),
            items:[...document.querySelectorAll('ol > li')].map(n=>{
              const r=n.getBoundingClientRect();return {x:r.x-a.x,y:r.y-a.y,w:r.width,h:r.height};})};
        }""")

    def assert_gap(self, first, second, expected):
        self.assertAlmostEqual(second["y"]-first["y"]-first["h"], expected, delta=.01)

    def test_all_seven_cards_have_required_gaps_limits_and_centering(self):
        self.assertEqual(len(self.cards), 7)
        for card in self.cards:
            with self.subTest(date=card["data"], card=card["numero"], kind=card["tipo"]):
                measured = self.render(card)
                self.assertTrue(_validate_layout(card, measured)["ok"])
                g = self.geometry(); fields = g["texts"]
                if card["tipo"] == "capa":
                    self.assert_gap(g["seal"], g["niche"], 32)
                    self.assert_gap(g["niche"], fields["credito"], 32)
                    self.assert_gap(fields["credito"], fields["titulo"], 48)
                    self.assert_gap(fields["titulo"], fields["apoio"], 32)
                    self.assertGreaterEqual(g["signature"]["y"]-fields["apoio"]["y"]-fields["apoio"]["h"], 32)
                    self.assertFalse(self.page.locator('.aqr-topo__info').count())
                else:
                    above = g["block"]["y"]-g["seal"]["y"]-g["seal"]["h"]
                    below = g["signature"]["y"]-g["block"]["y"]-g["block"]["h"]
                    self.assertAlmostEqual(above, below, delta=.1)
                    self.assertGreaterEqual(min(above, below), 60)
                    expected_counter = f'{card["numero"]}/{card["total"]}'
                    self.assertEqual(self.page.locator('.aqr-topo__info').inner_text(), expected_counter)
                    target = "pergunta" if card["tipo"] == "conversa" else "titulo"
                    self.assert_gap(fields["rotulo"], fields[target], 48)
                    self.assert_gap(fields[target], g["ornament"], 48)
                    if card["tipo"] == "passos":
                        self.assertEqual(len(g["items"]), len(card["itens"]))
                        self.assert_gap(g["ornament"], g["items"][0], 48)
                        for a, b in zip(g["items"], g["items"][1:]): self.assert_gap(a, b, 32)
                        self.assert_gap(g["items"][-1], fields["fonte"], 32)
                        for number in range(1, len(card["itens"])+1):
                            self.assertLessEqual(self.field(measured, f"item_{number}")["quantidade_linhas"], 3)
                    elif card["tipo"] == "oracao":
                        self.assert_gap(g["ornament"], fields["fala_1"], 48)
                        for number in range(1, len(card["falas"])):
                            self.assert_gap(fields[f"fala_{number}"], fields[f"fala_{number+1}"], 48)
                        if "origem" in card: self.assert_gap(fields[f'fala_{len(card["falas"])}'], fields["origem"], 32)
                        for number, speech in enumerate(card["falas"], 1):
                            if "aclamacao" in speech:
                                styles = self.page.locator(f'[data-text="fala_{number}"]').evaluate(
                                    'el=>{const s=getComputedStyle(el);return [s.fontFamily,s.fontWeight,s.fontStyle]}')
                                self.assertIn("Cormorant Garamond", styles[0])
                                self.assertEqual(styles[1:], ["500", "italic"])
                    else:
                        self.assert_gap(g["ornament"], fields["convite"], 48)
                        self.assertEqual(self.page.locator('.aqr-post').evaluate(
                            'el=>getComputedStyle(el).backgroundColor'), 'rgb(91, 46, 112)')

    def test_16_pixel_label_title_gap_is_rejected(self):
        for kind in ("passos", "oracao"):
            card = self.card(kind)
            with self.subTest(kind=kind):
                self.render(card)
                self.page.locator('[data-text="rotulo"]').evaluate("el=>el.style.marginBottom='0px'")
                fields = self.geometry()["texts"]
                self.assert_gap(fields["rotulo"], fields["titulo"], 16)
                with self.assertRaisesRegex(ValueError, r"rotulo.*titulo.*16.*48"):
                    _validate_layout(card, _measure(self.page, card))

    def test_16_pixel_rubric_prayer_gap_is_rejected(self):
        card = self.card("oracao"); self.render(card)
        self.page.locator('[data-text="fala_2"]').evaluate("el=>el.style.marginTop='0px'")
        fields = self.geometry()["texts"]
        self.assert_gap(fields["fala_1"], fields["fala_2"], 16)
        with self.assertRaisesRegex(ValueError, r"fala_1.*fala_2.*16.*48"):
            _validate_layout(card, _measure(self.page, card))

    def test_two_line_acclamation_is_rejected(self):
        card = deepcopy(self.card("oracao"))
        card["falas"][-1] = {"aclamacao": "Vinde, Senhor Jesus!\nVinde e ficai conosco!"}
        measured = self.render(card)
        self.assertEqual(self.field(measured, "fala_4")["quantidade_linhas"], 2)
        with self.assertRaisesRegex(ValueError, r"fala_4.*2 linhas.*1"):
            _validate_layout(card, measured)

    def test_optional_origin_follows_the_last_speech_by_32_pixels(self):
        card = deepcopy(self.card("oracao"))
        card["origem"] = "Texto escrito pela página."
        measured = self.render(card)
        self.assertTrue(_validate_layout(card, measured)["ok"])
        fields = self.geometry()["texts"]
        self.assert_gap(fields["fala_4"], fields["origem"], 32)
        self.assertEqual(self.field(measured, "origem")["quantidade_linhas"], 1)

    def test_four_line_list_item_is_rejected(self):
        card = deepcopy(self.card("passos"))
        card["itens"][0] = "Primeira linha.\nSegunda linha.\nTerceira linha.\nQuarta linha."
        measured = self.render(card)
        self.assertEqual(self.field(measured, "item_1")["quantidade_linhas"], 4)
        with self.assertRaisesRegex(ValueError, r"item_1.*4 linhas.*3"):
            _validate_layout(card, measured)

    def test_line_ending_in_book_abbreviation_or_ordinal_is_rejected(self):
        card = self.card("oracao")
        for html, ending, expression in (("Leiam Mc<br>13,33-37.", "Mc", r"livro|bíblic|Mc"),
                                          ("Acendam no 3º<br>domingo.", "3º", r"ordinal|3º")):
            with self.subTest(ending=ending):
                self.render(card)
                self.page.locator('[data-text="fala_1"]').evaluate('(el,html)=>el.innerHTML=html', html)
                measured = _measure(self.page, card)
                self.assertTrue(any(line.endswith(ending) for line in self.field(measured, "fala_1")["linhas"]))
                with self.assertRaisesRegex(ValueError, expression):
                    _validate_layout(card, measured)

    def test_broken_hyphenated_word_is_rejected(self):
        card = self.card("oracao"); self.render(card)
        self.page.locator('[data-text="fala_2"]').evaluate("el=>el.innerHTML='Senhor, ajudai-<br>nos a rezar.'")
        measured = _measure(self.page, card)
        self.assertTrue(any(line.endswith("-") for line in self.field(measured, "fala_2")["linhas"]))
        with self.assertRaisesRegex(ValueError, r"hífen"):
            _validate_layout(card, measured)

    def test_list_number_must_share_the_first_text_baseline(self):
        card = self.card("passos"); measured = self.render(card)
        for item in measured["lista"]:
            self.assertAlmostEqual(item["baseline_numero_px"], item["baseline_texto_px"], delta=.01)
        self.page.locator('[data-baseline="numero"]').first.evaluate("el=>el.style.transform='translateY(6px)'")
        measured = _measure(self.page, card)
        self.assertGreater(abs(measured["lista"][0]["baseline_numero_px"]-measured["lista"][0]["baseline_texto_px"]), 5)
        with self.assertRaisesRegex(ValueError, r"base"):
            _validate_layout(card, measured)

    def test_conversation_requires_the_whole_colored_card(self):
        card = self.card("conversa"); self.render(card)
        self.page.locator('.aqr-post').evaluate("el=>el.classList.remove('aqr-post--cor')")
        with self.assertRaisesRegex(ValueError, r"fundo|cor"):
            measured = _measure(self.page, card)
            _validate_layout(card, measured)
            path = self.folder / "invalid-conversa.png"
            self.page.screenshot(path=str(path), clip=self.page.locator('.aqr-post').bounding_box())
            _pixels(path, card, measured)

    def test_new_nonbreaking_rules_are_local_to_this_series(self):
        card = self.card("oracao"); self.render(card)
        reference = self.page.locator('[data-regra="referencia"]').first
        self.assertEqual(reference.inner_text(), "Mc\u00a013,33-37")
        self.assertEqual(reference.evaluate('el=>getComputedStyle(el).whiteSpace'), 'nowrap')
        self.render(self.card("passos"))
        ordinal = self.page.locator('[data-regra="ordinal"]').first
        self.assertEqual(ordinal.inner_text(), "3º\u00a0domingo")
        self.assertEqual(ordinal.evaluate('el=>getComputedStyle(el).whiteSpace'), 'nowrap')
        card = deepcopy(card); card["falas"][1] = {"oracao": "Senhor, ajudai-nos a rezar."}
        self.render(card)
        word = self.page.locator('[data-regra="hifen"]').filter(has_text="ajudai-nos").first
        self.assertEqual(word.inner_text(), "ajudai-nos")
        self.assertEqual(word.evaluate('el=>getComputedStyle(el).whiteSpace'), 'nowrap')
        self.assertEqual(text_html("Mc 13,33-37 e 3º domingo"), "Mc 13,33-37 e\u00a03º domingo")

    def test_pdf_preserves_all_text_and_rejects_an_extra_run(self):
        card = self.card("oracao")
        markup = self.markup(card)
        pdf = self.folder / "oracao.pdf"
        render_arte(self.page, markup, pdf.with_suffix('.png'), pdf_path=pdf, base_url=self.url)
        measured = _measure(self.page, card)
        self.assertTrue(_pdf_check(pdf, [card], [measured])["ok"])
        with fitz.open(pdf) as document:
            self.assertEqual(compact(document[0].get_text(sort=True)), compact(''.join(t['conteudo'] for t in measured['textos'])))
        extra = '<span style="position:absolute;left:80px;top:1280px;font:400 24px Lato">Texto extra</span>'
        altered = self.folder / "extra.pdf"
        render_arte(self.page, markup.replace('</article>', extra+'</article>'), altered.with_suffix('.png'), pdf_path=altered, base_url=self.url)
        with self.assertRaisesRegex(ValueError, r"texto|YAML"):
            _pdf_check(altered, [card], [measured])


if __name__ == "__main__":
    unittest.main()
