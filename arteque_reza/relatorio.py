"""Relatório de decisões e evidências da geração, sem depender de serviços externos."""
from __future__ import annotations

from pathlib import Path


def tree(root: Path, prefix: str = "") -> list[str]:
    children = sorted(root.iterdir(), key=lambda path: (not path.is_dir(), path.name))
    result = []
    for index, path in enumerate(children):
        last = index == len(children) - 1
        result.append(prefix + ("└── " if last else "├── ") + path.name + ("/" if path.is_dir() else ""))
        if path.is_dir():
            result.extend(tree(path, prefix + ("    " if last else "│   ")))
    return result


def write_report(output: Path, manifest: dict) -> Path:
    checks = manifest['checks']
    protection = manifest['elementos']['protection_area']
    comparison = checks['logos']['comparisons']
    max_difference = max(metric['mean_channel_difference'] for record in comparison for metric in record['metrics'])
    target = output / 'RELATORIO.md'
    # Include the report itself in the tree before computing its final contents.
    target.touch(exist_ok=True)
    lines = [
        '# Relatório de design — Arte que Reza',
        '',
        'Base reutilizável do gerador de artes de @artequereza.oficial, com as peças Selo, Nicho e Assinatura e arquivos preparados para testar no Canva.',
        '',
        '## Gerar novamente',
        '',
        'No diretório do repositório, com as dependências de requirements.txt instaladas:',
        '',
        '```bash',
        'python gerar.py componentes',
        '```',
        '',
        'O comando reutiliza o ambiente .venv quando necessário, extrai o ZIP sem alterar o conteúdo do kit, gera os arquivos e interrompe a execução se uma validação obrigatória falhar. A renderização usa Python 3, Playwright e /usr/bin/chromium. Não há requisições para fontes ou outros recursos externos durante a geração.',
        '',
        '## Saídas',
        '',
        '```text',
        'saida/',
        *tree(output),
        '```',
        '',
        '## Decisões de composição',
        '',
        '- O gap entre cruz e texto do selo é espaco-2, 16 px, conforme bundle.css; a menção a espaco-1 no texto do token não altera o CSS.',
        '- Os nomes antigos fonts/*.woff2 do JSON são mapeados pelo basename para os seis TTF de kit/fontes. As seis variantes precisam carregar e passar em document.fonts.check antes de cada PNG e PDF; uma fonte substituta causa erro.',
        '- As assinaturas usam a altura final de 52 px solicitada, embora a vitrine do kit mostre 72 px. A curta usa 40 px e gap de 16 px; a assinatura horizontal com @ mantém 32 px.',
        '- O cartão inteiro na cor do dia usa o tema pergaminho, que contém os tons profundos; cruz e textos usam sobre-cor e o logo é a versão capela.',
        '- Os elementos de lançamento usam roxo por tema. O santinho mantém papel e ouro. Uma variante verde separada reproduz a capa do Evangelho solicitada no teste de importação.',
        '- A imagem provisória vem apenas do degradê aqr-obra--luz rasterizado em 1080 × 1350. Dentro dos nichos só há imagens, sem degradês CSS.',
        '- Na página Canva, a imagem continua retangular, nos limites internos de 648 × 744 px e offset de 16 px, para preservar o mesmo enquadramento da capa CSS. A máscara SVG fica em x − 48, com 776 × 763 px; nenhum clip CSS é usado nessa versão.',
        '- Os SVGs de nicho têm duas cores, máscara e filete/parapeito. O arco externo tem raio W/2; o interno tem raio (W−32)/2 e centro coincidente. A máscara pode ser usada sobre uma imagem retangular.',
        '- Os viewBoxes dos logos são recortados para os limites reais do desenho, como solicitado. Os originais têm pequenas sobras e um corte de borda. Para comparar apenas a conversão de traço em preenchimento, o original é renderizado nos mesmos limites de desenho e no mesmo tamanho do convertido. O kit original não é alterado; os originais normalizados de comparação ficam em verificacao/logos/.',
        '- As prévias são pranchas de inspeção, com rótulos de 14 px fora das peças: selos 2160 × 1600, nichos 2160 × 3360 e assinaturas 2160 × 1320. As três páginas de prova permanecem em 1080 × 1350.',
        '- O Chromium arredonda a altura física do PDF em cerca de 0,54 pt. Na junção das páginas, a origem do conteúdo é compensada e MediaBox/CropBox são fixados em 810 × 1012,5 pt; o texto e as fontes permanecem vetoriais.',
        '',
        '## Área de proteção',
        '',
        f"A travessa mede {protection['crossbar_native_units']:g} unidades no símbolo, com escala {protection['symbol_scale']:g}: {protection['crossbar_svg_units']:.4f} unidades no SVG horizontal. No logo original com caixa de 52 px de altura, a proteção é **{protection['source_logo_52px']:.4f} px** em cada lado. No SVG para Canva com viewBox justo e 52 px, é **{protection['canva_tight_logo_52px']:.4f} px**, ou aproximadamente **13 px**.",
        '',
        '## Validação',
        '',
        f"- {checks['kit']['count']} arquivos do kit conferidos contra o ZIP do commit; nenhuma mudança na fonte da verdade.",
        f"- {checks['svgs']['count']} SVGs com tamanho menor que 3 MB e contagens zeradas para stroke, text, style, class, transform, degradês, Q e T.",
        '- PNGs conferidos contra as dimensões declaradas em verificacao/resultados.json, incluindo as pranchas, páginas e comparações de logos.',
        '- PDF com três páginas de 810 × 1012,5 pt, equivalentes a 1080 × 1350 px a 96 dpi. O selo e o título ou a pergunta de cada página continuam como texto extraível.',
        '- Fontes TrueType embutidas conferidas no próprio PDF: CormorantGaramond-SemiBold, CormorantGaramond-MediumItalic, Lato-Bold e Lato-Regular. As outras duas variantes estão nos TTF fornecidos e são verificadas no navegador, sem exigir que apareçam em páginas que não as usam.',
        '- Seis nichos conferidos por pixels no canto, topo, lateral, parapeito e três pontos do arco; tolerância de 3 níveis RGB para antialiasing.',
        f'- Nove logos comparados em dois fundos; maior diferença média por canal: {max_difference:.6f}/255, concentrada na rasterização das bordas. As imagens original/convertido e as métricas estão em verificacao/.',
        '- Navegador sem erros de console, execução ou HTTP durante a geração. A FICHA contém os valores de posição e tipografia medidos no DOM; os pseudoelementos são derivados dos estilos resolvidos e da caixa medida do nicho.',
        '',
        '## Limites e verificações externas',
        '',
        '- A importação real no Canva e a capacidade de editar cada objeto no editor não foram verificadas nesta sessão. O PDF, os SVGs e os TTF estão preparados para esse teste, com as verificações locais descritas acima.',
        '- A obra é provisória e não representa uma pintura sacra final.',
        '- A integração Documents e o modelo remoto Design Report não estão disponíveis nas ferramentas desta sessão. Este relatório é o documento local entregue; não foi criado um documento nesse serviço nem aplicado o modelo remoto.',
        '',
    ]
    target.write_text('\n'.join(lines),encoding='utf-8')
    return target
