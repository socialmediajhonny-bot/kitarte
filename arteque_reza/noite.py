"""Modelos das quatro séries da noite, com recortes locais antes de compor."""
from __future__ import annotations

from html import escape
from math import cos, pi, sin
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any

from PIL import Image, ImageColor, ImageDraw

from .base import PROJECT, assinatura, color, html_document, montar_arte, nicho, selo
from .conteudo import color_token, date_label
from .evangelho import _measure as measure_evangelho, _ornament, _text
from .igreja_domestica import BOOK_PATTERN, igreja_text_html
from .obras import artwork_geometry, crop_proof, inspect_artwork, uniform_margins
from .pdf_nicho import niches_from_elements, validate_niche_pdf
from .validacao import validate_niche_pixels


SERIES = {
    'olhe-de-novo': ('Olhe de Novo', 'PostOlheDeNovo', 'capela'),
    'por-dentro-da-missa': ('Por Dentro da Missa', 'PostPorDentroDaMissa', 'pergaminho'),
    'rezo-por-voce': ('Rezo por Você', 'PostRezoPorVoce', 'pergaminho'),
    'toda-bela': ('Toda Bela', 'PostTodaBela', 'capela'),
}
_BOOK_END = re.compile(r'(?:^|\s)(?:'+BOOK_PATTERN+r')[\W_]*$')


def expand_cards(series: str, days: list[dict]) -> list[dict]:
    """Preserve os blocos do conteúdo e a ordem aprovada de cada carrossel."""
    if series not in SERIES:
        raise ValueError('Série da noite desconhecida: '+series)
    result = []
    for day in days:
        if series == 'olhe-de-novo':
            blocks = [('obra', {'titulo': day['titulo'], 'obra': day['obra']}),
                      ('detalhe', {**day['detalhe'], 'obra': day['obra']}),
                      ('significado', day['significado']), ('onde', day['onde'])]
        elif series == 'por-dentro-da-missa':
            blocks = [('capa', day['capa'])]+[('explicacao', item) for item in day['explicacoes']]+[('fecho', day['fecho'])]
        elif series == 'rezo-por-voce':
            blocks = [('unico', {'titulo': day['titulo'], 'texto': day['texto']})]
        else:
            blocks = [('capa', {'info': day['info'], 'invocacao': day['invocacao'], 'obra': day['obra']}),
                      ('raiz', day['raiz']), ('oracao', day['oracao'])]
        for number, (kind, fields) in enumerate(blocks, 1):
            on_color = (series, kind) in {('por-dentro-da-missa', 'fecho'), ('toda-bela', 'oracao')}
            result.append({**fields, 'serie': series, 'modelo': SERIES[series][1],
                           'data': day['data'], 'cor': day['cor'], 'tipo': kind,
                           'numero': number, 'total': len(blocks), 'cartao_cor': on_color,
                           'tema': 'pergaminho' if on_color else SERIES[series][2]})
    return result


def expected_layout(card: dict) -> dict:
    """Tabela prevista no prompt; uma diferença válida é registrada na ficha."""
    series, number = card['serie'], card['numero']
    if series == 'olhe-de-novo':
        if number in (1, 2):
            return {'linhas': {'credito': 1, 'titulo': 1}, 'selo_nicho_px': 32, 'titulo_assinatura_px': 38}
        if number == 3:
            return {'linhas': {'rotulo': 1, 'titulo': 1, 'texto': 5, 'fonte': 1}, 'folga_px': 251.5}
        return {'linhas': {'rotulo': 1, **{f'credito_{i}': 2 for i in range(1, len(card['obras'])+1)},
                           'texto': 3, 'fonte': 1}, 'folga_px': 116}
    if series == 'por-dentro-da-missa':
        if card['tipo'] == 'capa':
            return {'linhas': {'pergunta': 2, 'resposta': 1}, 'folga_px': 369.5}
        if card['tipo'] == 'fecho':
            return {'linhas': {'rotulo': 1, 'frase': 2, 'convite': 1}, 'folga_px': 353.5}
        return {'linhas': {'rotulo': 1, 'titulo': 1, 'texto': 5 if number == 2 else 4, 'fonte': 2},
                'folga_px': 235.5 if number == 2 else 260.5}
    if series == 'rezo-por-voce':
        return {'linhas': {'titulo': 2, 'texto': 2}, 'folga_px': 352.5}
    if number == 1:
        return {'linhas': {'credito': 1, 'invocacao': 1}, 'selo_nicho_px': 32, 'invocacao_assinatura_px': 98}
    if number == 2:
        return {'linhas': {'rotulo': 1, 'versiculo': 1, 'referencia': 1, 'texto': 5, 'fonte': 1}, 'folga_px': 219.5}
    return {'linhas': {'rotulo': 1, 'frase': 2, 'convite': 1}, 'folga_px': 333.5}


