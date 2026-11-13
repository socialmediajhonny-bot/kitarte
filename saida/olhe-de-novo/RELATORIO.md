# Olhe de Novo

`python3 gerar.py olhe-de-novo`

## Conteúdo e composição

- Os textos foram escritos pela página e aprovados em 12/11/2026. O YAML preserva pontuação, aspas, acentos e quebras manuais; nenhum texto é gerado automaticamente.
- Feed de 1080 × 1350. Os modelos existem apenas no gerador, sem prévia equivalente no kit v4. Nenhum módulo compartilhado ou arquivo do kit é modificado.
- O helper igreja_text_html é importado intacto: protege palavras de uma letra, referências bíblicas inteiras, ordinais ligados à palavra seguinte e palavras com hífen. As quebras do YAML são mantidas.
- O gap de 16 px do aqr-texto recebe margens inline em tokens: 48 px entre rótulo e texto e em volta do ornamento; 32 px entre texto e fonte/referência e entre nicho e crédito. Cada par é medido no navegador com tolerância de ±0,01 px.
- Os cards com obra no alto seguem o selo e deixam pelo menos 32 px entre o último texto e a assinatura. Os demais centralizam o bloco entre selo e assinatura, com pelo menos 60 px de cada lado e diferença de centralização até 0,1 px.
- A cruz e o filete recebem a cor do dia; o ornamento usa ouro. Nos cartões inteiros na cor do dia, fundo na cor litúrgica e textos, cruz, ornamento e logo em sobre-cor.
- A assinatura usa a variante do tema, ou sobre-cor no cartão inteiro na cor. Cores, fontes, caixas, limites de linhas e trechos protegidos são validados no DOM e por pixels.
- Cada nicho recebe um JPEG já recortado na janela visível, qualidade 95 e sem subamostragem de cor, usando LANCZOS e Image.resize com box fracionária. O card e o PDF usam esse arquivo com foco 50% 50% e zoom 1. Isso evita a ampliação que borrou a obra de 25/12 na importação do Canva.
- O recorte mantém a dimensão nativa, limitado a 2× a área interna do nicho, sem ampliar o arquivo. As janelas explícitas exigem dimensão original exata, contenção completa e ampliação de até 1,2. Nenhuma obra original é alterada ou baixada.
- Cada obra recebe uma prova da imagem inteira a 1080 px com o contorno da janela do arco. Margens fotográficas visíveis geram aviso e nunca alteram o YAML.
- PostOlheDeNovo: quatro cards no tema capela, com contagem 1/4 a 4/4 em todos eles. Os dois primeiros têm nichos 640 × 840, crédito em uma linha e título em uma linha; o card 3 apresenta o significado e o card 4 mostra uma ou duas obras.
- No card 4, cada figura tem 380 px e o intervalo entre figuras é 56 px. Os nichos medem 340 × 420; com duas obras, ficam a 96 px um do outro e os parapeitos de 48 px se encostam sem sobrepor. Os créditos usam até duas linhas e text-wrap:balance.
- Os SVGs de nicho para o Canva ficam somente em elementos/ desta série, com fundo e filete do tema capela em liturgico-roxo; saida/canva/ permanece intacta.

## Tabela medida no navegador

| Data | Card | Tipo | Linhas medidas | Distâncias e folgas medidas | Previsto |
| --- | --- | --- | --- | --- | --- |
| 2026-12-09 | 1 | obra | credito: 1; titulo: 1 | selo_nicho_px: 32 px; nicho_credito_px: 32 px; credito_titulo_px: 48 px; titulo_assinatura_px: 38 px | credito: 1 linhas; titulo: 1 linhas; selo_nicho_px: 32 px; titulo_assinatura_px: 38 px |
| 2026-12-09 | 2 | detalhe | credito: 1; titulo: 1 | selo_nicho_px: 32 px; nicho_credito_px: 32 px; credito_titulo_px: 48 px; titulo_assinatura_px: 38 px | credito: 1 linhas; titulo: 1 linhas; selo_nicho_px: 32 px; titulo_assinatura_px: 38 px |
| 2026-12-09 | 3 | significado | rotulo: 1; titulo: 1; texto: 5; fonte: 1 | selo_texto_px: 251.5 px; texto_assinatura_px: 251.5 px; diferenca_centralizacao_px: 0 px; rotulo_titulo_px: 48 px; titulo_ornamento_px: 48 px; ornamento_texto_px: 48 px; texto_fonte_px: 32 px | rotulo: 1 linhas; titulo: 1 linhas; texto: 5 linhas; fonte: 1 linhas; folga_px: 251.5 px |
| 2026-12-09 | 4 | onde | rotulo: 1; credito_1: 2; credito_2: 2; texto: 3; fonte: 1 | selo_texto_px: 116 px; texto_assinatura_px: 116 px; diferenca_centralizacao_px: 0 px; rotulo_linha_nichos_px: 48 px; linha_nichos_texto_px: 48 px; texto_fonte_px: 32 px; nicho_1_credito_1_px: 32 px; nicho_2_credito_2_px: 32 px; distancia_entre_nichos_px: 96 px | rotulo: 1 linhas; credito_1: 2 linhas; credito_2: 2 linhas; texto: 3 linhas; fonte: 1 linhas; folga_px: 116 px |

