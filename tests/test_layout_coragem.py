"""Coragem: limites e distâncias medidos no Chromium real."""

from copy import deepcopy
from pathlib import Path
import shutil
import tempfile
import unittest
from urllib.parse import urlsplit

from PIL import Image
from playwright.sync_api import sync_playwright

from gerar import ensure_kit
from arteque_reza.base import PROJECT, await_fonts, generate_tokens_css, render_arte, resource_url
from arteque_reza.conteudo import local_artwork_path
from arteque_reza.conteudo_coragem import load_courage
from arteque_reza.coragem import _document, _measure, _pdf_check, _recommendation, _validate_layout
from arteque_reza.obras import inspect_artwork
from arteque_reza.renderizacao import local_server


@unittest.skipUnless(shutil.which('chromium'), 'Chromium é necessário para medir o layout real')
class CourageLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_kit()
        work = PROJECT/'work'; work.mkdir(exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(dir=work)
        cls.addClassCleanup(cls.temp.cleanup)
        cls.folder = Path(cls.temp.name)
        cls.css = generate_tokens_css(cls.folder/'tokens.css')
        cls.server = local_server(); cls.url = cls.server.__enter__()
        cls.addClassCleanup(cls.server.__exit__, None, None, None)
        cls.playwright = sync_playwright().start(); cls.addClassCleanup(cls.playwright.stop)
        cls.browser = cls.playwright.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
        cls.addClassCleanup(cls.browser.close)
        cls.context = cls.browser.new_context(device_scale_factor=1)
        cls.addClassCleanup(cls.context.close)
        cls.context.route('**/*', lambda route: route.continue_()
            if urlsplit(route.request.url).netloc == urlsplit(cls.url).netloc else route.abort())
        cls.page = cls.context.new_page()
        cls.days = load_courage(PROJECT/'conteudo/coragem.yaml')

    def render(self, day, format_name='feed'):
        self.page.set_viewport_size({'width': 1080, 'height': 1920 if format_name == 'status' else 1350})
        path = self.folder/'card.html'
        path.write_text(_document(day, self.css, local_artwork_path(day['obra']['arquivo']), format_name), encoding='utf-8')
        self.page.goto(self.url+resource_url(path)); await_fonts(self.page)
        return _measure(self.page, format_name)

    def test_supplied_phrases_and_distances_fit_both_formats(self):
        for day in self.days:
            for name, distances in [('feed', (66, 69)), ('status', (81, 84))]:
                with self.subTest(date=day['data'], format=name):
                    card = self.render(day, name)
                    result = _validate_layout(day, card)
                    self.assertTrue(result['ok'])
                    self.assertEqual(result['parapeito_frase_px'], distances[0])
                    self.assertEqual(result['referencia_assinatura_px'], distances[1])
                    texts = {text['campo']: text for text in card['textos']}
                    self.assertEqual(texts['frase']['quantidade_linhas'], 2)
                    self.assertEqual(texts['referencia']['quantidade_linhas'], 1)

    def test_three_line_phrase_is_rejected_in_each_format(self):
        for name in ('feed', 'status'):
            with self.subTest(format=name):
                day = deepcopy(self.days[0]); day['frase'] = 'Primeira frase\nSegunda frase\nTerceira frase'
                with self.assertRaisesRegex(ValueError, f'2026-12-14, {name}, frase: 3 linhas; limite 2'):
                    _validate_layout(day, self.render(day, name))

    def test_reference_is_free_text_but_must_stay_on_one_line(self):
        day = deepcopy(self.days[0]); day['referencia'] = 'Carta de um santo'
        self.assertTrue(_validate_layout(day, self.render(day))['ok'])
        day['referencia'] = 'Carta de um santo\nSegunda linha'
        with self.assertRaisesRegex(ValueError, '2026-12-14, feed, referencia: 2 linhas; limite 1'):
            _validate_layout(day, self.render(day))

    def test_manual_break_cannot_leave_one_letter_word_at_line_end(self):
        day = deepcopy(self.days[0]); day['frase'] = 'Vigiai e\nrezai sempre'
        with self.assertRaisesRegex(ValueError, 'frase: palavra de uma letra no fim'):
            _validate_layout(day, self.render(day))

    def test_phrase_cannot_touch_the_niche_sill(self):
        day = self.days[0]; self.render(day)
        self.page.locator('.aqr-texto').evaluate("el => el.style.transform='translateY(-50px)'")
        with self.assertRaisesRegex(ValueError, 'frase: distância ao parapeito 16.00px < 32px'):
            _validate_layout(day, _measure(self.page, 'feed'))

    def test_reference_must_keep_32_pixels_from_signature(self):
        day = self.days[0]; self.render(day)
        self.page.locator('.aqr-assinatura').evaluate("el => el.style.transform='translateY(-50px)'")
        with self.assertRaisesRegex(ValueError, 'referencia: distância à assinatura 19.00px < 32px'):
            _validate_layout(day, _measure(self.page, 'feed'))

    def test_unbroken_phrase_cannot_escape_the_art(self):
        day = deepcopy(self.days[0]); day['frase'] = 'Amém'*60
        with self.assertRaisesRegex(ValueError, 'frase: texto fora da arte'):
            _validate_layout(day, self.render(day))

    def test_margin_recommendation_removes_visible_uniform_border(self):
        # A landscape photo makes its 40px top border visible before zoom.
        art = self.folder/'painting.png'; width, height = 400, 300
        pixels = bytearray()
        for y in range(height):
            for x in range(width):
                pixels.extend((180, 180, 180) if y < 40 else
                    ((x*37+y*73)%256, (x*17+y*41)%256, (x*61+y*23)%256))
        Image.frombytes('RGB', (width, height), bytes(pixels)).save(art)
        before = inspect_artwork(art, '50% 50%', niche_width=600, niche_height=680)
        self.assertIn('topo', before['margens_visiveis'])
        recommendation = _recommendation(art, '50% 50%', 1, (600, 680), before)
        self.assertIsNotNone(recommendation)
        self.assertGreater(recommendation['zoom'], 1)
        self.assertLessEqual(recommendation['zoom'], 3)
        after = inspect_artwork(art, recommendation['foco'], recommendation['zoom'], niche_width=600, niche_height=680)
        self.assertEqual(after['margens_visiveis'], [])

    def test_pdf_text_matches_the_complete_expected_text_in_both_readers(self):
        day = self.days[0]; artwork = local_artwork_path(day['obra']['arquivo'])
        for format_name, base_format in [('feed', 'feed'), ('status', 'story')]:
            with self.subTest(format=format_name):
                pdf = self.folder/f'exact-{format_name}.pdf'
                render_arte(self.page, _document(day, self.css, artwork, format_name),
                    pdf.with_suffix('.png'), formato=base_format, pdf_path=pdf, base_url=self.url)
                result = _pdf_check(pdf, day, _measure(self.page, format_name))
                self.assertTrue(result['igualdade_texto_integral']['pymupdf'])
                self.assertTrue(result['igualdade_texto_integral']['pdftotext'])

    def test_pdf_rejects_extra_unmarked_text_with_all_expected_fields_and_fonts_present(self):
        day = self.days[0]; measured = self.render(day)
        markup = _document(day, self.css, local_artwork_path(day['obra']['arquivo']), 'feed')
        # An unmarked text run remains invisible to the expected-text metadata,
        # while Chromium embeds it with the same Lato font already used above.
        extra = '<span style="position:absolute;left:80px;top:1200px;font:400 24px Lato">Texto extra</span>'
        markup = markup.replace('</article>', extra+'</article>')
        pdf = self.folder/'extra.pdf'
        render_arte(self.page, markup, pdf.with_suffix('.png'), pdf_path=pdf, base_url=self.url)
        with self.assertRaisesRegex(ValueError, 'texto integral do PDF difere do conteúdo esperado'):
            _pdf_check(pdf, day, measured)


if __name__ == '__main__':
    unittest.main()