def artwork_window(artwork: Path, work: dict, niche_width: int, niche_height: int) -> dict:
    """Calcule uma janela original e recuse tamanho, limites ou ampliação inválidos."""
    artwork = Path(artwork)
    with Image.open(artwork) as raw:
        actual = raw.size
    if 'tamanho' in work and list(actual) != list(work['tamanho']):
        raise ValueError(f'{artwork.name}: tamanho real {actual} difere de tamanho {work["tamanho"]}.')
    if 'janela' not in work:
        geometry = inspect_artwork(artwork, work['foco'], work.get('zoom', 1),
                                   niche_width=niche_width, niche_height=niche_height)
    else:
        window = work['janela']
        if (not isinstance(window, list) or len(window) != 3
                or any(type(n) is not int for n in window) or min(window[:2]) < 0 or window[2] <= 0):
            raise ValueError('janela: use [x, y, largura] com inteiros não negativos e largura positiva.')
        x, y, width = window
        height = round(width*(niche_height-16)/(niche_width-32))
        if x+width > actual[0] or y+height > actual[1]:
            raise ValueError(f'{artwork.name}: janela fora do arquivo: {window}, altura {height}.')
        geometry = inspect_artwork(artwork, '50% 50%', niche_width=niche_width, niche_height=niche_height)
        geometry['janela_original'] = {'x': x, 'y': y, 'largura': width, 'altura': height}
        geometry['escala_com_zoom'] = (niche_width-32)/width
        margins = geometry['margens_detectadas']
        visible = []
        if margins['topo'] and y < margins['topo']: visible.append('topo')
        if margins['base'] and y+height > actual[1]-margins['base']: visible.append('base')
        if margins['esquerda'] and x < margins['esquerda']: visible.append('esquerda')
        if margins['direita'] and x+width > actual[0]-margins['direita']: visible.append('direita')
        geometry['margens_visiveis'] = visible
        geometry['avisos'] = ([f'{artwork.name}: margem da foto visível: '+', '.join(visible)] if visible else [])
    window = geometry['janela_original']
    if (window['x'] < 0 or window['y'] < 0 or window['x']+window['largura'] > actual[0]+1e-8
            or window['y']+window['altura'] > actual[1]+1e-8):
        raise ValueError(f'{artwork.name}: janela fora do arquivo.')
    geometry['ampliacao'] = (niche_width-32)/window['largura']
    if geometry['ampliacao'] > 1.2+1e-9:
        raise ValueError(f'{artwork.name}: ampliação {geometry["ampliacao"]:g} acima de 1,2.')
    return geometry


def crop_image(artwork: Path, geometry: dict) -> Image.Image:
    """Imagem antes de codificar JPEG, sem ampliação e aceitando janela fracionária."""
    window, area = geometry['janela_original'], geometry['area_interna']
    width, height = window['largura'], window['altura']
    if width > 2*area['largura'] or height > 2*area['altura']:
        size = (round(2*area['largura']), round(2*area['altura']))
    else:
        size = (round(width), round(height))
    with Image.open(artwork) as raw:
        source = raw.convert('RGB')
        return source.resize(size, Image.Resampling.LANCZOS,
                             box=(window['x'], window['y'], window['x']+width, window['y']+height))


def _window_proof(artwork: Path, output: Path, geometry: dict) -> None:
    with Image.open(artwork) as raw:
        width, height = raw.size
        full = raw.convert('RGB').resize((1080, round(height*1080/width)), Image.Resampling.LANCZOS)
    window, area = geometry['janela_original'], geometry['area_interna']
    tw, th = area['largura'], area['altura']
    def inverse(x, y):
        return ((window['x']+x*window['largura']/tw)*1080/width,
                (window['y']+y*window['altura']/th)*1080/width)
    curve = [inverse(tw/2+tw/2*cos(pi+i*pi/240), tw/2+tw/2*sin(pi+i*pi/240)) for i in range(241)]
    curve += [inverse(tw, th), inverse(0, th), curve[0]]
    draw = ImageDraw.Draw(full)
    draw.line(curve, fill='#faf6ee', width=9, joint='curve')
    draw.line(curve, fill='#5b2e70', width=4, joint='curve')
    full.save(output)


