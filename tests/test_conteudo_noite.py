"""Contrato estrito dos quatro YAMLs das séries da noite."""
from copy import deepcopy
from datetime import date, datetime
from pathlib import Path
import tempfile
import unittest

import yaml

from arteque_reza.base import PROJECT
from arteque_reza.conteudo_noite import LOADERS
from arteque_reza.igreja_domestica import BOOKS


def get_path(value, path):
    for key in path:
        value = value[key]
    return value


class NightContentTests(unittest.TestCase):
    def setUp(self):
        self.days = {slug: loader(PROJECT / 'conteudo' / f'{slug}.yaml') for slug, loader in LOADERS.items()}
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.file = Path(self.temp.name) / 'noite.yaml'

    def load(self, slug, days):
        self.file.write_text(yaml.safe_dump(days, allow_unicode=True), encoding='utf-8')
        return LOADERS[slug](self.file)

    def test_supplied_days_preserve_order_exact_text_and_manual_breaks(self):
        self.assertEqual([self.days[slug][0]['data'] for slug in LOADERS],
                         ['2026-12-09', '2026-12-10', '2026-12-11', '2026-12-12'])
        for slug, days in self.days.items():
            self.assertEqual(self.load(slug, days), days)
        look = self.days['olhe-de-novo'][0]
        self.assertEqual(look['detalhe']['janela'], [396, 2440, 608])
        self.assertEqual(look['detalhe']['tamanho'], [2996, 4226])
        self.assertEqual(look['onde']['obras'][0]['arquivo'], 'obras/stories/angelus.jpg')
        self.assertEqual(look['onde']['obras'][0]['credito'],
                         'Jan van Eyck · A Anunciação\nNational Gallery of Art')
        self.assertEqual(look['onde']['obras'][1]['credito'],
                         'El Greco · Santo Antônio de Pádua\nMuseu do Prado')
        self.assertEqual(look['significado']['fonte'],
                         'National Gallery, Londres: glossário (lírios) e ficha da obra · Lc 1,27')
        self.assertNotIn('\n', look['significado']['texto'])
        mass = self.days['por-dentro-da-missa'][0]
        self.assertEqual(mass['explicacoes'][0]['titulo'], 'Roxo: tempo de preparação')
        self.assertEqual(mass['explicacoes'][1]['titulo'], 'Rosa: o domingo Gaudete')
        self.assertIn('“tempo de piedosa e alegre expectativa”', mass['explicacoes'][0]['texto'])
        self.assertIn('“alegrai-vos”', mass['explicacoes'][1]['texto'])
        self.assertIn('“Alegrai-vos sempre no Senhor!” (Fl 4,4)', mass['explicacoes'][1]['texto'])
        self.assertEqual(mass['explicacoes'][0]['fonte'],
                         'Instrução Geral do Missal Romano, 345-346\n'
                         'Normas Universais sobre o Ano Litúrgico e o Calendário, 39')
        self.assertIn('Ângelus', mass['explicacoes'][1]['fonte'])
        self.assertEqual(self.days['rezo-por-voce'][0]['texto'],
                         'Amanhã, sábado, rezamos o terço por todas elas nos Stories.')
        fair = self.days['toda-bela'][0]
        self.assertEqual(fair['cor'], 'ouro')
        self.assertEqual(fair['oracao']['frase'], 'Santa Maria,\nrogai por nós.')
        self.assertEqual(fair['raiz']['referencia'], 'Lc 1,27')

    def test_root_required_and_unknown_fields_are_checked_in_each_series(self):
        for slug, days in self.days.items():
            for field in days[0]:
                with self.subTest(slug=slug, field=field):
                    changed = deepcopy(days)
                    del changed[0][field]
                    with self.assertRaisesRegex(ValueError, 'obrigatório'):
                        self.load(slug, changed)
            changed = deepcopy(days)
            changed[0]['extra'] = 'não permitido'
            with self.subTest(slug=slug), self.assertRaisesRegex(ValueError, 'desconhecido.*extra'):
                self.load(slug, changed)

    def test_nested_required_and_unknown_fields_are_checked(self):
        paths = {
            'olhe-de-novo': [('obra',), ('detalhe',), ('significado',), ('onde',), ('onde', 'obras', 0)],
            'por-dentro-da-missa': [('capa',), ('explicacoes', 0), ('fecho',)],
            'toda-bela': [('obra',), ('raiz',), ('oracao',)],
        }
        for slug, nested_paths in paths.items():
            for path in nested_paths:
                node = get_path(self.days[slug][0], path)
                for field in node:
                    if field == 'zoom':
                        continue
                    with self.subTest(slug=slug, path=path, field=field):
                        days = deepcopy(self.days[slug])
                        del get_path(days[0], path)[field]
                        with self.assertRaisesRegex(ValueError, 'obrigatório'):
                            self.load(slug, days)
                days = deepcopy(self.days[slug])
                get_path(days[0], path)['extra'] = 'indevido'
                with self.subTest(slug=slug, path=path), self.assertRaisesRegex(ValueError, 'desconhecido.*extra'):
                    self.load(slug, days)

    def test_duplicate_yaml_keys_are_rejected_in_each_series(self):
        for slug in LOADERS:
            source = (PROJECT / 'conteudo' / f'{slug}.yaml').read_text()
            color = self.days[slug][0]['cor']
            source = source.replace(f'  cor: {color}\n', f'  cor: {color}\n  cor: verde\n', 1)
            self.file.write_text(source)
            with self.subTest(slug=slug), self.assertRaisesRegex(ValueError, 'Campo repetido'):
                LOADERS[slug](self.file)

    def test_document_and_days_must_have_the_required_shapes(self):
        for slug in LOADERS:
            for invalid in (None, {}, 'texto', [], [None], [[]], [3]):
                with self.subTest(slug=slug, value=invalid), self.assertRaisesRegex(ValueError, 'lista não vazia|mapa'):
                    self.load(slug, invalid)

    def test_dates_reject_duplicates_invalid_values_and_timestamps(self):
        for slug, days in self.days.items():
            with self.subTest(slug=slug), self.assertRaisesRegex(ValueError, 'data repetida'):
                self.load(slug, days + deepcopy(days))
            for invalid in ('2026-02-30', '09/12/2026', None, True, datetime(2026, 12, 9, 20)):
                changed = deepcopy(days)
                changed[0]['data'] = invalid
                with self.subTest(slug=slug, value=invalid), self.assertRaises(ValueError):
                    self.load(slug, changed)

    def test_date_objects_and_other_weekdays_are_allowed(self):
        for slug, days in self.days.items():
            changed = deepcopy(days)
            changed[0]['data'] = date(2026, 12, 14)
            self.assertEqual(self.load(slug, changed)[0]['data'], '2026-12-14')

    def test_unknown_colors_are_rejected_in_each_series(self):
        for slug, days in self.days.items():
            for invalid in ('azul', '', None, True):
                changed = deepcopy(days)
                changed[0]['cor'] = invalid
                with self.subTest(slug=slug, value=invalid), self.assertRaisesRegex(ValueError, 'Cor desconhecida'):
                    self.load(slug, changed)

    def test_all_texts_reject_empty_or_non_text_values(self):
        def text_paths(value, prefix=()):
            if isinstance(value, dict):
                for key, child in value.items():
                    if key not in {'data', 'cor', 'arquivo', 'pagina', 'foco'}:
                        yield from text_paths(child, prefix + (key,))
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    yield from text_paths(child, prefix + (index,))
            elif isinstance(value, str):
                yield prefix
        for slug, days in self.days.items():
            for path in text_paths(days[0]):
                for invalid in (None, True, 4, '', ' \n '):
                    changed = deepcopy(days)
                    get_path(changed[0], path[:-1])[path[-1]] = invalid
                    with self.subTest(slug=slug, path=path, value=invalid), self.assertRaisesRegex(ValueError, 'texto não vazio'):
                        self.load(slug, changed)

    def test_where_works_requires_one_or_two_entries_and_preserves_order(self):
        original = self.days['olhe-de-novo']
        for invalid in (None, {}, 'obra', [], original[0]['onde']['obras'] * 2):
            days = deepcopy(original)
            days[0]['onde']['obras'] = invalid
            with self.subTest(value=invalid), self.assertRaisesRegex(ValueError, '1 ou 2 obras'):
                self.load('olhe-de-novo', days)
        days = deepcopy(original)
        days[0]['onde']['obras'].pop()
        self.assertEqual(self.load('olhe-de-novo', days)[0]['onde']['obras'], days[0]['onde']['obras'])

    def test_mass_requires_one_to_three_explanations(self):
        original = self.days['por-dentro-da-missa']
        for invalid in (None, {}, 'texto', [], original[0]['explicacoes'] * 2):
            days = deepcopy(original)
            days[0]['explicacoes'] = invalid
            with self.subTest(value=invalid), self.assertRaisesRegex(ValueError, '1 a 3 explicações'):
                self.load('por-dentro-da-missa', days)
        for count in (1, 3):
            days = deepcopy(original)
            days[0]['explicacoes'] = [deepcopy(original[0]['explicacoes'][0]) for _ in range(count)]
            self.assertEqual(len(self.load('por-dentro-da-missa', days)[0]['explicacoes']), count)

    def test_windows_require_three_integers_and_must_fit_inside_the_file(self):
        for path in [('detalhe',), ('onde', 'obras', 0)]:
            for invalid in ([0, 0], [0, 0, 0], [-1, 0, 608], [0, -1, 608],
                            [0, 0, -1], [False, 0, 608], [0, 0, 608.0], 'janela',
                            [2990, 0, 608], [0, 4200, 608]):
                days = deepcopy(self.days['olhe-de-novo'])
                get_path(days[0], path)['janela'] = invalid
                with self.subTest(path=path, value=invalid), self.assertRaisesRegex(ValueError, 'janela'):
                    self.load('olhe-de-novo', days)

    def test_window_size_must_be_two_positive_integers_and_match_the_actual_file(self):
        for path in [('detalhe',), ('onde', 'obras', 0)]:
            for invalid in ([2996], [0, 4226], [-1, 4226], [2996, False], [2996.0, 4226], [1000, 1000]):
                days = deepcopy(self.days['olhe-de-novo'])
                get_path(days[0], path)['tamanho'] = invalid
                with self.subTest(path=path, value=invalid), self.assertRaisesRegex(ValueError, 'tamanho'):
                    self.load('olhe-de-novo', days)

    def test_window_cannot_magnify_above_one_point_two(self):
        days = deepcopy(self.days['olhe-de-novo'])
        days[0]['detalhe']['janela'] = [396, 2440, 500]
        with self.assertRaisesRegex(ValueError, 'ampliação acima de 1,2'):
            self.load('olhe-de-novo', days)

    def test_bible_references_use_the_domestic_church_book_list(self):
        for book in BOOKS:
            days = deepcopy(self.days['toda-bela'])
            days[0]['raiz']['referencia'] = book + ' 1,27'
            self.assertEqual(self.load('toda-bela', days)[0]['raiz']['referencia'], book + ' 1,27')
        for invalid in ('XYZ 1,27', 'Lucas 1,27', 'Lc1,27', 'Lc 0,27', 'Lc 1,0', 'Lc 1,27 (Missa da noite)'):
            days = deepcopy(self.days['toda-bela'])
            days[0]['raiz']['referencia'] = invalid
            with self.subTest(value=invalid), self.assertRaisesRegex(ValueError, 'referencia'):
                self.load('toda-bela', days)

    def test_cover_info_has_at_most_sixteen_characters_and_no_support_field(self):
        days = deepcopy(self.days['toda-bela'])
        days[0]['info'] = 'a' * 17
        with self.assertRaisesRegex(ValueError, '16 caracteres'):
            self.load('toda-bela', days)
        days[0]['info'] = 'a' * 16
        self.assertEqual(self.load('toda-bela', days)[0]['info'], 'a' * 16)
        days[0]['apoio'] = 'Não cabe na composição'
        with self.assertRaisesRegex(ValueError, 'desconhecido.*apoio'):
            self.load('toda-bela', days)

    def test_works_reuse_current_local_path_focus_zoom_and_page_rules(self):
        for slug in ('olhe-de-novo', 'toda-bela'):
            for field, value in (('arquivo', '../obra.jpg'), ('arquivo', 'https://example.org/obra.jpg'),
                                 ('pagina', 'arquivo.jpg'), ('foco', '101% 50%'), ('zoom', True), ('zoom', .9)):
                days = deepcopy(self.days[slug])
                days[0]['obra'][field] = value
                with self.subTest(slug=slug, field=field, value=value), self.assertRaises(ValueError):
                    self.load(slug, days)
        for field, value in (('arquivo', '../obra.jpg'), ('arquivo', 'obras/ausente.jpg'),
                             ('pagina', 'arquivo.jpg'), ('foco', '50% 50%'), ('zoom', 1)):
            days = deepcopy(self.days['olhe-de-novo'])
            days[0]['onde']['obras'][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.load('olhe-de-novo', days)


if __name__ == '__main__':
    unittest.main()
