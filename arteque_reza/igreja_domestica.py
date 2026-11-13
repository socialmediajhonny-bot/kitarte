"""PostIgrejaDomestica: quatro composições locais, sem alterar o kit."""
from __future__ import annotations

from html import escape
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any

from PIL import Image, ImageColor

from .base import PROJECT, assinatura, color, html_document, montar_arte, nicho, selo
from .conteudo import color_token, date_label, text_html
from .evangelho import _measure as measure_evangelho, _ornament, _text
from .pdf_nicho import niches_from_elements, validate_niche_pdf
from .validacao import validate_niche_pixels


BOOKS = ('Gn','Ex','Lv','Nm','Dt','Js','Jz','Rt','1Sm','2Sm','1Rs','2Rs','1Cr','2Cr',
         'Esd','Ne','Tb','Jt','Est','1Mc','2Mc','Jó','Sl','Pr','Ecl','Ct','Sb','Eclo',
         'Is','Jr','Lm','Br','Ez','Dn','Os','Jl','Am','Ab','Jn','Mq','Na','Hab','Sf',
         'Ag','Zc','Ml','Mt','Mc','Lc','Jo','At','Rm','1Cor','2Cor','Gl','Ef','Fl','Cl',
         '1Ts','2Ts','1Tm','2Tm','Tt','Fm','Hb','Tg','1Pd','2Pd','1Jo','2Jo','3Jo','Jd','Ap')
BOOK_PATTERN = '|'.join(sorted(BOOKS, key=len, reverse=True))
_PROTECTED = re.compile(
    r'(?P<referencia>(?<!\w)(?:'+BOOK_PATTERN+r')\s+\d+(?:,\d+[a-z]?(?:[-.]\d+[a-z]?)*))'
    r'|(?P<ordinal>\d+[ºª]\s+\w+(?:-\w+)*)|(?P<hifen>\w+(?:-\w+)+)')
_BOOK_END = re.compile(r'(?:^|\s)(?:'+BOOK_PATTERN+r')[\W_]*$')


def igreja_text_html(value: str) -> str:
    """Mantenha referências, ordinais e palavras hifenizadas nesta série."""
    markup = text_html(value)
    def protect(match):
        kind = match.lastgroup
        text = match.group(0)
        if kind == 'referencia':
            text = re.sub(r'\s+', '\u00a0', text, count=1)
        elif kind == 'ordinal':
            text = re.sub(r'(?<=[ºª])\s+', '\u00a0', text, count=1)
        return (f'<span class="igreja-sem-quebra" data-regra="{kind}" '
                f'style="white-space:nowrap">{text}</span>')
    return _PROTECTED.sub(protect, markup)


def expand_cards(days: list[dict]) -> list[dict]:
    return [{**card, 'data': day['data'], 'cor': day['cor'],
             'numero': number, 'total': len(day['cards'])}
            for day in days for number, card in enumerate(day['cards'], 1)]


def expected_layout(card: dict) -> dict:
    kind = card['tipo']
    if kind == 'capa':
        return {'linhas': {'credito': 1, 'titulo': 1, 'apoio': 1},
                'selo_nicho_px': 32, 'apoio_assinatura_px': 116}
    if kind == 'passos':
        if card['data'] == '2026-12-13' and card['numero'] == 2:
            return {'linhas': {'titulo': 1, **{f'item_{i}': 2 for i in range(1,4)}, 'fonte': 1},
                    'folga_px': 194.5}
        return {'linhas': {'titulo': 1, **{f'item_{i}': 2 for i in range(1,5)}, 'fonte': 1},
                'folga_px': 128.5}
    if kind == 'oracao':
        return {'linhas': {'titulo': 1, 'fala_1': 2, 'fala_2': 4, 'fala_3': 1, 'fala_4': 1},
                'folga_px': 103.5}
    return {'linhas': {'pergunta': 2, 'convite': 1}, 'folga_px': 353.5}


def _field(tag: str, field: str, style: str, value: str, css: str = '',
           token: str = 'tinta', *, raw: bool = False) -> str:
    return _text(tag, field, style, value if raw else igreja_text_html(value), css, token, raw=True)


