# Igreja Doméstica

`python gerar.py igreja-domestica`

## Conteúdo e composição

- Os textos foram escritos pela página: os de 29/11 e 6/12 foram aprovados em 03/11/2026 e os de 13/12 em 12/11/2026. O YAML mantém as quebras manuais e a ordem dos cards, itens e falas.
- PostIgrejaDomestica usa feed 1080 × 1350 e tema pergaminho. O selo traz a série e a data; do segundo card em diante aparece a contagem à direita.
- A capa segue o fluxo abaixo do selo: Nicho 600 × 680 com foco e zoom do YAML, crédito, título e apoio. A imagem entra dentro do arco; o crédito aparece na capa, e a página da obra fica somente na ficha e neste relatório.
- Passos, oração e conversa mantêm o bloco centralizado entre selo e assinatura, com pelo menos 60 px de folga e diferença de centralização até 0,1 px. Na capa, o apoio fica a pelo menos 32 px da assinatura.
- O gap de 16 px do kit recebe margens inline em tokens: 48 px do rótulo ou da instrução ao texto seguinte e 32 px de um texto à sua fonte. Todos os pares são medidos no navegador com tolerância de ±0,01 px.
- A lista usa 820 px, coluna de número de 24 px, intervalo de 20 px e texto em corpo alinhado à esquerda com text-wrap:pretty. Cada número em Lato Bold fica na linha de base da primeira linha do item; entre itens há 32 px.
- Rubricas usam corpo/tinta-suave e até duas linhas; oração usa oracao/tinta e até seis; aclamação usa citacao, Cormorant Garamond Medium Italic, em uma linha. Há 48 px entre falas e 32 px antes da origem opcional.
- A cruz e o filete seguem a cor do YAML; números e ornamento são ouro. A conversa ocupa o cartão inteiro nessa cor, com todos os textos, cruz, ornamento e logo em sobre-cor.
- As palavras de uma letra seguem o helper compartilhado intacto. Só esta série protege palavras com hífen, referências bíblicas inteiras com espaço inseparável entre livro e capítulo e ordinais unidos à palavra seguinte, como 3º domingo.
- O modelo existe apenas no gerador, sem prévia equivalente no kit. Nenhum arquivo do kit ou recurso das novenas e dos stories foi alterado.

## Tabela prevista no prompt

| Data · card | Linhas previstas | Folgas previstas |
| --- | --- | --- |
| 29/11 · 1 · capa | crédito 1, título 1, apoio 1 | selo → nicho 32 px; apoio → assinatura 116 px |
| 29/11 · 2 · passos | título 1; itens 2, 2, 2 e 2; fonte 1 | 128,5 px acima e abaixo |
| 29/11 · 3 · oração | título 1; rubricas 2 e 1; oração 4; aclamação 1 | 103,5 px acima e abaixo |
| 29/11 · 4 · conversa | pergunta 2; convite 1 | 353,5 px acima e abaixo |
| 6/12 · 1 · capa | crédito 1, título 1, apoio 1 | selo → nicho 32 px; apoio → assinatura 116 px |
| 6/12 · 2 · oração | título 1; rubricas 2 e 1; oração 4; aclamação 1 | 103,5 px acima e abaixo |
| 6/12 · 3 · conversa | pergunta 2; convite 1 | 353,5 px acima e abaixo |
| 13/12 · 1 · capa | crédito 1, título 1, apoio 1 | selo → nicho 32 px; apoio → assinatura 116 px |
| 13/12 · 2 · passos | título 1; itens 2, 2 e 2; fonte 1 | 194,5 px acima e abaixo |
| 13/12 · 3 · passos | título 1; itens 2, 2, 2 e 2; fonte 1 | 128,5 px acima e abaixo |
| 13/12 · 4 · oração | título 1; rubricas 2 e 1; oração 4; aclamação 1 | 103,5 px acima e abaixo |
| 13/12 · 5 · conversa | pergunta 2; convite 1 | 353,5 px acima e abaixo |

## Valores medidos no navegador