## Diferenças da tabela prevista

Nenhuma diferença.

## Obras, janelas e recortes

### 2026-12-09 · card-1

Carlo Crivelli · A Anunciação, com Santo Emídio · National Gallery, Londres — https://nationalgallery.org.uk/paintings/NG739

Original local: `obras/olhe-de-novo/2026-12-09.jpg`. Foco `50% 70%`, zoom `1`.

Janela original x=0.000000, y=115.942105, largura=2996.000000, altura=4060.368421 px; ampliação=0.202937.
Arquivo recortado: `saida/olhe-de-novo/2026-12-09/obra-1.jpg`. Prova: `saida/olhe-de-novo/2026-12-09/recorte-1.png`.
Dimensão do JPEG recortado: 1216 × 1648 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 0, "esquerda": 0, "direita": 0}, "faixas_descartadas": [], "margens_visiveis": []}`.

Card 1 e recorte-1.png finais conferidos individualmente. Gabriel, Maria e o lírio ficam preservados dentro do arco na extensão em que já aparecem na pintura: os rostos, as mãos, as vestes e as flores permanecem legíveis. A asa à esquerda já encontra a borda do arquivo original; isso não é um corte novo introduzido pelo arco. A curva recorta a arquitetura e o céu na parte superior, sem atingir esses protagonistas. Nenhuma margem fotográfica foi vista.
### 2026-12-09 · card-2

Carlo Crivelli · A Anunciação, com Santo Emídio · National Gallery, Londres — https://nationalgallery.org.uk/paintings/NG739

Original local: `obras/olhe-de-novo/2026-12-09.jpg`. Janela aprovada `[396, 2440, 608]`, tamanho original `[2996, 4226]`.

Janela original x=396.000000, y=2440.000000, largura=608.000000, altura=824.000000 px; ampliação=1.000000.
Arquivo recortado: `saida/olhe-de-novo/2026-12-09/obra-2.jpg`. Prova: `saida/olhe-de-novo/2026-12-09/recorte-2.png`.
Dimensão do JPEG recortado: 608 × 824 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 0, "esquerda": 0, "direita": 0}, "faixas_descartadas": [], "margens_visiveis": []}`.

Card 2 e recorte-2.png finais conferidos individualmente. O rosto de Gabriel, a auréola dourada e o lírio estão dentro do arco, das flores até a mão que segura a haste. As laterais cortam asas e outros elementos periféricos, mas o conjunto de rosto, auréola, flores e mão pedido para este detalhe fica preservado. Nenhuma margem fotográfica foi vista.
### 2026-12-09 · card-4-1

Jan van Eyck · A Anunciação
National Gallery of Art — https://www.nga.gov/artworks/46-annunciation

Original local: `obras/stories/angelus.jpg`. Janela aprovada `[830, 2085, 307]`, tamanho original `[1137, 3000]`.

Janela original x=830.000000, y=2085.000000, largura=307.000000, altura=403.000000 px; ampliação=1.003257.
Arquivo recortado: `saida/olhe-de-novo/2026-12-09/obra-4-1.jpg`. Prova: `saida/olhe-de-novo/2026-12-09/recorte-4-1.png`.
Dimensão do JPEG recortado: 307 × 403 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 0, "esquerda": 0, "direita": 0}, "faixas_descartadas": [], "margens_visiveis": []}`.

O nicho esquerdo do card 4, o JPEG obra-4-1.jpg e recorte-4-1.png finais foram conferidos. As flores centrais do lírio ficam legíveis, mas a flor mais alta à direita entra parcialmente na janela retangular aprovada e perde mais pétalas pela curva do arco; portanto o conjunto das flores não está integralmente preservado. Algumas extremidades à direita já encontram a borda do arquivo original e não podem ser recuperadas com outra janela. Nenhuma margem fotográfica foi vista. O YAML aprovado foi mantido.

Sugestão somente para avaliação, sem alterar o YAML: {"janela": [717, 1830, 420], "tamanho": [1137, 3000], "altura_calculada_px": 551, "ampliacao": 0.7333333333333333, "tamanho_recortado_px": [420, 551], "nota": "Alternativa renderizada e inspecionada no card 4 e no JPEG temporários: inclui a flor alta e preserva todas as flores na extensão disponível no arquivo original, posicionando-as abaixo da curva. O livro e mais tecido azul passam a aparecer, e as flores ficam menores; as pontas já limitadas pela borda original não são recuperadas. A janela cabe integralmente no arquivo, tem ampliação 0,733333 e margens_visiveis vazias. Sugestão somente no relatório; nenhum foco ou janela do YAML foi alterado."}
### 2026-12-09 · card-4-2

El Greco · Santo Antônio de Pádua
Museu do Prado — https://commons.wikimedia.org/wiki/File:San_Antonio_de_Padua_(El_Greco).jpg

Original local: `obras/olhe-de-novo/2026-12-09-santo-antonio.jpg`. Janela aprovada `[200, 120, 1446]`, tamanho original `[2270, 3051]`.

Janela original x=200.000000, y=120.000000, largura=1446.000000, altura=1897.000000 px; ampliação=0.213001.
Arquivo recortado: `saida/olhe-de-novo/2026-12-09/obra-4-2.jpg`. Prova: `saida/olhe-de-novo/2026-12-09/recorte-4-2.png`.
Dimensão do JPEG recortado: 616 × 808 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 0, "esquerda": 0, "direita": 0}, "faixas_descartadas": [], "margens_visiveis": []}`.

