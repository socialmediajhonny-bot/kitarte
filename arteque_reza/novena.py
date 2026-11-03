"""PostNovena: composição e validação local, sem alterar as séries existentes."""
from __future__ import annotations

from html import escape
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any

from PIL import Image, ImageColor

from .base import assinatura, color, html_document, montar_arte, selo
from .conteudo import color_token, date_label, text_html
from .evangelho import _measure as measure_evangelho, _ornament, _text


REQUIRED_FONTS = {'Lato-Bold', 'Lato-Regular', 'CormorantGaramond-SemiBold',
                  'CormorantGaramond-Medium', 'CormorantGaramond-MediumItalic'}


def expand_cards(novenas: list[dict]) -> list[dict]:
    """Expanda a posição dos nove dias, preservando o texto aprovado do YAML."""
    cards = []
    for novena in novenas:
        for number, day in enumerate(novena['dias'], 1):
            cards.append({'novena': novena['id'], 'nome': novena['nome'],
                'cor': novena['cor'], **day, 'refrao': novena['refrao'],
                'numero': number, 'encerramento': False, 'slug': f'dia-{number}'})
        day = novena['encerramento']
        cards.append({'novena': novena['id'], 'nome': novena['nome'], **day,
            'refrao': day.get('final', novena['refrao']), 'numero': 9,
            'encerramento': True, 'slug': 'encerramento'})
    return cards


def expected_layout(card: dict) -> dict:
    if card['novena'] == 'imaculada':
        if card['encerramento']:
            return {'titulo_linhas': 1, 'oracao_linhas': 7, 'folga_px': 158}
        return {'titulo_linhas': 2 if card['numero'] == 8 else 1,
                'oracao_linhas': 6, 'folga_px': 116 if card['numero'] == 8 else 154}
    if card['novena'] == 'natal':
        if not card['encerramento'] and card['numero'] == 2:
            return {'titulo_linhas': 2, 'oracao_linhas': 5, 'folga_px': 146}
        if not card['encerramento'] and card['numero'] == 4:
            return {'titulo_linhas': 1, 'oracao_linhas': 6, 'folga_px': 154}
        return {'titulo_linhas': 1, 'oracao_linhas': 5, 'folga_px': 184}
    return {}


def novena_text_html(value: str) -> str:
    """Aplique a regra comum e preserve cada palavra hifenizada por inteiro."""
    markup = text_html(value)
    return re.sub(r'\w+(?:-\w+)+',
        lambda match: '<span class="novena-sem-quebra" style="white-space:nowrap">'+match.group(0)+'</span>',
        markup)


def _field(tag: str, field: str, style: str, value: str, css: str = '',
           token: str = 'tinta', *, raw: bool = False) -> str:
    return _text(tag, field, style, value if raw else novena_text_html(value), css, token, raw=True)


def _header(card: dict) -> str:
    markup = selo(card['nome'], date_label(card['data']))
    for original, field in [('selo-serie', 'selo'), ('selo-data', 'data')]:
        markup = markup.replace(f'data-element="{original}"',
            f'data-element="{original}" data-text="{field}" data-style="selo"')
    return markup


def _beads(card: dict) -> str:
    token = 'sobre-cor' if card['encerramento'] else 'ouro'
    count = 9 if card['encerramento'] else card['numero']
    label = f'Dia {count} de 9'
    circles = []
    for index in range(9):
        if index < count:
            style = f'r="9" fill="var(--{token})"'
        else:
            style = f'r="7.75" fill="none" stroke="var(--{token})" stroke-width="2.5"'
        circles.append(f'<circle cx="{9+36*index}" cy="9" {style}/>')
    return ('<svg data-element="contas" class="novena-contas" width="306" height="18" '
        f'viewBox="0 0 306 18" aria-label="{escape(label, quote=True)}" role="img" '
        'style="display:block;flex:none;margin-top:var(--espaco-3)">'+''.join(circles)+'</svg>')


