# Igreja Doméstica

`python gerar.py igreja-domestica --data 2027-01-10`

## Conteúdo e composição

- Os textos foram escritos pela página: os de 29/11 e 6/12 foram aprovados em 03/11/2026, os de 13/12 em 12/11/2026, os de 20 e 27/12 em 19/11/2026 e os de 3 e 10/1/2027 em 23/11/2026. O YAML mantém as quebras manuais e a ordem dos cards, itens e falas.
- PostIgrejaDomestica aceita de dois a seis cards e usa feed 1080 × 1350 e tema pergaminho. O selo traz a série e a data; do segundo card em diante aparece a contagem à direita.
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
| 20/12 · 1 · capa | crédito 1, título 1, apoio 1 | selo → nicho 32 px; apoio → assinatura 116 px |
| 20/12 · 2 · passos | título 1; itens 2, 2 e 2; fonte 1 | 194,5 px acima e abaixo |
| 20/12 · 3 · oração | título 1; orações 4 e 4 | 136,5 px acima e abaixo |
| 20/12 · 4 · oração | título 1; orações 3 e 3 | 198,5 px acima e abaixo |
| 20/12 · 5 · oração | título 1; oração 3; rubrica 1; aclamação 1; origem 1 | 176,5 px acima e abaixo |
| 20/12 · 6 · conversa | pergunta 2; convite 1 | 353,5 px acima e abaixo |
| 27/12 · 1 · capa | crédito 1, título 1, apoio 1 | selo → nicho 32 px; apoio → assinatura 116 px |
| 27/12 · 2 · passos | título 1; itens 2, 2, 2 e 2; fonte 1 | 128,5 px acima e abaixo |
| 27/12 · 3 · oração | título 1; rubricas 2 e 1; oração 3; aclamação 1; origem 1 | 102,5 px acima e abaixo |
| 27/12 · 4 · conversa | pergunta 2; convite 1 | 353,5 px acima e abaixo |

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
| 2026-12-20 | 1 | capa | credito: 1; titulo: 1; apoio: 1 | selo_nicho_px: 32px; nicho_credito_px: 32px; credito_titulo_px: 48px; titulo_apoio_px: 32px; apoio_assinatura_px: 116px |
| 2026-12-20 | 2 | passos | titulo: 1; item_1: 2; item_2: 2; item_3: 2; fonte: 1 | selo_texto_px: 194.5px; texto_assinatura_px: 194.5px; diferenca_centralizacao_px: 0px; rotulo_titulo_px: 48px; titulo_ornamento_px: 48px; ornamento_linha_item_1_px: 48px; linha_item_1_linha_item_2_px: 32px; linha_item_2_linha_item_3_px: 32px; linha_item_3_fonte_px: 32px |
| 2026-12-20 | 3 | oracao | titulo: 1; fala_1: 4; fala_2: 4 | selo_texto_px: 136.5px; texto_assinatura_px: 136.5px; diferenca_centralizacao_px: 0px; rotulo_titulo_px: 48px; titulo_ornamento_px: 48px; ornamento_fala_1_px: 48px; fala_1_fala_2_px: 48px |
| 2026-12-20 | 4 | oracao | titulo: 1; fala_1: 3; fala_2: 3 | selo_texto_px: 198.5px; texto_assinatura_px: 198.5px; diferenca_centralizacao_px: 0px; rotulo_titulo_px: 48px; titulo_ornamento_px: 48px; ornamento_fala_1_px: 48px; fala_1_fala_2_px: 48px |
| 2026-12-20 | 5 | oracao | titulo: 1; fala_1: 3; fala_2: 1; fala_3: 1; origem: 1 | selo_texto_px: 176.5px; texto_assinatura_px: 176.5px; diferenca_centralizacao_px: 0px; rotulo_titulo_px: 48px; titulo_ornamento_px: 48px; ornamento_fala_1_px: 48px; fala_1_fala_2_px: 48px; fala_2_fala_3_px: 48px; fala_3_origem_px: 32px |
| 2026-12-20 | 6 | conversa | pergunta: 2; convite: 1 | selo_texto_px: 353.5px; texto_assinatura_px: 353.5px; diferenca_centralizacao_px: 0px; rotulo_pergunta_px: 48px; pergunta_ornamento_px: 48px; ornamento_convite_px: 48px |
| 2026-12-27 | 1 | capa | credito: 1; titulo: 1; apoio: 1 | selo_nicho_px: 32px; nicho_credito_px: 32px; credito_titulo_px: 48px; titulo_apoio_px: 32px; apoio_assinatura_px: 116px |
| 2026-12-27 | 2 | passos | titulo: 1; item_1: 2; item_2: 2; item_3: 2; item_4: 2; fonte: 1 | selo_texto_px: 128.5px; texto_assinatura_px: 128.5px; diferenca_centralizacao_px: 0px; rotulo_titulo_px: 48px; titulo_ornamento_px: 48px; ornamento_linha_item_1_px: 48px; linha_item_1_linha_item_2_px: 32px; linha_item_2_linha_item_3_px: 32px; linha_item_3_linha_item_4_px: 32px; linha_item_4_fonte_px: 32px |
| 2026-12-27 | 3 | oracao | titulo: 1; fala_1: 2; fala_2: 3; fala_3: 1; fala_4: 1; origem: 1 | selo_texto_px: 102.5px; texto_assinatura_px: 102.5px; diferenca_centralizacao_px: 0px; rotulo_titulo_px: 48px; titulo_ornamento_px: 48px; ornamento_fala_1_px: 48px; fala_1_fala_2_px: 48px; fala_2_fala_3_px: 48px; fala_3_fala_4_px: 48px; fala_4_origem_px: 32px |
| 2026-12-27 | 4 | conversa | pergunta: 2; convite: 1 | selo_texto_px: 353.5px; texto_assinatura_px: 353.5px; diferenca_centralizacao_px: 0px; rotulo_pergunta_px: 48px; pergunta_ornamento_px: 48px; ornamento_convite_px: 48px |
| 2027-01-03 | 1 | capa | credito: 1; titulo: 1; apoio: 1 | selo_nicho_px: 32px; nicho_credito_px: 32px; credito_titulo_px: 48px; titulo_apoio_px: 32px; apoio_assinatura_px: 116px |
| 2027-01-03 | 2 | passos | titulo: 1; item_1: 2; item_2: 2; item_3: 2; item_4: 3; fonte: 1 | selo_texto_px: 103.5px; texto_assinatura_px: 103.5px; diferenca_centralizacao_px: 0px; rotulo_titulo_px: 48px; titulo_ornamento_px: 48px; ornamento_linha_item_1_px: 48px; linha_item_1_linha_item_2_px: 32px; linha_item_2_linha_item_3_px: 32px; linha_item_3_linha_item_4_px: 32px; linha_item_4_fonte_px: 32px |
| 2027-01-03 | 3 | oracao | titulo: 1; fala_1: 2; fala_2: 2; fala_3: 1; fala_4: 1; origem: 1 | selo_texto_px: 133.5px; texto_assinatura_px: 133.5px; diferenca_centralizacao_px: 0px; rotulo_titulo_px: 48px; titulo_ornamento_px: 48px; ornamento_fala_1_px: 48px; fala_1_fala_2_px: 48px; fala_2_fala_3_px: 48px; fala_3_fala_4_px: 48px; fala_4_origem_px: 32px |
| 2027-01-03 | 4 | conversa | pergunta: 2; convite: 1 | selo_texto_px: 353.5px; texto_assinatura_px: 353.5px; diferenca_centralizacao_px: 0px; rotulo_pergunta_px: 48px; pergunta_ornamento_px: 48px; ornamento_convite_px: 48px |
| 2027-01-10 | 1 | capa | credito: 1; titulo: 1; apoio: 1 | selo_nicho_px: 32px; nicho_credito_px: 32px; credito_titulo_px: 48px; titulo_apoio_px: 32px; apoio_assinatura_px: 116px |
| 2027-01-10 | 2 | passos | titulo: 1; item_1: 1; item_2: 2; item_3: 2; item_4: 2; fonte: 1 | selo_texto_px: 153.5px; texto_assinatura_px: 153.5px; diferenca_centralizacao_px: 0px; rotulo_titulo_px: 48px; titulo_ornamento_px: 48px; ornamento_linha_item_1_px: 48px; linha_item_1_linha_item_2_px: 32px; linha_item_2_linha_item_3_px: 32px; linha_item_3_linha_item_4_px: 32px; linha_item_4_fonte_px: 32px |
| 2027-01-10 | 3 | oracao | titulo: 1; fala_1: 2; fala_2: 2; fala_3: 1; fala_4: 1; origem: 1 | selo_texto_px: 133.5px; texto_assinatura_px: 133.5px; diferenca_centralizacao_px: 0px; rotulo_titulo_px: 48px; titulo_ornamento_px: 48px; ornamento_fala_1_px: 48px; fala_1_fala_2_px: 48px; fala_2_fala_3_px: 48px; fala_3_fala_4_px: 48px; fala_4_origem_px: 32px |
| 2027-01-10 | 4 | conversa | pergunta: 2; convite: 1 | selo_texto_px: 353.5px; texto_assinatura_px: 353.5px; diferenca_centralizacao_px: 0px; rotulo_pergunta_px: 48px; pergunta_ornamento_px: 48px; ornamento_convite_px: 48px |