def _header(card: dict) -> str:
    support = f'{card["numero"]}/{card["total"]}' if card['numero'] > 1 else None
    markup = selo('Igreja Doméstica', date_label(card['data']), support)
    for original, field in [('selo-serie','selo'), ('selo-data','data'), ('selo-info','contagem')]:
        markup = markup.replace(f'data-element="{original}"',
            f'data-element="{original}" data-text="{field}" data-style="selo"')
    return markup


def _baseline(kind: str) -> str:
    return (f'<span data-baseline="{kind}" aria-hidden="true" '
            'style="display:inline-block;width:0;height:0;vertical-align:baseline"></span>')


def _document(card: dict, css: Path, artwork: Path | None = None) -> str:
    kind = card['tipo']; on_color = kind == 'conversa'
    ink = 'sobre-cor' if on_color else 'tinta'
    quiet = 'sobre-cor' if on_color else 'tinta-suave'
    body = ''
    if kind == 'capa':
        if artwork is None: raise ValueError('A capa precisa da obra local ou provisória.')
        image = nicho(600,680,artwork,foco=card['obra']['foco'],zoom=card['obra'].get('zoom',1))
        image = image.replace('style="width:600px;height:680px;"',
            'style="width:600px;height:680px;margin-top:var(--espaco-3)"')
        image = image.replace('alt="Obra provisória"','alt="Obra da Igreja Doméstica"')
        image = image.replace('data-arquivo="obra-provisoria.png"',
            f'data-arquivo="{escape(artwork.relative_to(PROJECT).as_posix(),quote=True)}"')
        body += image
        body += _field('p','credito','credito aqr-credito',card['obra']['credito'],
            'margin-top:var(--espaco-3);max-width:920px',quiet)
        body += _field('h1','titulo','titulo aqr-titulo',card['titulo'],
            'margin-top:var(--espaco-4);max-width:880px')
        body += _field('p','apoio','corpo',card['apoio'],
            'margin-top:var(--espaco-3);max-width:760px;color:var(--tinta-suave)',quiet)
    else:
        body = '<div class="aqr-texto" style="margin-top:auto">'
        body += _field('p','rotulo','selo',card['rotulo'],
            f'margin-bottom:var(--espaco-3);color:var(--{quiet})',quiet)
        if kind == 'conversa':
            body += _field('p','pergunta','citacao aqr-citacao',card['pergunta'],
                'max-width:860px;color:var(--sobre-cor)',ink)
            body += _ornament(True)
            body += _field('p','convite','corpo',card['convite'], 'color:var(--sobre-cor)',ink)
        else:
            body += _field('h1','titulo','titulo aqr-titulo',card['titulo'],'max-width:880px')
            body += _ornament()
            if kind == 'passos':
                body += ('<ol data-element="lista" style="display:flex;flex-direction:column;'
                    'gap:var(--espaco-2);width:820px;margin:0;padding:0;list-style:none;text-align:left">')
                for number,item in enumerate(card['itens'],1):
                    top = 'margin-top:var(--espaco-2);' if number > 1 else ''
                    body += (f'<li data-item="{number}" style="{top}display:grid;grid-template-columns:24px minmax(0,1fr);'
                        'column-gap:20px;align-items:baseline">')
                    body += _field('span',f'numero_{number}','corpo',_baseline('numero')+str(number),
                        'font-weight:700;color:var(--ouro);align-self:first baseline', 'ouro',raw=True)
                    body += _field('p',f'item_{number}','corpo',_baseline('texto')+igreja_text_html(item),
                        'text-align:left;text-wrap:pretty;color:var(--tinta);align-self:first baseline',raw=True)
                    body += '</li>'
                body += '</ol>'
                body += _field('p','fonte','credito aqr-credito',card['fonte'],
                    'margin-top:var(--espaco-2)',quiet)
            elif kind == 'oracao':
                for number,speech in enumerate(card['falas'],1):
                    speech_kind,value = next(iter(speech.items()))
                    style,width,token = {'rubrica':('corpo',760,quiet),
                        'oracao':('oracao aqr-corpo',880,ink),
                        'aclamacao':('citacao aqr-citacao',860,ink)}[speech_kind]
                    top = 'margin-top:var(--espaco-3);' if number > 1 else ''
                    body += _field('p',f'fala_{number}',style,value,
                        f'{top}max-width:{width}px;color:var(--{token})',token)
                if 'origem' in card:
                    body += _field('p','origem','credito aqr-credito',card['origem'],
                        'margin-top:var(--espaco-2)',quiet)
        body += '</div>'
    post = montar_arte(_header(card)+body+assinatura('pergaminho',sobre_cor=on_color),
        tema='pergaminho',cor_do_dia=color_token(card['cor']),cartao_cor=on_color)
    return html_document(post,css,'@page{margin:0;}',
        f'Igreja Doméstica · {card["data"]} · {card["numero"]}/{card["total"]}')


