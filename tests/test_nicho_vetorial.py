"""Forma vetorial do filete e fidelidade à espessura da fonte do kit."""

from pathlib import Path
import re
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

from playwright.sync_api import sync_playwright

from arteque_reza.base import (KIT, NICHO_FILETE_ESPESSURA, PROJECT, color,
                              generate_tokens_css, html_document, montar_arte,
                              nicho, resource_url)
from arteque_reza.ficha import measure_page
from arteque_reza.renderizacao import local_server


class NicheVectorMarkupTests(unittest.TestCase):
    def test_exact_open_u_paths_for_the_two_requested_sizes(self):
        cases = (
            (680, 760, 'M0 760V340A340 340 0 0 1 680 340V760H677V340A337 337 0 0 0 3 340V760Z'),
            (600, 680, 'M0 680V300A300 300 0 0 1 600 300V680H597V300A297 297 0 0 0 3 300V680Z'),
        )
        for width, height, expected in cases:
            with self.subTest(size=(width, height)):
                markup = nicho(width, height, 'obras/2026-11-30.jpg')
                svgs = re.findall(r'<svg\b.*?</svg>', markup, re.S)
                self.assertEqual(len(svgs), 1)
                svg = ET.fromstring(svgs[0])
                self.assertEqual(svg.get('viewBox'), f'0 0 {width} {height}')
                self.assertEqual(svg.get('aria-hidden'), 'true')
                self.assertEqual(svg.get('data-element'), 'nicho-filete')
                self.assertEqual(svg.get('data-cor-token'), 'cor-do-dia')
                self.assertIn('position:absolute;inset:0;', svg.get('style'))
                self.assertIn('color:var(--moldura, var(--cor-do-dia));', svg.get('style'))
                self.assertEqual(len(svg), 1)
                self.assertEqual(svg[0].tag, 'path')
                self.assertEqual(svg[0].get('d'), expected)
                self.assertEqual(svg[0].get('fill'), 'currentColor')
                self.assertIsNone(svg[0].get('stroke'))

    def test_thickness_matches_the_kit_border(self):
        bundle = (KIT / 'design-system/bundle.css').read_text()
        rule = re.search(r'\.aqr-nicho::before\s*\{([^}]+)\}', bundle).group(1)
        thickness = float(re.search(r'\bborder:\s*([\d.]+)px\s+solid', rule).group(1))
        self.assertEqual(NICHO_FILETE_ESPESSURA, thickness)
        self.assertEqual(thickness, 3)

    def test_old_border_is_disabled_after_the_original_bundle(self):
        document = html_document('', PROJECT / 'saida/tokens.css')
        self.assertLess(document.index('bundle.css'), document.index('.aqr-nicho::before{content:none;}'))
        self.assertNotIn('.aqr-nicho::after', document)


@unittest.skipUnless(shutil.which('chromium'), 'Chromium é necessário para medir o SVG real')
class NicheVectorMeasurementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        work = PROJECT / 'work'
        work.mkdir(exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(dir=work)
        cls.addClassCleanup(cls.temp.cleanup)
        cls.folder = Path(cls.temp.name)
        cls.css = generate_tokens_css(cls.folder / 'tokens.css')
        cls.server = local_server()
        cls.url = cls.server.__enter__()
        cls.addClassCleanup(cls.server.__exit__, None, None, None)
        cls.playwright = sync_playwright().start()
        cls.addClassCleanup(cls.playwright.stop)
        cls.browser = cls.playwright.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
        cls.addClassCleanup(cls.browser.close)
        cls.page = cls.browser.new_page(viewport={'width': 1080, 'height': 1350})

    def test_ficha_keeps_the_niche_bounds_color_and_sill(self):
        cases = ((False, 'liturgico-vermelho'), (True, 'liturgico-vermelho'),
                 (True, 'liturgico-branco'))
        for moldura, liturgy in cases:
            with self.subTest(moldura=moldura, liturgy=liturgy):
                piece = nicho(680, 760, 'obras/2026-11-30.jpg')
                if moldura:
                    piece = piece.replace('style="width:', 'style="--moldura:var(--ouro);width:', 1)
                path = self.folder / 'card.html'
                path.write_text(html_document(montar_arte(piece, 'capela', liturgy), self.css))
                self.page.goto(self.url + resource_url(path))
                record = measure_page(self.page, 1, 'Nicho vetorial')
                elements = {item['element']: item for item in record['elements']}
                frame, host, sill = (elements[name] for name in ('nicho-filete', 'nicho', 'nicho-parapeito'))
                self.assertEqual(sum(item['element'] == 'nicho-filete' for item in record['elements']), 1)
                self.assertEqual(frame['kind'], 'svg')
                self.assertEqual([frame[key] for key in ('x', 'y', 'width', 'height')],
                                 [host[key] for key in ('x', 'y', 'width', 'height')])
                self.assertEqual(frame['hex'], color('ouro' if moldura else 'liturgico-vermelho', 'capela'))
                self.assertEqual(frame['token'], 'ouro' if moldura else 'cor-do-dia')
                self.assertEqual(sill['hex'], frame['hex'])
                self.assertEqual(sill['token'], frame['token'])
                self.assertEqual(sill['height'], 3)
                self.assertEqual(sill['y'], host['y'] + host['height'])
                self.assertEqual(self.page.locator('.aqr-nicho').evaluate("node=>getComputedStyle(node,'::before').content"), 'none')
                legacy = re.sub(r'<svg\b[^>]*data-element="nicho-filete".*?</svg>', '', piece, flags=re.S)
                path.write_text(html_document(montar_arte(legacy, 'capela', liturgy), self.css,
                                              extra_css='.aqr-nicho::before{content:"";}'))
                self.page.goto(self.url + resource_url(path))
                old = {item['element']: item for item in measure_page(self.page, 1, 'Nicho legado')['elements']}
                for name in ('nicho-filete', 'nicho-parapeito'):
                    for field in ('x', 'y', 'width', 'height', 'hex', 'token'):
                        self.assertEqual(elements[name][field], old[name][field], (name, field))
