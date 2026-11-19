"""Stories avulsos e preservação pixel a pixel dos oito stories fixos."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from urllib.parse import urlsplit

import fitz
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright
import yaml

from gerar import ensure_kit
from arteque_reza.base import PROJECT, await_fonts, generate_tokens_css, render_arte, resource_url
from arteque_reza.conteudo import local_artwork_path
from arteque_reza.conteudo_stories import load_stories
from arteque_reza.conteudo_stories_avulsos import load_stories_avulsos
from arteque_reza.renderizacao import local_server
from arteque_reza.stories import _document, _measure, _pdf_check, _pixels, _validate_layout
from arteque_reza.stories_avulsos import _adapt, generate


@unittest.skipUnless(shutil.which('chromium'), 'Chromium é necessário para medir o layout real')
class LooseStoryLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_kit()
        (PROJECT/'work').mkdir(exist_ok=True)
        cls.temporary = tempfile.TemporaryDirectory(dir=PROJECT/'work')
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.folder = Path(cls.temporary.name)
        cls.css = generate_tokens_css(cls.folder/'tokens.css')
        cls.server = local_server(); cls.url = cls.server.__enter__()
        cls.addClassCleanup(cls.server.__exit__, None, None, None)
        cls.playwright = sync_playwright().start(); cls.addClassCleanup(cls.playwright.stop)
        cls.browser = cls.playwright.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
        cls.addClassCleanup(cls.browser.close)
        cls.context = cls.browser.new_context(device_scale_factor=1, viewport={'width':1080,'height':1920})
        cls.addClassCleanup(cls.context.close)
        cls.context.route('**/*', lambda route: route.continue_()
                          if urlsplit(route.request.url).netloc == urlsplit(cls.url).netloc else route.abort())
        cls.page = cls.context.new_page()
        cls.stories = load_stories_avulsos(PROJECT/'conteudo/stories-avulsos.yaml')

    def render(self, original, *, markup=None, filename='story', tempo=None):
        if tempo is None:
            tempo, story = _adapt(original)
        else:
            story = original
        markup = markup or _document(tempo, story, self.css, local_artwork_path(story['obra']['arquivo']))
        png = self.folder/(filename+'.png'); pdf = png.with_suffix('.pdf')
        render_arte(self.page, markup, png, formato='story', pdf_path=pdf, base_url=self.url)
        measured = _measure(self.page, tempo, story, 1)
        return tempo, story, measured, png, pdf

    def test_all_six_approved_stories_keep_positions_lines_colors_and_pdf(self):
        self.assertEqual(len(self.stories),6)
        for original in self.stories:
            with self.subTest(story=original['id']):
                tempo,story,measured,png,pdf = self.render(original,filename=original['id'])
                layout = _validate_layout(tempo,story,measured)
                self.assertEqual(layout['posicoes'], {'selo_topo_px':240,'nicho_topo_px':328,
                    'nicho_base_px':1028,'titulo_topo_px':1076,'assinatura_topo_px':1628})
                self.assertEqual(layout['titulo_subtitulo_px'],48)
                self.assertGreaterEqual(layout['ultimo_texto_assinatura_px'],32)
                fields={text['campo']:text for text in measured['textos']}
                for name,lines in [('titulo',1),('subtitulo',1),('invocacao',3)]:
                    self.assertEqual(fields[name]['quantidade_linhas'],lines)
                self.assertEqual(fields['selo']['conteudo'],original['serie'])
                self.assertEqual(fields['hora']['conteudo'],'· '+original['apoio'])
                self.assertNotIn('resposta',fields)
                self.assertTrue(_pixels(png,tempo,story,measured)['ok'])
                proof=_pdf_check(pdf,[story],[measured])
                self.assertTrue(proof['ok'])
                self.assertTrue(proof['nicho_vetorial']['ok'])
                self.assertTrue(all(font['embutida']for font in proof['fontes']))

    def test_fixed_stories_remain_identical_in_all_four_seasons(self):
        content=load_stories(PROJECT/'conteudo/stories.yaml')
        for tempo in content['tempos']:
            reference=PROJECT/'saida/stories'/tempo['id']
            with fitz.open(reference/f'stories-{tempo["id"]}.pdf')as approved_pdf:
                for index,story in enumerate(content['stories']):
                    with self.subTest(tempo=tempo['id'],story=story['id']):
                        _,_,measured,png,pdf=self.render(story,tempo=tempo,filename='fixed-'+tempo['id']+'-'+story['id'])
                        self.assertTrue(_validate_layout(tempo,story,measured)['ok'])
                        with Image.open(reference/(story['id']+'.png'))as a,Image.open(png)as b:
                            self.assertEqual(a.size,b.size)
                            self.assertIsNone(ImageChops.difference(a.convert('RGB'),b.convert('RGB')).getbbox())
                        with fitz.open(pdf)as actual_pdf:
                            images=[]
                            for page in (approved_pdf[index],actual_pdf[0]):
                                pix=page.get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
                                images.append(Image.frombytes('RGB',(pix.width,pix.height),pix.samples))
                            self.assertEqual(images[0].size,images[1].size)
                            self.assertIsNone(ImageChops.difference(*images).getbbox())

    def test_sixteen_pixel_title_subtitle_gap_is_rejected(self):
        tempo,story,_,_,_=self.render(self.stories[0])
        self.page.locator('[data-text="subtitulo"]').evaluate("el=>el.style.marginTop='0px'")
        measured=_measure(self.page,tempo,story,1)
        with self.assertRaisesRegex(ValueError,r'titulo.*subtitulo.*16\.00px.*48px'):
            _validate_layout(tempo,story,measured)

    def test_response_is_optional_and_a_short_response_fits(self):
        original=deepcopy(self.stories[0]);original.update(invocacao='Rezemos juntos.',resposta='Amém.')
        tempo,story,measured,_,_=self.render(original)
        layout=_validate_layout(tempo,story,measured)
        self.assertEqual(layout['invocacao_resposta_px'],48)
        self.assertEqual(layout['posicoes']['assinatura_topo_px'],1628)

    def test_response_requires_48_pixels_and_32_pixels_before_signature(self):
        original=deepcopy(self.stories[0]);original.update(invocacao='Rezemos juntos.',resposta='Amém.')
        tempo,story,_,_,_=self.render(original)
        self.page.locator('[data-text="resposta"]').evaluate("el=>el.style.marginTop='0px'")
        with self.assertRaisesRegex(ValueError,r'invocacao.*resposta.*16\.00px.*48px'):
            _validate_layout(tempo,story,_measure(self.page,tempo,story,1))
        original['invocacao']='Primeira frase de oração.\nSegunda frase de oração.'
        tempo,story,measured,_,_=self.render(original)
        with self.assertRaisesRegex(ValueError,r'assinatura'):
            _validate_layout(tempo,story,measured)

    def test_line_limits_stop_generation_instead_of_changing_approved_text(self):
        for field,limit in [('titulo',1),('subtitulo',1),('invocacao',3),('resposta',2)]:
            with self.subTest(field=field):
                original=deepcopy(self.stories[0]);original[field]='\n'.join(['Linha de oração']*(limit+1))
                tempo,story,measured,_,_=self.render(original)
                with self.assertRaisesRegex(ValueError,rf'{field}: {limit+1} linhas; limite {limit}'):
                    _validate_layout(tempo,story,measured)

    def test_fixed_o_label_is_the_only_single_letter_exception(self):
        original=deepcopy(self.stories[1])
        tempo,story,measured,_,_=self.render(original)
        self.assertTrue(_validate_layout(tempo,story,measured)['ok'])
        for changes,field in [({'serie':'Outra série Ó'},'selo'),({'invocacao':'Primeira frase\nSegunda frase\nÓ'},'invocacao')]:
            with self.subTest(field=field):
                altered={**original,**changes}
                tempo,story,measured,_,_=self.render(altered)
                with self.assertRaisesRegex(ValueError,field+': palavra de uma letra'):
                    _validate_layout(tempo,story,measured)

    def test_pdf_rejects_missing_vector_niche_and_extra_text(self):
        original=self.stories[0]
        tempo,story,measured,_,_=self.render(original)
        markup=_document(tempo,story,self.css,local_artwork_path(story['obra']['arquivo']))
        removed,count=re.subn(r'<svg\b[^>]*data-element="nicho-filete"[^>]*>.*?</svg>','',markup,flags=re.S)
        self.assertEqual(count,1)
        _,_,_,_,pdf=self.render(original,markup=removed,filename='no-vector')
        with self.assertRaisesRegex(ValueError,r'nicho|filete|vetorial|preenchimento'):
            _pdf_check(pdf,[story],[measured])
        extra='<span style="position:absolute;left:80px;top:1800px;font:400 24px Lato">Texto extra</span>'
        _,_,_,_,pdf=self.render(original,markup=markup.replace('</article>',extra+'</article>'),filename='extra')
        with self.assertRaisesRegex(ValueError,'texto integral diferente'):
            _pdf_check(pdf,[story],[measured])


@unittest.skipUnless(shutil.which('chromium'),'Chromium é necessário para gerar grupos')
class LooseStoryGenerationTests(unittest.TestCase):
    def test_group_filter_preserves_other_group_png_pdf_and_records(self):
        with tempfile.TemporaryDirectory(dir=PROJECT/'work')as temporary:
            folder=Path(temporary)
            source=PROJECT/'conteudo/stories-avulsos.yaml'
            result=generate(folder,source)
            self.assertEqual((result['grupos'],result['cards'],result['pdfs']),(3,6,3))
            target=folder/'stories-avulsos'
            protected={p.relative_to(target).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                       for group in ['chave-de-davi-2026-12-20','comece-aqui']
                       for p in (target/group).iterdir()if p.is_file()}
            filtered=generate(folder,source,'terco-2026-12-12')
            self.assertEqual((filtered['grupos'],filtered['cards'],filtered['pdfs']),(1,1,1))
            self.assertTrue(all(hashlib.sha256((target/name).read_bytes()).hexdigest()==digest
                                for name,digest in protected.items()))
            records=list(target.glob('*/ficha.json'));self.assertEqual(len(records),3)
            for record_path in records:
                record=json.loads(record_path.read_text());self.assertEqual(record['textos_aprovados_em'],'2026-11-19')
                with fitz.open(record_path.parent/(record['grupo']+'.pdf'))as pdf:
                    self.assertEqual(len(pdf),len(record['cards']))
                for card in record['cards']:
                    self.assertEqual(card['textos_aprovados_em'],'2026-11-19')
                    self.assertEqual(card['distancias']['posicoes']['assinatura_topo_px'],1628)
            with self.assertRaisesRegex(ValueError,'Nenhum grupo'):
                generate(folder,source,'grupo-inexistente')

    def test_missing_local_artwork_uses_placeholder_and_marks_pending(self):
        with tempfile.TemporaryDirectory(dir=PROJECT/'work')as temporary:
            folder=Path(temporary)
            story=deepcopy(load_stories_avulsos(PROJECT/'conteudo/stories-avulsos.yaml')[0])
            story['obra']['arquivo']='obras/stories/obra-que-nao-existe.jpg'
            source=folder/'missing.yaml';source.write_text(yaml.safe_dump([story],allow_unicode=True))
            result=generate(folder,source)
            self.assertEqual(result['obras_pendentes'],[story['id']])
            record=json.loads((folder/'stories-avulsos'/story['grupo']/'ficha.json').read_text())
            card=record['cards'][0]
            self.assertTrue(card['obra_pendente'])
            self.assertEqual(card['obra_usada'],'saida/obra-provisoria.png')
            self.assertIsNone(card['prova_recorte'])


if __name__=='__main__':
    unittest.main()
