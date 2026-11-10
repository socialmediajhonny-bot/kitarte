"""Contrato do YAML: erros úteis antes de iniciar renderizações caras."""

from copy import deepcopy
from datetime import datetime
from pathlib import Path
import tempfile
import unittest
import warnings

import yaml

from arteque_reza.base import PROJECT
from arteque_reza.conteudo import (
    ContentWarning, color_token, date_label, expanded_reference,
    load_content, local_artwork_path, text_html,
)


class ContentTests(unittest.TestCase):
    def setUp(self):
        self.days = load_content(PROJECT / "conteudo/evangelho.yaml")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.file = Path(self.temp.name) / "content.yaml"

    def load(self, days):
        self.file.write_text(yaml.safe_dump(days, allow_unicode=True), encoding="utf-8")
        return load_content(self.file)

    def test_exact_content_preserves_manual_and_folded_lines(self):
        self.assertEqual(
            [day["data"] for day in self.days],
            ["2026-11-29", "2026-11-30"]
            + [f"2026-12-{number:02d}" for number in range(1, 32)],
        )
        by_date = {day["data"]: day for day in self.days}
        self.assertEqual(by_date["2026-11-29"]["titulo"], "O Senhor vem.\nFique acordado.")
        self.assertEqual(by_date["2026-11-29"]["trecho"], "O que vos digo, digo a todos:\nVigiai!")
        self.assertNotIn("\n", by_date["2026-11-29"]["reflexao"]["texto"])
        self.assertEqual(by_date["2026-12-13"]["obra"]["pagina"], "https://www.brooklynmuseum.org/objects/4449")
        self.assertEqual(by_date["2026-11-30"]["trecho"],
                         "Segui-me,\ne eu farei de vós\npescadores de homens.")
        self.assertNotIn("\n", by_date["2026-12-06"]["reflexao"]["texto"])
        self.assertEqual(by_date["2026-12-05"]["referencia"], "Mt 9,35-10,1.6-8")
        for day in ("2026-12-20", "2026-12-27"):
            self.assertNotIn("\n", by_date[day]["reflexao"]["texto"])
        self.assertEqual(by_date["2026-12-25"]["referencia"], "Lc 2,1-14 (Missa da noite)")
        self.assertEqual(by_date["2026-12-15"]["trecho"],
                         "O filho respondeu: ‘Não quero’. Mas depois mudou de opinião e foi.")
        self.assertNotIn("'", by_date["2026-12-15"]["trecho"])
        self.assertEqual(by_date["2026-12-18"]["trecho"],
                         "Eis que a virgem conceberá e dará à luz um filho. Ele será chamado pelo nome de Emanuel, que significa: Deus está conosco.")
        self.assertEqual(by_date["2026-12-20"]["obra"]["foco"], "25% 50%")
        self.assertEqual(by_date["2026-12-20"]["obra"]["zoom"], 1)

    def test_unknown_fields_rejected_at_each_level(self):
        for nested, label in ((None, "dia 1"), ("obra", "obra"), ("reflexao", "reflexao")):
            with self.subTest(nested=nested):
                days = deepcopy(self.days)
                target = days[0] if nested is None else days[0][nested]
                target["titlo"] = "erro de digitação"
                with self.assertRaisesRegex(ValueError, label + ".*campo desconhecido.*titlo"):
                    self.load(days)

    def test_missing_and_wrong_types_rejected(self):
        for field, value in (("titulo", ""), ("trecho", 5), ("pergunta", None), ("cor", ["rosa"])):
            with self.subTest(field=field):
                days = deepcopy(self.days)
                days[0][field] = value
                with self.assertRaises(ValueError):
                    self.load(days)
        days = deepcopy(self.days)
        del days[0]["obra"]["credito"]
        with self.assertRaisesRegex(ValueError, "obrigatório.*credito"):
            self.load(days)

    def test_invalid_dates_duplicate_dates_and_timestamps_rejected(self):
        for invalid in ("2026-02-30", "29/11/2026", datetime(2026, 11, 29, 6, 0)):
            with self.subTest(invalid=invalid):
                days = deepcopy(self.days)
                days[0]["data"] = invalid
                with self.assertRaisesRegex(ValueError, "data"):
                    self.load(days)
        with self.assertRaisesRegex(ValueError, "data repetida"):
            self.load([self.days[0], self.days[0]])

    def test_sunday_requires_reflection_but_weekday_allows_it_with_warning(self):
        days = deepcopy(self.days)
        del days[0]["reflexao"]
        with self.assertRaisesRegex(ValueError, "2026-11-29.*domingo sem reflexão"):
            self.load(days)
        days = [deepcopy(self.days[0])]
        days[0]["data"] = "2026-11-30"
        with warnings.catch_warnings(record=True) as found:
            warnings.simplefilter("always")
            self.assertIn("reflexao", self.load(days)[0])
        self.assertEqual(len(found), 1)
        self.assertIs(found[0].category, ContentWarning)
        self.assertIn("solenidades", str(found[0].message))
        del days[0]["reflexao"]
        with warnings.catch_warnings(record=True) as found:
            self.assertNotIn("reflexao", self.load(days)[0])
        self.assertEqual(found, [])

    def test_reference_books_and_syntax(self):
        for field in ("referencia", "trecho_ref"):
            for invalid in ("At 1,1", "Marcos 13,37", "Mc 13", "Jo 0,1", "Jo 1,0"):
                with self.subTest(field=field, value=invalid):
                    days = deepcopy(self.days)
                    days[0][field] = invalid
                    with self.assertRaisesRegex(ValueError, field + ".*referência inválida"):
                        self.load(days)
        self.assertEqual(expanded_reference("Jo 1,6-8.19-28"), "João 1,6-8.19-28")
        self.assertEqual(expanded_reference("Mc 13,33-37"), "Marcos 13,33-37")

    def test_reference_accepts_the_four_christmas_mass_names(self):
        for name in ("Missa da vigília", "Missa da noite", "Missa da aurora", "Missa do dia"):
            with self.subTest(name=name):
                day = deepcopy(self.days[0])
                reference = f"Lc 2,1-14 ({name})"
                day["referencia"] = reference
                self.assertEqual(self.load([day])[0]["referencia"], reference)

    def test_reference_rejects_inexact_mass_suffixes(self):
        for reference in ("Lc 2,1-14 (Missa)", "Lc 2,1-14 (missa da noite)",
                          "Lc 2,1-14(Missa da noite)"):
            with self.subTest(reference=reference):
                day = deepcopy(self.days[0])
                day["referencia"] = reference
                with self.assertRaisesRegex(ValueError, "referencia.*referência inválida"):
                    self.load([day])

    def test_excerpt_reference_rejects_mass_suffixes(self):
        for name in ("Missa da vigília", "Missa da noite", "Missa da aurora", "Missa do dia"):
            with self.subTest(name=name):
                day = deepcopy(self.days[0])
                day["trecho_ref"] = f"Lc 2,11 ({name})"
                with self.assertRaisesRegex(ValueError, "trecho_ref.*referência inválida"):
                    self.load([day])

    def test_expanded_reference_preserves_the_mass_name(self):
        self.assertEqual(expanded_reference("Lc 2,1-14 (Missa da noite)"),
                         "Lucas 2,1-14 (Missa da noite)")

    def test_colors_and_locale_independent_date_labels(self):
        self.assertEqual(color_token("ouro"), "liturgico-branco")
        self.assertEqual(color_token("branco"), "liturgico-branco")
        with self.assertRaisesRegex(ValueError, "Cor desconhecida"):
            color_token("azul")
        self.assertEqual(date_label("2026-11-29"), "dom, 29 nov")
        self.assertEqual(date_label("2026-12-13"), "dom, 13 dez")
        self.assertEqual(date_label("2026-10-17"), "sáb, 17 out")

    def test_artwork_never_uses_remote_or_outside_paths(self):
        for invalid in ("https://example.org/a.jpg", "//example.org/a.jpg", "../a.jpg", "/tmp/a.jpg", "C:\\a.jpg", "obras/a.jpg?x=1", "obras/a.jpg\n"):
            with self.subTest(invalid=invalid):
                days = deepcopy(self.days)
                days[0]["obra"]["arquivo"] = invalid
                with self.assertRaisesRegex(ValueError, "obra.arquivo"):
                    self.load(days)
        root = Path(self.temp.name) / "root"
        root.mkdir()
        (root / "outside").symlink_to(root.parent, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "sai do projeto"):
            local_artwork_path("outside/art.jpg", root)
        # Missing local work is valid; the renderer is responsible for fallback.
        self.assertEqual(local_artwork_path("obras/ausente.jpg", root), root / "obras/ausente.jpg")

    def test_duplicate_yaml_keys_are_errors(self):
        self.file.write_text("- data: 2026-11-29\n  data: 2026-12-13\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Campo repetido.*data"):
            load_content(self.file)

    def test_text_html_escapes_markup_and_preserves_only_manual_breaks(self):
        result = text_html('A mão e o coração\nÉ tempo à luz <b> & "paz"')
        self.assertEqual(
            result,
            'A\u00a0mão e\u00a0o\u00a0coração<br>É\u00a0tempo à\u00a0luz &lt;b&gt; &amp; &quot;paz&quot;',
        )
        self.assertEqual(text_html("Deus e\nMaria"), "Deus e<br>Maria")


if __name__ == "__main__":
    unittest.main()
