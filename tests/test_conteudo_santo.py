"""Contrato dos dois modelos de Santo do Dia antes de iniciar o render."""

from copy import deepcopy
from datetime import date, datetime
from pathlib import Path
import tempfile
import unittest

import yaml

from arteque_reza.base import PROJECT
from arteque_reza.conteudo_santo import COMMON_FIELDS, TYPE_FIELDS, load_saints


class SaintContentTests(unittest.TestCase):
    def setUp(self):
        self.days = load_saints(PROJECT / "conteudo/santo-do-dia.yaml")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.file = Path(self.temp.name) / "santo.yaml"

    def load(self, days):
        self.file.write_text(yaml.safe_dump(days, allow_unicode=True), encoding="utf-8")
        return load_saints(self.file)

    def test_supplied_content_has_exact_fields_and_unquoted_phrases(self):
        self.assertEqual([item["data"] for item in self.days], ["2026-11-30", "2026-12-03", "2026-12-08"])
        self.assertEqual([item["tipo"] for item in self.days], ["santinho", "santinho", "festa"])
        for day in self.days:
            self.assertEqual(set(day), TYPE_FIELDS[day["tipo"]])
        self.assertEqual(self.days[0]["frase"], "Encontramos o Messias.")
        self.assertEqual(self.days[0]["fonte"], "Palavras de André a Pedro, Jo 1,41")
        self.assertEqual(self.days[1]["fonte"], "Das cartas a Santo Inácio")
        self.assertEqual(self.days[2]["nome"], "Imaculada Conceição de Nossa Senhora")

    def test_every_model_field_is_required(self):
        for example in (self.days[0], self.days[2]):
            for field in TYPE_FIELDS[example["tipo"]]:
                with self.subTest(kind=example["tipo"], field=field):
                    item = deepcopy(example)
                    del item[field]
                    with self.assertRaisesRegex(ValueError, "campo obrigatório ausente.*" + field):
                        self.load([item])

    def test_unknown_fields_rejected_at_root_and_work(self):
        for example in (self.days[0], self.days[2]):
            for nested in (False, True):
                with self.subTest(kind=example["tipo"], nested=nested):
                    item = deepcopy(example)
                    target = item["obra"] if nested else item
                    target["nomme"] = "erro de digitação"
                    with self.assertRaisesRegex(ValueError, "campo desconhecido.*nomme"):
                        self.load([item])

    def test_festa_rejects_each_santinho_only_field(self):
        for field in TYPE_FIELDS["santinho"] - COMMON_FIELDS:
            with self.subTest(field=field):
                item = deepcopy(self.days[2])
                item[field] = self.days[0][field]
                with self.assertRaisesRegex(ValueError, "2026-12-08.*campo desconhecido.*" + field):
                    self.load([item])

    def test_type_must_be_one_of_the_two_named_models(self):
        for invalid in ("santo", "Festa", "", None, ["festa"]):
            with self.subTest(value=invalid):
                item = deepcopy(self.days[0])
                item["tipo"] = invalid
                with self.assertRaisesRegex(ValueError, "tipo"):
                    self.load([item])

    def test_sundays_rejected_for_both_models(self):
        for example in (self.days[0], self.days[2]):
            with self.subTest(kind=example["tipo"]):
                item = deepcopy(example)
                item["data"] = "2026-12-06"
                with self.assertRaisesRegex(ValueError, "2026-12-06.*domingo"):
                    self.load([item])

    def test_dates_normalize_to_iso_and_reject_invalid_or_duplicate_values(self):
        item = deepcopy(self.days[0])
        item["data"] = date(2026, 11, 30)
        self.assertEqual(self.load([item])[0]["data"], "2026-11-30")
        for invalid in ("30/11/2026", "2026-02-30", datetime(2026, 11, 30, 9, 0), None):
            with self.subTest(value=invalid):
                item["data"] = invalid
                with self.assertRaisesRegex(ValueError, "data"):
                    self.load([item])
        with self.assertRaisesRegex(ValueError, "2026-11-30.*data repetida"):
            self.load([self.days[0], self.days[0]])

    def test_text_fields_cannot_be_empty_or_have_nontext_types(self):
        for field in ("grau", "nome", "titulo", "frase", "fonte"):
            for invalid in ("  ", None, 123):
                with self.subTest(field=field, value=invalid):
                    item = deepcopy(self.days[0])
                    item[field] = invalid
                    with self.assertRaisesRegex(ValueError, field + ".*texto não vazio"):
                        self.load([item])

    def test_reuses_evangelho_color_table(self):
        for color in ("verde", "roxo", "ouro", "branco", "vermelho", "rosa"):
            item = deepcopy(self.days[0])
            item["cor"] = color
            self.assertEqual(self.load([item])[0]["cor"], color)
        item["cor"] = "azul"
        with self.assertRaisesRegex(ValueError, "Cor desconhecida"):
            self.load([item])

    def test_work_schema_and_local_paths_are_reused(self):
        for field in ("arquivo", "credito", "pagina", "foco"):
            with self.subTest(missing=field):
                item = deepcopy(self.days[0])
                del item["obra"][field]
                with self.assertRaisesRegex(ValueError, "obra.*obrigatório.*" + field):
                    self.load([item])
        for field, invalid in (
            ("arquivo", "https://example.org/saint.jpg"),
            ("arquivo", "../outside.jpg"),
            ("arquivo", "/tmp/saint.jpg"),
            ("pagina", "file:///tmp/page.html"),
            ("foco", "50% 101%"),
        ):
            with self.subTest(field=field, value=invalid):
                item = deepcopy(self.days[0])
                item["obra"][field] = invalid
                with self.assertRaisesRegex(ValueError, "obra." + field):
                    self.load([item])
        item = deepcopy(self.days[0])
        item["obra"]["arquivo"] = "obras/santo-do-dia/nao-existe.jpg"
        self.assertEqual(self.load([item])[0]["obra"], item["obra"])

    def test_manual_line_breaks_and_original_punctuation_are_preserved(self):
        item = deepcopy(self.days[0])
        item["frase"] = "Encontramos\no Messias."
        item["fonte"] = 'Fonte com “aspas” & <texto>'
        result = self.load([item])[0]
        self.assertEqual(result["frase"], item["frase"])
        self.assertEqual(result["fonte"], item["fonte"])

    def test_empty_or_wrong_shape_yaml_and_unsafe_tags_are_errors(self):
        for document in ("", "[]", "data: 2026-11-30", "- texto", "!!python/object/apply:os.system ['false']"):
            with self.subTest(document=document):
                self.file.write_text(document, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_saints(self.file)

    def test_duplicate_yaml_keys_are_errors(self):
        self.file.write_text("- data: 2026-11-30\n  data: 2026-12-03\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Campo repetido.*data"):
            load_saints(self.file)


if __name__ == "__main__":
    unittest.main()
