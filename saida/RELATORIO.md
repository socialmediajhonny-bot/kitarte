# Relatório de design — Arte que Reza

Base reutilizável do gerador de artes de @artequereza.oficial, com as peças Selo, Nicho e Assinatura e arquivos preparados para testar no Canva.

## Gerar novamente

No diretório do repositório, com as dependências de requirements.txt instaladas:

```bash
python gerar.py componentes
```

O comando reutiliza o ambiente .venv quando necessário, extrai o ZIP sem alterar o conteúdo do kit, gera os arquivos e interrompe a execução se uma validação obrigatória falhar. A renderização usa Python 3, Playwright e /usr/bin/chromium. Não há requisições para fontes ou outros recursos externos durante a geração.

## Saídas

```text
saida/
├── canva/
│   ├── elementos/
│   │   ├── fontes/
│   │   │   ├── licencas/
│   │   │   │   ├── OFL-CormorantGaramond.txt
│   │   │   │   └── OFL-Lato.txt
│   │   │   ├── CormorantGaramond-Medium.ttf
│   │   │   ├── CormorantGaramond-MediumItalic.ttf
│   │   │   ├── CormorantGaramond-SemiBold.ttf
│   │   │   ├── CormorantGaramond-SemiBoldItalic.ttf
│   │   │   ├── Lato-Bold.ttf
│   │   │   └── Lato-Regular.ttf
│   │   ├── logos/
│   │   │   ├── avatar-perfil.png
│   │   │   ├── avatar-perfil.svg
│   │   │   ├── logo-horizontal-capela.svg
│   │   │   ├── logo-horizontal-pergaminho.svg
│   │   │   ├── logo-horizontal-sobre-cor.svg
│   │   │   ├── logo-vertical-capela.svg
│   │   │   ├── logo-vertical-pergaminho.svg
│   │   │   ├── simbolo-capela.svg
│   │   │   ├── simbolo-pergaminho.svg
│   │   │   ├── simbolo-reduzido-capela.svg
│   │   │   └── simbolo-reduzido-pergaminho.svg
│   │   ├── variantes/
│   │   │   └── nicho-680x760-capela-verde.svg
│   │   ├── cruz-capela.svg
│   │   ├── cruz-pergaminho.svg
│   │   ├── nicho-340x420-santinho.svg
│   │   ├── nicho-600x680-coragem.svg
│   │   ├── nicho-600x700-angelus.svg
│   │   ├── nicho-640x760-toda-bela.svg
│   │   ├── nicho-680x760-capela.svg
│   │   └── nicho-720x900-status-coragem.svg
│   ├── FICHA.md
│   ├── medicoes.json
│   ├── pagina-1.png
│   ├── pagina-2.png
│   ├── pagina-3.png
│   └── teste-importacao.pdf
├── coragem/
│   ├── 2026-12-14/
│   │   ├── coragem-2026-12-14-feed.pdf
│   │   ├── coragem-2026-12-14-status.pdf
│   │   ├── feed.png
│   │   ├── ficha.json
│   │   ├── recorte-feed.png
│   │   ├── recorte-status.png
│   │   └── status.png
│   ├── 2026-12-28/
│   │   ├── coragem-2026-12-28-feed.pdf
│   │   ├── coragem-2026-12-28-status.pdf
│   │   ├── feed.png
│   │   ├── ficha.json
│   │   ├── recorte-feed.png
│   │   ├── recorte-status.png
│   │   └── status.png
│   ├── RELATORIO.md
│   ├── prancha.png
│   └── verificacao.json
├── evangelho/
│   ├── 2026-11-29/
│   │   ├── card-1.png
│   │   ├── card-2.png
│   │   ├── card-3.png
│   │   ├── card-4.png
│   │   ├── evangelho-2026-11-29.pdf
│   │   ├── ficha.json
│   │   └── recorte.png
│   ├── 2026-12-13/
│   │   ├── card-1.png
│   │   ├── card-2.png
│   │   ├── card-3.png
│   │   ├── card-4.png
│   │   ├── evangelho-2026-12-13.pdf
│   │   ├── ficha.json
│   │   └── recorte.png
│   ├── CONFERENCIA-KIT-V3.md
│   ├── RELATORIO.md
│   ├── conferencia-kit-v3.json
│   ├── prancha-cores.png
│   ├── prancha.png
│   └── verificacao.json
├── html/
│   ├── assinaturas.html
│   ├── nichos.html
│   ├── obra-provisoria.html
│   ├── pagina-1.html
│   ├── pagina-2.html
│   ├── pagina-3.html
│   └── selos.html
├── para-rezar/
│   ├── 2026-10-20/
│   │   ├── card-1.png
│   │   ├── ficha.json
│   │   └── para-rezar-2026-10-20.pdf
│   ├── 2026-12-15/
│   │   ├── card-1.png
│   │   ├── card-2.png
│   │   ├── ficha.json
│   │   └── para-rezar-2026-12-15.pdf
│   ├── RELATORIO.md
│   ├── prancha.png
│   └── verificacao.json
├── previas/
│   ├── assinaturas.png
│   ├── nichos.png
│   └── selos.png
├── santo-do-dia/
│   ├── 2026-11-30/
│   │   ├── card.png
│   │   ├── ficha.json
│   │   ├── recorte.png
│   │   └── santo-2026-11-30.pdf
│   ├── 2026-12-03/
│   │   ├── card.png
│   │   ├── ficha.json
│   │   ├── recorte.png
│   │   └── santo-2026-12-03.pdf
│   ├── 2026-12-08/
│   │   ├── card.png
│   │   ├── ficha.json
│   │   ├── recorte.png
│   │   └── santo-2026-12-08.pdf
│   ├── RELATORIO.md
│   ├── prancha.png
│   └── verificacao.json
├── verificacao/
│   ├── logos/
│   │   ├── avatar-perfil-convertido.png
│   │   ├── avatar-perfil-original.png
│   │   ├── avatar-perfil.svg
│   │   ├── comparacao.html
│   │   ├── logo-horizontal-capela-convertido.png
│   │   ├── logo-horizontal-capela-original.png
│   │   ├── logo-horizontal-capela.svg
│   │   ├── logo-horizontal-pergaminho-convertido.png
│   │   ├── logo-horizontal-pergaminho-original.png
│   │   ├── logo-horizontal-pergaminho.svg
│   │   ├── logo-horizontal-sobre-cor-convertido.png
│   │   ├── logo-horizontal-sobre-cor-original.png
│   │   ├── logo-horizontal-sobre-cor.svg
│   │   ├── logo-vertical-capela-convertido.png
│   │   ├── logo-vertical-capela-original.png
│   │   ├── logo-vertical-capela.svg
│   │   ├── logo-vertical-pergaminho-convertido.png
│   │   ├── logo-vertical-pergaminho-original.png
│   │   ├── logo-vertical-pergaminho.svg
│   │   ├── simbolo-capela-convertido.png
│   │   ├── simbolo-capela-original.png
│   │   ├── simbolo-capela.svg
│   │   ├── simbolo-pergaminho-convertido.png
│   │   ├── simbolo-pergaminho-original.png
│   │   ├── simbolo-pergaminho.svg
│   │   ├── simbolo-reduzido-capela-convertido.png
│   │   ├── simbolo-reduzido-capela-original.png
│   │   ├── simbolo-reduzido-capela.svg
│   │   ├── simbolo-reduzido-pergaminho-convertido.png
│   │   ├── simbolo-reduzido-pergaminho-original.png
│   │   └── simbolo-reduzido-pergaminho.svg
│   └── resultados.json
├── RELATORIO.md
├── obra-provisoria.png
└── tokens.css
```