_EXTRA_JS = r"""() => {
 const root=document.querySelector('.aqr-post'), ar=root.getBoundingClientRect();
 const rr=r=>({x:+(r.left-ar.left).toFixed(6),y:+(r.top-ar.top).toFixed(6),largura:+r.width.toFixed(6),altura:+r.height.toFixed(6)});
 const box=sel=>{const n=root.querySelector(sel);return n?rr(n.getBoundingClientRect()):null;};
 const hex=v=>'#'+v.match(/[\d.]+/g).slice(0,3).map(v=>(+v).toString(16).padStart(2,'0')).join('');
 const list=[...root.querySelectorAll('[data-item]')].map(n=>({
   numero_campo:n.querySelector('[data-text^="numero_"]').dataset.text,
   item_campo:n.querySelector('[data-text^="item_"]').dataset.text,
   caixa:rr(n.getBoundingClientRect()),
   baseline_numero_px:n.querySelector('[data-baseline="numero"]').getBoundingClientRect().top-ar.top,
   baseline_texto_px:n.querySelector('[data-baseline="texto"]').getBoundingClientRect().top-ar.top}));
 return {caixas:{ornamento:box('.aqr-ornamento'),lista:box('[data-element="lista"]'),assinatura:box('.aqr-assinatura')},
   lista:list,cores:{fundo:hex(getComputedStyle(root).backgroundColor),
     cruz:hex(getComputedStyle(root.querySelector('.aqr-selo__cruz')).color),
     ornamento:root.querySelector('.aqr-ornamento')?hex(getComputedStyle(root.querySelector('.aqr-ornamento')).color):null},
   logo:root.querySelector('[data-element="logo"]').getAttribute('data-arquivo'),
   estilos_texto:Object.fromEntries([...root.querySelectorAll('[data-text]')].map(n=>[n.dataset.text,getComputedStyle(n).fontStyle])),
   sem_quebra:[...root.querySelectorAll('.igreja-sem-quebra')].map(n=>({texto:n.textContent,
     regra:n.dataset.regra,white_space:getComputedStyle(n).whiteSpace,
     linhas:[...n.getClientRects()].map(r=>+(r.top-ar.top).toFixed(6))}))};
}"""


def _measure(page: Any, card: dict) -> dict:
    measured = measure_evangelho(page,card['numero'],1)
    measured.update({'tipo':card['tipo'],'modelo':'PostIgrejaDomestica','tema':'pergaminho',
        'data':card['data'],'cor':card['cor'],'numero':card['numero'],'total':card['total'],'conteudo':card})
    extra = page.evaluate(_EXTRA_JS)
    measured['caixas'].update(extra.pop('caixas')); measured.update(extra)
    measured['falas'] = [{'campo':f'fala_{n}','tipo':next(iter(speech))}
        for n,speech in enumerate(card.get('falas',[]),1)]
    for text in measured['textos']:
        field = text['campo']
        text['alinhamento_canva'] = ('start' if field in {'selo','data'} or field.startswith(('item_','numero_'))
            else 'end' if field == 'contagem' else 'center')
    boxes = measured['caixas']; block = boxes['bloco_texto']
    if block:
        seal,signature = boxes['selo'],boxes['assinatura']
        upper=block['y']-seal['y']-seal['altura'];lower=signature['y']-block['y']-block['altura']
        measured['distancias']={'selo_texto_px':upper,'texto_assinatura_px':lower,
            'diferenca_centralizacao_px':abs(upper-lower)}
    else: measured['distancias']={}
    return measured