def prepare_artworks(series: str, day: dict, target: Path) -> list[dict]:
    """Crie JPEGs recortados e provas na pasta da data; os originais são só lidos."""
    target = Path(target); target.mkdir(parents=True, exist_ok=True)
    if series == 'olhe-de-novo':
        jobs = [(1, 1, day['obra'], (640, 840), '1'),
                (2, 1, {**day['obra'], **day['detalhe']}, (640, 840), '2')]
        jobs += [(4, i, work, (340, 420), f'4-{i}') for i, work in enumerate(day['onde']['obras'], 1)]
    elif series == 'toda-bela':
        jobs = [(1, 1, day['obra'], (640, 760), '1')]
    else:
        return []
    records = []
    for number, index, work, size, suffix in jobs:
        artwork = PROJECT/work['arquivo']
        if not artwork.is_file():
            raise ValueError('Obra local ausente: '+work['arquivo'])
        geometry = artwork_window(artwork, work, niche_width=size[0], niche_height=size[1])
        # Os detectores atuais continuam sendo a fonte da análise de margens.
        assert uniform_margins(artwork) == geometry['margens_detectadas']
        cropped = target/f'obra-{suffix}.jpg'
        image = crop_image(artwork, geometry)
        image.save(cropped, quality=95, subsampling=0)
        proof = target/f'recorte-{suffix}.png'
        if 'janela' not in work:
            crop_proof(artwork, proof, work['foco'], zoom=work.get('zoom', 1),
                       niche_width=size[0], niche_height=size[1], date=day['data'])
        else:
            _window_proof(artwork, proof, geometry)
        keys = ('arquivo', 'credito', 'pagina', 'janela', 'tamanho') if 'janela' in work else ('arquivo', 'credito', 'pagina', 'foco')
        info = {key: work[key] for key in keys if key in work}
        if 'janela' not in work:
            info['zoom'] = work.get('zoom', 1)
        records.append({**info, 'card': number, 'indice': index,
                        'janela_original': geometry['janela_original'], 'ampliacao': geometry['ampliacao'],
                        'arquivo_recortado': cropped.resolve().relative_to(PROJECT).as_posix(),
                        'prova_recorte': proof.resolve().relative_to(PROJECT).as_posix(),
                        'tamanho_recortado': list(image.size), 'geometria': geometry,
                        'margens': {key: geometry[key] for key in ('margens_detectadas', 'faixas_descartadas', 'margens_visiveis')},
                        'margens_detectadas': geometry['margens_detectadas'],
                        'faixas_descartadas': geometry['faixas_descartadas'],
                        'margens_visiveis': geometry['margens_visiveis'], 'avisos': geometry['avisos']})
    return records


def _field(tag: str, field: str, style: str, value: str, css: str = '', token: str = 'tinta') -> str:
    return _text(tag, field, style, igreja_text_html(value), css+';color:var(--'+token+')', token, raw=True)


def _header(card: dict) -> str:
    series, number = card['serie'], card['numero']
    info = card.get('info') if series == 'toda-bela' and number == 1 else None
    if series in {'olhe-de-novo', 'por-dentro-da-missa'} or series == 'toda-bela' and number > 1:
        info = f'{number}/{card["total"]}'
    markup = selo(SERIES[series][0], date_label(card['data']), info)
    support = 'info' if series == 'toda-bela' and number == 1 else 'contagem'
    for original, field in [('selo-serie', 'selo'), ('selo-data', 'data'), ('selo-info', support)]:
        markup = markup.replace(f'data-element="{original}"', f'data-element="{original}" data-text="{field}" data-style="selo"')
    return markup


def _niche(record: dict, width: int, height: int, *, top: bool = False) -> str:
    image = PROJECT/record['arquivo_recortado']
    markup = nicho(width, height, image, foco='50% 50%', zoom=1)
    markup = markup.replace('alt="Obra provisória"', 'alt="Obra da série da noite"')
    markup = markup.replace('data-arquivo="obra-provisoria.png"',
                            f'data-arquivo="{escape(record["arquivo_recortado"], quote=True)}"')
    if top:
        markup = markup.replace(f'style="width:{width}px;height:{height}px;"',
                                f'style="width:{width}px;height:{height}px;margin-top:var(--espaco-3)"')
    return markup


