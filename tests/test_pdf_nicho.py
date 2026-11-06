"""Regressões das formas do nicho exportadas para o PDF do Canva."""

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

import fitz

from arteque_reza.base import PROJECT
from arteque_reza.pdf_nicho import niches_from_elements, validate_niche_pdf


class NichePDFTests(unittest.TestCase):
    HEX = '#b89cd9'
    COLOR = tuple(channel / 255 for channel in bytes.fromhex(HEX[1:]))

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'nicho.pdf'
        self.spec = {'page': 1, 'x': 200, 'y': 152,
                     'width': 680, 'height': 760, 'hex': self.HEX}

    def draw_u(self, page, *, offset=0, color=None):
        """One filled U path, with cubic arcs and the real 3 px thickness."""
        x, y = self.spec['x'] * .75 + offset, self.spec['y'] * .75 + offset
        width, height, thickness = self.spec['width'] * .75, self.spec['height'] * .75, 2.25
        radius = width / 2
        inner = radius - thickness
        cx, cy = x + radius, y + radius
        k = .5522847498307936
        shape = page.new_shape()
        shape.draw_line((x, y + height), (x, cy))
        shape.draw_bezier((x, cy), (x, cy - k * radius),
                          (cx - k * radius, y), (cx, y))
        shape.draw_bezier((cx, y), (cx + k * radius, y),
                          (x + width, cy - k * radius), (x + width, cy))
        shape.draw_line((x + width, cy), (x + width, y + height))
        shape.draw_line((x + width, y + height), (x + width - thickness, y + height))
        shape.draw_line((x + width - thickness, y + height), (x + width - thickness, cy))
        shape.draw_bezier((x + width - thickness, cy),
                          (x + width - thickness, cy - k * inner),
                          (cx + k * inner, y + thickness), (cx, y + thickness))
        shape.draw_bezier((cx, y + thickness), (cx - k * inner, y + thickness),
                          (x + thickness, cy - k * inner), (x + thickness, cy))
        shape.draw_line((x + thickness, cy), (x + thickness, y + height))
        shape.finish(color=None, fill=self.COLOR if color is None else color, closePath=True)
        shape.commit()

    def draw_sill(self, page, *, height=3):
        x = (self.spec['x'] - 48) * .75
        y = (self.spec['y'] + self.spec['height']) * .75
        page.draw_rect(fitz.Rect(x, y, x + (self.spec['width'] + 96) * .75,
                                 y + height * .75), color=None, fill=self.COLOR)

    def write_pdf(self, *, filets=1, sills=1, old_border=False,
                  offset=0, sill_height=3, color=None):
        with fitz.open() as document:
            page = document.new_page(width=810, height=1012.5)
            for _ in range(filets):
                self.draw_u(page, offset=offset, color=color)
            for _ in range(sills):
                self.draw_sill(page, height=sill_height)
            if old_border:
                x, y = self.spec['x'] * .75, self.spec['y'] * .75
                page.draw_rect(fitz.Rect(x, y, x + self.spec['width'] * .75,
                                         y + self.spec['height'] * .75),
                               color=None, fill=self.COLOR)
            document.save(self.path)
        return validate_niche_pdf(self.path, [self.spec])

    def test_one_curved_filled_u_and_one_sill_are_valid(self):
        result = self.write_pdf()
        self.assertTrue(result['ok'], result['errors'])
        self.assertEqual(len(result['nichos']), 1)
        for key in ('filete_vetorial', 'borda_antiga_ausente', 'parapeito_vetorial'):
            self.assertTrue(result['nichos'][0][key], key)

    def test_missing_or_duplicate_filet_is_rejected(self):
        for count in (0, 2):
            with self.subTest(count=count):
                result = self.write_pdf(filets=count)
                self.assertFalse(result['ok'])
                self.assertFalse(result['nichos'][0]['filete_vetorial'])
                self.assertTrue(result['nichos'][0]['parapeito_vetorial'])
                self.path.unlink()

    def test_old_full_box_rectangle_is_rejected_even_beside_valid_u(self):
        result = self.write_pdf(old_border=True)
        self.assertFalse(result['ok'])
        self.assertFalse(result['nichos'][0]['borda_antiga_ausente'])

    def test_missing_or_duplicate_sill_is_rejected(self):
        for count in (0, 2):
            with self.subTest(count=count):
                result = self.write_pdf(sills=count)
                self.assertFalse(result['ok'])
                self.assertFalse(result['nichos'][0]['parapeito_vetorial'])
                self.assertTrue(result['nichos'][0]['filete_vetorial'])
                self.path.unlink()

    def test_sill_with_wrong_height_is_rejected(self):
        for height in (3.5, 4):
            with self.subTest(height=height):
                result = self.write_pdf(sill_height=height)
                self.assertFalse(result['ok'])
                self.assertFalse(result['nichos'][0]['parapeito_vetorial'])
                self.path.unlink()

    def test_wrong_filet_color_is_rejected(self):
        result = self.write_pdf(color=(1, 0, 0))
        self.assertFalse(result['ok'])
        self.assertFalse(result['nichos'][0]['filete_vetorial'])

    def test_bbox_tolerance_is_half_a_point_not_half_a_pixel(self):
        result = self.write_pdf(offset=.4)
        self.assertTrue(result['ok'], result['errors'])
        self.path.unlink()
        result = self.write_pdf(offset=.6)
        self.assertFalse(result['ok'])
        self.assertFalse(result['nichos'][0]['filete_vetorial'])

    def test_wrong_page_cannot_match_another_pages_path(self):
        self.write_pdf()
        spec = deepcopy(self.spec)
        spec['page'] = 2
        result = validate_niche_pdf(self.path, [spec])
        self.assertFalse(result['ok'])
        self.assertTrue(result['errors'])

    def test_text_page_with_no_niche_does_not_require_shapes(self):
        self.write_pdf(filets=0, sills=0)
        result = validate_niche_pdf(self.path, [])
        self.assertTrue(result['ok'], result['errors'])
        self.assertEqual(result['nichos'], [])

    def test_invalid_specs_fail_instead_of_skipping_the_niche(self):
        self.write_pdf()
        for update in ({'page': 0}, {'page': 1.5}, {'page': True},
                       {'width': 0}, {'x': float('nan')}, {'hex': 'roxo'},
                       {'parapeito': {'x': 152, 'y': 912, 'width': 776, 'height': 4}}):
            with self.subTest(update=update):
                result = validate_niche_pdf(self.path, [{**self.spec, **update}])
                self.assertFalse(result['ok'])
                self.assertTrue(result['errors'])

    def test_helper_pairs_multiple_niches_in_the_same_page(self):
        elements = []
        for x in (200, 1000):
            elements += [
                {'element': 'nicho-parapeito', 'x': x - 48, 'y': 912,
                 'width': 776, 'height': 3, 'hex': self.HEX},
                {'element': 'nicho-filete', 'x': x, 'y': 152,
                 'width': 680, 'height': 760, 'hex': self.HEX},
            ]
        specs = niches_from_elements(elements, page=2)
        self.assertEqual([item['x'] for item in specs], [200, 1000])
        self.assertEqual([item['page'] for item in specs], [2, 2])
        self.assertEqual(specs[1]['parapeito']['x'], 952)
        self.assertEqual(niches_from_elements([], page=1), [])

    def test_helper_rejects_missing_ambiguous_or_wrong_color_sill(self):
        filet = {'element': 'nicho-filete', **self.spec}
        sill = {'element': 'nicho-parapeito', 'x': 152, 'y': 912,
                'width': 776, 'height': 3, 'hex': self.HEX}
        for elements in ([filet], [sill], [filet, sill, sill],
                         [filet, {**sill, 'hex': '#ffffff'}]):
            with self.subTest(elements=elements), self.assertRaises(ValueError):
                niches_from_elements(elements)

    def test_two_canva_regressions_keep_filet_and_sill_as_shapes(self):
        for day in ('2026-11-30', '2026-12-10'):
            with self.subTest(day=day):
                folder = PROJECT / 'saida/evangelho' / day
                record = json.loads((folder / 'ficha.json').read_text(encoding='utf-8'))
                elements = {item['element']: item for item in record['cards'][0]['elementos']}
                filet = elements['nicho-filete']
                sill = elements['nicho-parapeito']
                spec = {'page': 1, **{key: filet[key] for key in ('x', 'y', 'width', 'height', 'hex')},
                        'parapeito': {key: sill[key] for key in ('x', 'y', 'width', 'height')}}
                result = validate_niche_pdf(folder / f'evangelho-{day}.pdf', [spec])
                self.assertTrue(result['ok'], result['errors'])
                for key in ('filete_vetorial', 'borda_antiga_ausente', 'parapeito_vetorial'):
                    self.assertTrue(result['nichos'][0][key], key)


if __name__ == '__main__':
    unittest.main()
