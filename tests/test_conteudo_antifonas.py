"""Contrato das antífonas: datas, textos e dois tipos de janela da obra."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

import yaml

from arteque_reza.base import PROJECT
from arteque_reza.conteudo_noite import load_antiphons


class AntiphonContentTests(unittest.TestCase):
    def setUp(self):
        self.days = load_antiphons(PROJECT / 'conteudo/antifonas.yaml')
        self.temp = tempfile.TemporaryDirectory(dir=PROJECT / 'work')
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'antifonas.yaml'

    def load(self, days):
        self.path.write_text(yaml.safe_dump(days, allow_unicode=True), encoding='utf-8')
        return load_antiphons(self.path)

    def test_supplied_days_preserve_order_references_and_complete_antiphons(self):
        self.assertEqual([day['data'] for day in self.days],
                         ['2026-12-17', '2026-12-18', '2026-12-19',
                          '2026-12-21', '2026-12-22', '2026-12-23'])
        self.assertEqual([day['info'] for day in self.days],
                         ['1ª de 7', '2ª de 7', '3ª de 7', '5ª de 7', '6ª de 7', '7ª de 7'])
        self.assertEqual(self.load(self.days), self.days)
        self.assertEqual(self.days[0]['raiz']['referencia'], 'Eclo 24,5')
        self.assertEqual(self.days[2]['obra']['janela'], [584, 600, 845])
        self.assertEqual(self.days[2]['obra']['tamanho'], [2000, 1683])
        self.assertEqual(self.days[-1]['oracao']['antifona'],
                         'Ó Emanuel: Deus-conosco, nosso Rei Legislador, Esperança das nações e '
                         'dos povos Salvador: Vinde enfim para salvar-nos, ó Senhor e nosso Deus!')
        for day in self.days:
            self.assertNotIn('\n', day['oracao']['antifona'])
            self.assertNotIn('\n', day['raiz']['texto'])

    def test_required_and_unknown_fields_are_rejected_at_every_level(self):
        for where in ((), ('raiz',), ('oracao',), ('obra',)):
            original = self.days[0]
            for key in where:
                original = original[key]
            for field in set(original) - {'zoom'}:
                changed = deepcopy(self.days[:1]); node = changed[0]
                for key in where:
                    node = node[key]
                del node[field]
                with self.subTest(where=where, field=field), self.assertRaises(ValueError):
                    self.load(changed)
            changed = deepcopy(self.days[:1]); node = changed[0]
            for key in where:
                node = node[key]
            node['extra'] = 'não permitido'
            with self.subTest(where=where, field='extra'), self.assertRaisesRegex(ValueError, 'desconhecido'):
                self.load(changed)

    def test_duplicate_days_and_yaml_keys_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'repetida'):
            self.load([self.days[0], self.days[0]])
        self.path.write_text('- data: 2026-12-17\n  data: 2026-12-18\n')
        with self.assertRaisesRegex(ValueError, 'repetid'):
            load_antiphons(self.path)

    def test_date_and_number_must_correspond_to_december_17_to_23(self):
        for day, info in [('2026-12-16', '1ª de 7'), ('2026-12-24', '7ª de 7'),
                          ('2026-11-17', '1ª de 7'), ('2026-12-17', '2ª de 7'),
                          ('2026-12-17', '1a de 7'), ('2026-12-17', '1ª de 8')]:
            changed = deepcopy(self.days[:1]); changed[0].update(data=day, info=info)
            with self.subTest(day=day, info=info), self.assertRaises(ValueError):
                self.load(changed)
        # O schema permite a quarta; esta rodada usa a sua versão nos Stories.
        changed = deepcopy(self.days[:1]); changed[0].update(data='2026-12-20', info='4ª de 7')
        self.assertEqual(self.load(changed)[0]['info'], '4ª de 7')

    def test_unknown_color_and_biblical_book_are_rejected(self):
        changed = deepcopy(self.days[:1]); changed[0]['cor'] = 'azul'
        with self.assertRaises(ValueError):
            self.load(changed)
        changed = deepcopy(self.days[:1]); changed[0]['raiz']['referencia'] = 'Livro 24,5'
        with self.assertRaisesRegex(ValueError, 'livro bíblico'):
            self.load(changed)

    def test_window_schema_dimensions_bounds_and_magnification_are_checked(self):
        for window in ([584, 600], [-1, 600, 845], [584, 600, 0], [584, 600, True],
                       [1990, 600, 845], [584, 1600, 845], [584, 600, 500]):
            changed = deepcopy(self.days[2:3]); changed[0]['obra']['janela'] = window
            with self.subTest(window=window), self.assertRaises(ValueError):
                self.load(changed)
        for size in ([2000], [2000, 1684], [2000, -1]):
            changed = deepcopy(self.days[2:3]); changed[0]['obra']['tamanho'] = size
            with self.subTest(size=size), self.assertRaises(ValueError):
                self.load(changed)

    def test_window_and_focus_modes_cannot_be_mixed(self):
        changed = deepcopy(self.days[2:3]); changed[0]['obra']['foco'] = '50% 50%'
        with self.assertRaisesRegex(ValueError, 'desconhecido'):
            self.load(changed)
        changed = deepcopy(self.days[2:3]); del changed[0]['obra']['tamanho']
        with self.assertRaises(ValueError):
            self.load(changed)

    def test_missing_original_is_allowed_as_an_artwork_pending(self):
        for index in (0, 2):
            changed = deepcopy(self.days[index:index+1])
            changed[0]['obra']['arquivo'] = 'obras/antifonas/ausente-teste.jpg'
            self.assertEqual(self.load(changed)[0]['obra']['arquivo'],
                             'obras/antifonas/ausente-teste.jpg')


if __name__ == '__main__':
    unittest.main()