def _document(card: dict, css: Path, artworks: list[dict] | None = None,
              invocation_style: str = 'titulo-capa') -> str:
    series, kind = card['serie'], card['tipo']
    on_color, theme = card['cartao_cor'], card['tema']
    ink, quiet = ('sobre-cor', 'sobre-cor') if on_color else ('tinta', 'tinta-suave')
    works = sorted((a for a in (artworks or []) if a['card'] == card['numero']), key=lambda a: a['indice'])
    top_art = series == 'olhe-de-novo' and kind in {'obra', 'detalhe'} or series == 'toda-bela' and kind == 'capa'
    if top_art:
        if len(works) != 1:
            raise ValueError('A capa/detalhe precisa de exatamente uma obra previamente recortada.')
        height = 760 if series == 'toda-bela' else 840
        body = _niche(works[0], 640, height, top=True)
        credit = 'Detalhe da mesma obra' if kind == 'detalhe' else card['obra']['credito']
        body += _field('p', 'credito', 'credito aqr-credito', credit, 'margin-top:var(--espaco-3);max-width:920px', quiet)
        field = 'invocacao' if series == 'toda-bela' else 'titulo'
        style = invocation_style if field == 'invocacao' else 'titulo'
        body += _field('h1', field, style+' aqr-titulo', card[field], 'margin-top:var(--espaco-4);max-width:880px')
    else:
        body = '<div class="aqr-texto" style="margin-top:auto">'
        if series == 'rezo-por-voce':
            body += _ornament().replace('margin-block:var(--espaco-3)', 'margin-top:0;margin-bottom:var(--espaco-3)')
            body += _field('h1', 'titulo', 'titulo-capa aqr-titulo', card['titulo'], 'max-width:860px')
            body += _field('p', 'texto', 'corpo aqr-corpo aqr-suave', card['texto'],
                           'margin-top:var(--espaco-2);max-width:760px', quiet)
        elif series == 'por-dentro-da-missa' and kind == 'capa':
            body += _field('h1', 'pergunta', 'titulo-capa aqr-titulo', card['pergunta'], 'max-width:860px')
            body += _ornament()
            body += _field('p', 'resposta', 'corpo aqr-corpo', card['resposta'], 'max-width:760px')
        elif kind in {'significado', 'explicacao'}:
            body += _field('p', 'rotulo', 'selo', card['rotulo'], 'margin-bottom:var(--espaco-3)', quiet)
            body += _field('h1', 'titulo', 'titulo aqr-titulo', card['titulo'], 'max-width:880px')
            body += _ornament()
            body += _field('p', 'texto', 'corpo aqr-corpo', card['texto'], 'max-width:760px')
            body += _field('p', 'fonte', 'credito aqr-credito', card['fonte'], 'margin-top:var(--espaco-2);max-width:920px', quiet)
        elif kind == 'onde':
            if len(works) != len(card['obras']):
                raise ValueError('Todas as obras do card 4 precisam estar previamente recortadas.')
            body += _field('p', 'rotulo', 'selo', card['rotulo'], 'margin-bottom:var(--espaco-3)', quiet)
            body += ('<div data-element="linha-nichos" class="noite-nichos" '
                     'style="display:flex;gap:56px;justify-content:center;align-items:flex-start;width:100%">')
            for index, work in enumerate(works, 1):
                body += ('<figure class="noite-figura" style="display:flex;flex-direction:column;'
                         'align-items:center;width:380px;flex:none">')
                body += _niche(work, 340, 420)
                body += _field('figcaption', f'credito_{index}', 'credito aqr-credito', work['credito'],
                               'margin-top:var(--espaco-3);max-width:380px;text-wrap:balance', quiet)
                body += '</figure>'
            body += '</div>'
            body += _field('p', 'texto', 'corpo aqr-corpo', card['texto'], 'margin-top:var(--espaco-3);max-width:760px')
            body += _field('p', 'fonte', 'credito aqr-credito', card['fonte'], 'margin-top:var(--espaco-2);max-width:920px', quiet)
        elif series == 'toda-bela' and kind == 'raiz':
            body += _field('p', 'rotulo', 'selo', card['rotulo'], 'margin-bottom:var(--espaco-3)', quiet)
            body += _field('p', 'versiculo', 'citacao aqr-citacao', card['versiculo'], 'max-width:860px')
            body += _field('p', 'referencia', 'referencia aqr-referencia', card['referencia'], 'margin-top:var(--espaco-2)', 'ouro')
            body += _ornament()
            body += _field('p', 'texto', 'corpo aqr-corpo', card['texto'], 'max-width:760px')
            body += _field('p', 'fonte', 'credito aqr-credito', card['fonte'], 'margin-top:var(--espaco-2);max-width:920px', quiet)
        else:
            body += _field('p', 'rotulo', 'selo', card['rotulo'], 'margin-bottom:var(--espaco-3)', quiet)
            phrase_style = 'citacao-grande' if series == 'toda-bela' else 'citacao'
            body += _field('p', 'frase', phrase_style+' aqr-citacao', card['frase'], 'max-width:860px', ink)
            body += _ornament(on_color)
            body += _field('p', 'convite', 'corpo', card['convite'], '', ink)
        body += '</div>'
    post = montar_arte(_header(card)+body+assinatura(theme, sobre_cor=on_color),
                       tema=theme, cor_do_dia=color_token(card['cor']), cartao_cor=on_color)
    return html_document(post, css, '@page{margin:0;} .aqr-post--cor .aqr-corpo{color:var(--sobre-cor);}',
                         f'{SERIES[series][0]} · {card["data"]} · {card["numero"]}/{card["total"]}')


