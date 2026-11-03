"""Entrega final das duas novenas e persistência do resultado no Canva."""

from copy import deepcopy
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest

import fitz
from PIL import Image, ImageChops

from arteque_reza.base import PROJECT
from arteque_reza.conteudo_novena import load_novenas
from arteque_reza.serie_novena import _report, generate


def compact(value):
    return re.sub(r"\s+", "", value)


@unittest.skipUnless(shutil.which("chromium"), "Chromium é necessário para gerar os PDFs reais")
class NovenaSeriesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        work = PROJECT / "work"
        work.mkdir(exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(dir=work)
        cls.addClassCleanup(cls.temp.cleanup)
        cls.output = Path(cls.temp.name)
        cls.content = PROJECT / "conteudo/novenas.yaml"
        cls.novenas = load_novenas(cls.content)
        cls.result = generate(cls.output, cls.content)
        cls.target = cls.output / "novena"
        cls.checks = json.loads((cls.target / "verificacao.json").read_text(encoding="utf-8"))

    def test_final_mode_writes_ten_cards_ordered_pdf_and_matching_board_for_each_novena(self):
        slugs = [f"dia-{number}" for number in range(1, 10)] + ["encerramento"]
        for novena in self.novenas:
            identifier = novena["id"]
            with self.subTest(novena=identifier):
                folder = self.target / identifier
                self.assertEqual(
                    {path.name for path in folder.iterdir()},
                    {slug + ".png" for slug in slugs}
                    | {"prancha.png", "ficha.json", f"novena-{identifier}.pdf"},
                )
                ficha = json.loads((folder / "ficha.json").read_text(encoding="utf-8"))
                self.assertEqual(ficha["modo"], "final")
                self.assertEqual([card["slug"] for card in ficha["cards"]], slugs)
                self.assertEqual([card["arquivo"] for card in ficha["cards"]],
                                 [slug + ".png" for slug in slugs])
                self.assertEqual([card["data"] for card in ficha["cards"]],
                                 [day["data"] for day in novena["dias"]]
                                 + [novena["encerramento"]["data"]])
                self.assertEqual([card["pagina"] for card in ficha["cards"]], list(range(1, 11)))

                with fitz.open(folder / f"novena-{identifier}.pdf") as document:
                    self.assertEqual(len(document), 10)
                    for page, card in zip(document, ficha["cards"]):
                        self.assertEqual((page.rect.width, page.rect.height), (810, 1012.5))
                        expected = "".join(text["conteudo"] for text in card["textos"])
                        self.assertEqual(compact(page.get_text(sort=True)), compact(expected))

                # Mesmo formato da prova: cada card a 1/3, com etiquetas fora
                # das artes. Conferir os pixels também detecta ordem trocada.
                with Image.open(folder / "prancha.png") as raw_board:
                    board = raw_board.convert("RGB")
                self.assertEqual(board.size, (3880, 586))
                for index, slug in enumerate(slugs):
                    with Image.open(folder / (slug + ".png")) as image:
                        self.assertEqual(image.size, (1080, 1350))
                        expected = image.convert("RGB").resize((360, 450), Image.Resampling.LANCZOS)
                    x = 32 + index * 384
                    actual = board.crop((x, 104, x + 360, 554))
                    self.assertIsNone(ImageChops.difference(actual, expected).getbbox(), slug)

    def test_regenerated_report_keeps_the_canva_result_in_both_modes(self):
        heading = "## Resultado no Canva (03/11/2026)"
        report = self.target / "RELATORIO.md"
        for mode in ("teste-canva", "final"):
            with self.subTest(modo=mode):
                checks = deepcopy(self.checks)
                checks["modo"] = mode
                report.unlink(missing_ok=True)
                _report(self.target, checks, "python gerar.py novena")
                text = report.read_text(encoding="utf-8")
                self.assertEqual(text.count(heading), 1)
                section = text.split(heading, 1)[1].split("\n## ", 1)[0]
                self.assertIn("62 px", section)
                self.assertIn("itálico", section)
                self.assertIn("anéis", section)
                self.assertIn("API", section)
                self.assertRegex(section, r"1[,.]426")
                self.assertRegex(section, r"1[,.]409")
                self.assertIn("refrão", section)


if __name__ == "__main__":
    unittest.main()