def _document(card: dict, css: Path) -> str:
    closing = card['encerramento']
    ink = 'sobre-cor' if closing else 'tinta'
    quiet = 'sobre-cor' if closing else 'tinta-suave'
    gold = 'sobre-cor' if closing else 'ouro'
    label = 'Encerramento' if closing else f'Dia {card["numero"]} de 9'
    body = '<div class="aqr-texto" style="margin-top:auto">'
    body += _field('p', 'contagem', 'selo', label,
        f'margin-bottom:var(--espaco-3);color:var(--{quiet})', quiet)
    body += _field('h1', 'titulo', 'titulo aqr-titulo', card['titulo'],
        f'max-width:820px;color:var(--{ink})', ink)
    if 'fonte' in card:
        body += _field('p', 'fonte', 'referencia aqr-referencia', card['fonte'],
            f'margin-top:var(--espaco-2);color:var(--{gold})', gold)
    body += _ornament(closing)
    refrain = (f'<em data-refrao style="font-family:var(--font-serifa);font-weight:500;'
        f'font-style:italic;color:var(--{quiet})">'+novena_text_html(card['refrao'])+'</em>')
    prayer = novena_text_html(card['oracao'])+'<br>'+refrain
    body += _field('p', 'oracao', 'oracao aqr-corpo', prayer,
        f'max-width:880px;color:var(--{ink})', ink, raw=True)
    body += _beads(card)+'</div>'
    post = montar_arte(_header(card)+body+assinatura('pergaminho', sobre_cor=closing),
        tema='pergaminho', cor_do_dia=color_token(card['cor']), cartao_cor=closing)
    return html_document(post, css, '@page{margin:0;}',
        f'{card["nome"]} · {card["data"]} · {label}')