def _validate_layout(card: dict, measured: dict) -> dict:
    errors=[]; label=f'{card["data"]}, card {card["numero"]}'
    values={text['campo']:text for text in measured['textos']};kind=card['tipo']
    limits={'titulo':2,'credito':1,'apoio':1,'fonte':1,'origem':1,'pergunta':4,'convite':1}
    for n in range(1,len(card.get('itens',[]))+1): limits[f'item_{n}']=3
    for speech in measured['falas']:
        limits[speech['campo']]={'rubrica':2,'oracao':6,'aclamacao':1}[speech['tipo']]
    for field,text in values.items():
        if field in limits and text['quantidade_linhas']>limits[field]:
            errors.append(f'{label}, {field}: {text["quantidade_linhas"]} linhas; limite {limits[field]}.')
        box=text['caixa']
        if box['x']<-.1 or box['y']<-.1 or box['x']+box['largura']>1080.1 or box['y']+box['altura']>1350.1:
            errors.append(f'{label}, {field}: texto fora da arte.')
        for line,linebox in zip(text['linhas'],text['caixas_das_linhas']):
            if re.search(r'(?:^|\s)[aàeéoóAÀEÉOÓ][\W_]*$',line):
                errors.append(f'{label}, {field}: palavra de uma letra no fim de {line!r}.')
            if line.rstrip().endswith(('-', '\u2010', '\u2011', '\u00ad')):
                errors.append(f'{label}, {field}: linha termina em hífen: {line!r}.')
            if re.search(r'\d+[ºª][\W_]*$',line):
                errors.append(f'{label}, {field}: linha termina em ordinal: {line!r}.')
            if _BOOK_END.search(line):
                errors.append(f'{label}, {field}: linha termina em abreviação bíblica: {line!r}.')
            if linebox['largura'] and (linebox['x']<box['x']-.1 or linebox['x']+linebox['largura']>box['x']+box['largura']+.1):
                errors.append(f'{label}, {field}: linha transborda a largura do campo.')
    boxes={field:text['caixa'] for field,text in values.items()}
    boxes.update({key:value for key,value in measured['caixas'].items() if value is not None})
    for number,item in enumerate(measured['lista'],1): boxes[f'linha_item_{number}']=item['caixa']
    if kind=='capa':
        pairs=[('selo','nicho',32),('nicho','credito',32),('credito','titulo',48),('titulo','apoio',32)]
    elif kind=='passos':
        pairs=[('rotulo','titulo',48),('titulo','ornamento',48),('ornamento','linha_item_1',48)]
        pairs += [(f'linha_item_{n}',f'linha_item_{n+1}',32) for n in range(1,len(card['itens']))]
        pairs += [(f'linha_item_{len(card["itens"])}','fonte',32)]
    elif kind=='oracao':
        pairs=[('rotulo','titulo',48),('titulo','ornamento',48),('ornamento','fala_1',48)]
        pairs += [(f'fala_{n}',f'fala_{n+1}',48) for n in range(1,len(card['falas']))]
        if 'origem' in card: pairs += [(f'fala_{len(card["falas"])}','origem',32)]
    else:
        pairs=[('rotulo','pergunta',48),('pergunta','ornamento',48),('ornamento','convite',48)]
    distances=dict(measured['distancias'])
    for first,second,wanted in pairs:
        a,b=boxes[first],boxes[second];gap=b['y']-a['y']-a['altura']
        distances[f'{first}_{second}_px']=round(gap,6)
        if abs(gap-wanted)>.01:
            errors.append(f'{label}, {first} → {second}: distância {gap:.2f}px; esperado {wanted}px (±0,01).')
    if kind=='capa':
        a,b=boxes['apoio'],boxes['assinatura'];gap=b['y']-a['y']-a['altura']
        distances['apoio_assinatura_px']=gap
        if gap<31.99: errors.append(f'{label}: apoio a menos de 32px da assinatura.')
    else:
        if distances['diferenca_centralizacao_px']>.1:errors.append(f'{label}: bloco de texto não centralizado.')
        if min(distances['selo_texto_px'],distances['texto_assinatura_px'])<59.99:
            errors.append(f'{label}: bloco de texto a menos de 60px do selo ou da assinatura.')
    for item in measured['lista']:
        if abs(item['baseline_numero_px']-item['baseline_texto_px'])>.01:
            errors.append(f'{label}, {item["numero_campo"]}: número fora da linha de base do item.')
        number=values[item['numero_campo']]
        if number['fonte']!='Lato' or number['peso']!='700' or number['cor']!=color('ouro'):
            errors.append(f'{label}, {item["numero_campo"]}: número precisa de Lato Bold em ouro.')
    on_color=kind=='conversa';ink=color('sobre-cor' if on_color else 'tinta')
    quiet=color('sobre-cor' if on_color else 'tinta-suave');gold=color('sobre-cor' if on_color else 'ouro')
    wanted_cross=color('sobre-cor') if on_color else color(color_token(card['cor']))
    wanted_bg=color(color_token(card['cor'])) if on_color else color('fundo')
    if measured['cores']['cruz']!=wanted_cross:errors.append(f'{label}: cruz na cor errada.')
    if measured['cores']['fundo']!=wanted_bg:errors.append(f'{label}: fundo não ocupa o cartão inteiro na cor esperada.')
    if measured['cores']['ornamento'] is not None and measured['cores']['ornamento']!=gold:
        errors.append(f'{label}: ornamento na cor errada.')
    quiet_fields={'data','contagem','rotulo','credito','apoio','fonte','origem'}
    quiet_fields.update(speech['campo'] for speech in measured['falas'] if speech['tipo']=='rubrica')
    for field,text in values.items():
        wanted=gold if field.startswith('numero_') else quiet if field in quiet_fields else ink
        if text['cor']!=wanted:errors.append(f'{label}, {field}: texto na cor errada.')
    for speech in measured['falas']:
        text=values[speech['campo']]
        if speech['tipo']=='aclamacao' and (text['estilo']!='citacao' or text['fonte']!='Cormorant Garamond'
                or text['peso']!='500' or measured['estilos_texto'][speech['campo']]!='italic'):
            errors.append(f'{label}, {speech["campo"]}: aclamação precisa de Cormorant Garamond Medium Italic.')
    logo='logo-horizontal-sobre-cor.svg' if on_color else 'logo-horizontal-pergaminho.svg'
    if not measured['logo'].endswith(logo):errors.append(f'{label}: assinatura na variante errada.')
    for word in measured['sem_quebra']:
        if word['white_space']!='nowrap' or len(set(word['linhas']))>1:
            errors.append(f'{label}: texto protegido partido: {word["texto"]!r}.')
    result={'ok':not errors,'distancias':distances,'limites':limits,'lista':measured['lista'],
        'esperado':expected_layout(card),'errors':errors}
    if errors:raise ValueError('; '.join(errors))
    return result


