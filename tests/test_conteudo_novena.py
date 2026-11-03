"""Contrato das novenas: datas, texto aprovado e entradas inválidas."""

from copy import deepcopy
from datetime import date, datetime
from pathlib import Path
import tempfile
import unittest

import yaml

from arteque_reza.base import PROJECT
from arteque_reza.conteudo_novena import (
    CLOSING_REQUIRED_FIELDS, DAY_FIELDS, NOVENA_FIELDS, load_novenas,
)


class NovenaContentTests(unittest.TestCase):
    def setUp(self):
        self.content = load_novenas(PROJECT / "conteudo/novenas.yaml")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.file = Path(self.temp.name) / "novenas.yaml"

    def load(self, content):
        self.file.write_text(yaml.safe_dump(content, allow_unicode=True), encoding="utf-8")
        return load_novenas(self.file)

    def test_supplied_content_preserves_text_order_dates_and_optional_fields(self):
        imaculada, natal = self.content
        self.assertEqual([novena["id"] for novena in self.content], ["imaculada", "natal"])
        self.assertEqual([novena["cor"] for novena in self.content], ["roxo", "roxo"])
        self.assertEqual(imaculada["dias"][0]["data"], "2026-11-29")
        self.assertEqual(imaculada["dias"][-1]["data"], "2026-12-07")
        self.assertEqual(natal["dias"][0]["data"], "2026-12-16")
        self.assertEqual(natal["encerramento"]["data"], "2026-12-25")
        self.assertEqual(imaculada["refrao"],
                         "Ó Maria concebida sem pecado,\nrogai por nós que recorremos a vós.")
        self.assertNotIn("fonte", imaculada["encerramento"])
        self.assertNotIn("final", imaculada["encerramento"])
        self.assertEqual(natal["encerramento"]["fonte"], "Jo 1,14")
        self.assertEqual(natal["encerramento"]["final"], "Glória a Deus nas alturas!")
        self.assertEqual(sum(len(n["dias"]) + 1 for n in self.content), 20)
        for novena in self.content:
            for day in novena["dias"]:
                self.assertEqual(set(day), DAY_FIELDS)
                self.assertNotIn("\n", day["oracao"])
        self.assertEqual(self.load(self.content), self.content)

    def test_novena_with_eight_or_ten_days_is_rejected(self):
        for count in (8, 10):
            with self.subTest(count=count):
                content = deepcopy(self.content)
                days = content[0]["dias"]
                if count == 8:
                    days.pop()
                else:
                    days.append(deepcopy(days[-1]))
                with self.assertRaisesRegex(ValueError, "exatamente 9 dias"):
                    self.load(content)

    def test_nine_days_must_be_consecutive_in_list_order(self):
        for replacement in ("2026-11-29", "2026-12-01", "2026-11-28"):
            with self.subTest(replacement=replacement):
                content = deepcopy(self.content)
                content[0]["dias"][1]["data"] = replacement
                with self.assertRaisesRegex(ValueError, "datas consecutivas"):
                    self.load(content)
        content = deepcopy(self.content)
        content[0]["dias"].reverse()
        with self.assertRaisesRegex(ValueError, "datas consecutivas"):
            self.load(content)

    def test_closing_date_must_immediately_follow_the_ninth_day(self):
        for replacement in ("2026-12-07", "2026-12-09", "2026-12-06"):
            with self.subTest(replacement=replacement):
                content = deepcopy(self.content)
                content[0]["encerramento"]["data"] = replacement
                with self.assertRaisesRegex(ValueError, "seguinte ao 9º dia"):
                    self.load(content)

    def test_dates_are_valid_iso_days_and_not_timestamps(self):
        for level in ("day", "closing"):
            for invalid in ("2026-02-30", "29/11/2026", "2026-1-01", "2026-11-29T00:00:00", "", None, 123, True, datetime(2026, 11, 29)):
                with self.subTest(level=level, value=invalid):
                    content = deepcopy(self.content)
                    target = content[0]["dias"][0] if level == "day" else content[0]["encerramento"]
                    target["data"] = invalid
                    with self.assertRaisesRegex(ValueError, "data"):
                        self.load(content)
        content = deepcopy(self.content)
        for novena in content:
            for day in novena["dias"] + [novena["encerramento"]]:
                day["data"] = date.fromisoformat(day["data"])
        self.assertEqual(self.load(content), self.content)

    def test_prayer_limit_is_240_and_does_not_count_the_refrain(self):
        for level in ("day", "closing"):
            content = deepcopy(self.content)
            target = content[0]["dias"][0] if level == "day" else content[0]["encerramento"]
            target["oracao"] = "A" * 240
            content[0]["refrao"] = "B" * 1000
            self.assertEqual(self.load(content)[0]["refrao"], "B" * 1000)
            target["oracao"] += "A"
            with self.subTest(level=level), self.assertRaisesRegex(ValueError, "241 caracteres; limite 240"):
                self.load(content)

    def test_every_required_field_is_checked_and_no_default_is_inserted(self):
        for level, fields in (("novena", NOVENA_FIELDS), ("day", DAY_FIELDS),
                              ("closing", CLOSING_REQUIRED_FIELDS)):
            for field in fields:
                with self.subTest(level=level, field=field):
                    content = deepcopy(self.content)
                    target = content[0] if level == "novena" else content[0]["dias"][0] if level == "day" else content[0]["encerramento"]
                    del target[field]
                    with self.assertRaisesRegex(ValueError, "obrigatório.*" + field):
                        self.load(content)

    def test_unknown_fields_are_rejected_in_novena_day_and_closing(self):
        for level in ("novena", "day", "closing"):
            with self.subTest(level=level):
                content = deepcopy(self.content)
                target = content[0] if level == "novena" else content[0]["dias"][0] if level == "day" else content[0]["encerramento"]
                target["desconhecido"] = "erro"
                with self.assertRaisesRegex(ValueError, "campo desconhecido.*desconhecido"):
                    self.load(content)

    def test_text_fields_and_optional_closing_fields_must_be_nonempty_text(self):
        for level, fields in (("novena", ("nome", "refrao")),
                              ("day", ("titulo", "fonte", "oracao")),
                              ("closing", ("titulo", "oracao", "fonte", "final"))):
            for field in fields:
                for invalid in ("", " \n\t ", None, 123, False):
                    with self.subTest(level=level, field=field, value=invalid):
                        content = deepcopy(self.content)
                        target = content[0] if level == "novena" else content[0]["dias"][0] if level == "day" else content[0]["encerramento"]
                        target[field] = invalid
                        with self.assertRaisesRegex(ValueError, field + ".*texto não vazio"):
                            self.load(content)

    def test_identifiers_are_unique_and_safe_for_output_paths(self):
        content = deepcopy(self.content)
        content[1]["id"] = content[0]["id"]
        with self.assertRaisesRegex(ValueError, "id de novena repetido"):
            self.load(content)
        for invalid in ("", " ", "..", "../escape", "/tmp/novena", "a/b", "a\\b", "https://example.org/a", "com espaço", "novena\n", "-opcao", "imaculada.png", None, 12):
            with self.subTest(value=invalid):
                content = deepcopy(self.content)
                content[0]["id"] = invalid
                with self.assertRaisesRegex(ValueError, r"\.id"):
                    self.load(content)
        for valid in ("imaculada", "Novena_2", "123"):
            content = deepcopy(self.content)
            content[0]["id"] = valid
            self.assertEqual(self.load(content)[0]["id"], valid)

    def test_colors_reuse_the_existing_editorial_tokens_at_both_levels(self):
        for level in ("novena", "closing"):
            for value in ("verde", "roxo", "ouro", "branco", "vermelho", "rosa"):
                content = deepcopy(self.content)
                target = content[0] if level == "novena" else content[0]["encerramento"]
                target["cor"] = value
                self.assertEqual(self.load(content)[0]["cor"] if level == "novena" else self.load(content)[0]["encerramento"]["cor"], value)
            for invalid in ("azul", "Roxo", "", None, 12, False):
                with self.subTest(level=level, value=invalid):
                    content = deepcopy(self.content)
                    target = content[0] if level == "novena" else content[0]["encerramento"]
                    target["cor"] = invalid
                    with self.assertRaisesRegex(ValueError, "Cor desconhecida"):
                        self.load(content)

    def test_root_days_and_items_have_the_expected_shapes(self):
        for invalid in (None, [], "texto", {}, [None], ["texto"]):
            with self.subTest(root=invalid), self.assertRaises(ValueError):
                self.load(invalid)
        for invalid in (None, "texto", {}, [None] * 9, ["texto"] * 9):
            with self.subTest(days=invalid):
                content = deepcopy(self.content)
                content[0]["dias"] = invalid
                with self.assertRaises(ValueError):
                    self.load(content)
        for invalid in (None, "texto", []):
            with self.subTest(closing=invalid):
                content = deepcopy(self.content)
                content[0]["encerramento"] = invalid
                with self.assertRaises(ValueError):
                    self.load(content)

    def test_repeated_yaml_keys_are_rejected_before_content_validation(self):
        for document in (
            "- id: imaculada\n  id: natal\n",
            "- dias:\n    - data: 2026-11-29\n      data: 2026-11-30\n",
            "- encerramento:\n    cor: ouro\n    cor: roxo\n",
        ):
            with self.subTest(document=document):
                self.file.write_text(document, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "Campo repetido"):
                    load_novenas(self.file)

    def test_unsafe_yaml_tags_are_rejected(self):
        self.file.write_text("!!python/object/apply:os.system ['false']", encoding="utf-8")
        with self.assertRaises(ValueError):
            load_novenas(self.file)


if __name__ == "__main__":
    unittest.main()