_EXTRA_JS = r"""() => {
 const article=document.querySelector('.aqr-post'),root=article.getBoundingClientRect();
 const rr=r=>({x:+(r.left-root.left).toFixed(6),y:+(r.top-root.top).toFixed(6),largura:+r.width.toFixed(6),altura:+r.height.toFixed(6)});
 const hex=value=>{if(value==='none')return 'none';const v=value.match(/[\d.]+/g);return '#'+v.slice(0,3).map(v=>(+v).toString(16).padStart(2,'0')).join('');};
 const box=selector=>{const n=article.querySelector(selector);return n?rr(n.getBoundingClientRect()):null;};
 const prayer=article.querySelector('[data-text="oracao"]'),ref=prayer.querySelector('[data-refrao]');
 function lines(node,excludeRef=false){
   const fragments=[],walker=document.createTreeWalker(node,NodeFilter.SHOW_TEXT);let tn;
   while(tn=walker.nextNode()){
     if(excludeRef&&ref.contains(tn))continue;
     for(let i=0;i<tn.textContent.length;i++){
       const r=document.createRange();r.setStart(tn,i);r.setEnd(tn,i+1);
       const b=[...r.getClientRects()].find(b=>b.height>0&&b.width>0);
       if(b)fragments.push({char:tn.textContent[i],box:b});
     }
   }
   const groups=[];
   for(const f of fragments){const mid=f.box.top+f.box.height/2;
     let g=groups.find(g=>Math.abs(g.mid-mid)<4);
     if(!g){g={mid,texto:'',left:f.box.left,right:f.box.right,top:f.box.top,bottom:f.box.bottom};groups.push(g);}
     g.texto+=f.char;g.left=Math.min(g.left,f.box.left);g.right=Math.max(g.right,f.box.right);g.top=Math.min(g.top,f.box.top);g.bottom=Math.max(g.bottom,f.box.bottom);
   }
   return groups.sort((a,b)=>a.mid-b.mid).map(g=>({texto:g.texto.trim(),caixa:rr({left:g.left,top:g.top,width:g.right-g.left,height:g.bottom-g.top})}));
 }
 const refLines=lines(ref),bodyLines=lines(prayer,true),s=getComputedStyle(ref),ps=getComputedStyle(prayer);
 const startsOwn=refLines.length>0&&bodyLines.length>0&&refLines[0].caixa.y-bodyLines.at(-1).caixa.y>parseFloat(ps.lineHeight)*.9;
 const svg=article.querySelector('[data-element="contas"]');
 const circles=[...svg.querySelectorAll('circle')].map(n=>{const cs=getComputedStyle(n);return {cx:+n.getAttribute('cx'),cy:+n.getAttribute('cy'),raio:+n.getAttribute('r'),preenchimento:hex(cs.fill),contorno:hex(cs.stroke),espessura_contorno:parseFloat(cs.strokeWidth)};});
 const cross=article.querySelector('.aqr-selo__cruz');
 return {caixas:{ornamento:box('.aqr-ornamento'),contas:box('[data-element="contas"]'),assinatura:box('.aqr-assinatura')},
   refrao:{linhas:refLines.map(l=>l.texto),caixas_das_linhas:refLines.map(l=>l.caixa),estilo:s.fontStyle,fonte:s.fontFamily,peso:s.fontWeight,cor:hex(s.color),tamanho_px:parseFloat(s.fontSize),entrelinha_px:parseFloat(s.lineHeight),em_linha_propria:startsOwn,linhas_oracao:bodyLines},
   contas:{largura:svg.getBoundingClientRect().width,altura:svg.getBoundingClientRect().height,aria_label:svg.getAttribute('aria-label'),circulos:circles},
   cores:{fundo:hex(getComputedStyle(article).backgroundColor),cruz:hex(getComputedStyle(cross).color),ornamento:hex(getComputedStyle(article.querySelector('.aqr-ornamento')).color)},
   estrutura:{paragrafos_oracao:article.querySelectorAll('p[data-text="oracao"]').length,refrao_no_paragrafo:ref.closest('p')===prayer,em_quantidade:prayer.querySelectorAll('em').length,logo:article.querySelector('[data-element="logo"]').getAttribute('data-arquivo')||article.querySelector('[data-element="logo"]').getAttribute('src')},
   sem_quebra:[...article.querySelectorAll('.novena-sem-quebra')].map(n=>({texto:n.textContent,white_space:getComputedStyle(n).whiteSpace}))};
}"""


def _measure(page: Any, card: dict) -> dict:
    measured = measure_evangelho(page, card['numero'], 1)
    measured.update({'tipo': 'Novena', 'modelo': 'PostNovena', 'tema': 'pergaminho',
        'novena': card['novena'], 'data': card['data'], 'numero': card['numero'],
        'encerramento': card['encerramento'], 'slug': card['slug'], 'conteudo': card})
    extra = page.evaluate(_EXTRA_JS)
    measured['caixas'].update(extra.pop('caixas'))
    measured.update(extra)
    for text in measured['textos']:
        text['alinhamento_canva'] = 'start' if text['campo'] in {'selo','data'} else 'center'
        if text['campo'] == 'oracao':
            refboxes = measured['refrao']['caixas_das_linhas']
            flags = [any(abs(box['y']-r['y'])<4 for r in refboxes) for box in text['caixas_das_linhas']]
            text['linhas_de_refrao'] = flags
            text['linhas_marcadas'] = [{'texto':line,'caixa':box,'eh_refrao':flag}
                for line,box,flag in zip(text['linhas'],text['caixas_das_linhas'],flags)]
    block,seal,signature = (measured['caixas'][key] for key in ('bloco_texto','selo','assinatura'))
    above = block['y']-seal['y']-seal['altura']
    below = signature['y']-block['y']-block['altura']
    measured['distancias'] = {'selo_texto_px':above,'texto_assinatura_px':below,
        'diferenca_centralizacao_px':abs(above-below)}
    return measured


