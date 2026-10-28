"""Os limites editoriais contam linhas produzidas pelo Chromium, inclusive vazias."""
from copy import deepcopy
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

from gerar import ensure_kit
from arteque_reza.base import PROJECT, await_fonts, generate_tokens_css, resource_url
from arteque_reza.conteudo_oracao import load_prayers
from arteque_reza.para_rezar import _document, _measure, _validate_layout
from arteque_reza.renderizacao import local_server


@unittest.skipUnless(shutil.which('chromium'), 'Chromium necessário para contar as linhas reais')
class PrayerLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_kit()
        work = PROJECT/'work'; work.mkdir(exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(dir=work)
        cls.addClassCleanup(cls.temp.cleanup)
        cls.folder = Path(cls.temp.name)
        cls.css = generate_tokens_css(cls.folder/'tokens.css')
        cls.server = local_server(); cls.url = cls.server.__enter__()
        cls.addClassCleanup(cls.server.__exit__, None, None, None)
        cls.playwright = sync_playwright().start(); cls.addClassCleanup(cls.playwright.stop)
        cls.browser = cls.playwright.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
        cls.addClassCleanup(cls.browser.close)
        cls.context = cls.browser.new_context(device_scale_factor=1, viewport={'width':1080,'height':1350})
        cls.addClassCleanup(cls.context.close)
        cls.context.route('**/*',lambda route:route.continue_() if urlsplit(route.request.url).netloc==urlsplit(cls.url).netloc else route.abort())
        cls.page = cls.context.new_page()
        cls.days = load_prayers(PROJECT/'conteudo/para-rezar.yaml')

    def render(self, day, number):
        path = self.folder/'card.html'; path.write_text(_document(day, number, self.css), encoding='utf-8')
        self.page.goto(self.url+resource_url(path)); await_fonts(self.page)
        return _measure(self.page, day, number)

    @staticmethod
    def field(card, name):
        return next(text for text in card['textos'] if text['campo']==name)

    def test_supplied_prayers_have_expected_lines_and_equal_vertical_gaps(self):
        for day, counts, gaps in [(self.days[0], [7], [195.5]), (self.days[1], [6,6], [266.5,323])]:
            for number, count in enumerate(counts,1):
                with self.subTest(date=day['data'],card=number):
                    card = self.render(day,number)
                    self.assertEqual(self.field(card,'oracao')['quantidade_linhas'],count)
                    self.assertTrue(_validate_layout(day,card)['ok'])
                    self.assertAlmostEqual(card['distancias']['selo_texto_px'],gaps[number-1])
                    self.assertAlmostEqual(card['distancias']['texto_assinatura_px'],gaps[number-1])

    def test_eleven_prayer_lines_fail_on_first_card(self):
        day = deepcopy(self.days[0]); day['partes'][0] = '\n'.join(['Rezai sempre.']*11)
        card = self.render(day,1)
        self.assertEqual(self.field(card,'oracao')['quantidade_linhas'],11)
        with self.assertRaisesRegex(ValueError,r'2026-10-20, card 1, oracao: 11 linhas; limite 10'):
            _validate_layout(day,card)

    def test_fifteen_prayer_lines_fail_on_later_card(self):
        day = deepcopy(self.days[1]); day['partes'][1] = '\n'.join(['Rezai sempre.']*15)
        card = self.render(day,2)
        self.assertEqual(self.field(card,'oracao')['quantidade_linhas'],15)
        with self.assertRaisesRegex(ValueError,r'2026-12-15, card 2, oracao: 15 linhas; limite 14'):
            _validate_layout(day,card)

    def test_blank_forced_lines_count_toward_limit(self):
        day = deepcopy(self.days[0]); day['partes'][0] = 'Primeira linha.\n'+('\n'*9)+'Última linha.'
        card = self.render(day,1); text = self.field(card,'oracao')
        self.assertEqual(text['quantidade_linhas'],11)
        self.assertEqual(text['linhas'][1],'')
        with self.assertRaisesRegex(ValueError,r'oracao: 11 linhas; limite 10'):
            _validate_layout(day,card)

    def test_three_title_lines_fail(self):
        day = deepcopy(self.days[0]); day['titulo'] = 'Oração\npara pedir\nproteção'
        card = self.render(day,1)
        self.assertEqual(self.field(card,'titulo')['quantidade_linhas'],3)
        with self.assertRaisesRegex(ValueError,r'titulo: 3 linhas; limite 2'):
            _validate_layout(day,card)

    def test_manual_break_cannot_leave_one_letter_at_end(self):
        day = deepcopy(self.days[0]); day['partes'][0] = 'Vigiai e\nrezai sempre.'
        card = self.render(day,1)
        with self.assertRaisesRegex(ValueError,r'oracao: palavra de uma letra no fim'):
            _validate_layout(day,card)

    def test_unbroken_word_cannot_escape_the_prayer_column(self):
        day = deepcopy(self.days[0]); day['partes'][0] = 'Amém'*100
        card = self.render(day,1)
        self.assertGreater(self.field(card,'oracao')['caixas_das_linhas'][0]['largura'],880)
        with self.assertRaisesRegex(ValueError,r'oracao: linha transborda a largura do campo'):
            _validate_layout(day,card)


if __name__=='__main__':
    unittest.main()
