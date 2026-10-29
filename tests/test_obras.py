"""Geometria do zoom e detecção de margens em imagens sintéticas e reais."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from arteque_reza.base import PROJECT, nicho
from arteque_reza.conteudo import _work, load_content
from arteque_reza.conteudo_santo import load_saints
from arteque_reza.obras import artwork_geometry, crop_proof, inspect_artwork, uniform_margins


class ArtworkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.image = self.folder / 'image.png'
        Image.new('RGB', (1000, 500), '#a06030').save(self.image)

    def test_window_matches_cover_then_zoom_around_the_focus(self):
        # Cover occupies 1488×744px. Doubling about (25%,75%) produces a
        # 217.742×250px source window anchored at that same original point.
        result = artwork_geometry(self.image, '25% 75%', 2)
        window = result['janela_original']
        self.assertAlmostEqual(window['largura'], 648 / (744 / 500 * 2))
        self.assertAlmostEqual(window['altura'], 250)
        self.assertAlmostEqual(window['x'], (1000 - window['largura']) * .25)
        self.assertAlmostEqual(window['y'], 187.5)
        self.assertAlmostEqual((250 - window['x']) * result['escala_com_zoom'], 648 * .25)
        self.assertAlmostEqual((375 - window['y']) * result['escala_com_zoom'], 744 * .75)

    def test_zoom_one_matches_the_previous_cover_geometry(self):
        for width, height in ((680, 760), (340, 420), (600, 680), (720, 900)):
            with self.subTest(size=(width, height)):
                result = artwork_geometry(self.image, '50% 50%', niche_width=width, niche_height=height)
                scale = max((width - 32) / 1000, (height - 16) / 500)
                window = result['janela_original']
                self.assertAlmostEqual(window['largura'], (width - 32) / scale)
                self.assertAlmostEqual(window['altura'], (height - 16) / scale)
                self.assertAlmostEqual(window['x'], (1000 - window['largura']) / 2)
                self.assertAlmostEqual(window['y'], (500 - window['altura']) / 2)

    def test_focus_at_edges_keeps_the_zoom_anchor_fixed(self):
        for focus, x_fraction, y_fraction in [('0% 0%', 0, 0), ('100% 100%', 1, 1), ('45% 15%', .45, .15)]:
            with self.subTest(focus=focus):
                result = artwork_geometry(self.image, focus, 1.3)
                window = result['janela_original']
                self.assertAlmostEqual(window['x'], (1000 - window['largura']) * x_fraction)
                self.assertAlmostEqual(window['y'], (500 - window['altura']) * y_fraction)

    def test_zoom_schema_is_optional_numeric_finite_and_bounded(self):
        work = deepcopy(load_content(PROJECT / 'conteudo/evangelho.yaml')[0]['obra'])
        work.pop('zoom', None)
        self.assertNotIn('zoom', _work(work, 'teste.obra'))
        for good in (1, 1.05, 1.3, 3):
            with self.subTest(zoom=good):
                self.assertEqual(_work({**work, 'zoom': good}, 'teste.obra')['zoom'], good)
        for invalid in (0, .99, 3.01, -1, True, False, None, '1.1', float('nan'), float('inf')):
            with self.subTest(zoom=invalid):
                with self.assertRaisesRegex(ValueError, 'zoom'):
                    _work({**work, 'zoom': invalid}, 'teste.obra')
                with self.assertRaisesRegex(ValueError, 'zoom'):
                    artwork_geometry(self.image, '50% 50%', invalid)

    def test_niche_keeps_its_clip_and_applies_scale_only_to_the_image(self):
        plain = nicho(680, 760, PROJECT / 'saida/obra-provisoria.png')
        self.assertNotIn('transform:', plain)
        self.assertNotIn('object-position:', plain)
        zoomed = nicho(680, 760, PROJECT / 'saida/obra-provisoria.png', foco='45% 15%', zoom=1.3)
        self.assertIn('style="width:680px;height:760px;"', zoomed)
        self.assertIn('<div class="aqr-nicho__obra" data-element="nicho-recorte">', zoomed)
        self.assertIn('object-position:45% 15%;transform:scale(1.3);transform-origin:45% 15%', zoomed)
        self.assertEqual(zoomed.count('<img '), 1)
        self.assertEqual(zoomed.count('transform:'), 1)

    def _checker(self, top=0, bottom=0, left=0, right=0, top_std=0):
        image = Image.new('L', (80, 80))
        image.putdata([40 if (x + y) % 2 else 220 for y in range(80) for x in range(80)])
        for y in range(top):
            for x in range(80): image.putpixel((x, y), 100 + (top_std if x % 2 else -top_std))
        for y in range(80 - bottom, 80):
            for x in range(80): image.putpixel((x, y), 100)
        for x in range(left):
            for y in range(80): image.putpixel((x, y), 100)
        for x in range(80 - right, 80):
            for y in range(80): image.putpixel((x, y), 100)
        image.save(self.image)

    def test_uniform_margin_requires_four_contiguous_rows_and_std_below_six(self):
        for rows, sigma, expected in ((3, 0, 0), (4, 0, 4), (4, 5, 4), (4, 6, 0), (4, 7, 0)):
            with self.subTest(rows=rows, sigma=sigma):
                self._checker(top=rows, top_std=sigma)
                self.assertEqual(uniform_margins(self.image)['topo'], expected)
        self._checker()
        with Image.open(self.image) as source:
            source.load()
            for y in range(10, 15):
                for x in range(80): source.putpixel((x, y), 100)
            source.save(self.image)
        self.assertEqual(uniform_margins(self.image)['topo'], 0)

    def test_each_margin_warns_only_when_the_visible_window_intersects_it(self):
        self._checker(top=4, bottom=5, left=6, right=7)
        self.assertEqual(uniform_margins(self.image), {'topo': 4, 'base': 5, 'esquerda': 6, 'direita': 7})
        old = inspect_artwork(self.image, '50% 50%', niche_width=112, niche_height=96, date='2026-11-29')
        self.assertEqual(old['margens_visiveis'], ['topo', 'base', 'esquerda', 'direita'])
        self.assertIn('2026-11-29: margem da foto visível', old['avisos'][0])
        zoomed = inspect_artwork(self.image, '50% 50%', 2, niche_width=112, niche_height=96)
        self.assertEqual(zoomed['margens_visiveis'], [])
        self.assertEqual(zoomed['avisos'], [])
        # A 4px margin that touches only the excluded boundary is not visible.
        touch = inspect_artwork(self.image, '50% 50%', 80 / 72, niche_width=112, niche_height=96)
        self.assertNotIn('topo', touch['margens_visiveis'])

    def test_old_gospel_covers_warn_about_top_and_bottom_margins(self):
        for date in ('2026-11-29', '2026-12-13'):
            with self.subTest(date=date):
                result = inspect_artwork(PROJECT / f'obras/{date}.jpg', '50% 50%', date=date)
                self.assertEqual(result['margens_visiveis'], ['topo', 'base'])
                self.assertEqual(result['avisos'], [f'{date}: margem da foto visível no topo e na base; aumente o zoom'])

    def test_tissot_photographic_margins_still_have_the_original_widths(self):
        expected = {
            '2026-11-29': {'topo': 32, 'base': 22, 'esquerda': 0, 'direita': 7},
            '2026-12-13': {'topo': 32, 'base': 31, 'esquerda': 9, 'direita': 17},
        }
        for date, margins in expected.items():
            with self.subTest(date=date):
                result = inspect_artwork(PROJECT / f'obras/{date}.jpg', '50% 50%')
                self.assertEqual(result['margens_detectadas'], margins)
                self.assertEqual(result['faixas_descartadas'], [])

    def test_dark_painting_with_white_photographic_border_has_margins(self):
        image = Image.new('L', (80, 80), 255)
        for y in range(6, 74):
            for x in range(6, 74): image.putpixel((x, y), 20 if (x + y) % 2 else 40)
        image.save(self.image)
        result = inspect_artwork(self.image, '50% 50%', niche_width=112, niche_height=96)
        self.assertEqual(result['margens_detectadas'], dict.fromkeys(('topo', 'base', 'esquerda', 'direita'), 6))
        self.assertEqual(result['margens_visiveis'], ['topo', 'base', 'esquerda', 'direita'])
        self.assertTrue(result['avisos'])
        self.assertEqual(result['faixas_descartadas'], [])

    def test_dark_uniform_band_matching_the_interior_is_part_of_the_painting(self):
        image = Image.new('L', (80, 80))
        image.putdata([5 if (x + y) % 2 else 35 for y in range(80) for x in range(80)])
        for y in range(5):
            for x in range(80): image.putpixel((x, y), 20)
        image.save(self.image)
        result = inspect_artwork(self.image, '50% 50%', niche_width=112, niche_height=96)
        self.assertEqual(result['margens_detectadas'], dict.fromkeys(('topo', 'base', 'esquerda', 'direita'), 0))
        self.assertEqual(result['faixas_descartadas'], [{'lado': 'topo', 'largura': 5, 'diferenca_cinza': 0}])
        self.assertEqual(result['avisos'], [])

    def test_margin_contrast_threshold_is_at_least_ten_gray_levels(self):
        for difference in (9, 10):
            with self.subTest(difference=difference):
                image = Image.new('L', (80, 80))
                image.putdata([90 + difference if (x + y) % 2 else 110 + difference
                               for y in range(80) for x in range(80)])
                for y in range(4):
                    for x in range(80): image.putpixel((x, y), 100)
                image.save(self.image)
                result = inspect_artwork(self.image, '50% 50%')
                self.assertEqual(result['margens_detectadas']['topo'], 4 if difference == 10 else 0)
                self.assertEqual(result['faixas_descartadas'], [] if difference == 10 else
                                 [{'lado': 'topo', 'largura': 4, 'diferenca_cinza': 9}])

    def test_entirely_uniform_image_does_not_establish_a_photographic_border(self):
        result = inspect_artwork(self.image, '50% 50%')
        self.assertEqual(result['margens_detectadas'], dict.fromkeys(('topo', 'base', 'esquerda', 'direita'), 0))
        self.assertEqual(result['avisos'], [])
        self.assertEqual(len(result['faixas_descartadas']), 4)
        self.assertTrue(all(band['diferenca_cinza'] == 0 for band in result['faixas_descartadas']))

    def test_mercy_painting_discards_its_dark_bands_at_both_requested_zooms(self):
        artwork = PROJECT / 'obras/stories/misericordia.jpg'
        expected = {'base': (39, 2.6), 'esquerda': (211, .2), 'direita': (218, 1.1)}
        for zoom in (1, 1.15):
            with self.subTest(zoom=zoom):
                result = inspect_artwork(artwork, '50% 8%', zoom, niche_width=600, niche_height=700)
                self.assertEqual(result['margens_detectadas'], dict.fromkeys(('topo', 'base', 'esquerda', 'direita'), 0))
                self.assertEqual(result['margens_visiveis'], [])
                self.assertEqual(result['avisos'], [])
                self.assertEqual({band['lado'] for band in result['faixas_descartadas']}, set(expected))
                for band in result['faixas_descartadas']:
                    width, difference = expected[band['lado']]
                    self.assertEqual(band['largura'], width)
                    self.assertAlmostEqual(band['diferenca_cinza'], difference, delta=.05)

    def test_other_repository_paintings_have_no_uniform_bands(self):
        excluded = {'obras/2026-11-29.jpg', 'obras/2026-12-13.jpg', 'obras/stories/misericordia.jpg'}
        for artwork in sorted((PROJECT / 'obras').rglob('*.jpg')):
            if artwork.relative_to(PROJECT).as_posix() in excluded:
                continue
            with self.subTest(artwork=artwork.name):
                result = inspect_artwork(artwork, '50% 50%')
                self.assertFalse(any(result['margens_detectadas'].values()))
                self.assertEqual(result['faixas_descartadas'], [])

    def test_the_five_requested_new_framings_have_no_visible_uniform_margin(self):
        gospel = load_content(PROJECT / 'conteudo/evangelho.yaml')
        saints = load_saints(PROJECT / 'conteudo/santo-do-dia.yaml')
        expected = [('45% 50%', 1.1), ('50% 50%', 1.1), ('45% 15%', 1.05), ('50% 0%', 1.3), ('50% 20%', 1)]
        for day, (focus, zoom) in zip(gospel + saints, expected):
            with self.subTest(date=day['data']):
                self.assertEqual(day['obra']['foco'], focus)
                self.assertEqual(day['obra'].get('zoom', 1), zoom)
                size = (340, 420) if day.get('tipo') == 'santinho' else (600, 680) if day.get('tipo') == 'festa' else (680, 760)
                result = inspect_artwork(PROJECT / day['obra']['arquivo'], focus, zoom,
                                         niche_width=size[0], niche_height=size[1], date=day['data'])
                self.assertEqual(result['margens_visiveis'], [])
                self.assertEqual(result['avisos'], [])
        self.assertNotIn('zoom', saints[-1]['obra'])

    def test_crop_proof_uses_the_zoomed_window_on_the_full_original(self):
        output = self.folder / 'recorte.png'
        result = crop_proof(self.image, output, '25% 75%', zoom=2)
        self.assertEqual(result['janela_original'], artwork_geometry(self.image, '25% 75%', 2)['janela_original'])
        with Image.open(output) as image:
            self.assertEqual(image.size, (1080, 540))
            window = result['janela_original']
            middle = round((window['x'] + window['largura'] / 2) * 1.08)
            bottom = round((window['y'] + window['altura']) * 1.08)
            self.assertEqual(image.getpixel((middle, bottom)), (91, 46, 112))


if __name__ == '__main__':
    unittest.main()