def _validate_layout(card: dict, measured: dict) -> dict:
    errors = []; label = f'{card["novena"]}, {card["slug"]}'
    values = {text['campo']:text for text in measured['textos']}
    for text in measured['textos']:
        field = text['campo']; limit = {'titulo':2,'oracao':8}.get(field)
        if limit and text['quantidade_linhas'] > limit:
            errors.append(f'{label}, {field}: {text["quantidade_linhas"]} linhas; limite {limit}.')
        box = text['caixa']
        if box['x'] < -.1 or box['y'] < -.1 or box['x']+box['largura'] > 1080.1 or box['y']+box['altura'] > 1350.1:
            errors.append(f'{label}, {field}: texto fora da arte.')
        for line,linebox in zip(text['linhas'],text['caixas_das_linhas']):
            if line.rstrip().endswith(('-', '\u2010', '\u2011', '\u00ad')):
                errors.append(f'{label}, {field}: linha termina em hífen: {line!r}.')
            if re.search(r'(?:^|\s)[aàeéoóAÀEÉOÓ][\W_]*$',line):
                errors.append(f'{label}, {field}: palavra de uma letra no fim de {line!r}.')
            if linebox['largura'] and (linebox['x'] < box['x']-.1 or linebox['x']+linebox['largura'] > box['x']+box['largura']+.1):
                errors.append(f'{label}, {field}: linha transborda a largura do campo.')
    boxes = {name:item['caixa'] for name,item in values.items()}
    boxes.update({'ornamento':measured['caixas']['ornamento'],'contas':measured['caixas']['contas']})
    pairs = [('contagem','titulo',48)]
    if 'fonte' in card:
        pairs += [('titulo','fonte',32),('fonte','ornamento',48)]
    else:
        pairs += [('titulo','ornamento',48)]
    pairs += [('ornamento','oracao',48),('oracao','contas',48)]
    distances = dict(measured['distancias'])
    for first,second,wanted in pairs:
        a,b = boxes[first],boxes[second]
        gap = b['y']-a['y']-a['altura']
        distances[f'{first}_{second}_px'] = round(gap,6)
        if abs(gap-wanted) > .01:
            errors.append(f'{label}, {first} → {second}: distância {gap:.2f}px; esperado {wanted}px (±0,01).')
    if distances['diferenca_centralizacao_px'] > .01:
        errors.append(f'{label}: bloco não centralizado entre selo e assinatura.')
    if min(distances['selo_texto_px'],distances['texto_assinatura_px']) < 59.99:
        errors.append(f'{label}: bloco a menos de 60px do selo ou da assinatura.')
    refrain = measured['refrao']; expected_ref = card['refrao'].splitlines()
    compact = lambda text:re.sub(r'\s+','',text)
    if not refrain['em_linha_propria']:
        errors.append(f'{label}: refrão precisa começar em linha própria.')
    if refrain['estilo'] != 'italic' or 'Cormorant Garamond' not in refrain['fonte'] or refrain['peso'] != '500':
        errors.append(f'{label}: refrão precisa ser Cormorant Garamond Medium Italic.')
    if [compact(line) for line in refrain['linhas']] != [compact(line) for line in expected_ref]:
        errors.append(f'{label}: refrão não mantém as linhas do YAML.')
    if card['novena'] == 'imaculada' and (len(refrain['linhas']) != 2 or not refrain['linhas'][0].endswith('pecado,')):
        errors.append(f'{label}: refrão da Imaculada deve ter duas linhas, com quebra depois de pecado,.')
    structure = measured['estrutura']
    if structure['paragrafos_oracao'] != 1 or not structure['refrao_no_paragrafo'] or structure['em_quantidade'] != 1:
        errors.append(f'{label}: oração e refrão devem ficar no mesmo parágrafo, com um em.')
    if values['oracao']['entrelinha_px'] != 62 or refrain['entrelinha_px'] != 62:
        errors.append(f'{label}: oração e refrão precisam de entrelinha de 62px.')
    if values['oracao']['tamanho_px'] != 44 or refrain['tamanho_px'] != 44:
        errors.append(f'{label}: oração e refrão precisam de tamanho de 44px.')
    closing = card['encerramento']; ink = color('sobre-cor' if closing else 'tinta')
    quiet = color('sobre-cor' if closing else 'tinta-suave')
    gold = color('sobre-cor' if closing else 'ouro')
    expected_cross = '#faf6ee' if closing else '#5b2e70'
    expected_bg = '#866420' if closing else color('fundo')
    if measured['cores']['cruz'] != expected_cross:
        errors.append(f'{label}: cruz {measured["cores"]["cruz"]}; esperado {expected_cross}.')
    if measured['cores']['fundo'] != expected_bg:
        errors.append(f'{label}: fundo {measured["cores"]["fundo"]}; esperado {expected_bg}.')
    if measured['cores']['ornamento'] != gold:
        errors.append(f'{label}: ornamento na cor errada.')
    for name,text in values.items():
        wanted = quiet if name in {'contagem','data'} else gold if name == 'fonte' else ink
        if text['cor'] != wanted:
            errors.append(f'{label}, {name}: cor {text["cor"]}; esperado {wanted}.')
    if refrain['cor'] != quiet:
        errors.append(f'{label}: refrão na cor errada.')
    expected_logo = 'logo-horizontal-sobre-cor.svg' if closing else 'logo-horizontal-pergaminho.svg'
    if not structure['logo'].endswith(expected_logo):
        errors.append(f'{label}: assinatura incorreta.')
    beads = measured['contas']; count = 9 if closing else card['numero']
    expected_label = f'Dia {count} de 9'
    if beads['largura'] != 306 or beads['altura'] != 18 or beads['aria_label'] != expected_label or len(beads['circulos']) != 9:
        errors.append(f'{label}: contas precisam de nove círculos em SVG 306 × 18 com rótulo correto.')
    for index,circle in enumerate(beads['circulos']):
        if circle['cx'] != 9+36*index or circle['cy'] != 9:
            errors.append(f'{label}: contas com posição incorreta no círculo {index+1}.')
        if index < count:
            valid = circle['raio'] == 9 and circle['preenchimento'] == gold and circle['contorno'] == 'none'
        else:
            valid = (circle['raio'] == 7.75 and circle['preenchimento'] == 'none'
                and circle['contorno'] == gold and circle['espessura_contorno'] == 2.5)
        if not valid:
            errors.append(f'{label}: contas com preenchimento, raio, contorno ou cor incorretos no círculo {index+1}.')
    for word in measured['sem_quebra']:
        if word['white_space'] != 'nowrap':
            errors.append(f'{label}: palavra com hífen pode ser quebrada: {word["texto"]}.')
    result = {'ok':not errors,'distancias':distances,'limites':{'titulo':2,'oracao':8},
        'refrao':refrain,'contas':beads,'esperado':expected_layout(card),'errors':errors}
    if errors:raise ValueError('; '.join(errors))
    return result


