"""Render real das Antífonas, fontes, espaços e rejeição de artes inválidas."""
from copy import deepcopy
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import urlsplit

from PIL import Image
from playwright.sync_api import sync_playwright

from gerar import ensure_kit
from arteque_reza.base import PROJECT, await_fonts, generate_tokens_css, render_arte, resource_url
from arteque_reza.conteudo_noite import load_antiphons
from arteque_reza.noite import (
    _document, _measure, _pdf_check, _pixels, _validate_layout,
    artwork_window, expand_cards, expected_layout, prepare_artworks,
)
from arteque_reza.renderizacao import local_server
from arteque_reza.serie_noite import approval_date


@unittest.skipUnless(shutil.which('chromium'), 'Chromium é necessário para o render real')
class AntiphonLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_kit()
        cls.temp = tempfile.TemporaryDirectory(dir=PROJECT/'work')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.folder = Path(cls.temp.name)
        cls.css = generate_tokens_css(cls.folder/'tokens.css')
        cls.days = load_antiphons(PROJECT/'conteudo/antifonas.yaml')
        cls.cards = expand_cards('antifonas', cls.days)
        cls.artworks = {day['data']: prepare_artworks('antifonas', day, cls.folder/day['data'])
                        for day in cls.days}
        cls.server = local_server(); cls.url = cls.server.__enter__()
        cls.addClassCleanup(cls.server.__exit__, None, None, None)
        cls.playwright = sync_playwright().start(); cls.addClassCleanup(cls.playwright.stop)
        cls.browser = cls.playwright.chromium.launch(executable_path=shutil.which('chromium'),
                                                    args=['--no-sandbox'])
        cls.addClassCleanup(cls.browser.close)
        cls.context = cls.browser.new_context(device_scale_factor=1,
                                             viewport={'width': 1080, 'height': 1350})
        cls.addClassCleanup(cls.context.close)
        cls.context.route('**/*', lambda route: route.continue_()
                          if urlsplit(route.request.url).netloc == urlsplit(cls.url).netloc else route.abort())
        cls.page = cls.context.new_page()

    def render(self, card, *, style='titulo-capa'):
        path = self.folder/'card.html'
        path.write_text(_document(card, self.css, self.artworks[card['data']],
                                  invocation_style=style), encoding='utf-8')
        self.page.goto(self.url+resource_url(path)); await_fonts(self.page)
        return _measure(self.page, card)

    def test_all_eighteen_cards_match_the_preview_and_required_pixels(self):
        self.assertEqual(len(self.cards), 18)
        for card in self.cards:
            with self.subTest(date=card['data'], card=card['numero']):
                measured = self.render(card)
                checked = _validate_layout(card, measured)
                fields = {text['campo']: text for text in measured['textos']}
                expected = expected_layout(card)
                for field, count in expected['linhas'].items():
                    self.assertEqual(fields[field]['quantidade_linhas'], count)
                distances = checked['distancias']
                if 'folga_px' in expected:
                    self.assertAlmostEqual(distances['selo_texto_px'], expected['folga_px'], delta=.01)
                    self.assertAlmostEqual(distances['texto_assinatura_px'], expected['folga_px'], delta=.01)
                else:
                    self.assertAlmostEqual(distances['selo_nicho_px'], 32, delta=.01)
                    self.assertAlmostEqual(distances['titulo_assinatura_px'], 98, delta=.01)
                path = self.folder/'pixels.png'
                self.page.screenshot(path=str(path), clip=self.page.locator('.aqr-post').bounding_box())
                self.assertTrue(_pixels(path, card, measured)['ok'])
                if card['tipo'] == 'oracao':
                    text = fields['antifona']
                    self.assertEqual((text['tamanho_px'], text['entrelinha_px']), (44, 62))
                    self.assertEqual((text['fonte'], text['peso']), ('Cormorant Garamond', '500'))

    def test_fixed_series_name_is_the_only_one_letter_line_exception(self):
        card = self.cards[0]
        measured = self.render(card)
        self.assertTrue(_validate_layout(card, measured)['ok'])
        self.assertEqual(next(t for t in measured['textos'] if t['campo']=='selo')['linhas'],
                         ['Antífonas do Ó'])
        self.page.locator('[data-text="selo"]').evaluate("el=>el.innerHTML='Antífonas do<br>Ó'")
        with self.assertRaises(ValueError):
            _validate_layout(card, _measure(self.page, card))
        card = self.cards[2]
        self.render(card)
        self.page.locator('[data-text="antifona"]').evaluate("el=>el.innerHTML='Senhor Ó<br>Vinde salvar-nos.'")
        with self.assertRaisesRegex(ValueError, 'uma letra'):
            _validate_layout(card, _measure(self.page, card))

    def test_prayer_label_and_source_must_keep_48_and_32_pixels(self):
        card = self.cards[2]
        for field, css, expected in [('rotulo', 'marginBottom', 48), ('fonte', 'marginTop', 32)]:
            with self.subTest(field=field):
                self.render(card)
                self.page.locator(f'[data-text="{field}"]').evaluate('(el,key)=>el.style[key]="0px"', css)
                with self.assertRaisesRegex(ValueError, f'16.*{expected}'):
                    _validate_layout(card, _measure(self.page, card))

    def test_six_prayer_lines_and_two_source_lines_are_rejected(self):
        card = self.cards[2]
        for field, count in [('antifona', 6), ('fonte', 2)]:
            with self.subTest(field=field):
                self.render(card)
                self.page.locator(f'[data-text="{field}"]').evaluate(
                    '(el,count)=>el.innerHTML=Array(count).fill("Vinde, Senhor Jesus!").join("<br>")', count)
                with self.assertRaisesRegex(ValueError, field+'.*linhas'):
                    _validate_layout(card, _measure(self.page, card))

    def test_wrong_colored_background_and_logo_are_rejected(self):
        card = self.cards[2]
        self.render(card)
        self.page.locator('.aqr-post').evaluate('el=>el.style.backgroundColor="#ffffff"')
        with self.assertRaisesRegex(ValueError, 'fundo'):
            _validate_layout(card, _measure(self.page, card))
        self.render(card)
        logo = self.page.locator('[data-element="logo"]')
        self.assertEqual(logo.get_attribute('data-arquivo'), 'kit/logos/logo-horizontal-sobre-cor.svg')
        logo.evaluate("el=>el.setAttribute('data-arquivo','kit/logos/logo-horizontal-capela.svg')")
        self.assertEqual(logo.get_attribute('data-arquivo'), 'kit/logos/logo-horizontal-capela.svg')
        with self.assertRaisesRegex(ValueError, 'assinatura'):
            _validate_layout(card, _measure(self.page, card))

    def test_pdf_requires_embedded_fonts_exact_text_and_vector_niche(self):
        card = self.cards[0]
        png = self.folder/'pdf-card.png'; pdf = png.with_suffix('.pdf')
        render_arte(self.page, _document(card, self.css, self.artworks[card['data']]),
                    png, pdf_path=pdf, base_url=self.url)
        measured = _measure(self.page, card)
        check = _pdf_check(pdf, [card], [measured])
        self.assertTrue(check['ok']); self.assertTrue(check['nicho_vetorial']['ok'])
        import fitz
        extra = self.folder/'texto-a-mais.pdf'
        with fitz.open(pdf) as document:
            document[0].insert_text((40, 30), 'Texto extra')
            document.save(extra)
        with self.assertRaisesRegex(ValueError, 'texto|fonte'):
            _pdf_check(extra, [card], [measured])
        markup = _document(card, self.css, self.artworks[card['data']])
        altered, count = re.subn(r'<svg\b[^>]*data-element="nicho-filete"[^>]*>.*?</svg>',
                                 '', markup, flags=re.S)
        self.assertEqual(count, 1)
        without = self.folder/'sem-filete.pdf'
        render_arte(self.page, altered, without.with_suffix('.png'), pdf_path=without, base_url=self.url)
        with self.assertRaisesRegex(ValueError, 'nicho|filete|vetorial|preenchimento'):
            _pdf_check(without, [card], [measured])

    def test_long_cover_title_can_fall_back_to_two_lines(self):
        card = deepcopy(self.cards[0])
        card['titulo'] = 'Ó Sabedoria eterna, que governais todo o universo'
        first = self.render(card)
        self.assertGreater(next(t for t in first['textos'] if t['campo']=='titulo')['quantidade_linhas'], 1)
        measured = self.render(card, style='titulo')
        title = next(t for t in measured['textos'] if t['campo']=='titulo')
        self.assertEqual(title['estilo'], 'titulo')
        self.assertEqual(title['quantidade_linhas'], 2)
        self.assertTrue(_validate_layout(card, measured)['ok'])

    def test_artwork_missing_is_pending_and_wrong_original_size_stops(self):
        day = deepcopy(self.days[0]); day['obra']['arquivo']='obras/antifonas/ausente-teste.jpg'
        art = prepare_artworks('antifonas', day, self.folder/'pending')[0]
        self.assertTrue(art['obra_pendente'])
        self.assertEqual(art['arquivo_usado'], 'saida/obra-provisoria.png')
        fake = self.folder/'dimension-root'; path=fake/'obras/antifonas/2026-12-17.jpg'
        path.parent.mkdir(parents=True); Image.new('RGB', (100, 100)).save(path)
        with patch('arteque_reza.noite.PROJECT', fake), self.assertRaisesRegex(ValueError, 'tamanho real'):
            artwork_window(path, day['obra'], 640, 760)

    def test_approval_date_is_preserved_for_old_dates(self):
        for series, day in [('olhe-de-novo','2026-12-09'), ('toda-bela','2026-12-12'),
                            ('por-dentro-da-missa','2026-12-10'), ('rezo-por-voce','2026-12-11')]:
            self.assertEqual(approval_date(series, day), '2026-11-12')
        for series, day in [('antifonas','2026-12-17'), ('olhe-de-novo','2026-12-30'),
                            ('toda-bela','2026-12-26')]:
            self.assertEqual(approval_date(series, day), '2026-11-19')


if __name__ == '__main__':
    unittest.main()