def _pixels(path: Path, card: dict, measured: dict) -> dict:
    errors=[];samples=[];on_color=card['tipo']=='conversa'
    cross=measured['caixas']['cruz']
    with Image.open(path) as raw:
        image=raw.convert('RGB')
        for name,x,y,wanted in [('fundo',8,8,color(color_token(card['cor'])) if on_color else color('fundo')),
            ('cruz',cross['x']+9,cross['y']+18,color('sobre-cor') if on_color else color(color_token(card['cor'])))]:
            point=(int(x),int(y));actual=image.getpixel(point);ok=actual==ImageColor.getrgb(wanted)
            samples.append({'elemento':name,'pixel':list(point),'rgb':list(actual),'esperado':wanted,'ok':ok})
            if not ok:errors.append(f'{card["data"]}, card {card["numero"]}, {name}: cor incorreta.')
    niche=None
    if measured['caixas']['nicho']:
        box=measured['caixas']['nicho']
        niche=validate_niche_pixels(path,[{'name':'nicho','x':box['x'],'y':box['y'],
            'width':box['largura'],'height':box['altura'],'filete':color(color_token(card['cor'])),
            'background':color('fundo')}])
        errors.extend(niche['errors'])
    result={'ok':not errors,'amostras':samples,'nicho':niche,'errors':errors}
    if errors:raise ValueError('; '.join(errors))
    return result