_EXTRA_JS = r"""() => {
 const root=document.querySelector('.aqr-post'), ar=root.getBoundingClientRect();
 const rr=r=>({x:+(r.left-ar.left).toFixed(6),y:+(r.top-ar.top).toFixed(6),largura:+r.width.toFixed(6),altura:+r.height.toFixed(6)});
 const box=sel=>{const n=root.querySelector(sel);return n?rr(n.getBoundingClientRect()):null;};
 const hex=v=>'#'+v.match(/[\d.]+/g).slice(0,3).map(v=>(+v).toString(16).padStart(2,'0')).join('');
 return {caixas:{ornamento:box('.aqr-ornamento'),assinatura:box('.aqr-assinatura'),linha_nichos:box('.noite-nichos')},
   nichos:[...root.querySelectorAll('.aqr-nicho')].map(n=>rr(n.getBoundingClientRect())),
   figuras:[...root.querySelectorAll('.noite-figura')].map(n=>rr(n.getBoundingClientRect())),
   cores:{fundo:hex(getComputedStyle(root).backgroundColor),cruz:hex(getComputedStyle(root.querySelector('.aqr-selo__cruz')).color),
     ornamento:root.querySelector('.aqr-ornamento')?hex(getComputedStyle(root.querySelector('.aqr-ornamento')).color):null},
   tema_dom:root.dataset.theme,logo:root.querySelector('[data-element="logo"]').getAttribute('data-arquivo'),
   estilos_texto:Object.fromEntries([...root.querySelectorAll('[data-text]')].map(n=>[n.dataset.text,getComputedStyle(n).fontStyle])),
   sem_quebra:[...root.querySelectorAll('.igreja-sem-quebra')].map(n=>({texto:n.textContent,regra:n.dataset.regra,
     white_space:getComputedStyle(n).whiteSpace,linhas:[...n.getClientRects()].map(r=>+(r.top-ar.top).toFixed(6))}))};
}"""


def _measure(page: Any, card: dict) -> dict:
    measured = measure_evangelho(page, card['numero'], 1)
    # No medidor compartilhado, "referencia" é o apoio do selo. Aqui a mesma
    # palavra também nomeia o campo bíblico da Toda Bela, que deve ficar distinto.
    measured['caixas']['info_topo'] = measured['caixas'].pop('referencia', None)
    measured.update({key: card[key] for key in ('serie', 'modelo', 'tipo', 'data', 'cor', 'numero', 'total', 'tema', 'cartao_cor')})
    measured['conteudo'] = card
    extra = page.evaluate(_EXTRA_JS)
    measured['caixas'].update(extra.pop('caixas')); measured.update(extra)
    for text in measured['textos']:
        text['alinhamento_canva'] = ('start' if text['campo'] in {'selo', 'data'} else
                                    'end' if text['campo'] in {'contagem', 'info'} else 'center')
    boxes=measured['caixas'];block=boxes['bloco_texto']
    if block:
        seal,signature=boxes['selo'],boxes['assinatura']
        upper=block['y']-seal['y']-seal['altura'];lower=signature['y']-block['y']-block['altura']
        measured['distancias']={'selo_texto_px':upper,'texto_assinatura_px':lower,'diferenca_centralizacao_px':abs(upper-lower)}
    else:
        measured['distancias']={}
    return measured


def _limits(card: dict, values: dict) -> dict:
    series, kind=card['serie'],card['tipo']
    if series=='olhe-de-novo':
        if kind in {'obra','detalhe'}:return {'credito':1,'titulo':1}
        if kind=='significado':return {'rotulo':1,'titulo':2,'texto':6,'fonte':2}
        return {'rotulo':1,**{f'credito_{i}':2 for i in range(1,len(card['obras'])+1)},'texto':4,'fonte':1}
    if series=='por-dentro-da-missa':
        if kind=='capa':return {'pergunta':2,'resposta':3}
        if kind=='explicacao':return {'rotulo':1,'titulo':2,'texto':6,'fonte':2}
        return {'rotulo':1,'frase':4,'convite':1}
    if series=='rezo-por-voce':return {'titulo':2,'texto':2}
    if kind=='capa':return {'credito':1,'invocacao':1 if values['invocacao']['estilo']=='titulo-capa'else 2}
    if kind=='raiz':return {'rotulo':1,'versiculo':3,'referencia':1,'texto':5,'fonte':1}
    return {'rotulo':1,'frase':3,'convite':1}