## Diferenças da tabela prevista

- 2027-01-03, card 2: item_4: 3 linhas; previsto 2; selo_texto_px: 103.5px; previsto 128.5px; texto_assinatura_px: 103.5px; previsto 128.5px
- 2027-01-03, card 3: fala_2: 2 linhas; previsto 4; selo_texto_px: 133.5px; previsto 103.5px; texto_assinatura_px: 133.5px; previsto 103.5px
- 2027-01-10, card 2: item_1: 1 linhas; previsto 2; selo_texto_px: 153.5px; previsto 128.5px; texto_assinatura_px: 153.5px; previsto 128.5px
- 2027-01-10, card 3: fala_2: 2 linhas; previsto 4; selo_texto_px: 133.5px; previsto 103.5px; texto_assinatura_px: 133.5px; previsto 103.5px

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
### 2026-12-20

Lorenzo Lotto · A Natividade · National Gallery of Art, Washington — https://commons.wikimedia.org/wiki/File:Lorenzo_Lotto,_The_Nativity,_1523,_NGA_431.jpg

Obra real local, sem novo download. Recorte gerado com a pintura inteira e o contorno da janela do arco.
Foco `50% 100%`, zoom `1.15`; janela original x=199.174, y=895.505, largura=2655.65, altura=3104.49 px.

