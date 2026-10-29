"""Ó e ó seguem a mesma regra de ligação das demais palavras de uma letra."""
from copy import deepcopy
import json
import unittest

from arteque_reza.base import PROJECT
from arteque_reza.conteudo import load_content, text_html
from arteque_reza.conteudo_coragem import load_courage
from arteque_reza.conteudo_oracao import load_prayers
from arteque_reza.conteudo_santo import load_saints
from arteque_reza.coragem import _validate_layout as validate_courage
from arteque_reza.evangelho import _validate_layout as validate_gospel
from arteque_reza.para_rezar import _validate_layout as validate_prayer
from arteque_reza.santo import _validate_layout as validate_saint


class TextTests(unittest.TestCase):
    def test_o_with_accent_is_bound_to_the_next_word_before_escaping(self):
        self.assertEqual(text_html('Ó Sangue e Água; ó <Deus> & paz'),
                         'Ó\u00a0Sangue e\u00a0Água; ó\u00a0&lt;Deus&gt; &amp; paz')

    def test_manual_break_and_accent_inside_a_word_are_preserved(self):
        self.assertEqual(text_html('Ó\nSangue; avó querida; paletó azul'),
                         'Ó<br>Sangue; avó querida; paletó azul')

    def test_all_existing_series_reject_a_line_ending_in_o_with_accent(self):
        cases = [
            (load_content(PROJECT/'conteudo/evangelho.yaml')[0], 'evangelho/2026-11-29', 1, 'trecho', validate_gospel),
            (load_saints(PROJECT/'conteudo/santo-do-dia.yaml')[0], 'santo-do-dia/2026-11-30', 0, 'frase', validate_saint),
            (load_prayers(PROJECT/'conteudo/para-rezar.yaml')[0], 'para-rezar/2026-10-20', 0, 'oracao', validate_prayer),
            (load_courage(PROJECT/'conteudo/coragem.yaml')[0], 'coragem/2026-12-14', 0, 'frase', validate_courage),
        ]
        for day, folder, index, field, validate in cases:
            card = json.loads((PROJECT/'saida'/folder/'ficha.json').read_text())['cards'][index]
            self.assertTrue(validate(day, card)['ok'])
            for letter in ('Ó', 'ó'):
                with self.subTest(series=folder, letter=letter):
                    changed = deepcopy(card)
                    text = next(t for t in changed['textos'] if t['campo'] == field)
                    text['linhas'][0] = 'Vinde ' + letter
                    with self.assertRaisesRegex(ValueError, 'palavra de uma letra no fim'):
                        validate(day, changed)


if __name__ == '__main__':
    unittest.main()
