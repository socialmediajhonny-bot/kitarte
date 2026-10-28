"""Contrato do Coragem: referência livre, obra local e zoom opcional estrito."""

from copy import deepcopy
from datetime import date, datetime
from pathlib import Path
import tempfile
import unittest

import yaml

from arteque_reza.base import PROJECT
from arteque_reza.conteudo_coragem import COURAGE_FIELDS, load_courage


class CourageContentTests(unittest.TestCase):
    def setUp(self):
        self.days = load_courage(PROJECT / "conteudo/coragem.yaml")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.file = Path(self.temp.name) / "coragem.yaml"

    def load(self, days):
        self.file.write_text(yaml.safe_dump(days, allow_unicode=True), encoding="utf-8")
        return load_courage(self.file)

    def test_supplied_content_preserves_manual_breaks_and_has_no_added_defaults(self):
        self.assertEqual([day["data"] for day in self.days], ["2026-12-14", "2026-12-28"])
        self.assertEqual(self.days[0]["frase"], "Criai ânimo, não tenhais medo!\nVede, é vosso Deus.")
        for day in self.days:
            self.assertEqual(set(day), COURAGE_FIELDS)
            self.assertNotIn("zoom", day["obra"])
        self.assertEqual(self.days[1]["referencia"], "Lc 2,10")

    def test_all_required_fields_and_unknown_fields_at_each_level(self):
        for nested, fields in ((False, COURAGE_FIELDS), (True, {"arquivo", "credito", "pagina", "foco"})):
            for field in fields:
                with self.subTest(nested=nested, missing=field):
                    day = deepcopy(self.days[0])
                    target = day["obra"] if nested else day
                    del target[field]
                    with self.assertRaisesRegex(ValueError, "obrigatório.*" + field):
                        self.load([day])
            day = deepcopy(self.days[0])
            target = day["obra"] if nested else day
            target["fokko"] = "50% 50%"
            with self.assertRaisesRegex(ValueError, "desconhecido.*fokko"):
                self.load([day])

    def test_reference_is_free_text_and_line_breaks_are_left_for_render_validation(self):
        day = deepcopy(self.days[0])
        day["referencia"] = "Santo Agostinho · Confissões"
        self.assertEqual(self.load([day])[0]["referencia"], day["referencia"])
        day["referencia"] = "Santo Agostinho\nConfissões"
        self.assertEqual(self.load([day])[0]["referencia"], day["referencia"])

    def test_zoom_accepts_numeric_boundaries_and_preserves_original_value(self):
        for zoom in (1, 1.05, 1.3, 2, 3):
            with self.subTest(zoom=zoom):
                day = deepcopy(self.days[0])
                day["obra"]["zoom"] = zoom
                self.assertEqual(self.load([day])[0]["obra"], day["obra"])

    def test_zoom_rejects_outside_range_bool_text_and_nonfinite_numbers(self):
        for zoom in (0.99, 3.01, -1, 0, True, False, "1.1", None, float("nan"), float("inf"), float("-inf")):
            with self.subTest(zoom=zoom):
                day = deepcopy(self.days[0])
                day["obra"]["zoom"] = zoom
                with self.assertRaisesRegex(ValueError, "obra.zoom"):
                    self.load([day])

    def test_work_stays_local_with_missing_files_allowed(self):
        for invalid in ("https://example.org/image.jpg", "../image.jpg", "/tmp/image.jpg", "C:\\image.jpg"):
            with self.subTest(path=invalid):
                day = deepcopy(self.days[0])
                day["obra"]["arquivo"] = invalid
                with self.assertRaisesRegex(ValueError, "obra.arquivo"):
                    self.load([day])
        day["obra"]["arquivo"] = "obras/coragem/ausente.jpg"
        self.assertEqual(self.load([day])[0]["obra"], day["obra"])

    def test_dates_normalize_without_new_weekday_restrictions(self):
        day = deepcopy(self.days[0])
        day["data"] = date(2026, 12, 20)  # Domingo não é proibido para Coragem.
        self.assertEqual(self.load([day])[0]["data"], "2026-12-20")
        for invalid in ("2026-02-30", "14/12/2026", datetime(2026, 12, 14, 9), None):
            with self.subTest(value=invalid):
                day["data"] = invalid
                with self.assertRaisesRegex(ValueError, "data"):
                    self.load([day])
        with self.assertRaisesRegex(ValueError, "data repetida"):
            self.load([self.days[0], self.days[0]])

    def test_color_table_and_nonempty_text_fields(self):
        for color in ("verde", "roxo", "ouro", "branco", "vermelho", "rosa"):
            day = deepcopy(self.days[0])
            day["cor"] = color
            self.assertEqual(self.load([day])[0]["cor"], color)
        day["cor"] = "azul"
        with self.assertRaisesRegex(ValueError, "Cor desconhecida"):
            self.load([day])
        for field in ("frase", "referencia"):
            for invalid in ("", " \n ", None, 123):
                with self.subTest(field=field, value=invalid):
                    day = deepcopy(self.days[0])
                    day[field] = invalid
                    with self.assertRaisesRegex(ValueError, field + ".*texto não vazio"):
                        self.load([day])

    def test_safe_yaml_duplicate_keys_and_wrong_document_shapes(self):
        for document in (
            "", "[]", "data: 2026-12-14", "- texto",
            "!!python/object/apply:os.system ['false']",
            "- data: 2026-12-14\n  data: 2026-12-28\n",
        ):
            with self.subTest(document=document):
                self.file.write_text(document, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_courage(self.file)


if __name__ == "__main__":
    unittest.main()
