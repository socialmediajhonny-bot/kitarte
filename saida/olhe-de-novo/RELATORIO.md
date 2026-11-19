# Olhe de Novo

`python3 gerar.py olhe-de-novo --data 2026-12-30`

## Conteúdo e composição

- Os textos foram escritos pela página. Aprovação por data: 2026-12-09 → 2026-11-12; 2026-12-30 → 2026-11-19. O YAML preserva pontuação, aspas, acentos e quebras manuais; nenhum texto é gerado automaticamente.
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
| 2026-12-30 | 1 | obra | credito: 1; titulo: 1 | selo_nicho_px: 32 px; nicho_credito_px: 32 px; credito_titulo_px: 48 px; titulo_assinatura_px: 38 px | credito: 1 linhas; titulo: 1 linhas; selo_nicho_px: 32 px; titulo_assinatura_px: 38 px |
| 2026-12-30 | 2 | detalhe | credito: 1; titulo: 1 | selo_nicho_px: 32 px; nicho_credito_px: 32 px; credito_titulo_px: 48 px; titulo_assinatura_px: 38 px | credito: 1 linhas; titulo: 1 linhas; selo_nicho_px: 32 px; titulo_assinatura_px: 38 px |
| 2026-12-30 | 3 | significado | rotulo: 1; titulo: 1; texto: 4; fonte: 1 | selo_texto_px: 276.5 px; texto_assinatura_px: 276.5 px; diferenca_centralizacao_px: 0 px; rotulo_titulo_px: 48 px; titulo_ornamento_px: 48 px; ornamento_texto_px: 48 px; texto_fonte_px: 32 px | rotulo: 1 linhas; titulo: 1 linhas; texto: 4 linhas; fonte: 1 linhas; folga_px: 276.5 px |
| 2026-12-30 | 4 | onde | rotulo: 1; credito_1: 2; credito_2: 2; texto: 3; fonte: 1 | selo_texto_px: 116 px; texto_assinatura_px: 116 px; diferenca_centralizacao_px: 0 px; rotulo_linha_nichos_px: 48 px; linha_nichos_texto_px: 48 px; texto_fonte_px: 32 px; nicho_1_credito_1_px: 32 px; nicho_2_credito_2_px: 32 px; distancia_entre_nichos_px: 96 px | rotulo: 1 linhas; credito_1: 2 linhas; credito_2: 2 linhas; texto: 3 linhas; fonte: 1 linhas; folga_px: 116 px |

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
### 2026-12-30 · card-1

Sandro Botticelli · A Natividade mística · National Gallery, Londres — https://commons.wikimedia.org/wiki/File:Mystic_Nativity_by_Sandro_Botticelli.jpg

Original local: `obras/olhe-de-novo/2026-12-30.jpg`. Foco `50% 50%`, zoom `1`.

Janela original x=0.000000, y=126.052632, largura=2792.000000, altura=3783.894737 px; ampliação=0.217765.
Arquivo recortado: `saida/olhe-de-novo/2026-12-30/obra-1.jpg`. Prova: `saida/olhe-de-novo/2026-12-30/recorte-1.png`.
Dimensão do JPEG recortado: 1216 × 1648 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 0, "esquerda": 0, "direita": 0}, "faixas_descartadas": [], "margens_visiveis": []}`.

Capa e recorte-1.png finais conferidos. Maria, José, o Menino e as cabeças do boi e do burro ficam preservados no núcleo da Natividade. A curva intercepta os anjos nas extremidades do coro superior; a base também corta partes das figuras e vestes periféricas dos abraços inferiores. A composição inteira da pintura não cabe neste arco, mas o núcleo da cena permanece legível. Não há margem fotográfica visível. Foco e zoom aprovados mantidos.
### 2026-12-30 · card-2

Sandro Botticelli · A Natividade mística · National Gallery, Londres — https://commons.wikimedia.org/wiki/File:Mystic_Nativity_by_Sandro_Botticelli.jpg

Original local: `obras/olhe-de-novo/2026-12-30.jpg`. Janela aprovada `[950, 2110, 600]`, tamanho original `[2792, 4036]`.

Janela original x=950.000000, y=2110.000000, largura=600.000000, altura=813.000000 px; ampliação=1.013333.
Arquivo recortado: `saida/olhe-de-novo/2026-12-30/obra-2.jpg`. Prova: `saida/olhe-de-novo/2026-12-30/recorte-2.png`.
Dimensão do JPEG recortado: 600 × 813 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 0, "esquerda": 0, "direita": 0}, "faixas_descartadas": [], "margens_visiveis": []}`.