O nicho direito do card 4, o JPEG obra-4-2.jpg e recorte-4-2.png finais foram conferidos. O rosto de Santo Antônio, as flores do lírio e a mão que segura a haste ficam dentro do arco. O corte termina junto ao punho e exclui a parte inferior do corpo e o livro, conforme a proposta de detalhe; os dedos e o rosto permanecem preservados. Nenhuma margem fotográfica foi vista.

## Avisos e pendências

Nenhum aviso geométrico ou de composição. Ressalva visual: no card 4, a flor mais alta à direita do lírio do van Eyck fica parcial. A janela alternativa `[717, 1830, 420]` foi conferida e está detalhada nas notas da obra; o YAML aprovado não foi alterado.

## PDF e conferências

Um PDF por data, com todos os cards na ordem do YAML e páginas de 810 × 1012,5 pt. PyMuPDF, pdffonts e pdftotext verificam fontes TTF embutidas e texto integral igual ao YAML. Cada nicho tem o filete em U e o parapeito vetoriais conferidos, inclusive os dois nichos do card 4 do Olhe de Novo.
As fichas registram caixas de cada linha de texto, tema, cores, conteúdos aprovados, janela original, ampliação e arquivo recortado de cada obra. Os renders usam somente recursos e seis fontes locais.

## O que conferir no Canva

- Cada texto na sua caixa: selo, data, contagem ou info, rótulo, título ou pergunta, crédito, texto, fonte, versículo, referência, frase e convite.
- A obra dentro do arco, sem borrão, usando o arquivo já recortado.
- O filete, o parapeito e o ornamento como formas.
- No card 4 de 9/12, os dois nichos lado a lado, com os parapeitos encostados.
- Nenhuma caixa solta, nem contendo só um espaço; conferir que dois textos não foram fundidos.

A importação destes PDFs no editor do Canva permanece uma conferência manual.
A evidência da geração está em [verificacao.json](verificacao.json).

## Árvore

```text
saida/olhe-de-novo/
  2026-12-09/card-1.png
  2026-12-09/card-2.png
  2026-12-09/card-3.png
  2026-12-09/card-4.png
  2026-12-09/ficha.json
  2026-12-09/obra-1.jpg
  2026-12-09/obra-2.jpg
  2026-12-09/obra-4-1.jpg
  2026-12-09/obra-4-2.jpg
  2026-12-09/olhe-de-novo-2026-12-09.pdf
  2026-12-09/recorte-1.png
  2026-12-09/recorte-2.png
  2026-12-09/recorte-4-1.png
  2026-12-09/recorte-4-2.png
  NOTAS-DAS-OBRAS.json
  RELATORIO.md
  elementos/nicho-340x420-olhe-de-novo.svg
  elementos/nicho-640x840-olhe-de-novo.svg
  prancha.png
  verificacao.json
```

<!-- inicio-prova-prompt15 -->
## Prova de preservação do prompt 15

BASE: `109d8c8f6fbb69ab6cae37ce8459658e3f863379`. Nenhum download foi feito nesta execução. As cinco imagens locais têm os tamanhos exigidos; as quatro novas não têm margens fotográficas ou faixas uniformes descartadas.

**Controle inicial:** os oito comandos foram executados na BASE limpa, com `git status` vazio antes de cada um. Cada arquivo modificado foi comparado: PNG por pixel, páginas PDF a 2× por PyMuPDF e JSON/Markdown normalizando apenas a porta local. **Prova após as alterações:** os sete comandos das outras séries foram executados novamente, antes da geração das novas pastas. Nenhum PNG, PDF ou ficha mudou além da porta local prevista. Todos os seus arquivos foram restaurados à BASE.

**Exceções de relatórios, autorizadas pelo usuário:**

| Relatório restaurado e excluído do commit | Evidência |
| --- | --- |
| `saida/RELATORIO.md` | Mesma desatualização e árvore regenerada nas duas execuções, com texto idêntico salvo a porta local. |
| `saida/evangelho/RELATORIO.md` | A regeneração remove o apêndice manual do prompt 14 igualmente na BASE limpa; nenhum PNG/PDF/ficha é alterado além da porta. |
| `saida/santo-do-dia/RELATORIO.md` | Mesma remoção das 72 linhas do apêndice do prompt 13, de 427 para 355 linhas. |

Para cada relatório, o texto gerado com o código novo foi comparado ao texto gerado no controle da BASE limpa; as diferenças são iguais. Os três arquivos foram restaurados byte a byte e ficam fora do commit. Não foi aplicada exceção a outra diferença. Nenhum auxiliar em `work/` integra a entrega.

**Igreja Doméstica:** as duas datas anteriores foram comparadas e restauradas byte a byte, incluindo cards, PDFs, recortes e fichas. As notas dessas datas e os arquivos `CONFERENCIA-PROMPT-10.md` e `conferencia-prompt10.json` foram preservados. Só a data 13/12 e os quatro arquivos gerais autorizados mudam.