Capa e recorte finais conferidos individualmente com foco 50% 100% e zoom 1.15. Os rostos de Maria, José e do Menino, as mãos dos adultos e o corpo inteiro do Menino ficam dentro do arco. A janela prioriza a Sagrada Família e a manjedoura; as laterais retiram partes periféricas dos mantos e o alto deixa fora os anjos e o crucifixo que aparecem na pintura inteira. Esses cortes não atingem os rostos, os gestos centrais ou o corpo do Menino. O detector registra uma margem de 4 px no topo do original, mas ela fica fora da janela e não aparece na arte. O foco e o zoom aprovados foram mantidos; não é necessário ajuste para preservar os protagonistas.
### 2026-12-27

Rembrandt · A Sagrada Família · Museu Hermitage, São Petersburgo — https://commons.wikimedia.org/wiki/File:Harmensz_van_Rijn_Rembrandt_-_%D0%A1%D0%B2%D1%8F%D1%82%D0%BE%D0%B5_%D1%81%D0%B5%D0%BC%D0%B5%D0%B9%D1%81%D1%82%D0%B2%D0%BE_-_Google_Art_Project.jpg

Obra real local, sem novo download. Recorte gerado com a pintura inteira e o contorno da janela do arco.
Foco `50% 75%`, zoom `1.1`; janela original x=139.409, y=555.432, largura=2788.18, altura=3259.42 px.

Capa e recorte finais conferidos individualmente com foco 50% 75% e zoom 1.1. Maria, o Menino no berço e José ao fundo mantêm seus rostos e os gestos essenciais dentro do arco; o Menino, o berço e o livro de Maria ficam preservados. José permanece na área escura da pintura, como no original. Um anjo sobre a família continua visível, enquanto o grupo de anjos do canto superior esquerdo e partes periféricas do ambiente ficam fora do arco. Não há margem fotográfica detectada ou visível. O foco e o zoom aprovados foram mantidos; não é necessário ajuste para preservar a Sagrada Família.
### 2027-01-03