def _tokens(card: dict, field: str) -> str:
    if card['cartao_cor']:return 'sobre-cor'
    if field=='referencia':return 'ouro'
    if field in {'data','contagem','info','rotulo','fonte','credito'} or field.startswith('credito_'):
        return 'tinta-suave'
    if card['serie']=='rezo-por-voce'and field=='texto':return 'tinta-suave'
    return 'tinta'


def _validate_layout(card: dict, measured: dict) -> dict:
    errors=[];label=f'{card["data"]}, card {card["numero"]}'
    values={text['campo']:text for text in measured['textos']}
    limits=_limits(card,values)
    for field,text in values.items():
        if field in limits and text['quantidade_linhas']>limits[field]:
            errors.append(f'{label}, {field}: {text["quantidade_linhas"]} linhas; limite {limits[field]}.')
        box=text['caixa']
        if box['x']<-.1 or box['y']<-.1 or box['x']+box['largura']>1080.1 or box['y']+box['altura']>1350.1:
            errors.append(f'{label}, {field}: texto fora da arte.')
        for line,linebox in zip(text['linhas'],text['caixas_das_linhas']):
            if re.search(r'(?:^|\s)[aàeéoóAÀEÉOÓ][\W_]*$',line):errors.append(f'{label}, {field}: palavra de uma letra no fim de {line!r}.')
            if line.rstrip().endswith(('-', '\u2010','\u2011','\u00ad')):errors.append(f'{label}, {field}: linha termina em hífen: {line!r}.')
            if re.search(r'\d+[ºª][\W_]*$',line):errors.append(f'{label}, {field}: linha termina em ordinal: {line!r}.')
            if _BOOK_END.search(line):errors.append(f'{label}, {field}: linha termina em abreviação bíblica: {line!r}.')
            if linebox['largura']and(linebox['x']<box['x']-.1 or linebox['x']+linebox['largura']>box['x']+box['largura']+.1):
                errors.append(f'{label}, {field}: linha transborda a largura do campo.')
    boxes={field:text['caixa']for field,text in values.items()}
    boxes.update({key:value for key,value in measured['caixas'].items()if value is not None})
    series,kind=card['serie'],card['tipo'];pairs=[]
    top_art=series=='olhe-de-novo'and kind in {'obra','detalhe'}or series=='toda-bela'and kind=='capa'
    if top_art:
        last='invocacao'if series=='toda-bela'else'titulo'
        pairs=[('selo','nicho',32),('nicho','credito',32),('credito',last,48)]
    elif series=='rezo-por-voce':pairs=[('ornamento','titulo',48),('titulo','texto',32)]
    elif series=='por-dentro-da-missa'and kind=='capa':pairs=[('pergunta','ornamento',48),('ornamento','resposta',48)]
    elif kind in {'significado','explicacao'}:
        pairs=[('rotulo','titulo',48),('titulo','ornamento',48),('ornamento','texto',48),('texto','fonte',32)]
    elif kind=='onde':
        pairs=[('rotulo','linha_nichos',48),('linha_nichos','texto',48),('texto','fonte',32)]
        for i,niche in enumerate(measured['nichos'],1):
            boxes[f'nicho_{i}']=niche;pairs.append((f'nicho_{i}',f'credito_{i}',32))
    elif series=='toda-bela'and kind=='raiz':
        pairs=[('rotulo','versiculo',48),('versiculo','referencia',32),('referencia','ornamento',48),('ornamento','texto',48),('texto','fonte',32)]
    else:pairs=[('rotulo','frase',48),('frase','ornamento',48),('ornamento','convite',48)]
    distances=dict(measured['distancias'])
    for first,second,wanted in pairs:
        a,b=boxes[first],boxes[second];gap=b['y']-a['y']-a['altura'];distances[f'{first}_{second}_px']=round(gap,6)
        if abs(gap-wanted)>.01:errors.append(f'{label}, {first} → {second}: distância {gap:.2f}px; esperado {wanted}px (±0,01).')
    if top_art:
        a,b=boxes[last],boxes['assinatura'];gap=b['y']-a['y']-a['altura'];distances[last+'_assinatura_px']=gap
        if gap<31.99:errors.append(f'{label}: {last} a menos de 32px da assinatura.')
    else:
        if distances['diferenca_centralizacao_px']>.1:errors.append(f'{label}: bloco de texto não centralizado.')
        if min(distances['selo_texto_px'],distances['texto_assinatura_px'])<59.99:errors.append(f'{label}: bloco a menos de 60px do selo ou assinatura.')
    if kind=='onde':
        figures=measured['figuras'];niches=measured['nichos'];count=len(card['obras'])
        if len(figures)!=count or len(niches)!=count:errors.append(f'{label}: quantidade de figuras/nichos incorreta.')
        if figures:
            left,right=figures[0]['x'],figures[-1]['x']+figures[-1]['largura']
            if abs((left+right)/2-540)>.01:errors.append(f'{label}: obras não centralizadas.')
        if len(niches)==2:
            gap=niches[1]['x']-niches[0]['x']-niches[0]['largura'];distances['distancia_entre_nichos_px']=gap
            if abs(gap-96)>.01 or abs(niches[0]['y']-niches[1]['y'])>.01:errors.append(f'{label}: nichos sem alinhamento ou distância de 96px.')
    theme=card['tema'];on_color=card['cartao_cor']
    wanted_bg=color(color_token(card['cor'])if on_color else'fundo',theme)
    wanted_cross=color('sobre-cor'if on_color else color_token(card['cor']),theme)
    wanted_ornament=color('sobre-cor'if on_color else'ouro',theme)
    if measured['cores']['fundo']!=wanted_bg:errors.append(f'{label}: fundo não ocupa o cartão inteiro na cor esperada.')
    if measured['cores']['cruz']!=wanted_cross:errors.append(f'{label}: cruz na cor errada.')
    if measured['cores']['ornamento']is not None and measured['cores']['ornamento']!=wanted_ornament:errors.append(f'{label}: ornamento na cor errada.')
    if measured['tema_dom']!=theme:errors.append(f'{label}: tema errado.')
    for field,text in values.items():
        if text['cor']!=color(_tokens(card,field),theme):errors.append(f'{label}, {field}: texto na cor errada.')
    logo='logo-horizontal-sobre-cor.svg'if on_color else f'logo-horizontal-{theme}.svg'
    if not measured['logo'].endswith(logo):errors.append(f'{label}: assinatura na variante errada.')
    for word in measured['sem_quebra']:
        if word['white_space']!='nowrap'or len(set(word['linhas']))>1:errors.append(f'{label}: texto protegido partido: {word["texto"]!r}.')
    result={'ok':not errors,'distancias':distances,'limites':limits,'esperado':expected_layout(card),'errors':errors}
    if errors:raise ValueError('; '.join(errors))
    return result


