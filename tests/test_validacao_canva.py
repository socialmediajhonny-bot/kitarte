"""O auditor independente rejeita PDFs e fichas adulterados em cópias temporárias."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import ArrayObject, DecodedStreamObject, NameObject

from arteque_reza.base import PROJECT
from arteque_reza.validacao_canva import (
    inspect_layer, inspect_rotation, inspect_tagging, validate_canva,
)


FIXTURE = PROJECT/'saida/teste-canva'
GOSPEL = PROJECT/'saida/evangelho/2026-11-29/evangelho-2026-11-29.pdf'


@unittest.skipUnless((FIXTURE/'teste-canva-a.pdf').is_file()
                     and (FIXTURE/'teste-canva-b.pdf').is_file(),
                     'Gere os PDFs de teste-canva antes de auditar cópias adulteradas')
class CanvaValidatorTests(unittest.TestCase):
    def setUp(self):
        work=PROJECT/'work'; work.mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=work)
        self.addCleanup(self.temp.cleanup)
        self.output=Path(self.temp.name)
        for filename in ('teste-canva-a.pdf','teste-canva-b.pdf','ficha.json'):
            shutil.copyfile(FIXTURE/filename,self.output/filename)

    def writer(self,key):
        return PdfWriter(clone_from=PdfReader(self.output/f'teste-canva-{key}.pdf'))

    def save(self,writer,key):
        writer.write(self.output/f'teste-canva-{key}.pdf')

    def test_tagged_b_without_markinfo_is_rejected_after_clone(self):
        writer=self.writer('b')
        del writer.root_object['/MarkInfo']
        self.save(writer,'b')
        tags=inspect_tagging(self.output/'teste-canva-b.pdf')
        self.assertTrue(tags['struct_tree_root_presente'])
        self.assertFalse(tags['marcado'])
        result=validate_canva(self.output,GOSPEL)
        self.assertFalse(result['ok'])
        self.assertTrue(any('PDF B: marcação incorreta' in error for error in result['errors']))

    def test_layer_form_without_transparency_group_is_rejected(self):
        writer=self.writer('a')
        forms=[ref.get_object() for ref in writer.pages[2]['/Resources']['/XObject'].values()
               if ref.get_object().get('/Subtype')=='/Form']
        self.assertEqual(len(forms),1)
        del forms[0]['/Group']
        self.save(writer,'a')
        layer=inspect_layer(self.output/'teste-canva-a.pdf',3,'Mc 13,37')
        self.assertFalse(layer['ok'])
        self.assertEqual(layer['forms_alvo'],1)
        self.assertFalse(layer['forms'][0]['grupo_transparencia'])

    def test_root_and_markinfo_cannot_hide_an_empty_parent_tree(self):
        writer=self.writer('b')
        tree=writer.root_object['/StructTreeRoot']
        tree['/ParentTree'][NameObject('/Nums')]=ArrayObject()
        self.save(writer,'b')
        tags=inspect_tagging(self.output/'teste-canva-b.pdf')
        self.assertTrue(tags['struct_tree_root_presente'])
        self.assertTrue(tags['marked_true'])
        self.assertFalse(tags['estrutura_preservada'])
        self.assertFalse(tags['marcado'])

    def test_layer_with_two_text_blocks_is_rejected_even_when_text_overlaps(self):
        writer=self.writer('a')
        resources=writer.pages[2]['/Resources']['/XObject']
        name=next(k for k,v in resources.items() if v.get_object().get('/Subtype')=='/Form')
        original=resources[name].get_object()
        duplicate=DecodedStreamObject()
        for key,value in original.items():
            if key not in ('/Filter','/DecodeParms','/Length'):
                duplicate[key]=value
        duplicate.set_data(original.get_data()+original.get_data())
        resources[NameObject(name)]=writer._add_object(duplicate)
        self.save(writer,'a')
        layer=inspect_layer(self.output/'teste-canva-a.pdf',3,'Mc 13,37')
        self.assertFalse(layer['ok'])
        self.assertEqual(layer['forms'][0]['blocos_bt'],2)
        self.assertEqual(layer['forms'][0]['blocos_et'],2)

    def test_rotation_of_other_lines_is_rejected(self):
        writer=self.writer('a')
        writer.pages[4].add_transformation(Transformation().rotate(.5))
        self.save(writer,'a')
        rotation=inspect_rotation(self.output/'teste-canva-a.pdf',5,'Mc 13,37')
        self.assertFalse(rotation['ok'])
        others=[line for line in rotation['linhas'] if line['texto_sem_espacos']!='Mc13,37']
        self.assertTrue(any(abs(line['angulo_graus'])>.05 for line in others))

    def test_incorrect_dom_gap_in_ficha_cannot_override_pdf_measurements(self):
        fixture=json.loads((self.output/'ficha.json').read_text())
        fixture['documentos']['a']['paginas'][6]['distancia_par_px']=31
        result=validate_canva(self.output,GOSPEL,fixture)
        self.assertFalse(result['ok'])
        self.assertTrue(any('A7: respiro DOM não é 32px' in error for error in result['errors']))
        gap=result['checks']['respiros'][0]
        self.assertAlmostEqual(gap['incremento_pdf_px'],16,delta=.5)
        self.assertFalse(gap['dom_ok'])


if __name__=='__main__':
    unittest.main()