def _pixels(path: Path, card: dict, measured: dict) -> dict:
    errors = []; samples = []
    with Image.open(path) as raw:
        image = raw.convert('RGB')
        def sample(name,x,y,wanted):
            actual = image.getpixel((int(x),int(y))); expected = ImageColor.getrgb(wanted)
            samples.append({'elemento':name,'pixel':[int(x),int(y)],'rgb':list(actual),'esperado':wanted,'ok':actual==expected})
            if actual != expected:errors.append(f'{card["novena"]}, {card["slug"]}, {name}: pixel {actual}; esperado {wanted}.')
        cross = measured['caixas']['cruz']; ornament = measured['caixas']['ornamento']
        closing = card['encerramento']; ink = '#faf6ee' if closing else color('ouro')
        sample('fundo',8,8,'#866420' if closing else color('fundo'))
        sample('cruz',cross['x']+9,cross['y']+18,'#faf6ee' if closing else '#5b2e70')
        sample('ornamento',ornament['x']+7,ornament['y']+10,ink)
        box = measured['caixas']['contas']; count = 9 if closing else card['numero']
        for index in range(9):
            sample(f'conta {index+1}',box['x']+9+36*index,box['y']+9,
                ink if index < count else '#866420' if closing else color('fundo'))
    result = {'ok':not errors,'amostras':samples,'errors':errors}
    if errors:raise ValueError('; '.join(errors))
    return result


