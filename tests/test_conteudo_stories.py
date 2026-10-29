"""Contrato dos stories: tempos, horas, ids seguros e obra local opcionalmente ampliada."""

from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

import yaml

from arteque_reza.base import PROJECT
from arteque_reza.conteudo_stories import (
    ROOT_FIELDS, SEASON_FIELDS, STORY_REQUIRED_FIELDS, load_stories,
)


class StoryContentTests(unittest.TestCase):
    def setUp(self):
        self.content = load_stories(PROJECT / "conteudo/stories.yaml")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.file = Path(self.temp.name) / "stories.yaml"

    def load(self, content):
        self.file.write_text(yaml.safe_dump(content, allow_unicode=True), encoding="utf-8")
        return load_stories(self.file)

    def test_supplied_content_has_no_dates_or_added_defaults_and_preserves_order(self):
        self.assertEqual(set(self.content), {"tempos", "stories"})
        self.assertEqual([item["id"] for item in self.content["tempos"]], ["advento", "natal", "tempo-comum", "quaresma"])
        self.assertEqual([item["id"] for item in self.content["stories"]], ["angelus", "misericordia"])
        angelus, mercy = self.content["stories"]
        self.assertEqual(angelus["hora"], "12h")
        self.assertEqual(mercy["hora"], "15h")
        self.assertEqual(angelus["resposta"], "E ela concebeu do Espírito Santo. Ave, Maria…")
        self.assertEqual(mercy["invocacao"], "Ó Sangue e Água, que jorrastes\ndo Coração de Jesus como fonte\nde misericórdia para nós, eu confio em Vós!")
        self.assertNotIn("resposta", mercy)
        self.assertNotIn("zoom", angelus["obra"])
        self.assertEqual(mercy["obra"]["zoom"], 1.15)
        for story in self.content["stories"]:
            self.assertNotIn("data", story)
        self.assertEqual(self.load(self.content), self.content)

    def test_root_season_story_and_work_each_reject_unknown_fields(self):
        for level in ("root", "season", "story", "work"):
            with self.subTest(level=level):
                content = deepcopy(self.content)
                target = {
                    "root": content,
                    "season": content["tempos"][0],
                    "story": content["stories"][0],
                    "work": content["stories"][0]["obra"],
                }[level]
                target["desconhecido"] = "erro de digitação"
                with self.assertRaisesRegex(ValueError, "campo desconhecido.*desconhecido"):
                    self.load(content)

    def test_required_fields_are_not_defaulted_at_any_level(self):
        levels = (
            ("root", ROOT_FIELDS),
            ("season", SEASON_FIELDS),
            ("story", STORY_REQUIRED_FIELDS),
            ("work", {"arquivo", "credito", "pagina", "foco"}),
        )
        for level, fields in levels:
            for field in fields:
                with self.subTest(level=level, missing=field):
                    content = deepcopy(self.content)
                    target = {
                        "root": content,
                        "season": content["tempos"][0],
                        "story": content["stories"][0],
                        "work": content["stories"][0]["obra"],
                    }[level]
                    del target[field]
                    with self.assertRaisesRegex(ValueError, "obrigatório.*" + field):
                        self.load(content)

    def test_seasons_and_stories_must_be_nonempty_lists_of_maps(self):
        for field in ("tempos", "stories"):
            for invalid in (None, [], "texto", {}, [None], ["texto"]):
                with self.subTest(field=field, value=invalid):
                    content = deepcopy(self.content)
                    content[field] = invalid
                    with self.assertRaisesRegex(ValueError, field):
                        self.load(content)

    def test_ids_are_unique_in_each_list_independently(self):
        for field, label in (("tempos", "tempo"), ("stories", "story")):
            with self.subTest(field=field):
                content = deepcopy(self.content)
                content[field][1]["id"] = content[field][0]["id"]
                with self.assertRaisesRegex(ValueError, "id de " + label + " repetido"):
                    self.load(content)
        content = deepcopy(self.content)
        content["tempos"][0]["id"] = content["stories"][0]["id"]
        self.assertEqual(self.load(content), content)

    def test_ids_cannot_escape_output_directories_or_form_unsafe_filenames(self):
        for field in ("tempos", "stories"):
            for invalid in ("", " ", "..", "../escape", "/tmp/story", "a/b", "a\\b", "https://example.org/a", "com espaço", "story\n", "-opcao", "angelus.png", None, 12):
                with self.subTest(field=field, value=invalid):
                    content = deepcopy(self.content)
                    content[field][0]["id"] = invalid
                    with self.assertRaisesRegex(ValueError, r"\.id"):
                        self.load(content)
        for valid in ("tempo-comum", "Story_2", "123"):
            content = deepcopy(self.content)
            content["stories"][0]["id"] = valid
            self.assertEqual(self.load(content)["stories"][0]["id"], valid)

    def test_hours_accept_exactly_0h_through_23h(self):
        for hour in range(24):
            content = deepcopy(self.content)
            content["stories"][0]["hora"] = f"{hour}h"
            self.assertEqual(self.load(content)["stories"][0]["hora"], f"{hour}h")
        for invalid in ("12:00", "24h", "-1h", "00h", "01h", "012h", "12H", "12 h", " 12h", "12h\n", 12, None):
            with self.subTest(hour=invalid):
                content = deepcopy(self.content)
                content["stories"][0]["hora"] = invalid
                with self.assertRaisesRegex(ValueError, r"stories\[1\]\.hora"):
                    self.load(content)

    def test_colors_reuse_the_existing_six_color_schema(self):
        for color in ("verde", "roxo", "ouro", "branco", "vermelho", "rosa"):
            content = deepcopy(self.content)
            content["tempos"][0]["cor"] = color
            self.assertEqual(self.load(content)["tempos"][0]["cor"], color)
        for invalid in ("azul", "Roxo", "", None, 12):
            with self.subTest(color=invalid):
                content = deepcopy(self.content)
                content["tempos"][0]["cor"] = invalid
                with self.assertRaisesRegex(ValueError, "Cor desconhecida"):
                    self.load(content)

    def test_all_text_fields_and_optional_response_must_be_nonempty_text(self):
        for level, fields in (("tempos", ("nome",)), ("stories", ("titulo", "subtitulo", "invocacao", "resposta"))):
            for field in fields:
                for invalid in ("", " \n\t ", None, 123):
                    with self.subTest(level=level, field=field, value=invalid):
                        content = deepcopy(self.content)
                        content[level][0][field] = invalid
                        with self.assertRaisesRegex(ValueError, field + ".*texto não vazio"):
                            self.load(content)
        content = deepcopy(self.content)
        del content["stories"][0]["resposta"]
        self.assertNotIn("resposta", self.load(content)["stories"][0])

    def test_work_zoom_is_optional_finite_numeric_and_in_range(self):
        for zoom in (1, 1.05, 2, 3):
            content = deepcopy(self.content)
            content["stories"][0]["obra"]["zoom"] = zoom
            self.assertEqual(self.load(content)["stories"][0]["obra"]["zoom"], zoom)
        for zoom in (0.99, 3.01, 0, -1, True, False, "1.1", None, float("nan"), float("inf"), float("-inf")):
            with self.subTest(zoom=zoom):
                content = deepcopy(self.content)
                content["stories"][0]["obra"]["zoom"] = zoom
                with self.assertRaisesRegex(ValueError, "obra.zoom"):
                    self.load(content)

    def test_works_are_local_and_may_be_pending_without_downloads(self):
        for invalid in ("https://example.org/image.jpg", "../image.jpg", "/tmp/image.jpg", "C:\\image.jpg"):
            with self.subTest(path=invalid):
                content = deepcopy(self.content)
                content["stories"][0]["obra"]["arquivo"] = invalid
                with self.assertRaisesRegex(ValueError, "obra.arquivo"):
                    self.load(content)
        content["stories"][0]["obra"]["arquivo"] = "obras/stories/ausente.jpg"
        self.assertEqual(self.load(content), content)

    def test_yaml_keys_cannot_be_repeated_in_root_or_items(self):
        for document in (
            "tempos: []\ntempos: []\nstories: []\n",
            "tempos:\n  - id: advento\n    id: natal\nstories: []\n",
            "tempos: []\nstories:\n  - id: angelus\n    id: misericordia\n",
            "tempos: []\nstories:\n  - obra:\n      arquivo: um.jpg\n      arquivo: dois.jpg\n",
        ):
            with self.subTest(document=document):
                self.file.write_text(document, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "Campo repetido"):
                    load_stories(self.file)

    def test_safe_yaml_rejects_unsafe_tags_and_wrong_root_shapes(self):
        for document in ("", "[]", "- texto", "texto", "!!python/object/apply:os.system ['false']"):
            with self.subTest(document=document):
                self.file.write_text(document, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_stories(self.file)


if __name__ == "__main__":
    unittest.main()
