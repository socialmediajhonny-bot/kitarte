"""Contrato dos PDFs experimentais: estrutura, camada, giro e respiro reais."""
from math import atan2, degrees
from pathlib import Path
import shutil
import tempfile
import unittest

import fitz
from pypdf import PdfReader
from pypdf.generic import ContentStream

from gerar import ensure_kit
from arteque_reza.base import PROJECT
from arteque_reza.teste_canva import generate


@unittest.skipUnless(shutil.which('chromium'), 'Chromium necessário para produzir os PDFs reais')
class CanvaExperimentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_kit()
        work=PROJECT/'work';work.mkdir(exist_ok=True)
        cls.temp=tempfile.TemporaryDirectory(dir=work)
        cls.addClassCleanup(cls.temp.cleanup)
        cls.output=Path(cls.temp.name)
        cls.result=generate(cls.output)
        cls.target=cls.output/'teste-canva'

    def test_only_b_retains_marked_structure_after_pdf_box_correction(self):
        a=PdfReader(self.target/'teste-canva-a.pdf')
        b=PdfReader(self.target/'teste-canva-b.pdf')
        self.assertEqual((len(a.pages),len(b.pages)),(14,2))
        for name in ('/StructTreeRoot','/MarkInfo'):
            self.assertNotIn(name,a.trailer['/Root'])
            self.assertIn(name,b.trailer['/Root'])
        self.assertIs(b.trailer['/Root']['/MarkInfo']['/Marked'].value,True)
        for reader in (a,b):
            for page in reader.pages:
                self.assertEqual(list(page.mediabox),[0,0,810,1012.5])
                self.assertEqual(list(page.cropbox),[0,0,810,1012.5])

    def test_opacity_produces_a_transparency_form_with_one_text_block(self):
        reader=PdfReader(self.target/'teste-canva-a.pdf')
        for index in (2,3):
            with self.subTest(page=index+1):
                forms=[]
                for reference in reader.pages[index]['/Resources'].get('/XObject',{}).values():
                    obj=reference.get_object()
                    if obj.get('/Subtype')=='/Form' and obj.get('/Group',{}).get('/S')=='/Transparency':
                        forms.append(obj)
                self.assertEqual(len(forms),1)
                operations=ContentStream(forms[0],reader).operations
                self.assertEqual(sum(operator==b'BT' for _,operator in operations),1)
                self.assertEqual(sum(operator==b'ET' for _,operator in operations),1)
                self.assertTrue(any(operator in {b'Tj',b'TJ'} for _,operator in operations))

    def test_half_degree_rotation_applies_to_only_the_target_line(self):
        with fitz.open(self.target/'teste-canva-a.pdf') as document:
            for index,target in ((4,'Mc 13,37'),(5,'Para rezar hoje')):
                found=0
                for block in document[index].get_text('dict')['blocks']:
                    for line in block.get('lines',[]):
                        text=''.join(span['text'] for span in line['spans'])
                        angle=degrees(atan2(line['dir'][1],line['dir'][0]))
                        if text==target:
                            found+=1;self.assertAlmostEqual(angle,.5,delta=.05)
                        else:
                            self.assertAlmostEqual(angle,0,delta=.05)
                self.assertEqual(found,1)

    def test_margin_increases_dom_and_pdf_line_gaps_by_the_requested_amount(self):
        import json
        fixture=json.loads((self.target/'ficha.json').read_text(encoding='utf-8'))
        pages=fixture['documentos']['a']['paginas']
        def line(document,index,text):
            for block in document[index].get_text('dict')['blocks']:
                for item in block.get('lines',[]):
                    if ''.join(span['text'] for span in item['spans']).replace('\xa0',' ')==text:
                        return item['bbox']
            self.fail(f'Linha ausente: {index+1} {text!r}')
        with fitz.open(self.target/'teste-canva-a.pdf') as document:
            for offset,increment in ((6,16),(8,32),(10,64),(12,112)):
                for variant in (0,1):
                    index=offset+variant
                    with self.subTest(page=index+1):
                        self.assertEqual(pages[index]['distancia_par_px'],16+increment)
                        upper='Vigiai!' if variant==0 else 'Para rezar hoje'
                        lower='Mc 13,37' if variant==0 else 'O que em mim está dormindo'
                        base_gap=line(document,variant,lower)[1]-line(document,variant,upper)[3]
                        actual_gap=line(document,index,lower)[1]-line(document,index,upper)[3]
                        self.assertAlmostEqual((actual_gap-base_gap)/.75,increment,delta=.5)


if __name__=='__main__':
    unittest.main()