def _pdf_check(path: Path, cards: list[dict], measured: list[dict]) -> dict:
    import fitz
    errors = []; fonts = {}; pages = []; expected_pages = []
    compact = lambda text:re.sub(r'\s+','',text)
    with fitz.open(path) as document:
        if len(document) != len(cards):errors.append(f'{path.name}: número de páginas incorreto.')
        for index,page in enumerate(document):
            expected = compact(''.join(text['conteudo'] for text in measured[index]['textos'])) if index < len(measured) else ''
            expected_pages.append(expected)
            actual = compact(page.get_text(sort=True))
            equal = expected == actual
            same_size = abs(page.rect.width-810)<.01 and abs(page.rect.height-1012.5)<.01
            pages.append({'pagina':index+1,'largura_pt':page.rect.width,'altura_pt':page.rect.height,
                'texto_igual_yaml_sem_espacos':equal,'dimensoes_ok':same_size})
            if not equal:errors.append(f'{path.name}, página {index+1}: texto integral diferente do YAML.')
            if not same_size:errors.append(f'{path.name}, página {index+1}: dimensão diferente de 810 × 1012,5 pt.')
            for info in page.get_fonts(full=True):
                xref = info[0]
                if xref in fonts:continue
                _,extension,_,data = document.extract_font(xref)
                name = re.sub(r'^[A-Z]{6}\+','',info[3])
                ttf = bool(data) and extension.lower() in {'ttf','ttc'} and data[:4] in {b'\x00\x01\x00\x00',b'true',b'ttcf'}
                fonts[xref] = {'nome':name,'formato':extension,'embutida':ttf,'bytes':len(data)}
                if not ttf:errors.append(f'{path.name}: fonte TTF não embutida: {name}.')
    missing = REQUIRED_FONTS-{item['nome'] for item in fonts.values()}
    if missing:errors.append('Fontes ausentes: '+', '.join(sorted(missing)))
    poppler_fonts = None; poppler_text = None
    if shutil.which('pdffonts'):
        process = subprocess.run(['pdffonts',str(path)],capture_output=True,text=True,check=False)
        poppler_fonts = process.stdout
        if process.returncode:errors.append('pdffonts falhou: '+process.stderr)
        for name in REQUIRED_FONTS:
            if name not in poppler_fonts:errors.append(f'pdffonts não lista {name}.')
        for line in poppler_fonts.splitlines()[2:]:
            match = re.search(r'\s(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$',line)
            if match and match.group(1) != 'yes':errors.append('pdffonts encontrou fonte não embutida: '+line)
    else:errors.append('pdffonts indisponível.')
    if shutil.which('pdftotext'):
        process = subprocess.run(['pdftotext','-layout',str(path),'-'],capture_output=True,text=True,check=False)
        poppler_text = process.stdout
        if process.returncode:errors.append('pdftotext falhou: '+process.stderr)
        actual_pages = [compact(part) for part in poppler_text.split('\f') if part.strip()]
        if actual_pages != expected_pages:errors.append(f'{path.name}: texto integral de pdftotext difere do YAML.')
    else:errors.append('pdftotext indisponível.')
    result = {'ok':not errors,'paginas':pages,'fontes':list(fonts.values()),'fontes_exigidas':sorted(REQUIRED_FONTS),
        'pdffonts':poppler_fonts,'pdftotext':poppler_text,'texto_igual_yaml_sem_espacos':not errors,'errors':errors}
    if errors:raise ValueError('; '.join(errors))
    return result
