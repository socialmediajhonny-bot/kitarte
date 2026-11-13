"""Contrato estrito dos carrosséis de Igreja Doméstica."""

from copy import deepcopy
from datetime import date, datetime
from pathlib import Path
import tempfile
import unittest

import yaml

from arteque_reza.base import PROJECT
from arteque_reza.conteudo_igreja_domestica import (
    CARD_FIELDS, CARD_REQUIRED_FIELDS, DAY_FIELDS, load_domestic_church,
)


class DomesticChurchContentTests(unittest.TestCase):
    def setUp(self):
        self.days = load_domestic_church(PROJECT / "conteudo/igreja-domestica.yaml")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.file = Path(self.temp.name) / "igreja-domestica.yaml"

    def load(self, days):
        self.file.write_text(yaml.safe_dump(days, allow_unicode=True), encoding="utf-8")
        return load_domestic_church(self.file)

    def test_supplied_days_preserve_order_manual_breaks_and_approved_text(self):
        self.assertEqual([day["data"] for day in self.days], ["2026-11-29", "2026-12-06", "2026-12-13"])
        self.assertEqual([[card["tipo"] for card in day["cards"]] for day in self.days],
                         [["capa", "passos", "oracao", "conversa"], ["capa", "oracao", "conversa"],
                          ["capa", "passos", "passos", "oracao", "conversa"]])
        self.assertEqual(self.days[0]["cards"][2]["falas"][0]["rubrica"],
                         "Leiam o Evangelho do dia, Mc 13,33-37.\nDepois, quem conduz reza:")
        self.assertIn("3º domingo", self.days[0]["cards"][1]["itens"][1])
        self.assertEqual(self.days[1]["cards"][0]["obra"]["foco"], "50% 50%")
        self.assertEqual(self.load(self.days), self.days)
        for day in self.days:
            self.assertEqual(set(day), DAY_FIELDS)
            self.assertNotIn("zoom", day["cards"][0]["obra"])
            for card in day["cards"]:
                self.assertEqual(set(card), CARD_REQUIRED_FIELDS[card["tipo"]])

    def test_non_sunday_duplicate_or_invalid_dates_are_rejected(self):
        days = deepcopy(self.days)
        days[0]["data"] = "2026-11-30"
        with self.assertRaisesRegex(ValueError, "domingo"):
            self.load(days)
        days = deepcopy(self.days)
        days[1]["data"] = days[0]["data"]
        with self.assertRaisesRegex(ValueError, "data repetida"):
            self.load(days)
        for value in ("2026-02-30", "29/11/2026", None, True, datetime(2026, 11, 29, 6)):
            with self.subTest(value=value):
                days = deepcopy(self.days)
                days[0]["data"] = value
                with self.assertRaises(ValueError):
                    self.load(days)
        days[0]["data"] = date(2026, 11, 29)
        self.assertEqual(self.load(days)[0]["data"], "2026-11-29")

    def test_cards_require_two_to_five_entries(self):
        day = deepcopy(self.days[0])
        for invalid in (None, {}, "cards", [], day["cards"][:1], day["cards"] + day["cards"][1:3]):
            with self.subTest(value=invalid):
                changed = deepcopy(day)
                changed["cards"] = invalid
                with self.assertRaisesRegex(ValueError, "2 a 5 cards"):
                    self.load([changed])
        for cards in ([day["cards"][0], day["cards"][1]],
                      [*day["cards"][:3], deepcopy(day["cards"][2]), day["cards"][-1]]):
            changed = deepcopy(day)
            changed["cards"] = cards
            self.assertEqual(len(self.load([changed])[0]["cards"]), len(cards))

    def test_cover_must_be_first_and_unique(self):
        for cards in (self.days[0]["cards"][1:],
                      [self.days[0]["cards"][1], self.days[0]["cards"][0]],
                      [self.days[0]["cards"][0], self.days[0]["cards"][0]]):
            with self.subTest(cards=cards):
                day = deepcopy(self.days[0])
                day["cards"] = deepcopy(cards)
                with self.assertRaisesRegex(ValueError, "capa.*primeiro e único"):
                    self.load([day])

    def test_conversation_is_optional_but_can_only_be_last(self):
        day = deepcopy(self.days[0])
        day["cards"].pop()
        self.assertEqual(self.load([day])[0]["cards"], day["cards"])
        for cards in ([self.days[0]["cards"][0], self.days[0]["cards"][-1], self.days[0]["cards"][1]],
                      [self.days[0]["cards"][0], self.days[0]["cards"][-1], self.days[0]["cards"][-1]]):
            with self.subTest(cards=cards):
                day["cards"] = deepcopy(cards)
                with self.assertRaisesRegex(ValueError, "conversa.*último"):
                    self.load([day])

    def test_required_and_unknown_fields_are_checked_for_each_card_type(self):
        day = self.days[0]
        for index, card in enumerate(day["cards"]):
            for field in CARD_REQUIRED_FIELDS[card["tipo"]]:
                with self.subTest(tipo=card["tipo"], field=field):
                    changed = deepcopy(day)
                    del changed["cards"][index][field]
                    with self.assertRaisesRegex(ValueError, "tipo|obrigatório"):
                        self.load([changed])
            changed = deepcopy(day)
            changed["cards"][index]["errado"] = "campo indevido"
            with self.assertRaisesRegex(ValueError, "desconhecido.*errado"):
                self.load([changed])
        for field in DAY_FIELDS:
            changed = deepcopy(day)
            del changed[field]
            with self.assertRaisesRegex(ValueError, "obrigatório"):
                self.load([changed])
        changed = deepcopy(day)
        changed["extra"] = "campo indevido"
        with self.assertRaisesRegex(ValueError, "desconhecido.*extra"):
            self.load([changed])

    def test_unknown_card_types_and_non_maps_are_rejected(self):
        for invalid in ("tipo-desconhecido", "Capa", "", 1, None, []):
            with self.subTest(tipo=invalid):
                day = deepcopy(self.days[0])
                day["cards"][0]["tipo"] = invalid
                with self.assertRaisesRegex(ValueError, "tipo"):
                    self.load([day])
        for invalid in (None, "card", [], 3):
            day = deepcopy(self.days[0])
            day["cards"][0] = invalid
            with self.assertRaisesRegex(ValueError, "mapa"):
                self.load([day])

    def test_optional_origin_is_preserved_and_only_allowed_on_prayer_cards(self):
        day = deepcopy(self.days[0])
        day["cards"][2]["origem"] = "Oração escrita pela página"
        self.assertEqual(self.load([day])[0]["cards"][2]["origem"], "Oração escrita pela página")
        for index in (0, 1, 3):
            with self.subTest(card=index):
                changed = deepcopy(day)
                changed["cards"][index]["origem"] = "origem"
                with self.assertRaisesRegex(ValueError, "desconhecido.*origem"):
                    self.load([changed])

    def test_steps_need_two_to_five_nonempty_texts(self):
        for invalid in (None, "texto", {}, [], ["um"], ["item"]*6):
            with self.subTest(items=invalid):
                day = deepcopy(self.days[0])
                day["cards"][1]["itens"] = invalid
                with self.assertRaisesRegex(ValueError, "2 a 5 textos"):
                    self.load([day])
        for invalid in (None, True, "", " \n ", {}, []):
            day = deepcopy(self.days[0])
            day["cards"][1]["itens"][0] = invalid
            with self.assertRaisesRegex(ValueError, "texto não vazio"):
                self.load([day])

    def test_speeches_need_a_nonempty_list_of_single_known_keys(self):
        for invalid in (None, {}, "fala", []):
            day = deepcopy(self.days[0])
            day["cards"][2]["falas"] = invalid
            with self.assertRaisesRegex(ValueError, "lista não vazia"):
                self.load([day])
        for invalid in (None, "fala", {}, {"rubrica": "Rubrica", "oracao": "Oração"}, {"texto": "Texto"}):
            with self.subTest(speech=invalid):
                day = deepcopy(self.days[0])
                day["cards"][2]["falas"][0] = invalid
                with self.assertRaisesRegex(ValueError, "mapa|única chave|desconhecido"):
                    self.load([day])

    def test_at_least_one_prayer_speech_is_required_and_order_is_preserved(self):
        day = deepcopy(self.days[0])
        day["cards"][2]["falas"] = [{"rubrica": "Acendam as velas."}, {"aclamacao": "Amém!"}]
        with self.assertRaisesRegex(ValueError, "pelo menos uma oracao"):
            self.load([day])
        speeches = [{"oracao": "Senhor, ouvi-nos."}, {"rubrica": "Rezem juntos."},
                    {"oracao": "Senhor, ajudai-nos."}, {"aclamacao": "Amém!"}]
        day["cards"][2]["falas"] = speeches
        self.assertEqual(self.load([day])[0]["cards"][2]["falas"], speeches)

    def test_all_text_fields_reject_empty_or_non_text_values(self):
        for index, card in enumerate(self.days[0]["cards"]):
            for field in CARD_FIELDS[card["tipo"]] - {"tipo", "obra", "itens", "falas"}:
                for invalid in (None, True, 4, "", " \n "):
                    with self.subTest(card=index, field=field, value=invalid):
                        day = deepcopy(self.days[0])
                        day["cards"][index][field] = invalid
                        with self.assertRaisesRegex(ValueError, "texto não vazio"):
                            self.load([day])
        for key in ("rubrica", "oracao", "aclamacao"):
            day = deepcopy(self.days[0])
            day["cards"][2]["falas"] = [{"oracao": "Uma oração."}, {key: " "}]
            with self.assertRaisesRegex(ValueError, "texto não vazio"):
                self.load([day])

    def test_work_reuses_strict_local_path_focus_zoom_and_credit_validation(self):
        for field in ("arquivo", "credito", "pagina", "foco"):
            day = deepcopy(self.days[0])
            del day["cards"][0]["obra"][field]
            with self.assertRaisesRegex(ValueError, "obrigatório"):
                self.load([day])
        invalid_fields = (("arquivo", "../obra.jpg"), ("arquivo", "https://example.org/image.jpg"),
                          ("pagina", "arquivo.jpg"), ("foco", "101% 50%"), ("zoom", True), ("zoom", 0.9))
        for field, value in invalid_fields:
            with self.subTest(field=field, value=value):
                day = deepcopy(self.days[0])
                day["cards"][0]["obra"][field] = value
                with self.assertRaises(ValueError):
                    self.load([day])
        for zoom in (1, 1.3, 3):
            day = deepcopy(self.days[0])
            day["cards"][0]["obra"]["zoom"] = zoom
            self.assertEqual(self.load([day])[0]["cards"][0]["obra"]["zoom"], zoom)
        day["cards"][0]["obra"]["arquivo"] = "obras/igreja-domestica/ausente.jpg"
        self.assertEqual(self.load([day])[0]["cards"][0]["obra"]["arquivo"],
                         "obras/igreja-domestica/ausente.jpg")

    def test_root_shape_duplicate_keys_and_invalid_colors_are_rejected(self):
        for invalid in (None, {}, "texto", [], [None]):
            with self.subTest(value=invalid):
                with self.assertRaises(ValueError):
                    self.load(invalid)
        self.file.write_text("- data: 2026-11-29\n  data: 2026-12-06\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Campo repetido"):
            load_domestic_church(self.file)
        for invalid in ("azul", None, True):
            day = deepcopy(self.days[0])
            day["cor"] = invalid
            with self.assertRaisesRegex(ValueError, "Cor desconhecida"):
                self.load([day])


if __name__ == "__main__":
    unittest.main()