Card 2 e recorte-2.png finais conferidos. Os rostos, olhos e focinhos do boi e do burro estão dentro do arco, com os chifres do boi legíveis. O alto das orelhas/crina do burro encontra a curva superior; vestes e personagens periféricos ficam parciais neste detalhe fechado. A manjedoura e o Menino continuam reconhecíveis. Não há margem fotográfica visível. A janela aprovada foi mantida; não foi demonstrada correção integral de todas as extremidades sem abrir mais a cena.
### 2026-12-30 · card-4-1

Ícone russo, séc. XV · A Natividade
Catedral da Anunciação, Moscou — https://commons.wikimedia.org/wiki/File:Nativity_(15th_c.,_Annunciation_Cathedral_in_Moscow).jpg

Original local: `obras/olhe-de-novo/2026-12-30-icone.jpg`. Janela aprovada `[470, 650, 320]`, tamanho original `[1400, 1858]`.

Janela original x=470.000000, y=650.000000, largura=320.000000, altura=420.000000 px; ampliação=0.962500.
Arquivo recortado: `saida/olhe-de-novo/2026-12-30/obra-4-1.jpg`. Prova: `saida/olhe-de-novo/2026-12-30/recorte-4-1.png`.
Dimensão do JPEG recortado: 320 × 420 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 0, "esquerda": 0, "direita": 0}, "faixas_descartadas": [], "margens_visiveis": []}`.

Nicho esquerdo do card 4 e recorte-4-1.png conferidos no ícone russo. As duas cabeças dos animais e o Menino na manjedoura ficam preservados na extensão pintada. Os corpos dos animais já são ocultados pela manjedoura no original; o arco recorta a composição periférica, deixando Maria e os outros personagens fora do detalhe. Não há margem fotográfica visível.
### 2026-12-30 · card-4-2

Giotto · A Natividade
Capela Scrovegni, Pádua — https://commons.wikimedia.org/wiki/File:Giotto_di_Bondone_-_No._17_Scenes_from_the_Life_of_Christ_-_1._Nativity_-_Birth_of_Jesus_-_WGA09193.jpg

Original local: `obras/olhe-de-novo/2026-12-30-giotto.jpg`. Janela aprovada `[20, 430, 320]`, tamanho original `[950, 966]`.

Janela original x=20.000000, y=430.000000, largura=320.000000, altura=420.000000 px; ampliação=0.962500.
Arquivo recortado: `saida/olhe-de-novo/2026-12-30/obra-4-2.jpg`. Prova: `saida/olhe-de-novo/2026-12-30/recorte-4-2.png`.
Dimensão do JPEG recortado: 320 × 420 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 0, "esquerda": 0, "direita": 0}, "faixas_descartadas": [], "margens_visiveis": []}`.

Nicho direito do card 4 e recorte-4-2.png conferidos no Giotto. As cabeças dos dois animais, o rosto do Menino e o gesto junto da manjedoura permanecem legíveis na extensão disponível da obra. A curva corta o alto da cabeça e a auréola de Maria; José aparece parcial à direita. O animal à esquerda já encontra o limite esquerdo da própria composição. Este é um detalhe dos animais, sem margem fotográfica visível.

## Avisos e pendências

Nenhum aviso geométrico ou de composição. Os cortes visuais de figuras e elementos periféricos estão registrados nas notas de cada obra; o YAML aprovado foi mantido.

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
  2026-12-30/card-1.png
  2026-12-30/card-2.png
  2026-12-30/card-3.png
  2026-12-30/card-4.png
  2026-12-30/ficha.json
  2026-12-30/obra-1.jpg
  2026-12-30/obra-2.jpg
  2026-12-30/obra-4-1.jpg
  2026-12-30/obra-4-2.jpg
  2026-12-30/olhe-de-novo-2026-12-30.pdf
  2026-12-30/recorte-1.png
  2026-12-30/recorte-2.png
  2026-12-30/recorte-4-1.png
  2026-12-30/recorte-4-2.png
  NOTAS-DAS-OBRAS.json
  RELATORIO.md
  elementos/nicho-340x420-olhe-de-novo.svg
  elementos/nicho-640x840-olhe-de-novo.svg
  prancha.png
  verificacao.json
```
