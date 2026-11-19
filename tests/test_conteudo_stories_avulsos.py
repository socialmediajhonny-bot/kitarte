"""Contrato dos stories avulsos e do nome opcional da série nos stories fixos."""

from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image
import yaml

from arteque_reza.base import PROJECT
from arteque_reza.conteudo_stories import load_stories
from arteque_reza.conteudo_stories_avulsos import (
    REQUIRED_FIELDS, load_stories_avulsos,
)


class StandaloneStoryContentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)/'stories.yaml'
        source = PROJECT/'conteudo/stories-avulsos.yaml'
        if not source.is_file():
            source = PROJECT/'work/prompt16/conteudo-rascunho/stories-avulsos.yaml'
        self.content = load_stories_avulsos(source)

    def load(self, document):
        self.path.write_text(yaml.safe_dump(document, allow_unicode=True, sort_keys=False), encoding='utf-8')
        return load_stories_avulsos(self.path)

    def test_supplied_six_stories_keep_group_order_and_exact_manual_lines(self):
        self.assertEqual([s['id'] for s in self.content], [
            'terco-2026-12-12', 'chave-de-davi-1', 'chave-de-davi-2',
            'comece-aqui-1', 'comece-aqui-2', 'comece-aqui-3',
        ])
        self.assertEqual([s['grupo'] for s in self.content], [
            'terco-2026-12-12', 'chave-de-davi-2026-12-20', 'chave-de-davi-2026-12-20',
            'comece-aqui', 'comece-aqui', 'comece-aqui',
        ])
        self.assertEqual(self.content[0]['invocacao'],
            'Santa Maria, Mãe de Deus,\nrogai por nós, pecadores,\nagora e na hora de nossa morte. Amém.')
        self.assertEqual(self.content[1]['invocacao'],
            'Ó Chave de Davi, Cetro da casa de Israel,\nque abris e ninguém fecha,\nque fechais e ninguém abre:')
        self.assertEqual(self.content[2]['invocacao'],
            'vinde logo e libertai o homem prisioneiro,\nque, nas trevas e na sombra da morte,\nestá sentado.')
        self.assertEqual(self.content[3]['invocacao'],
            '«A beleza e a cor das imagens\nestimulam a minha oração»,\ndizia São João Damasceno.')
        for story in self.content:
            self.assertNotIn('resposta', story)
            self.assertNotIn('hora', story)
            self.assertNotIn('tempos', story)
            self.assertNotIn('textos_aprovados_em', story)
        self.assertEqual(self.load(self.content), self.content)

    def test_list_and_story_maps_are_required(self):
        for value in (None, [], {}, 'texto', [None], ['texto']):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.load(value)

    def test_unknown_fields_and_each_required_field_are_rejected(self):
        for field in ('data', 'hora', 'tempos', 'desconhecido'):
            document = deepcopy(self.content)
            document[0][field] = 'erro'
            with self.subTest(unknown=field), self.assertRaisesRegex(ValueError, 'campo desconhecido'):
                self.load(document)
        for field in REQUIRED_FIELDS:
            document = deepcopy(self.content)
            del document[0][field]
            with self.subTest(missing=field), self.assertRaisesRegex(ValueError, 'obrigatório.*'+field):
                self.load(document)
        document = deepcopy(self.content)
        document[0]['obra']['janela'] = [0, 0, 500]
        with self.assertRaisesRegex(ValueError, 'campo desconhecido.*janela'):
            self.load(document)

    def test_every_text_and_optional_response_must_be_nonempty(self):
        for field in ('serie', 'apoio', 'titulo', 'subtitulo', 'invocacao', 'resposta'):
            for invalid in ('', ' \n\t ', None, 12):
                document = deepcopy(self.content)
                document[0][field] = invalid
                with self.subTest(field=field, value=invalid), self.assertRaisesRegex(ValueError, field+'.*texto não vazio'):
                    self.load(document)
        document = deepcopy(self.content)
        document[0]['resposta'] = 'Rogai por nós.\nAmém.'
        self.assertEqual(self.load(document)[0]['resposta'], document[0]['resposta'])

    def test_ids_are_unique_across_groups_but_repeated_groups_are_allowed(self):
        document = deepcopy(self.content)
        document[-1]['id'] = document[0]['id']
        self.assertNotEqual(document[-1]['grupo'], document[0]['grupo'])
        with self.assertRaisesRegex(ValueError, 'id de story repetido'):
            self.load(document)
        document = deepcopy(self.content)
        document[0]['grupo'] = document[1]['grupo']
        self.assertEqual(self.load(document)[0]['grupo'], document[1]['grupo'])

    def test_story_ids_and_groups_are_safe_filename_components(self):
        for field in ('id', 'grupo'):
            for invalid in ('', '..', '../escape', '/tmp/story', 'a/b', 'a\\b',
                            'com espaço', 'id\n', '-opcao', 'story.png', None, 4):
                document = deepcopy(self.content)
                document[0][field] = invalid
                with self.subTest(field=field, value=invalid), self.assertRaisesRegex(ValueError, field):
                    self.load(document)
            for valid in ('grupo-2', 'Story_2', '123'):
                document = deepcopy(self.content)
                document[0][field] = valid
                self.assertEqual(self.load(document)[0][field], valid)

    def test_colors_reuse_the_current_liturgical_palette(self):
        for value in ('verde', 'roxo', 'ouro', 'branco', 'vermelho', 'rosa'):
            document = deepcopy(self.content)
            document[0]['cor'] = value
            self.assertEqual(self.load(document)[0]['cor'], value)
        for value in ('azul', 'Roxo', '', None, 5):
            document = deepcopy(self.content)
            document[0]['cor'] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'Cor desconhecida'):
                self.load(document)

    def test_work_fields_and_local_file_paths_are_strict(self):
        for field in ('arquivo', 'credito', 'pagina', 'foco'):
            document = deepcopy(self.content)
            del document[0]['obra'][field]
            with self.subTest(missing=field), self.assertRaisesRegex(ValueError, 'obrigatório.*'+field):
                self.load(document)
        for field, value in (
            ('arquivo', 'https://example.org/a.jpg'), ('arquivo', '../a.jpg'),
            ('arquivo', '/tmp/a.jpg'), ('pagina', 'file:///tmp/a.jpg'),
            ('pagina', 'sem-url'), ('pagina', 'https://example.org/com espaço'),
            ('foco', '50 50'), ('foco', '101% 50%'), ('foco', '-1% 50%'),
        ):
            document = deepcopy(self.content)
            document[0]['obra'][field] = value
            with self.subTest(field=field, value=value), self.assertRaisesRegex(ValueError, field):
                self.load(document)

    def test_zoom_is_optional_finite_and_between_one_and_three(self):
        for value in (1, 1.05, 2, 3):
            document = deepcopy(self.content)
            document[0]['obra']['zoom'] = value
            self.assertEqual(self.load(document)[0]['obra']['zoom'], value)
        for value in (0.99, 3.01, 0, -1, True, False, '1.15', None, float('nan'), float('inf')):
            document = deepcopy(self.content)
            document[0]['obra']['zoom'] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'zoom'):
                self.load(document)
        document = deepcopy(self.content)
        del document[0]['obra']['zoom']
        self.assertNotIn('zoom', self.load(document)[0]['obra'])

    def test_known_original_dimensions_are_checked_before_rendering(self):
        wrong = Path(self.temp.name)/'wrong-size.jpg'
        Image.new('RGB', (12, 17), 'white').save(wrong)
        for artwork in ('obras/stories/terco.jpg', 'obras/stories/chave-de-davi.jpg',
                        'obras/stories/comece-aqui-1.jpg', 'obras/stories/comece-aqui-2.jpg',
                        'obras/stories/comece-aqui-3.jpg'):
            document = [deepcopy(self.content[0])]
            document[0]['obra']['arquivo'] = artwork
            with self.subTest(artwork=artwork), patch(
                    'arteque_reza.conteudo_stories_avulsos.local_artwork_path', return_value=wrong):
                with self.assertRaisesRegex(ValueError, r'tamanho 12 × 17; esperado'):
                    self.load(document)

    def test_missing_artwork_is_kept_for_the_placeholder_without_opening_or_downloading(self):
        document = [deepcopy(self.content[0])]
        document[0]['obra']['arquivo'] = 'obras/stories/ausente-prompt16.jpg'
        self.assertFalse((PROJECT/document[0]['obra']['arquivo']).exists())
        with patch('arteque_reza.conteudo_stories_avulsos.Image.open', side_effect=AssertionError('não abrir ausente')):
            self.assertEqual(self.load(document), document)

    def test_repeated_yaml_keys_unsafe_tags_and_invalid_roots_are_rejected(self):
        for text in (
            '- id: um\n  id: dois\n',
            '- obra:\n    arquivo: um.jpg\n    arquivo: dois.jpg\n',
            "!!python/object/apply:os.system ['false']", '', '{}', 'texto',
        ):
            self.path.write_text(text, encoding='utf-8')
            with self.subTest(text=text), self.assertRaises(ValueError):
                load_stories_avulsos(self.path)

    def test_fixed_stories_accept_optional_series_without_injecting_defaults(self):
        document = load_stories(PROJECT/'conteudo/stories.yaml')
        for story in document['stories']:
            self.assertNotIn('serie', story)
        self.path.write_text(yaml.safe_dump(document, allow_unicode=True), encoding='utf-8')
        self.assertEqual(load_stories(self.path), document)
        document['stories'][0]['serie'] = 'Rezo por Você'
        self.path.write_text(yaml.safe_dump(document, allow_unicode=True), encoding='utf-8')
        self.assertEqual(load_stories(self.path)['stories'][0]['serie'], 'Rezo por Você')
        for invalid in ('', ' \n ', None, 8):
            document['stories'][0]['serie'] = invalid
            self.path.write_text(yaml.safe_dump(document, allow_unicode=True), encoding='utf-8')
            with self.subTest(value=invalid), self.assertRaisesRegex(ValueError, 'serie.*texto não vazio'):
                load_stories(self.path)


if __name__ == '__main__':
    unittest.main()