def _pdf_check(path: Path, cards: list[dict], measured: list[dict]) -> dict:
    import fitz
    errors=[];fonts={};pages=[];expected_pages=[];required=set()
    compact=lambda value:re.sub(r'\s+','',value)
    for card in measured:
        for text in card['textos']:
            if text['fonte']=='Lato': required.add('Lato-Bold' if text['peso']=='700' else 'Lato-Regular')
            else: required.add('CormorantGaramond-SemiBold' if text['peso']=='600' else
                'CormorantGaramond-MediumItalic' if text['estilo']=='citacao' else 'CormorantGaramond-Medium')
    with fitz.open(path) as document:
        if len(document)!=len(cards):errors.append(f'{path.name}: número de páginas incorreto.')
        for index,page in enumerate(document):
            expected=compact(''.join(text['conteudo'] for text in measured[index]['textos'])) if index<len(measured) else ''
            expected_pages.append(expected);equal=compact(page.get_text(sort=True))==expected
            dimension_ok=abs(page.rect.width-810)<.01 and abs(page.rect.height-1012.5)<.01
            pages.append({'pagina':index+1,'largura_pt':page.rect.width,'altura_pt':page.rect.height,
                'texto_igual_yaml_sem_espacos':equal,'dimensoes_ok':dimension_ok})
            if not equal:errors.append(f'{path.name}, página {index+1}: texto integral diferente do YAML.')
            if not dimension_ok:errors.append(f'{path.name}, página {index+1}: tamanho PDF incorreto.')
            for info in page.get_fonts(full=True):
                xref=info[0]
                if xref in fonts:continue
                _,extension,_,data=document.extract_font(xref);name=re.sub(r'^[A-Z]{6}\+','',info[3])
                embedded=bool(data) and extension.lower() in {'ttf','ttc'} and data[:4] in {b'\x00\x01\x00\x00',b'true',b'ttcf'}
                fonts[xref]={'nome':name,'formato':extension,'embutida':embedded,'bytes':len(data)}
                if not embedded:errors.append(f'{path.name}: fonte TTF não embutida: {name}.')
    missing=required-{font['nome'] for font in fonts.values()}
    if missing:errors.append('Fontes ausentes: '+', '.join(sorted(missing)))
    font_text=text_output=None
    if shutil.which('pdffonts'):
        process=subprocess.run(['pdffonts',str(path)],capture_output=True,text=True,check=False);font_text=process.stdout
        if process.returncode:errors.append('pdffonts falhou: '+process.stderr)
        for line in font_text.splitlines()[2:]:
            match=re.search(r'\s(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$',line)
            if match and match.group(1)!='yes':errors.append('pdffonts encontrou fonte não embutida: '+line)
    else:errors.append('pdffonts indisponível.')
    if shutil.which('pdftotext'):
        process=subprocess.run(['pdftotext','-layout',str(path),'-'],capture_output=True,text=True,check=False);text_output=process.stdout
        if process.returncode:errors.append('pdftotext falhou: '+process.stderr)
        if [compact(part) for part in text_output.split('\f') if part.strip()]!=expected_pages:
            errors.append(f'{path.name}: texto integral de pdftotext difere do YAML.')
    else:errors.append('pdftotext indisponível.')
    niches=[niche for number, card in enumerate(measured,1)
            for niche in niches_from_elements(card['elementos'],page=number)]
    vector_niche=validate_niche_pdf(path,niches)
    errors.extend(vector_niche['errors'])
    result={'ok':not errors,'paginas':pages,'fontes':list(fonts.values()),'fontes_exigidas':sorted(required),
        'pdffonts':font_text,'pdftotext':text_output,'texto_igual_yaml_sem_espacos':not errors,
        'nicho_vetorial':vector_niche,'errors':errors}
    if errors:raise ValueError('; '.join(errors))
    return result