def _pixels(path: Path, card: dict, measured: dict) -> dict:
    errors=[];samples=[];theme=card['tema'];on_color=card['cartao_cor'];cross=measured['caixas']['cruz']
    points=[('fundo',8,8,color(color_token(card['cor'])if on_color else'fundo',theme)),
            ('cruz',cross['x']+9,cross['y']+18,color('sobre-cor'if on_color else color_token(card['cor']),theme))]
    ornament=measured['caixas'].get('ornamento')
    if ornament:
        points.append(('ornamento',ornament['x']+ornament['largura']/2,ornament['y']+ornament['altura']/2,color('sobre-cor'if on_color else'ouro',theme)))
    with Image.open(path)as raw:
        image=raw.convert('RGB')
        for name,x,y,wanted in points:
            point=(int(x),int(y));actual=image.getpixel(point);ok=actual==ImageColor.getrgb(wanted)
            samples.append({'elemento':name,'pixel':list(point),'rgb':list(actual),'esperado':wanted,'ok':ok})
            if not ok:errors.append(f'{card["data"]}, card {card["numero"]}, {name}: cor incorreta.')
        for text in measured['textos']:
            box=text['caixa'];wanted=ImageColor.getrgb(color(_tokens(card,text['campo']),theme))
            region=image.crop((int(box['x']),int(box['y']),int(box['x']+box['largura']+.999),int(box['y']+box['altura']+.999)))
            present=any(rgb==wanted for _,rgb in(region.getcolors(region.width*region.height)or[]))
            samples.append({'elemento':text['campo'],'cor_em_pixel':list(wanted),'presente':present,'ok':present})
            if not present:errors.append(f'{text["campo"]}: cor do texto ausente nos pixels renderizados.')
    niches=None
    if measured['nichos']:
        niches=validate_niche_pixels(path,[{'name':f'nicho-{i}','x':b['x'],'y':b['y'],'width':b['largura'],'height':b['altura'],
                                           'filete':color(color_token(card['cor']),theme),'background':color('fundo',theme)}
                                          for i,b in enumerate(measured['nichos'],1)])
        errors.extend(niches['errors'])
    result={'ok':not errors,'amostras':samples,'nichos':niches,'errors':errors}
    if errors:raise ValueError('; '.join(errors))
    return result