| Data | Card | Tipo | Linhas | Distâncias e folgas |
| --- | --- | --- | --- | --- |
| 2026-11-29 | 1 | capa | credito: 1; titulo: 1; apoio: 1 | selo_nicho_px: 32px; nicho_credito_px: 32px; credito_titulo_px: 48px; titulo_apoio_px: 32px; apoio_assinatura_px: 116px |
| 2026-11-29 | 2 | passos | titulo: 1; item_1: 2; item_2: 2; item_3: 2; item_4: 2; fonte: 1 | selo_texto_px: 128.5px; texto_assinatura_px: 128.5px; diferenca_centralizacao_px: 0px; rotulo_titulo_px: 48px; titulo_ornamento_px: 48px; ornamento_linha_item_1_px: 48px; linha_item_1_linha_item_2_px: 32px; linha_item_2_linha_item_3_px: 32px; linha_item_3_linha_item_4_px: 32px; linha_item_4_fonte_px: 32px |
| 2026-11-29 | 3 | oracao | titulo: 1; fala_1: 2; fala_2: 4; fala_3: 1; fala_4: 1 | selo_texto_px: 103.5px; texto_assinatura_px: 103.5px; diferenca_centralizacao_px: 0px; rotulo_titulo_px: 48px; titulo_ornamento_px: 48px; ornamento_fala_1_px: 48px; fala_1_fala_2_px: 48px; fala_2_fala_3_px: 48px; fala_3_fala_4_px: 48px |
| 2026-11-29 | 4 | conversa | pergunta: 2; convite: 1 | selo_texto_px: 353.5px; texto_assinatura_px: 353.5px; diferenca_centralizacao_px: 0px; rotulo_pergunta_px: 48px; pergunta_ornamento_px: 48px; ornamento_convite_px: 48px |
| 2026-12-06 | 1 | capa | credito: 1; titulo: 1; apoio: 1 | selo_nicho_px: 32px; nicho_credito_px: 32px; credito_titulo_px: 48px; titulo_apoio_px: 32px; apoio_assinatura_px: 116px |
| 2026-12-06 | 2 | oracao | titulo: 1; fala_1: 2; fala_2: 4; fala_3: 1; fala_4: 1 | selo_texto_px: 103.5px; texto_assinatura_px: 103.5px; diferenca_centralizacao_px: 0px; rotulo_titulo_px: 48px; titulo_ornamento_px: 48px; ornamento_fala_1_px: 48px; fala_1_fala_2_px: 48px; fala_2_fala_3_px: 48px; fala_3_fala_4_px: 48px |
| 2026-12-06 | 3 | conversa | pergunta: 2; convite: 1 | selo_texto_px: 353.5px; texto_assinatura_px: 353.5px; diferenca_centralizacao_px: 0px; rotulo_pergunta_px: 48px; pergunta_ornamento_px: 48px; ornamento_convite_px: 48px |
| 2026-12-13 | 1 | capa | credito: 1; titulo: 1; apoio: 1 | selo_nicho_px: 32px; nicho_credito_px: 32px; credito_titulo_px: 48px; titulo_apoio_px: 32px; apoio_assinatura_px: 116px |
| 2026-12-13 | 2 | passos | titulo: 1; item_1: 2; item_2: 2; item_3: 2; fonte: 1 | selo_texto_px: 194.5px; texto_assinatura_px: 194.5px; diferenca_centralizacao_px: 0px; rotulo_titulo_px: 48px; titulo_ornamento_px: 48px; ornamento_linha_item_1_px: 48px; linha_item_1_linha_item_2_px: 32px; linha_item_2_linha_item_3_px: 32px; linha_item_3_fonte_px: 32px |
| 2026-12-13 | 3 | passos | titulo: 1; item_1: 2; item_2: 2; item_3: 2; item_4: 2; fonte: 1 | selo_texto_px: 128.5px; texto_assinatura_px: 128.5px; diferenca_centralizacao_px: 0px; rotulo_titulo_px: 48px; titulo_ornamento_px: 48px; ornamento_linha_item_1_px: 48px; linha_item_1_linha_item_2_px: 32px; linha_item_2_linha_item_3_px: 32px; linha_item_3_linha_item_4_px: 32px; linha_item_4_fonte_px: 32px |
| 2026-12-13 | 4 | oracao | titulo: 1; fala_1: 2; fala_2: 4; fala_3: 1; fala_4: 1 | selo_texto_px: 103.5px; texto_assinatura_px: 103.5px; diferenca_centralizacao_px: 0px; rotulo_titulo_px: 48px; titulo_ornamento_px: 48px; ornamento_fala_1_px: 48px; fala_1_fala_2_px: 48px; fala_2_fala_3_px: 48px; fala_3_fala_4_px: 48px |
| 2026-12-13 | 5 | conversa | pergunta: 2; convite: 1 | selo_texto_px: 353.5px; texto_assinatura_px: 353.5px; diferenca_centralizacao_px: 0px; rotulo_pergunta_px: 48px; pergunta_ornamento_px: 48px; ornamento_convite_px: 48px |

## Diferenças da tabela prevista

Nenhuma diferença.

## Obras, enquadramentos e recortes

### 2026-11-29

Georges de La Tour · São José carpinteiro · Museu do Louvre — https://pop.culture.gouv.fr/notice/joconde/000PE001637

Obra real local, sem novo download. Recorte gerado com a pintura inteira e o contorno da janela do arco.
Foco `50% 40%`, zoom `1.0`; janela original x=0, y=247.893, largura=3096, altura=3619.27 px.