Burne-Jones e Morris & Co. · A Adoração dos Magos · Museu d'Orsay — https://commons.wikimedia.org/wiki/File:Edward_Burne-Jones_-_The_Adoration_of_the_Magi_-_Google_Art_Project.jpg

Obra real local, sem novo download. Recorte gerado com a pintura inteira e o contorno da janela do arco.
Foco `42% 55%`, zoom `1.4`; janela original x=933.51, y=415.957, largura=1617.36, altura=1890.71 px.

Capa e recorte finais conferidos com foco 42% 55% e zoom 1.4. Maria com o Menino no colo e o anjo que segura a estrela ficam dentro do arco; o primeiro rei, de manto vermelho, aparece à direita só em parte. José, à esquerda, e os outros dois reis ficam fora, porque a tapeçaria é muito mais larga que o arco. A borda tecida não entra no arco, e não há margem fotográfica visível. O foco e o zoom do YAML foram mantidos.
### 2027-01-10

Verrocchio e Leonardo · O Batismo de Cristo · Galeria Uffizi, Florença — https://commons.wikimedia.org/wiki/File:Andrea_del_Verrocchio,_Leonardo_da_Vinci_-_Baptism_of_Christ_-_Uffizi.jpg

Obra real local, sem novo download. Recorte gerado com a pintura inteira e o contorno da janela do arco.
Foco `50% 40%`, zoom `1.1`; janela original x=71.1364, y=80.3247, largura=1422.73, altura=1663.19 px.

Capa e recorte finais conferidos com foco 50% 40% e zoom 1.1. Cristo, São João Batista derramando a água, a pomba no alto e os dois anjos ajoelhados à esquerda ficam dentro do arco; a palmeira e a paisagem laterais aparecem em parte. Não há margem fotográfica detectada ou visível. O foco e o zoom do YAML foram mantidos.

## Avisos e pendências

- 2027-01-03, card 2: item_4: 3 linhas; previsto 2; selo_texto_px: 103.5px; previsto 128.5px; texto_assinatura_px: 103.5px; previsto 128.5px
- 2027-01-03, card 3: fala_2: 2 linhas; previsto 4; selo_texto_px: 133.5px; previsto 103.5px; texto_assinatura_px: 133.5px; previsto 103.5px
- 2027-01-10, card 2: item_1: 1 linhas; previsto 2; selo_texto_px: 153.5px; previsto 128.5px; texto_assinatura_px: 153.5px; previsto 128.5px
- 2027-01-10, card 3: fala_2: 2 linhas; previsto 4; selo_texto_px: 133.5px; previsto 103.5px; texto_assinatura_px: 133.5px; previsto 103.5px
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
  2026-12-20/card-1.png
  2026-12-20/card-2.png
  2026-12-20/card-3.png
  2026-12-20/card-4.png
  2026-12-20/card-5.png
  2026-12-20/card-6.png
  2026-12-20/ficha.json
  2026-12-20/igreja-domestica-2026-12-20.pdf
  2026-12-20/recorte.png
  2026-12-27/card-1.png
  2026-12-27/card-2.png
  2026-12-27/card-3.png
  2026-12-27/card-4.png
  2026-12-27/ficha.json
  2026-12-27/igreja-domestica-2026-12-27.pdf
  2026-12-27/recorte.png
  2027-01-03/card-1.png
  2027-01-03/card-2.png
  2027-01-03/card-3.png
  2027-01-03/card-4.png
  2027-01-03/ficha.json
  2027-01-03/igreja-domestica-2027-01-03.pdf
  2027-01-03/recorte.png
  2027-01-10/card-1.png
  2027-01-10/card-2.png
  2027-01-10/card-3.png
  2027-01-10/card-4.png
  2027-01-10/ficha.json
  2027-01-10/igreja-domestica-2027-01-10.pdf
  2027-01-10/recorte.png
  CONFERENCIA-PROMPT-10.md
  NOTAS-DAS-OBRAS.json
  RELATORIO.md
  conferencia-prompt10.json
  prancha.png
  verificacao.json
```