**Testes:** 240 testes passaram (105,707 s): 201 anteriores e 39 novos. `test_conteudo_noite.py` acrescenta 17 testes dos leitores estritos, janelas e referências; `test_layout_noite.py` acrescenta 22 testes de layout, cores, PDF, próximos títulos, uma obra e recortes. Na Igreja, apenas os dois testes autorizados foram ajustados para três datas, 12 cards e a cor do dia. O teste de `--data` também demonstrou preservação byte a byte de PNG, PDF e ficha de outra data.

**Escopo:** os módulos compartilhados, o kit, o ZIP e as obras originais permanecem intactos. O uso dos helpers existentes foi conferido pelas importações abaixo; na Igreja, as alterações ficaram limitadas à previsão de 13/12 e à aprovação por data e relatório.

```text
arteque_reza/conteudo_noite.py:8:import yaml
arteque_reza/conteudo_noite.py:10:from .conteudo import (
arteque_reza/conteudo_noite.py:14:from .igreja_domestica import BOOKS
arteque_reza/noite.py:7:import re
arteque_reza/noite.py:8:import shutil
arteque_reza/noite.py:9:import subprocess
arteque_reza/noite.py:14:from .base import PROJECT, assinatura, color, html_document, montar_arte, nicho, selo
arteque_reza/noite.py:15:from .conteudo import color_token, date_label
arteque_reza/noite.py:16:from .evangelho import _measure as measure_evangelho, _ornament, _text
arteque_reza/noite.py:17:from .igreja_domestica import BOOK_PATTERN, igreja_text_html
arteque_reza/noite.py:18:from .obras import artwork_geometry, crop_proof, inspect_artwork, uniform_margins
arteque_reza/noite.py:19:from .pdf_nicho import niches_from_elements, validate_niche_pdf
arteque_reza/noite.py:20:from .validacao import validate_niche_pixels
arteque_reza/serie_noite.py:9:import json
arteque_reza/serie_noite.py:11:import shutil
arteque_reza/serie_noite.py:18:from .base import PROJECT, KIT, color, generate_tokens_css, render_arte
arteque_reza/serie_noite.py:19:from .canva import niche_svg, validate_svg
arteque_reza/serie_noite.py:20:from .conteudo_noite import LOADERS
arteque_reza/serie_noite.py:21:from .noite import (_document, _measure, _pdf_check, _pixels, _validate_layout,
arteque_reza/serie_noite.py:23:from .renderizacao import local_server
arteque_reza/serie_noite.py:24:from .validacao import validate_kit, validate_pngs
```

### Prova por arquivo PNG e PDF anterior

Todos os arquivos abaixo estão idênticos byte a byte à BASE. Cada PNG e cada página no mesmo rasterizador têm zero pixel diferente, caixa de diferença vazia e maior diferença por canal zero. Nenhum PDF foi modificado em bytes; a escala da comparação exigida é 2×.