def _pdf_check(path: Path, cards: list[dict], measured: list[dict]) -> dict:
    """Confira cada caixa e a página integral, sem perder a ordem das colunas.

    A ordem lógica do conteúdo preserva cada crédito completo. A extração por
    posição intercala as linhas dos dois créditos lado a lado do card 4; por
    isso PyMuPDF sem reordenação e pdftotext -raw são usados, além da conferência
    independente de cada caixa. Nenhum texto fora dessas caixas é tolerado.
    """
    import fitz
    errors=[];fonts={};pages=[];expected_pages=[];required=set()
    normal=lambda value:' '.join(value.split())
    for measurement in measured:
        for text in measurement['textos']:
            if text['fonte']=='Lato':
                required.add('Lato-Bold' if text['peso']=='700' else 'Lato-Regular')
            else:
                italic=measurement['estilos_texto'][text['campo']]=='italic'
                required.add('CormorantGaramond-SemiBold' if text['peso']=='600' else
                             'CormorantGaramond-MediumItalic' if italic else 'CormorantGaramond-Medium')
    with fitz.open(path)as document:
        if len(document)!=len(cards)or len(measured)!=len(cards):
            errors.append(f'{path.name}: número de páginas incorreto.')
        for index,page in enumerate(document):
            if index>=len(measured):
                continue
            measurement=measured[index]
            expected=normal(' '.join(text['conteudo']for text in measurement['textos']))
            expected_pages.append(expected)
            extracted=normal(page.get_text(sort=False));equal=extracted==expected
            dimensions=abs(page.rect.width-810)<.01 and abs(page.rect.height-1012.5)<.01
            fields=[]
            for text in measurement['textos']:
                box=text['caixa'];scale=.75
                rectangle=fitz.Rect(box['x']*scale-1,box['y']*scale-1,
                                    (box['x']+box['largura'])*scale+1,(box['y']+box['altura'])*scale+1)
                actual=normal(page.get_textbox(rectangle));wanted=normal(text['conteudo'])
                field_equal=actual==wanted
                fields.append({'campo':text['campo'],'texto_igual_yaml':field_equal})
                if not field_equal:
                    errors.append(f'{path.name}, página {index+1}, {text["campo"]}: texto na caixa diferente do YAML.')
            if not equal:errors.append(f'{path.name}, página {index+1}: texto integral diferente do YAML ou texto a mais.')
            if not dimensions:errors.append(f'{path.name}, página {index+1}: tamanho PDF incorreto.')
            pages.append({'pagina':index+1,'largura_pt':page.rect.width,'altura_pt':page.rect.height,
                          'texto_igual_yaml_com_espacos':equal,'dimensoes_ok':dimensions,'campos':fields})
            for info in page.get_fonts(full=True):
                xref=info[0]
                if xref in fonts:continue
                _,extension,_,data=document.extract_font(xref);name=re.sub(r'^[A-Z]{6}\+','',info[3])
                embedded=bool(data)and extension.lower()in {'ttf','ttc'}and data[:4]in {b'\x00\x01\x00\x00',b'true',b'ttcf'}
                fonts[xref]={'nome':name,'formato':extension,'embutida':embedded,'bytes':len(data)}
                if not embedded:errors.append(f'{path.name}: fonte TTF não embutida: {name}.')
    missing=required-{font['nome']for font in fonts.values()}
    if missing:errors.append('Fontes ausentes: '+', '.join(sorted(missing)))
    font_text=text_output=None
    if shutil.which('pdffonts'):
        process=subprocess.run(['pdffonts',str(path)],capture_output=True,text=True,check=False)
        font_text=process.stdout
        if process.returncode:errors.append('pdffonts falhou: '+process.stderr)
        for line in font_text.splitlines()[2:]:
            match=re.search(r'\s(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$',line)
            if match and match.group(1)!='yes':errors.append('pdffonts encontrou fonte não embutida: '+line)
    else:errors.append('pdffonts indisponível.')
    if shutil.which('pdftotext'):
        process=subprocess.run(['pdftotext','-raw',str(path),'-'],capture_output=True,text=True,check=False)
        text_output=process.stdout
        if process.returncode:errors.append('pdftotext falhou: '+process.stderr)
        if [normal(part)for part in text_output.split('\f')if part.strip()]!=expected_pages:
            errors.append(f'{path.name}: texto integral de pdftotext difere do YAML.')
    else:errors.append('pdftotext indisponível.')
    niches=[niche for number,measurement in enumerate(measured,1)
            for niche in niches_from_elements(measurement['elementos'],page=number)]
    vector_niche=validate_niche_pdf(path,niches);errors.extend(vector_niche['errors'])
    result={'ok':not errors,'paginas':pages,'fontes':list(fonts.values()),'fontes_exigidas':sorted(required),
            'pdffonts':font_text,'pdftotext':text_output,'pdftotext_modo':'raw',
            'texto_igual_yaml_com_espacos':not errors,'nicho_vetorial':vector_niche,'errors':errors}
    if errors:raise ValueError('; '.join(errors))
    return result
