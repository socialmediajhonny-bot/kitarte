"""Novenas: layout real, refrão unido à oração e rejeição de artes inválidas."""

from copy import deepcopy
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

from gerar import ensure_kit
from arteque_reza.base import (
    PROJECT, await_fonts, generate_tokens_css, render_arte, resource_url,
)
from arteque_reza.conteudo_novena import load_novenas
from arteque_reza.novena import (
    _document, _measure, _pdf_check, _pixels, _validate_layout, expand_cards,
)
from arteque_reza.renderizacao import local_server


def compact(value):
    return re.sub(r"\s+", "", value)


@unittest.skipUnless(shutil.which("chromium"), "Chromium é necessário para medir o layout real")
class NovenaLayoutTests(unittest.TestCase):
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
            executable_path=shutil.which("chromium"), args=["--no-sandbox"])
        cls.addClassCleanup(cls.browser.close)
        cls.context = cls.browser.new_context(
            device_scale_factor=1, viewport={"width": 1080, "height": 1350})
        cls.addClassCleanup(cls.context.close)
        cls.context.route("**/*", lambda route: route.continue_()
            if urlsplit(route.request.url).netloc == urlsplit(cls.url).netloc else route.abort())
        cls.page = cls.context.new_page()
        cls.novenas = load_novenas(PROJECT / "conteudo/novenas.yaml")
        cls.cards = expand_cards(cls.novenas)

    def card(self, novena="imaculada", numero=1, encerramento=False):
        return next(card for card in self.cards
            if card["novena"] == novena and card["numero"] == numero
            and card["encerramento"] == encerramento)

    def render(self, card):
        path = self.folder / "card.html"
        path.write_text(_document(card, self.css), encoding="utf-8")
        self.page.goto(self.url + resource_url(path))
        await_fonts(self.page)
        return _measure(self.page, card)

    def geometry(self):
        return self.page.evaluate("""() => {
          const a=document.querySelector('.aqr-post').getBoundingClientRect();
          const box=sel=>{const n=document.querySelector(sel);if(!n)return null;
            const r=n.getBoundingClientRect();return {x:r.x-a.x,y:r.y-a.y,w:r.width,h:r.height};};
          const text={};for(const n of document.querySelectorAll('[data-text]'))
            text[n.dataset.text]=box('[data-text="'+n.dataset.text+'"]');
          return {text,seal:box('.aqr-selo'),block:box('.aqr-texto'),
            signature:box('.aqr-assinatura'),ornament:box('.aqr-ornamento'),
            beads:box('[data-element="contas"]')};
        }""")

    def assert_gap(self, first, second, expected):
        self.assertAlmostEqual(second["y"]-first["y"]-first["h"], expected, delta=.01)

    def assert_art_rejected(self, card, expression):
        """Aceite que uma cor inválida seja detectada no DOM ou nos pixels."""
        with self.assertRaisesRegex(ValueError, expression):
            measured = _measure(self.page, card)
            _validate_layout(card, measured)
            path = self.folder / "invalid.png"
            self.page.screenshot(path=str(path),
                clip=self.page.locator(".aqr-post").bounding_box(), animations="disabled")
            _pixels(path, card, measured)

    def test_all_twenty_cards_have_required_gaps_centering_and_single_prayer(self):
        self.assertEqual(len(self.cards), 20)
        for card in self.cards:
            with self.subTest(novena=card["novena"], slug=card["slug"]):
                measured = self.render(card)
                self.assertTrue(_validate_layout(card, measured)["ok"])
                geometry = self.geometry()
                texts = geometry["text"]
                self.assert_gap(texts["contagem"], texts["titulo"], 48)
                if "fonte" in card:
                    self.assert_gap(texts["titulo"], texts["fonte"], 32)
                    self.assert_gap(texts["fonte"], geometry["ornament"], 48)
                else:
                    self.assert_gap(texts["titulo"], geometry["ornament"], 48)
                self.assert_gap(geometry["ornament"], texts["oracao"], 48)
                self.assert_gap(texts["oracao"], geometry["beads"], 48)
                above = geometry["block"]["y"]-geometry["seal"]["y"]-geometry["seal"]["h"]
                below = geometry["signature"]["y"]-geometry["block"]["y"]-geometry["block"]["h"]
                self.assertGreaterEqual(above, 60)
                self.assertGreaterEqual(below, 60)
                self.assertAlmostEqual(above, below, delta=.01)
                fields = {text["campo"]: text for text in measured["textos"]}
                self.assertLessEqual(fields["titulo"]["quantidade_linhas"], 2)
                self.assertLessEqual(fields["oracao"]["quantidade_linhas"], 8)
                self.assertNotIn("refrao", fields)
                prayer = self.page.locator('[data-text="oracao"]')
                self.assertEqual(prayer.evaluate("el=>el.tagName"), "P")
                self.assertEqual(prayer.locator("em[data-refrao]").count(), 1)
                self.assertEqual(compact(prayer.inner_text()), compact(card["oracao"]+card["refrao"]))
                self.assertEqual(prayer.evaluate("el=>getComputedStyle(el).lineHeight"), "62px")
                for word in self.page.locator(".novena-sem-quebra").all():
                    self.assertRegex(word.inner_text(), r"^\w+(?:-\w+)+$")
                    self.assertEqual(word.evaluate("el=>getComputedStyle(el).whiteSpace"), "nowrap")

    def test_16_pixel_counter_title_gap_is_rejected(self):
        card = self.card()
        self.render(card)
        self.page.locator('[data-text="contagem"]').evaluate("el=>el.style.marginBottom='0px'")
        geometry = self.geometry()
        self.assert_gap(geometry["text"]["contagem"], geometry["text"]["titulo"], 16)
        with self.assertRaisesRegex(ValueError, r"contagem.*titulo.*16.*48"):
            _validate_layout(card, _measure(self.page, card))

    def test_16_pixel_title_source_gap_is_rejected(self):
        card = self.card()
        self.render(card)
        self.page.locator('[data-text="fonte"]').evaluate("el=>el.style.marginTop='0px'")
        geometry = self.geometry()
        self.assert_gap(geometry["text"]["titulo"], geometry["text"]["fonte"], 16)
        with self.assertRaisesRegex(ValueError, r"titulo.*fonte.*16.*32"):
            _validate_layout(card, _measure(self.page, card))

    def test_refrain_on_the_same_line_as_the_prayer_is_rejected(self):
        card = deepcopy(self.card())
        card["oracao"] = "Maria."
        self.render(card)
        self.page.locator('[data-text="oracao"]').evaluate("""el=>{
          const em=el.querySelector('em[data-refrao]');
          el.replaceChildren(document.createTextNode('Maria. '),em);
        }""")
        with self.assertRaisesRegex(ValueError, r"refrão"):
            _validate_layout(card, _measure(self.page, card))

    def test_marian_refrain_must_break_after_the_comma(self):
        card = self.card()
        self.render(card)
        self.page.locator("em[data-refrao]").evaluate("""el=>{
          el.innerHTML='Ó Maria concebida sem<br>pecado, rogai por nós que recorremos a vós.';
        }""")
        with self.assertRaisesRegex(ValueError, r"refrão"):
            _validate_layout(card, _measure(self.page, card))

    def test_marian_refrain_has_two_marked_lines_and_italic_type(self):
        for card in (self.card(), self.card(numero=9, encerramento=True)):
            with self.subTest(slug=card["slug"]):
                measured = self.render(card)
                refrain = measured["refrao"]
                self.assertEqual(len(refrain["linhas"]), 2)
                self.assertTrue(refrain["linhas"][0].endswith("pecado,"))
                self.assertTrue(refrain["em_linha_propria"])
                prayer = next(text for text in measured["textos"] if text["campo"] == "oracao")
                self.assertEqual(prayer["linhas_de_refrao"][-2:], [True, True])
                self.assertEqual(sum(prayer["linhas_de_refrao"]), 2)
                styles = self.page.locator("em[data-refrao]").evaluate("""el=>{
                  const s=getComputedStyle(el);return [s.fontFamily,s.fontWeight,s.fontStyle,s.color];
                }""")
                self.assertIn("Cormorant Garamond", styles[0])
                self.assertEqual(styles[1:3], ["500", "italic"])
                self.assertEqual(styles[3], "rgb(250, 246, 238)" if card["encerramento"] else "rgb(102, 86, 71)")

    def test_refrain_without_italic_is_rejected(self):
        card = self.card()
        self.render(card)
        self.page.locator("em[data-refrao]").evaluate("el=>el.style.fontStyle='normal'")
        with self.assertRaisesRegex(ValueError, r"refrão"):
            _validate_layout(card, _measure(self.page, card))

    def test_manual_line_ending_in_hyphen_is_rejected(self):
        card = self.card()
        self.render(card)
        self.page.locator('[data-text="oracao"]').evaluate("""el=>{
          const em=el.querySelector('em[data-refrao]');
          el.innerHTML='Maria, ajudai-<br>nos a rezar.<br>';
          el.append(em);
        }""")
        measured = _measure(self.page, card)
        self.assertTrue(any(line.rstrip().endswith("-")
            for text in measured["textos"] for line in text["linhas"]))
        with self.assertRaisesRegex(ValueError, r"hífen"):
            _validate_layout(card, measured)

    def test_beads_have_nine_positions_and_expected_fill(self):
        for card in (self.card(numero=1), self.card(numero=8), self.card(numero=9, encerramento=True)):
            with self.subTest(slug=card["slug"]):
                self.render(card)
                actual = self.page.locator('[data-element="contas"]').evaluate("""el=>({
                  width:el.getBoundingClientRect().width,height:el.getBoundingClientRect().height,
                  label:el.getAttribute('aria-label'), circles:[...el.querySelectorAll('circle')].map(n=>{
                    const s=getComputedStyle(n);return {x:+n.getAttribute('cx'),y:+n.getAttribute('cy'),
                      radius:+n.getAttribute('r'),fill:s.fill,stroke:s.stroke,width:parseFloat(s.strokeWidth)};
                  })})""")
                self.assertEqual((actual["width"], actual["height"]), (306,18))
                self.assertEqual(actual["label"], f'Dia {card["numero"]} de 9')
                self.assertEqual(len(actual["circles"]), 9)
                color = "rgb(250, 246, 238)" if card["encerramento"] else "rgb(134, 100, 32)"
                for index, circle in enumerate(actual["circles"]):
                    self.assertEqual((circle["x"],circle["y"]), (9+36*index,9))
                    self.assertEqual(circle["radius"], 9 if index < card["numero"] else 7.75)
                    if index < card["numero"]:
                        self.assertEqual(circle["fill"], color)
                    else:
                        self.assertEqual(circle["fill"], "none")
                        self.assertEqual(circle["stroke"], color)
                        self.assertEqual(circle["width"], 2.5)

    def test_beads_reject_wrong_quantity_fill_and_color(self):
        mutations = (
            "svg=>svg.lastElementChild.remove()",
            "svg=>svg.querySelector('circle').setAttribute('fill','none')",
            "svg=>svg.querySelector('circle').setAttribute('fill','#ff0000')",
        )
        card = self.card()
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.render(card)
                self.page.locator('[data-element="contas"]').evaluate(mutation)
                self.assert_art_rejected(card, r"contas")

    def test_daily_cross_is_purple_even_on_liturgically_different_dates(self):
        for date in ("2026-11-30", "2026-12-03", "2026-12-07"):
            card = next(card for card in self.cards if card["data"]==date)
            with self.subTest(date=date):
                self.render(card)
                self.assertEqual(self.page.locator('.aqr-selo__cruz').evaluate(
                    "el=>getComputedStyle(el).color"), "rgb(91, 46, 112)")
                self.assertTrue(_validate_layout(card, _measure(self.page, card))["ok"])
        card = next(card for card in self.cards if card["data"]=="2026-11-30")
        self.render(card)
        self.page.locator('.aqr-selo__cruz').evaluate("el=>el.style.color='#ff0000'")
        self.assert_art_rejected(card, r"cruz")

    def test_closing_card_requires_whole_gold_background_and_light_ink(self):
        for name in ("imaculada", "natal"):
            card = self.card(name, numero=9, encerramento=True)
            with self.subTest(novena=name):
                self.render(card)
                actual = self.page.locator('.aqr-post').evaluate("el=>getComputedStyle(el).backgroundColor")
                self.assertEqual(actual, "rgb(134, 100, 32)")
                self.assertTrue(self.page.locator('.aqr-assinatura img').get_attribute('src').endswith('logo-horizontal-sobre-cor.svg'))
                for node in self.page.locator('[data-text]').all():
                    self.assertEqual(node.evaluate("el=>getComputedStyle(el).color"), "rgb(250, 246, 238)")
                self.page.locator('.aqr-post').evaluate("el=>el.style.backgroundColor='var(--fundo)'")
                self.assert_art_rejected(card, r"fundo")

    def test_christmas_closing_replaces_the_usual_refrain(self):
        card = self.card("natal", numero=9, encerramento=True)
        self.render(card)
        text = self.page.locator('[data-text="oracao"]').inner_text()
        self.assertIn(compact("Glória a Deus nas alturas!"), compact(text))
        self.assertNotIn(compact("Vinde, Senhor Jesus!"), compact(text))
        self.assertEqual(self.page.locator('[data-text="fonte"]').inner_text(), "Jo 1,14")

    def test_pdf_matches_full_text_and_rejects_an_extra_unmarked_run(self):
        card = self.card()
        markup = _document(card, self.css)
        pdf = self.folder / "novena.pdf"
        render_arte(self.page, markup, pdf.with_suffix('.png'), pdf_path=pdf, base_url=self.url)
        measured = _measure(self.page, card)
        self.assertTrue(_pdf_check(pdf, [card], [measured])["ok"])
        extra = '<span style="position:absolute;left:80px;top:1220px;font:400 24px Lato">Texto extra</span>'
        altered = self.folder / "extra.pdf"
        render_arte(self.page, markup.replace('</article>', extra+'</article>'),
            altered.with_suffix('.png'), pdf_path=altered, base_url=self.url)
        with self.assertRaisesRegex(ValueError, r"texto.*(?:difere|diferente)|PDF.*texto"):
            _pdf_check(altered, [card], [measured])


if __name__ == "__main__":
    unittest.main()
