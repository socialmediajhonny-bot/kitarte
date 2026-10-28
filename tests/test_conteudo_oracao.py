"""Contrato editorial de Para Rezar antes da medição das linhas no navegador."""

from copy import deepcopy
from datetime import date, datetime
from pathlib import Path
import tempfile
import unittest
import warnings

import yaml

from arteque_reza.base import PROJECT
from arteque_reza.conteudo import ContentWarning
from arteque_reza.conteudo_oracao import PRAYER_FIELDS, load_prayers, prayer_warnings


class PrayerContentTests(unittest.TestCase):
    def setUp(self):
        self.days = load_prayers(PROJECT / "conteudo/para-rezar.yaml")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.file = Path(self.temp.name) / "oracao.yaml"

    def load(self, days):
        self.file.write_text(yaml.safe_dump(days, allow_unicode=True), encoding="utf-8")
        return load_prayers(self.file)

    def test_supplied_content_preserves_fields_and_folded_parts_in_order(self):
        self.assertEqual([day["data"] for day in self.days], ["2026-10-20", "2026-12-15"])
        self.assertEqual([len(day["partes"]) for day in self.days], [1, 2])
        for day in self.days:
            self.assertEqual(set(day), PRAYER_FIELDS)
            self.assertTrue(all("\n" not in part for part in day["partes"]))
        self.assertEqual(self.days[0]["origem"], "Papa Leão XIII, 1886")
        self.assertTrue(self.days[1]["partes"][0].endswith("de vos ter ofendido;"))
        self.assertTrue(self.days[1]["partes"][1].startswith("pesa-me também"))

    def test_all_fields_required_and_unknown_fields_are_errors(self):
        for field in PRAYER_FIELDS:
            with self.subTest(missing=field):
                day = deepcopy(self.days[0])
                del day[field]
                with self.assertRaisesRegex(ValueError, "obrigatório.*" + field):
                    self.load([day])
        day = deepcopy(self.days[0])
        day["intencoa"] = "erro de digitação"
        with self.assertRaisesRegex(ValueError, "desconhecido.*intencoa"):
            self.load([day])

    def test_parts_require_a_nonempty_list_of_nonempty_strings(self):
        for invalid in ([], None, "oração", {}, [""], [" \n\t "], [None], [123], ["Amém.", ""]):
            with self.subTest(parts=invalid):
                day = deepcopy(self.days[0])
                day["partes"] = invalid
                with self.assertRaisesRegex(ValueError, "2026-10-20.partes"):
                    self.load([day])

    def test_every_nonlast_part_needs_one_of_the_four_terminal_marks(self):
        for ending in (".", ";", "!", "?"):
            with self.subTest(ending=ending):
                day = deepcopy(self.days[0])
                day["partes"] = ["Primeira" + ending, "Parte do meio" + ending + " \n", "Última sem pontuação"]
                self.assertEqual(self.load([day])[0]["partes"], day["partes"])
        day["partes"] = ["Primeira.", "Parte do meio sem pontuação", "Última."]
        with self.assertRaisesRegex(ValueError, r"2026-10-20.partes\[2\].*deve terminar"):
            self.load([day])
        day["partes"] = ["Primeira,", "Última."]
        with self.assertRaisesRegex(ValueError, r"partes\[1\].*deve terminar"):
            self.load([day])

    def test_single_card_over_400_characters_only_warns_and_has_no_hidden_metadata(self):
        day = deepcopy(self.days[0])
        day["partes"] = ["á" * 400]
        with warnings.catch_warnings(record=True) as found:
            warnings.simplefilter("always")
            self.assertEqual(self.load([day])[0], day)
        self.assertEqual(found, [])
        day["partes"] = ["á" * 401]
        with warnings.catch_warnings(record=True) as found:
            warnings.simplefilter("always")
            result = self.load([day])[0]
        self.assertEqual(result, day)
        self.assertEqual(len(found), 1)
        self.assertIs(found[0].category, ContentWarning)
        self.assertEqual(str(found[0].message), prayer_warnings(day)[0])
        self.assertIn("2026-10-20", str(found[0].message))
        self.assertIn("401 caracteres", str(found[0].message))
        # Only a single card has this advisory, even if a carousel part is long.
        day["partes"] = ["á" * 401 + ".", "Última."]
        with warnings.catch_warnings(record=True) as found:
            warnings.simplefilter("always")
            self.load([day])
        self.assertEqual(found, [])

    def test_text_and_manual_breaks_are_never_rewritten(self):
        day = deepcopy(self.days[0])
        day["titulo"] = "Primeira linha\nSegunda linha"
        day["partes"] = ['Senhor,\nacolhei-nos & guardai-nos.\nAmém.']
        self.assertEqual(self.load([day])[0], day)

    def test_dates_are_iso_without_new_weekday_restrictions(self):
        day = deepcopy(self.days[0])
        day["data"] = date(2026, 12, 20)  # Domingo também é permitido.
        self.assertEqual(self.load([day])[0]["data"], "2026-12-20")
        for invalid in ("2026-02-30", "20/10/2026", datetime(2026, 10, 20, 9), None):
            with self.subTest(value=invalid):
                day["data"] = invalid
                with self.assertRaisesRegex(ValueError, "data"):
                    self.load([day])
        with self.assertRaisesRegex(ValueError, "data repetida"):
            self.load([self.days[0], self.days[0]])

    def test_invalid_colors_and_nontext_fields_rejected(self):
        for color in ("verde", "roxo", "ouro", "branco", "vermelho", "rosa"):
            day = deepcopy(self.days[0])
            day["cor"] = color
            self.assertEqual(self.load([day])[0]["cor"], color)
        day["cor"] = "azul"
        with self.assertRaisesRegex(ValueError, "Cor desconhecida"):
            self.load([day])
        for field in ("titulo", "intencao", "origem"):
            for invalid in (None, " ", 123):
                with self.subTest(field=field, value=invalid):
                    day = deepcopy(self.days[0])
                    day[field] = invalid
                    with self.assertRaisesRegex(ValueError, field + ".*texto não vazio"):
                        self.load([day])

    def test_safe_yaml_duplicate_keys_and_wrong_document_shapes(self):
        documents = (
            "", "[]", "data: 2026-10-20", "- texto",
            "!!python/object/apply:os.system ['false']",
            "- data: 2026-10-20\n  data: 2026-12-15\n",
        )
        for document in documents:
            with self.subTest(document=document):
                self.file.write_text(document, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_prayers(self.file)


if __name__ == "__main__":
    unittest.main()