Obra real local, conferida na capa e no recorte: o rosto de São José, o rosto do Menino Jesus e a chama da vela ficam inteiros dentro do arco com foco 50% 40% e zoom 1. O recorte retira parte do fundo superior e da base da tela, preservando o trabalho de carpintaria e a luz entre as figuras. Não há margem fotográfica visível; o enquadramento do YAML foi mantido. Nenhum ajuste de foco ou zoom é necessário para preservar os rostos e a vela.
### 2026-12-06

Ateliê de Georges de La Tour · A educação da Virgem · The Frick Collection — https://collections.frick.org/objects/214/the-education-of-the-virgin

Obra real local, sem novo download. Recorte gerado com a pintura inteira e o contorno da janela do arco.
Foco `50% 50%`, zoom `1.0`; janela original x=481.94, y=0, largura=2425.12, altura=2835 px.

Obra real local, conferida na capa e no recorte: os dois rostos e a chama da vela ficam inteiros dentro do arco com foco 50% 50% e zoom 1. O recorte corta partes laterais da tela e parte do alto do lenço, preservando os rostos, a vela e a cena da leitura. A faixa escura de 78 px na base pertence à pintura e foi descartada pelo detector por diferença de cinza de aproximadamente 0,04 nível em relação ao interior. Não há margem fotográfica visível; o enquadramento do YAML foi mantido. Nenhum ajuste de foco ou zoom é necessário para preservar os rostos e a vela.
### 2026-12-13

Giotto e oficina · O presépio de Greccio · Basílica de São Francisco, Assis — https://commons.wikimedia.org/wiki/File:Giotto_di_Bondone_(und_Werkstatt)_007.jpg

Obra real local, sem novo download. Recorte gerado com a pintura inteira e o contorno da janela do arco.
Foco `50% 50%`, zoom `1.0`; janela original x=0, y=205.69, largura=2536, altura=2964.62 px.

Obra real local, conferida individualmente na capa e no recorte: São Francisco ajoelhado, o Menino na cena da manjedoura e o sacerdote à direita ficam inteiros dentro do arco na extensão em que aparecem na pintura, com rostos e gestos preservados. A curva corta apenas partes da arquitetura nos cantos superiores; a janela também retira faixas decorativas do alto e da base, sem cortar essas três figuras. Não há margem fotográfica visível. O foco 50% 50% e o zoom 1 do YAML foram mantidos; nenhum ajuste é necessário para preservar São Francisco, o Menino e o sacerdote.

## Avisos e pendências

Nenhum aviso.
Obras pendentes: nenhuma.

## PDF e conferências

Cada data recebe um PDF com os cards na ordem do YAML, páginas de 810 × 1012,5 pt e texto e fontes embutidas conferidos por PyMuPDF, pdffonts e pdftotext. A ficha preserva as caixas de cada linha, as falas, as posições da lista e os dados do enquadramento.
Nas capas, o filete do nicho é uma faixa vetorial em U. PyMuPDF exige um único preenchimento curvo na caixa do nicho, nenhuma assinatura da borda antiga feita de retângulos recortados e o parapeito retangular separado de 3 px. A verificação fica em nicho_vetorial dentro do PDF e interrompe a geração se falhar.

A importação destes PDFs no editor do Canva ainda não foi executada.

## O que conferir no Canva

- Cada texto na sua caixa: selo, contagem, rótulo, título, apoio, crédito, cada rubrica, a oração, a aclamação, cada número e cada item, a fonte, a pergunta e o convite.
- A obra dentro do arco.
- O filete, o parapeito e o ornamento como formas.
- Nenhuma caixa solta.

A evidência da geração está em [verificacao.json](verificacao.json).

A preservação das saídas anteriores e a conferência independente desta série estão registradas em [CONFERENCIA-PROMPT-10.md](CONFERENCIA-PROMPT-10.md), com [evidência detalhada](conferencia-prompt10.json).

## Árvore

```text
saida/igreja-domestica/
  2026-11-29/card-1.png
  2026-11-29/card-2.png
  2026-11-29/card-3.png
  2026-11-29/card-4.png
  2026-11-29/ficha.json
  2026-11-29/igreja-domestica-2026-11-29.pdf
  2026-11-29/recorte.png
  2026-12-06/card-1.png
  2026-12-06/card-2.png
  2026-12-06/card-3.png
  2026-12-06/ficha.json
  2026-12-06/igreja-domestica-2026-12-06.pdf
  2026-12-06/recorte.png
  2026-12-13/card-1.png
  2026-12-13/card-2.png
  2026-12-13/card-3.png
  2026-12-13/card-4.png
  2026-12-13/card-5.png
  2026-12-13/ficha.json
  2026-12-13/igreja-domestica-2026-12-13.pdf
  2026-12-13/recorte.png
  CONFERENCIA-PROMPT-10.md
  NOTAS-DAS-OBRAS.json
  RELATORIO.md
  conferencia-prompt10.json
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

A prova completa por arquivo PNG e página PDF está no [relatório de Olhe de Novo](../olhe-de-novo/RELATORIO.md).

<!-- fim-prova-prompt15 -->