## Decisões de composição

- O gap entre cruz e texto do selo é espaco-2, 16 px, conforme bundle.css; a menção a espaco-1 no texto do token não altera o CSS.
- Os nomes antigos fonts/*.woff2 do JSON são mapeados pelo basename para os seis TTF de kit/fontes. As seis variantes precisam carregar e passar em document.fonts.check antes de cada PNG e PDF; uma fonte substituta causa erro.
- As assinaturas usam a altura final de 52 px solicitada, embora a vitrine do kit mostre 72 px. A curta usa 40 px e gap de 16 px; a assinatura horizontal com @ mantém 32 px.
- O cartão inteiro na cor do dia usa o tema pergaminho, que contém os tons profundos; cruz, textos e o novo logo-horizontal-sobre-cor.svg usam sobre-cor (#faf6ee), conforme o kit v2.
- Os elementos de lançamento usam roxo por tema. O santinho mantém papel e ouro. Uma variante verde separada reproduz a capa do Evangelho solicitada no teste de importação.
- A imagem provisória vem apenas do degradê aqr-obra--luz rasterizado em 1080 × 1350. Dentro dos nichos só há imagens, sem degradês CSS.
- Na página Canva, a imagem continua retangular, nos limites internos de 648 × 744 px e offset de 16 px, para preservar o mesmo enquadramento da capa CSS. A máscara SVG fica em x − 48, com 776 × 763 px; nenhum clip CSS é usado nessa versão.
- Os SVGs de nicho têm duas cores, máscara e filete/parapeito. O arco externo tem raio W/2; o interno tem raio (W−32)/2 e centro coincidente. A máscara pode ser usada sobre uma imagem retangular.
- Os viewBoxes dos logos são recortados para os limites reais do desenho, como solicitado. Os originais têm pequenas sobras e um corte de borda. Para comparar apenas a conversão de traço em preenchimento, o original é renderizado nos mesmos limites de desenho e no mesmo tamanho do convertido. O kit original não é alterado; os originais normalizados de comparação ficam em verificacao/logos/.
- As prévias são pranchas de inspeção, com rótulos de 14 px fora das peças: selos 2160 × 1600, nichos 2160 × 3360 e assinaturas 2160 × 1320. As três páginas de prova permanecem em 1080 × 1350.
- O Chromium arredonda a altura física do PDF em cerca de 0,54 pt. Na junção das páginas, a origem do conteúdo é compensada e MediaBox/CropBox são fixados em 810 × 1012,5 pt; o texto e as fontes permanecem vetoriais.

## Área de proteção

A travessa mede 26 unidades no símbolo, com escala 1.0517: 27.3442 unidades no SVG horizontal. No logo original com caixa de 52 px de altura, a proteção é **12.7023 px** em cada lado. No SVG para Canva com viewBox justo e 52 px, é **13.0000 px**, ou aproximadamente **13 px**.

## Validação

- Kit v4 final: 44 arquivos e 11 ativos de logo conferidos contra o ZIP do commit; o LEIA-ME cita o Nicho e não há mudança na fonte da verdade.
- 19 SVGs com tamanho menor que 3 MB e contagens zeradas para stroke, text, style, class, transform, degradês, Q e T.
- PNGs conferidos contra as dimensões declaradas em verificacao/resultados.json, incluindo as pranchas, páginas e comparações de logos.
- PDF com três páginas de 810 × 1012,5 pt, equivalentes a 1080 × 1350 px a 96 dpi. O selo e o título ou a pergunta de cada página continuam como texto extraível.
- Fontes TrueType embutidas conferidas no próprio PDF: CormorantGaramond-SemiBold, CormorantGaramond-MediumItalic, Lato-Bold e Lato-Regular. As outras duas variantes estão nos TTF fornecidos e são verificadas no navegador, sem exigir que apareçam em páginas que não as usam.
- Seis nichos conferidos por pixels no canto, topo, lateral, parapeito e três pontos do arco; tolerância de 3 níveis RGB para antialiasing.
- 10 logos SVG comparados em dois fundos; maior diferença média por canal: 0.237187/255, concentrada na rasterização das bordas. As imagens original/convertido e as métricas estão em verificacao/.
- Navegador sem erros de console, execução ou HTTP durante a geração. A FICHA contém os valores de posição e tipografia medidos no DOM; os pseudoelementos são derivados dos estilos resolvidos e da caixa medida do nicho.

## Limites e verificações externas

- A importação real no Canva e a capacidade de editar cada objeto no editor não foram verificadas nesta sessão. O PDF, os SVGs e os TTF estão preparados para esse teste, com as verificações locais descritas acima.
- A obra é provisória e não representa uma pintura sacra final.
- A integração Documents e o modelo remoto Design Report não estão disponíveis nas ferramentas desta sessão. Este relatório é o documento local entregue; não foi criado um documento nesse serviço nem aplicado o modelo remoto.