| Arquivo | Pixels diferentes por imagem/página |
| --- | --- |
| `saida/canva/elementos/logos/avatar-perfil.png` | 0 |
| `saida/canva/pagina-1.png` | 0 |
| `saida/canva/pagina-2.png` | 0 |
| `saida/canva/pagina-3.png` | 0 |
| `saida/canva/teste-importacao.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/coragem/2026-12-14/coragem-2026-12-14-feed.pdf` | p1: 0 |
| `saida/coragem/2026-12-14/coragem-2026-12-14-status.pdf` | p1: 0 |
| `saida/coragem/2026-12-14/feed.png` | 0 |
| `saida/coragem/2026-12-14/recorte-feed.png` | 0 |
| `saida/coragem/2026-12-14/recorte-status.png` | 0 |
| `saida/coragem/2026-12-14/status.png` | 0 |
| `saida/coragem/2026-12-28/coragem-2026-12-28-feed.pdf` | p1: 0 |
| `saida/coragem/2026-12-28/coragem-2026-12-28-status.pdf` | p1: 0 |
| `saida/coragem/2026-12-28/feed.png` | 0 |
| `saida/coragem/2026-12-28/recorte-feed.png` | 0 |
| `saida/coragem/2026-12-28/recorte-status.png` | 0 |
| `saida/coragem/2026-12-28/status.png` | 0 |
| `saida/coragem/prancha.png` | 0 |
| `saida/evangelho/2026-11-29/card-1.png` | 0 |
| `saida/evangelho/2026-11-29/card-2.png` | 0 |
| `saida/evangelho/2026-11-29/card-3.png` | 0 |
| `saida/evangelho/2026-11-29/card-4.png` | 0 |
| `saida/evangelho/2026-11-29/evangelho-2026-11-29.pdf` | p1: 0, p2: 0, p3: 0, p4: 0 |
| `saida/evangelho/2026-11-29/recorte.png` | 0 |
| `saida/evangelho/2026-11-30/card-1.png` | 0 |
| `saida/evangelho/2026-11-30/card-2.png` | 0 |
| `saida/evangelho/2026-11-30/card-3.png` | 0 |
| `saida/evangelho/2026-11-30/evangelho-2026-11-30.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-11-30/recorte.png` | 0 |
| `saida/evangelho/2026-12-01/card-1.png` | 0 |
| `saida/evangelho/2026-12-01/card-2.png` | 0 |
| `saida/evangelho/2026-12-01/card-3.png` | 0 |
| `saida/evangelho/2026-12-01/evangelho-2026-12-01.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-01/recorte.png` | 0 |
| `saida/evangelho/2026-12-02/card-1.png` | 0 |
| `saida/evangelho/2026-12-02/card-2.png` | 0 |
| `saida/evangelho/2026-12-02/card-3.png` | 0 |
| `saida/evangelho/2026-12-02/evangelho-2026-12-02.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-02/recorte.png` | 0 |
| `saida/evangelho/2026-12-03/card-1.png` | 0 |
| `saida/evangelho/2026-12-03/card-2.png` | 0 |
| `saida/evangelho/2026-12-03/card-3.png` | 0 |
| `saida/evangelho/2026-12-03/evangelho-2026-12-03.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-03/recorte.png` | 0 |
| `saida/evangelho/2026-12-04/card-1.png` | 0 |
| `saida/evangelho/2026-12-04/card-2.png` | 0 |
| `saida/evangelho/2026-12-04/card-3.png` | 0 |
| `saida/evangelho/2026-12-04/evangelho-2026-12-04.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-04/recorte.png` | 0 |
| `saida/evangelho/2026-12-05/card-1.png` | 0 |
| `saida/evangelho/2026-12-05/card-2.png` | 0 |
| `saida/evangelho/2026-12-05/card-3.png` | 0 |
| `saida/evangelho/2026-12-05/evangelho-2026-12-05.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-05/recorte.png` | 0 |
| `saida/evangelho/2026-12-06/card-1.png` | 0 |
| `saida/evangelho/2026-12-06/card-2.png` | 0 |
| `saida/evangelho/2026-12-06/card-3.png` | 0 |
| `saida/evangelho/2026-12-06/card-4.png` | 0 |
| `saida/evangelho/2026-12-06/evangelho-2026-12-06.pdf` | p1: 0, p2: 0, p3: 0, p4: 0 |
| `saida/evangelho/2026-12-06/recorte.png` | 0 |
| `saida/evangelho/2026-12-07/card-1.png` | 0 |
| `saida/evangelho/2026-12-07/card-2.png` | 0 |
| `saida/evangelho/2026-12-07/card-3.png` | 0 |
| `saida/evangelho/2026-12-07/evangelho-2026-12-07.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-07/recorte.png` | 0 |
| `saida/evangelho/2026-12-08/card-1.png` | 0 |
| `saida/evangelho/2026-12-08/card-2.png` | 0 |
| `saida/evangelho/2026-12-08/card-3.png` | 0 |
| `saida/evangelho/2026-12-08/evangelho-2026-12-08.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-08/recorte.png` | 0 |
| `saida/evangelho/2026-12-09/card-1.png` | 0 |
| `saida/evangelho/2026-12-09/card-2.png` | 0 |
| `saida/evangelho/2026-12-09/card-3.png` | 0 |
| `saida/evangelho/2026-12-09/evangelho-2026-12-09.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-09/recorte.png` | 0 |
| `saida/evangelho/2026-12-10/card-1.png` | 0 |
| `saida/evangelho/2026-12-10/card-2.png` | 0 |
| `saida/evangelho/2026-12-10/card-3.png` | 0 |
| `saida/evangelho/2026-12-10/evangelho-2026-12-10.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-10/recorte.png` | 0 |
| `saida/evangelho/2026-12-11/card-1.png` | 0 |
| `saida/evangelho/2026-12-11/card-2.png` | 0 |
| `saida/evangelho/2026-12-11/card-3.png` | 0 |
| `saida/evangelho/2026-12-11/evangelho-2026-12-11.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-11/recorte.png` | 0 |
| `saida/evangelho/2026-12-12/card-1.png` | 0 |
| `saida/evangelho/2026-12-12/card-2.png` | 0 |
| `saida/evangelho/2026-12-12/card-3.png` | 0 |
| `saida/evangelho/2026-12-12/evangelho-2026-12-12.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-12/recorte.png` | 0 |
| `saida/evangelho/2026-12-13/card-1.png` | 0 |
| `saida/evangelho/2026-12-13/card-2.png` | 0 |
| `saida/evangelho/2026-12-13/card-3.png` | 0 |
| `saida/evangelho/2026-12-13/card-4.png` | 0 |
| `saida/evangelho/2026-12-13/evangelho-2026-12-13.pdf` | p1: 0, p2: 0, p3: 0, p4: 0 |
| `saida/evangelho/2026-12-13/recorte.png` | 0 |
| `saida/evangelho/2026-12-14/card-1.png` | 0 |
| `saida/evangelho/2026-12-14/card-2.png` | 0 |
| `saida/evangelho/2026-12-14/card-3.png` | 0 |
| `saida/evangelho/2026-12-14/evangelho-2026-12-14.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-14/recorte.png` | 0 |
| `saida/evangelho/2026-12-15/card-1.png` | 0 |
| `saida/evangelho/2026-12-15/card-2.png` | 0 |
| `saida/evangelho/2026-12-15/card-3.png` | 0 |
| `saida/evangelho/2026-12-15/evangelho-2026-12-15.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-15/recorte.png` | 0 |
| `saida/evangelho/2026-12-16/card-1.png` | 0 |
| `saida/evangelho/2026-12-16/card-2.png` | 0 |
| `saida/evangelho/2026-12-16/card-3.png` | 0 |
| `saida/evangelho/2026-12-16/evangelho-2026-12-16.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-16/recorte.png` | 0 |
| `saida/evangelho/2026-12-17/card-1.png` | 0 |
| `saida/evangelho/2026-12-17/card-2.png` | 0 |
| `saida/evangelho/2026-12-17/card-3.png` | 0 |
| `saida/evangelho/2026-12-17/evangelho-2026-12-17.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-17/recorte.png` | 0 |
| `saida/evangelho/2026-12-18/card-1.png` | 0 |
| `saida/evangelho/2026-12-18/card-2.png` | 0 |
| `saida/evangelho/2026-12-18/card-3.png` | 0 |
| `saida/evangelho/2026-12-18/evangelho-2026-12-18.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-18/recorte.png` | 0 |
| `saida/evangelho/2026-12-19/card-1.png` | 0 |
| `saida/evangelho/2026-12-19/card-2.png` | 0 |
| `saida/evangelho/2026-12-19/card-3.png` | 0 |
| `saida/evangelho/2026-12-19/evangelho-2026-12-19.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-19/recorte.png` | 0 |
| `saida/evangelho/2026-12-20/card-1.png` | 0 |
| `saida/evangelho/2026-12-20/card-2.png` | 0 |
| `saida/evangelho/2026-12-20/card-3.png` | 0 |
| `saida/evangelho/2026-12-20/card-4.png` | 0 |
| `saida/evangelho/2026-12-20/evangelho-2026-12-20.pdf` | p1: 0, p2: 0, p3: 0, p4: 0 |
| `saida/evangelho/2026-12-20/recorte.png` | 0 |
| `saida/evangelho/2026-12-21/card-1.png` | 0 |
| `saida/evangelho/2026-12-21/card-2.png` | 0 |
| `saida/evangelho/2026-12-21/card-3.png` | 0 |
| `saida/evangelho/2026-12-21/evangelho-2026-12-21.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-21/recorte.png` | 0 |
| `saida/evangelho/2026-12-22/card-1.png` | 0 |
| `saida/evangelho/2026-12-22/card-2.png` | 0 |
| `saida/evangelho/2026-12-22/card-3.png` | 0 |
| `saida/evangelho/2026-12-22/evangelho-2026-12-22.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-22/recorte.png` | 0 |
| `saida/evangelho/2026-12-23/card-1.png` | 0 |
| `saida/evangelho/2026-12-23/card-2.png` | 0 |
| `saida/evangelho/2026-12-23/card-3.png` | 0 |
| `saida/evangelho/2026-12-23/evangelho-2026-12-23.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-23/recorte.png` | 0 |
| `saida/evangelho/2026-12-24/card-1.png` | 0 |
| `saida/evangelho/2026-12-24/card-2.png` | 0 |
| `saida/evangelho/2026-12-24/card-3.png` | 0 |
| `saida/evangelho/2026-12-24/evangelho-2026-12-24.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-24/recorte.png` | 0 |
| `saida/evangelho/2026-12-25/card-1.png` | 0 |
| `saida/evangelho/2026-12-25/card-2.png` | 0 |
| `saida/evangelho/2026-12-25/card-3.png` | 0 |
| `saida/evangelho/2026-12-25/evangelho-2026-12-25.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-25/recorte.png` | 0 |
| `saida/evangelho/2026-12-26/card-1.png` | 0 |
| `saida/evangelho/2026-12-26/card-2.png` | 0 |
| `saida/evangelho/2026-12-26/card-3.png` | 0 |
| `saida/evangelho/2026-12-26/evangelho-2026-12-26.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-26/recorte.png` | 0 |
| `saida/evangelho/2026-12-27/card-1.png` | 0 |
| `saida/evangelho/2026-12-27/card-2.png` | 0 |
| `saida/evangelho/2026-12-27/card-3.png` | 0 |
| `saida/evangelho/2026-12-27/card-4.png` | 0 |
| `saida/evangelho/2026-12-27/evangelho-2026-12-27.pdf` | p1: 0, p2: 0, p3: 0, p4: 0 |
| `saida/evangelho/2026-12-27/recorte.png` | 0 |
| `saida/evangelho/2026-12-28/card-1.png` | 0 |
| `saida/evangelho/2026-12-28/card-2.png` | 0 |
| `saida/evangelho/2026-12-28/card-3.png` | 0 |
| `saida/evangelho/2026-12-28/evangelho-2026-12-28.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-28/recorte.png` | 0 |
| `saida/evangelho/2026-12-29/card-1.png` | 0 |
| `saida/evangelho/2026-12-29/card-2.png` | 0 |
| `saida/evangelho/2026-12-29/card-3.png` | 0 |
| `saida/evangelho/2026-12-29/evangelho-2026-12-29.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-29/recorte.png` | 0 |
| `saida/evangelho/2026-12-30/card-1.png` | 0 |
| `saida/evangelho/2026-12-30/card-2.png` | 0 |
| `saida/evangelho/2026-12-30/card-3.png` | 0 |
| `saida/evangelho/2026-12-30/evangelho-2026-12-30.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-30/recorte.png` | 0 |
| `saida/evangelho/2026-12-31/card-1.png` | 0 |
| `saida/evangelho/2026-12-31/card-2.png` | 0 |
| `saida/evangelho/2026-12-31/card-3.png` | 0 |
| `saida/evangelho/2026-12-31/evangelho-2026-12-31.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-31/recorte.png` | 0 |
| `saida/evangelho/prancha-cores.png` | 0 |
| `saida/evangelho/prancha.png` | 0 |
| `saida/igreja-domestica/2026-11-29/card-1.png` | 0 |
| `saida/igreja-domestica/2026-11-29/card-2.png` | 0 |
| `saida/igreja-domestica/2026-11-29/card-3.png` | 0 |
| `saida/igreja-domestica/2026-11-29/card-4.png` | 0 |
| `saida/igreja-domestica/2026-11-29/igreja-domestica-2026-11-29.pdf` | p1: 0, p2: 0, p3: 0, p4: 0 |
| `saida/igreja-domestica/2026-11-29/recorte.png` | 0 |
| `saida/igreja-domestica/2026-12-06/card-1.png` | 0 |
| `saida/igreja-domestica/2026-12-06/card-2.png` | 0 |
| `saida/igreja-domestica/2026-12-06/card-3.png` | 0 |
| `saida/igreja-domestica/2026-12-06/igreja-domestica-2026-12-06.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/igreja-domestica/2026-12-06/recorte.png` | 0 |
| `saida/novena/imaculada/dia-1.png` | 0 |
| `saida/novena/imaculada/dia-2.png` | 0 |
| `saida/novena/imaculada/dia-3.png` | 0 |
| `saida/novena/imaculada/dia-4.png` | 0 |
| `saida/novena/imaculada/dia-5.png` | 0 |
| `saida/novena/imaculada/dia-6.png` | 0 |
| `saida/novena/imaculada/dia-7.png` | 0 |
| `saida/novena/imaculada/dia-8.png` | 0 |
| `saida/novena/imaculada/dia-9.png` | 0 |
| `saida/novena/imaculada/encerramento.png` | 0 |
| `saida/novena/imaculada/novena-imaculada.pdf` | p1: 0, p2: 0, p3: 0, p4: 0, p5: 0, p6: 0, p7: 0, p8: 0, p9: 0, p10: 0 |
| `saida/novena/imaculada/prancha.png` | 0 |
| `saida/novena/natal/dia-1.png` | 0 |
| `saida/novena/natal/dia-2.png` | 0 |
| `saida/novena/natal/dia-3.png` | 0 |
| `saida/novena/natal/dia-4.png` | 0 |
| `saida/novena/natal/dia-5.png` | 0 |
| `saida/novena/natal/dia-6.png` | 0 |
| `saida/novena/natal/dia-7.png` | 0 |
| `saida/novena/natal/dia-8.png` | 0 |
| `saida/novena/natal/dia-9.png` | 0 |
| `saida/novena/natal/encerramento.png` | 0 |
| `saida/novena/natal/novena-natal.pdf` | p1: 0, p2: 0, p3: 0, p4: 0, p5: 0, p6: 0, p7: 0, p8: 0, p9: 0, p10: 0 |
| `saida/novena/natal/prancha.png` | 0 |
| `saida/novena/teste-canva/dia-1.png` | 0 |
| `saida/novena/teste-canva/dia-8.png` | 0 |
| `saida/novena/teste-canva/encerramento.png` | 0 |
| `saida/novena/teste-canva/novena-teste-canva.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/novena/teste-canva/prancha.png` | 0 |
| `saida/obra-provisoria.png` | 0 |
| `saida/para-rezar/2026-10-20/card-1.png` | 0 |
| `saida/para-rezar/2026-10-20/para-rezar-2026-10-20.pdf` | p1: 0 |
| `saida/para-rezar/2026-12-15/card-1.png` | 0 |
| `saida/para-rezar/2026-12-15/card-2.png` | 0 |
| `saida/para-rezar/2026-12-15/para-rezar-2026-12-15.pdf` | p1: 0, p2: 0 |
| `saida/para-rezar/prancha.png` | 0 |
| `saida/previas/assinaturas.png` | 0 |
| `saida/previas/nichos.png` | 0 |
| `saida/previas/selos.png` | 0 |
| `saida/santo-do-dia/2026-11-30/card.png` | 0 |
| `saida/santo-do-dia/2026-11-30/recorte.png` | 0 |
| `saida/santo-do-dia/2026-11-30/santo-2026-11-30.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-01/card.png` | 0 |
| `saida/santo-do-dia/2026-12-01/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-01/santo-2026-12-01.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-02/card.png` | 0 |
| `saida/santo-do-dia/2026-12-02/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-02/santo-2026-12-02.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-03/card.png` | 0 |
| `saida/santo-do-dia/2026-12-03/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-03/santo-2026-12-03.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-04/card.png` | 0 |
| `saida/santo-do-dia/2026-12-04/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-04/santo-2026-12-04.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-05/card.png` | 0 |
| `saida/santo-do-dia/2026-12-05/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-05/santo-2026-12-05.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-07/card.png` | 0 |
| `saida/santo-do-dia/2026-12-07/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-07/santo-2026-12-07.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-08/card.png` | 0 |
| `saida/santo-do-dia/2026-12-08/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-08/santo-2026-12-08.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-09/card.png` | 0 |
| `saida/santo-do-dia/2026-12-09/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-09/santo-2026-12-09.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-10/card.png` | 0 |
| `saida/santo-do-dia/2026-12-10/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-10/santo-2026-12-10.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-11/card.png` | 0 |
| `saida/santo-do-dia/2026-12-11/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-11/santo-2026-12-11.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-12/card.png` | 0 |
| `saida/santo-do-dia/2026-12-12/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-12/santo-2026-12-12.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-14/card.png` | 0 |
| `saida/santo-do-dia/2026-12-14/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-14/santo-2026-12-14.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-15/card.png` | 0 |
| `saida/santo-do-dia/2026-12-15/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-15/santo-2026-12-15.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-16/card.png` | 0 |
| `saida/santo-do-dia/2026-12-16/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-16/santo-2026-12-16.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-24/card.png` | 0 |
| `saida/santo-do-dia/2026-12-24/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-24/santo-2026-12-24.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-25/card.png` | 0 |
| `saida/santo-do-dia/2026-12-25/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-25/santo-2026-12-25.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-26/card.png` | 0 |
| `saida/santo-do-dia/2026-12-26/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-26/santo-2026-12-26.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-28/card.png` | 0 |
| `saida/santo-do-dia/2026-12-28/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-28/santo-2026-12-28.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-29/card.png` | 0 |
| `saida/santo-do-dia/2026-12-29/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-29/santo-2026-12-29.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-30/card.png` | 0 |
| `saida/santo-do-dia/2026-12-30/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-30/santo-2026-12-30.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-31/card.png` | 0 |
| `saida/santo-do-dia/2026-12-31/recorte.png` | 0 |
| `saida/santo-do-dia/2026-12-31/santo-2026-12-31.pdf` | p1: 0 |
| `saida/santo-do-dia/prancha.png` | 0 |
| `saida/stories/advento/angelus.png` | 0 |
| `saida/stories/advento/misericordia.png` | 0 |
| `saida/stories/advento/stories-advento.pdf` | p1: 0, p2: 0 |
| `saida/stories/natal/angelus.png` | 0 |
| `saida/stories/natal/misericordia.png` | 0 |
| `saida/stories/natal/stories-natal.pdf` | p1: 0, p2: 0 |
| `saida/stories/prancha.png` | 0 |
| `saida/stories/quaresma/angelus.png` | 0 |
| `saida/stories/quaresma/misericordia.png` | 0 |
| `saida/stories/quaresma/stories-quaresma.pdf` | p1: 0, p2: 0 |
| `saida/stories/recorte-angelus.png` | 0 |
| `saida/stories/recorte-misericordia.png` | 0 |
| `saida/stories/tempo-comum/angelus.png` | 0 |
| `saida/stories/tempo-comum/misericordia.png` | 0 |
| `saida/stories/tempo-comum/stories-tempo-comum.pdf` | p1: 0, p2: 0 |
| `saida/teste-canva/prancha.png` | 0 |
| `saida/teste-canva/teste-canva-a.pdf` | p1: 0, p2: 0, p3: 0, p4: 0, p5: 0, p6: 0, p7: 0, p8: 0, p9: 0, p10: 0, p11: 0, p12: 0, p13: 0, p14: 0 |
| `saida/teste-canva/teste-canva-b.pdf` | p1: 0, p2: 0 |
| `saida/verificacao/logos/avatar-perfil-convertido.png` | 0 |
| `saida/verificacao/logos/avatar-perfil-original.png` | 0 |
| `saida/verificacao/logos/logo-horizontal-capela-convertido.png` | 0 |
| `saida/verificacao/logos/logo-horizontal-capela-original.png` | 0 |
| `saida/verificacao/logos/logo-horizontal-pergaminho-convertido.png` | 0 |
| `saida/verificacao/logos/logo-horizontal-pergaminho-original.png` | 0 |
| `saida/verificacao/logos/logo-horizontal-sobre-cor-convertido.png` | 0 |
| `saida/verificacao/logos/logo-horizontal-sobre-cor-original.png` | 0 |
| `saida/verificacao/logos/logo-vertical-capela-convertido.png` | 0 |
| `saida/verificacao/logos/logo-vertical-capela-original.png` | 0 |
| `saida/verificacao/logos/logo-vertical-pergaminho-convertido.png` | 0 |
| `saida/verificacao/logos/logo-vertical-pergaminho-original.png` | 0 |
| `saida/verificacao/logos/simbolo-capela-convertido.png` | 0 |
| `saida/verificacao/logos/simbolo-capela-original.png` | 0 |
| `saida/verificacao/logos/simbolo-pergaminho-convertido.png` | 0 |
| `saida/verificacao/logos/simbolo-pergaminho-original.png` | 0 |
| `saida/verificacao/logos/simbolo-reduzido-capela-convertido.png` | 0 |
| `saida/verificacao/logos/simbolo-reduzido-capela-original.png` | 0 |
| `saida/verificacao/logos/simbolo-reduzido-pergaminho-convertido.png` | 0 |
| `saida/verificacao/logos/simbolo-reduzido-pergaminho-original.png` | 0 |
<!-- fim-prova-prompt15 -->
