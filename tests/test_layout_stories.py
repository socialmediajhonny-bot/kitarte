"""Stories: limites, posições, Ó inseparável e PDF com texto integral."""

from copy import deepcopy
from pathlib import Path
import shutil
import tempfile
import unittest
from urllib.parse import urlsplit

from PIL import Image
from playwright.sync_api import sync_playwright

from gerar import ensure_kit
from arteque_reza.base import PROJECT, await_fonts, generate_tokens_css, render_arte, resource_url
from arteque_reza.conteudo import local_artwork_path, text_html
from arteque_reza.conteudo_stories import load_stories
from arteque_reza.obras import artwork_geometry
from arteque_reza.renderizacao import local_server
from arteque_reza.stories import (_document, _measure, _pdf_check, _preview_check,
    _source_warnings, _validate_layout, _visual_note)


@unittest.skipUnless(shutil.which('chromium'), 'Chromium é necessário para medir o layout real')
class StoryLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_kit()
        work = PROJECT/'work'; work.mkdir(exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(dir=work)
        cls.addClassCleanup(cls.temp.cleanup)
        cls.folder = Path(cls.temp.name); cls.css = generate_tokens_css(cls.folder/'tokens.css')
        cls.server = local_server(); cls.url = cls.server.__enter__()
        cls.addClassCleanup(cls.server.__exit__, None, None, None)
        cls.playwright = sync_playwright().start(); cls.addClassCleanup(cls.playwright.stop)
        cls.browser = cls.playwright.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
        cls.addClassCleanup(cls.browser.close)
        cls.context = cls.browser.new_context(device_scale_factor=1, viewport={'width':1080,'height':1920})
        cls.addClassCleanup(cls.context.close)
        cls.context.route('**/*', lambda route:route.continue_()
            if urlsplit(route.request.url).netloc == urlsplit(cls.url).netloc else route.abort())
        cls.page = cls.context.new_page()
        content = load_stories(PROJECT/'conteudo/stories.yaml')
        cls.tempo = content['tempos'][0]; cls.stories = content['stories']

    def render(self, story):
        path = self.folder/'story.html'
        path.write_text(_document(self.tempo,story,self.css,local_artwork_path(story['obra']['arquivo'])),encoding='utf-8')
        self.page.goto(self.url+resource_url(path)); await_fonts(self.page)
        return _measure(self.page,self.tempo,story,1)

    def test_given_stories_keep_the_preview_positions_and_expected_distances(self):
        for story,gap in zip(self.stories,(127,69)):
            with self.subTest(story=story['id']):
                measured = self.render(story); result = _validate_layout(self.tempo,story,measured)
                self.assertTrue(result['ok'])
                self.assertEqual(result['posicoes'],{'selo_topo_px':240,'nicho_topo_px':328,
                    'nicho_base_px':1028,'titulo_topo_px':1076,'assinatura_topo_px':1628})
                self.assertEqual(result['ultimo_texto_assinatura_px'],gap)
                self.assertEqual(result['nicho_bloco_texto_px'],48)
                fields = {text['campo']:text for text in measured['textos']}
                self.assertEqual(fields['titulo']['quantidade_linhas'],1)
                self.assertEqual(fields['subtitulo']['quantidade_linhas'],1)
                self.assertEqual(fields['invocacao']['quantidade_linhas'],1 if story['id']=='angelus' else 3)

    def test_mercy_uses_the_approved_zoom_and_preserves_the_requested_window(self):
        story = self.stories[1]
        self.assertEqual(story['obra']['foco'], '50% 8%')
        self.assertEqual(story['obra']['zoom'], 1.15)
        artwork = local_artwork_path(story['obra']['arquivo'])
        framing = artwork_geometry(artwork, story['obra']['foco'], story['obra']['zoom'],
            niche_width=600, niche_height=700)
        window = framing['janela_original']
        for field, expected in [('x',116), ('y',91), ('largura',1547), ('altura',1863)]:
            self.assertAlmostEqual(window[field], expected, delta=1)
        self.render(story)
        self.assertEqual(self.page.locator('.aqr-nicho__obra img').evaluate(
            "el=>getComputedStyle(el).transform"), 'matrix(1.15, 0, 0, 1.15, 0, 0)')
        note = _visual_note(story, artwork, False, framing)
        self.assertNotIn('sugestao_opcional', note)
        for essential in ('rosto', 'auréola', 'duas mãos', 'mangas', 'começo dos raios'):
            self.assertIn(essential, note['nota'])

    def test_preview_at_the_origin_is_identical_outside_the_artwork_and_rejects_a_changed_pixel(self):
        story = self.stories[0]
        tempo = {'id':'tempo-comum', 'nome':'Tempo Comum', 'cor':'verde'}
        target = self.folder/'preview-check'; reference = target/'tempo-comum/angelus.png'
        artwork = local_artwork_path(story['obra']['arquivo'])
        render_arte(self.page, _document(tempo,story,self.css,artwork), reference,
            formato='story', base_url=self.url)
        result = _preview_check(self.page,self.css,target,self.folder/'preview-work',self.url)
        self.assertTrue(result['ok'])
        self.assertEqual(result['origem_article_px'], [0,0])
        self.assertEqual(result['pixels_alterados_fora_obra'], 0)
        self.assertIsNone(result['diferenca'])
        with Image.open(reference) as raw:
            altered = raw.convert('RGB')
        altered.putpixel((8,8),(255,0,0)); altered.save(reference)
        result = _preview_check(self.page,self.css,target,self.folder/'preview-work',self.url)
        self.assertFalse(result['ok'])
        self.assertEqual(result['pixels_alterados_fora_obra'], 1)
        self.assertTrue((PROJECT/result['diferenca']).is_file())

    def test_title_subtitle_invocation_and_response_limits_reject_extra_lines(self):
        for field,limit in [('titulo',1),('subtitulo',1),('invocacao',3),('resposta',2)]:
            with self.subTest(field=field):
                story = deepcopy(self.stories[0]); story[field] = '\n'.join(['Linha de oração']*(limit+1))
                measured = self.render(story)
                text = next(text for text in measured['textos'] if text['campo']==field)
                self.assertEqual(text['quantidade_linhas'],limit+1)
                with self.assertRaisesRegex(ValueError,f'advento, angelus, {field}: {limit+1} linhas; limite {limit}'):
                    _validate_layout(self.tempo,story,measured)

    def test_three_visible_invocation_lines_plus_empty_forced_line_exceed_limit(self):
        story = deepcopy(self.stories[1]); story['invocacao'] = 'Primeira frase\n\nSegunda frase\nTerceira frase'
        measured = self.render(story)
        text = next(text for text in measured['textos'] if text['campo']=='invocacao')
        self.assertEqual(text['linhas'][1],'')
        self.assertEqual(text['quantidade_linhas'],4)
        with self.assertRaisesRegex(ValueError,'invocacao: 4 linhas; limite 3'):
            _validate_layout(self.tempo,story,measured)

    def test_last_text_requires_at_least_32_pixels_before_the_signature(self):
        story = self.stories[0]; self.render(story)
        self.page.locator('.aqr-assinatura').evaluate("el=>el.style.transform='translateY(-100px)'")
        with self.assertRaisesRegex(ValueError,'resposta: distância à assinatura 27.00px < 32px'):
            _validate_layout(self.tempo,story,_measure(self.page,self.tempo,story,1))

    def test_o_with_acute_accent_is_joined_to_the_following_word(self):
        self.assertEqual(text_html('Ó Sangue e Água, ó fonte de paz.'),'Ó\u00a0Sangue e\u00a0Água, ó\u00a0fonte de paz.')
        measured = self.render(self.stories[1])
        invocation = next(text for text in measured['textos'] if text['campo']=='invocacao')
        self.assertTrue(invocation['linhas'][0].startswith('Ó\u00a0Sangue'))
        story = deepcopy(self.stories[1]); story['invocacao'] = 'Ó\nSangue e Água'
        with self.assertRaisesRegex(ValueError,'invocacao: palavra de uma letra no fim'):
            _validate_layout(self.tempo,story,self.render(story))

    def test_unbroken_text_cannot_escape_the_story(self):
        story = deepcopy(self.stories[0]); story['subtitulo'] = 'Amém'*80
        with self.assertRaisesRegex(ValueError,'subtitulo: (texto fora da arte|linha transborda)'):
            _validate_layout(self.tempo,story,self.render(story))

    def test_pdf_checks_the_complete_expected_text_and_rejects_an_unmarked_extra_run(self):
        story = self.stories[0]; artwork = local_artwork_path(story['obra']['arquivo'])
        markup = _document(self.tempo,story,self.css,artwork)
        pdf = self.folder/'story.pdf'
        render_arte(self.page,markup,pdf.with_suffix('.png'),formato='story',pdf_path=pdf,base_url=self.url)
        measured = _measure(self.page,self.tempo,story,1)
        result = _pdf_check(pdf,[story],[measured])
        self.assertTrue(result['paginas'][0]['texto_integral_pymupdf_igual'])
        self.assertTrue(result['paginas'][0]['texto_integral_pdftotext_igual'])
        self.assertEqual(len(result['fontes_exigidas']),5)
        extra = '<span style="position:absolute;left:80px;top:1700px;font:400 24px Lato">Texto extra</span>'
        corrupted = markup.replace('</article>',extra+'</article>')
        altered = self.folder/'extra.pdf'
        render_arte(self.page,corrupted,altered.with_suffix('.png'),formato='story',pdf_path=altered,base_url=self.url)
        with self.assertRaisesRegex(ValueError,'texto integral diferente do conteúdo esperado'):
            _pdf_check(altered,[story],[measured])

    def test_photo_size_and_width_are_warnings_not_exceptions(self):
        path = self.folder/'small.png'
        Image.new('RGB',(200,300),'red').save(path)
        with path.open('ab') as stream: stream.write(b'\0'*4_000_001)
        warnings = _source_warnings(self.stories[0],path)
        self.assertEqual(len(warnings),2)
        self.assertTrue(any('acima de 4 MB' in warning for warning in warnings))
        self.assertTrue(any('abaixo de 1000px' in warning for warning in warnings))


if __name__ == '__main__':
    unittest.main()
