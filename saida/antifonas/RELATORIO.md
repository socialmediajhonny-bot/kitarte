# Antífonas do Ó

`python3 gerar.py antifonas`

## Conteúdo e composição

- Os textos foram escritos pela página. Aprovação por data: 2026-12-17 → 2026-11-19; 2026-12-18 → 2026-11-19; 2026-12-19 → 2026-11-19; 2026-12-21 → 2026-11-19; 2026-12-22 → 2026-11-19; 2026-12-23 → 2026-11-19. O YAML preserva pontuação, aspas, acentos e quebras manuais; nenhum texto é gerado automaticamente.
- Feed de 1080 × 1350. Os modelos existem apenas no gerador, sem prévia equivalente no kit v4. Nenhum módulo compartilhado ou arquivo do kit é modificado.
- O helper igreja_text_html é importado intacto: protege palavras de uma letra, referências bíblicas inteiras, ordinais ligados à palavra seguinte e palavras com hífen. As quebras do YAML são mantidas.
- O gap de 16 px do aqr-texto recebe margens inline em tokens: 48 px entre rótulo e texto e em volta do ornamento; 32 px entre texto e fonte/referência e entre nicho e crédito. Cada par é medido no navegador com tolerância de ±0,01 px.
- Os cards com obra no alto seguem o selo e deixam pelo menos 32 px entre o último texto e a assinatura. Os demais centralizam o bloco entre selo e assinatura, com pelo menos 60 px de cada lado e diferença de centralização até 0,1 px.
- A cruz e o filete recebem a cor do dia; o ornamento usa ouro. Nos cartões inteiros na cor do dia, fundo na cor litúrgica e textos, cruz, ornamento e logo em sobre-cor.
- A assinatura usa a variante do tema, ou sobre-cor no cartão inteiro na cor. Cores, fontes, caixas, limites de linhas e trechos protegidos são validados no DOM e por pixels.
- Cada nicho recebe um JPEG já recortado na janela visível, qualidade 95 e sem subamostragem de cor, usando LANCZOS e Image.resize com box fracionária. O card e o PDF usam esse arquivo com foco 50% 50% e zoom 1. Isso evita a ampliação que borrou a obra de 25/12 na importação do Canva.
- O recorte mantém a dimensão nativa, limitado a 2× a área interna do nicho, sem ampliar o arquivo. As janelas explícitas exigem dimensão original exata, contenção completa e ampliação de até 1,2. Nenhuma obra original é alterada ou baixada.
- Cada obra recebe uma prova da imagem inteira a 1080 px com o contorno da janela do arco. Margens fotográficas visíveis geram aviso e nunca alteram o YAML.
- PostAntifona: três cards de 17 a 23/12. A capa traz o info Nª de 7, nicho 640 × 760 e título em titulo-capa, com recuo automático para titulo em até duas linhas. Os demais cards têm contagem 2/3 e 3/3.
- O card De onde vem segue a raiz da Toda Bela, com versículo em citacao, referência em Lato Bold ouro e texto em corpo. O card Para rezar hoje usa o cartão inteiro na cor, antífona em oracao de 44/62 px até cinco linhas, fonte em credito e convite em corpo.
- Rótulo → antífona: 48 px; antífona → fonte: 32 px; fonte → ornamento: 48 px; ornamento → convite: 48 px. O bloco fica centralizado e com pelo menos 60 px de cada lado.
- O nome fixo Antífonas do Ó no selo é uma única linha e recebe a exceção à regra de palavra de uma letra no fim da linha; a regra continua valendo nos demais textos.

## Tabela medida no navegador

| Data | Card | Tipo | Linhas medidas | Distâncias e folgas medidas | Previsto |
| --- | --- | --- | --- | --- | --- |
| 2026-12-17 | 1 | capa | credito: 1; titulo: 1 | selo_nicho_px: 32 px; nicho_credito_px: 32 px; credito_titulo_px: 48 px; titulo_assinatura_px: 98 px | credito: 1 linhas; titulo: 1 linhas; selo_nicho_px: 32 px; titulo_assinatura_px: 98 px |
| 2026-12-17 | 2 | raiz | rotulo: 1; versiculo: 2; referencia: 1; texto: 4; fonte: 1 | selo_texto_px: 210.5 px; texto_assinatura_px: 210.5 px; diferenca_centralizacao_px: 0 px; rotulo_versiculo_px: 48 px; versiculo_referencia_px: 32 px; referencia_ornamento_px: 48 px; ornamento_texto_px: 48 px; texto_fonte_px: 32 px | rotulo: 1 linhas; versiculo: 2 linhas; referencia: 1 linhas; texto: 4 linhas; fonte: 1 linhas; folga_px: 210.5 px |
| 2026-12-17 | 3 | oracao | rotulo: 1; antifona: 4; fonte: 1; convite: 1 | selo_texto_px: 265.5 px; texto_assinatura_px: 265.5 px; diferenca_centralizacao_px: 0 px; rotulo_antifona_px: 48 px; antifona_fonte_px: 32 px; fonte_ornamento_px: 48 px; ornamento_convite_px: 48 px | rotulo: 1 linhas; antifona: 4 linhas; fonte: 1 linhas; convite: 1 linhas; folga_px: 265.5 px |
| 2026-12-18 | 1 | capa | credito: 1; titulo: 1 | selo_nicho_px: 32 px; nicho_credito_px: 32 px; credito_titulo_px: 48 px; titulo_assinatura_px: 98 px | credito: 1 linhas; titulo: 1 linhas; selo_nicho_px: 32 px; titulo_assinatura_px: 98 px |
| 2026-12-18 | 2 | raiz | rotulo: 1; versiculo: 1; referencia: 1; texto: 4; fonte: 1 | selo_texto_px: 244.5 px; texto_assinatura_px: 244.5 px; diferenca_centralizacao_px: 0 px; rotulo_versiculo_px: 48 px; versiculo_referencia_px: 32 px; referencia_ornamento_px: 48 px; ornamento_texto_px: 48 px; texto_fonte_px: 32 px | rotulo: 1 linhas; versiculo: 1 linhas; referencia: 1 linhas; texto: 4 linhas; fonte: 1 linhas; folga_px: 244.5 px |
| 2026-12-18 | 3 | oracao | rotulo: 1; antifona: 4; fonte: 1; convite: 1 | selo_texto_px: 265.5 px; texto_assinatura_px: 265.5 px; diferenca_centralizacao_px: 0 px; rotulo_antifona_px: 48 px; antifona_fonte_px: 32 px; fonte_ornamento_px: 48 px; ornamento_convite_px: 48 px | rotulo: 1 linhas; antifona: 4 linhas; fonte: 1 linhas; convite: 1 linhas; folga_px: 265.5 px |
| 2026-12-19 | 1 | capa | credito: 1; titulo: 1 | selo_nicho_px: 32 px; nicho_credito_px: 32 px; credito_titulo_px: 48 px; titulo_assinatura_px: 98 px | credito: 1 linhas; titulo: 1 linhas; selo_nicho_px: 32 px; titulo_assinatura_px: 98 px |
| 2026-12-19 | 2 | raiz | rotulo: 1; versiculo: 2; referencia: 1; texto: 4; fonte: 1 | selo_texto_px: 210.5 px; texto_assinatura_px: 210.5 px; diferenca_centralizacao_px: 0 px; rotulo_versiculo_px: 48 px; versiculo_referencia_px: 32 px; referencia_ornamento_px: 48 px; ornamento_texto_px: 48 px; texto_fonte_px: 32 px | rotulo: 1 linhas; versiculo: 2 linhas; referencia: 1 linhas; texto: 4 linhas; fonte: 1 linhas; folga_px: 210.5 px |
| 2026-12-19 | 3 | oracao | rotulo: 1; antifona: 4; fonte: 1; convite: 1 | selo_texto_px: 265.5 px; texto_assinatura_px: 265.5 px; diferenca_centralizacao_px: 0 px; rotulo_antifona_px: 48 px; antifona_fonte_px: 32 px; fonte_ornamento_px: 48 px; ornamento_convite_px: 48 px | rotulo: 1 linhas; antifona: 4 linhas; fonte: 1 linhas; convite: 1 linhas; folga_px: 265.5 px |
| 2026-12-21 | 1 | capa | credito: 1; titulo: 1 | selo_nicho_px: 32 px; nicho_credito_px: 32 px; credito_titulo_px: 48 px; titulo_assinatura_px: 98 px | credito: 1 linhas; titulo: 1 linhas; selo_nicho_px: 32 px; titulo_assinatura_px: 98 px |
| 2026-12-21 | 2 | raiz | rotulo: 1; versiculo: 3; referencia: 1; texto: 4; fonte: 1 | selo_texto_px: 176.5 px; texto_assinatura_px: 176.5 px; diferenca_centralizacao_px: 0 px; rotulo_versiculo_px: 48 px; versiculo_referencia_px: 32 px; referencia_ornamento_px: 48 px; ornamento_texto_px: 48 px; texto_fonte_px: 32 px | rotulo: 1 linhas; versiculo: 3 linhas; referencia: 1 linhas; texto: 4 linhas; fonte: 1 linhas; folga_px: 176.5 px |
| 2026-12-21 | 3 | oracao | rotulo: 1; antifona: 4; fonte: 1; convite: 1 | selo_texto_px: 265.5 px; texto_assinatura_px: 265.5 px; diferenca_centralizacao_px: 0 px; rotulo_antifona_px: 48 px; antifona_fonte_px: 32 px; fonte_ornamento_px: 48 px; ornamento_convite_px: 48 px | rotulo: 1 linhas; antifona: 4 linhas; fonte: 1 linhas; convite: 1 linhas; folga_px: 265.5 px |
| 2026-12-22 | 1 | capa | credito: 1; titulo: 1 | selo_nicho_px: 32 px; nicho_credito_px: 32 px; credito_titulo_px: 48 px; titulo_assinatura_px: 98 px | credito: 1 linhas; titulo: 1 linhas; selo_nicho_px: 32 px; titulo_assinatura_px: 98 px |
| 2026-12-22 | 2 | raiz | rotulo: 1; versiculo: 2; referencia: 1; texto: 4; fonte: 1 | selo_texto_px: 210.5 px; texto_assinatura_px: 210.5 px; diferenca_centralizacao_px: 0 px; rotulo_versiculo_px: 48 px; versiculo_referencia_px: 32 px; referencia_ornamento_px: 48 px; ornamento_texto_px: 48 px; texto_fonte_px: 32 px | rotulo: 1 linhas; versiculo: 2 linhas; referencia: 1 linhas; texto: 4 linhas; fonte: 1 linhas; folga_px: 210.5 px |
| 2026-12-22 | 3 | oracao | rotulo: 1; antifona: 4; fonte: 1; convite: 1 | selo_texto_px: 265.5 px; texto_assinatura_px: 265.5 px; diferenca_centralizacao_px: 0 px; rotulo_antifona_px: 48 px; antifona_fonte_px: 32 px; fonte_ornamento_px: 48 px; ornamento_convite_px: 48 px | rotulo: 1 linhas; antifona: 4 linhas; fonte: 1 linhas; convite: 1 linhas; folga_px: 265.5 px |
| 2026-12-23 | 1 | capa | credito: 1; titulo: 1 | selo_nicho_px: 32 px; nicho_credito_px: 32 px; credito_titulo_px: 48 px; titulo_assinatura_px: 98 px | credito: 1 linhas; titulo: 1 linhas; selo_nicho_px: 32 px; titulo_assinatura_px: 98 px |
| 2026-12-23 | 2 | raiz | rotulo: 1; versiculo: 2; referencia: 1; texto: 4; fonte: 1 | selo_texto_px: 210.5 px; texto_assinatura_px: 210.5 px; diferenca_centralizacao_px: 0 px; rotulo_versiculo_px: 48 px; versiculo_referencia_px: 32 px; referencia_ornamento_px: 48 px; ornamento_texto_px: 48 px; texto_fonte_px: 32 px | rotulo: 1 linhas; versiculo: 2 linhas; referencia: 1 linhas; texto: 4 linhas; fonte: 1 linhas; folga_px: 210.5 px |
| 2026-12-23 | 3 | oracao | rotulo: 1; antifona: 3; fonte: 1; convite: 1 | selo_texto_px: 296.5 px; texto_assinatura_px: 296.5 px; diferenca_centralizacao_px: 0 px; rotulo_antifona_px: 48 px; antifona_fonte_px: 32 px; fonte_ornamento_px: 48 px; ornamento_convite_px: 48 px | rotulo: 1 linhas; antifona: 3 linhas; fonte: 1 linhas; convite: 1 linhas; folga_px: 296.5 px |

## Diferenças da tabela prevista

Nenhuma diferença.

## Obras, janelas e recortes

### 2026-12-17 · card-1

Auvergne, séc. XII · Virgem com o Menino em majestade · The Met, Nova York — https://commons.wikimedia.org/wiki/File:Enthroned_Virgin_and_Child_MET_DP102902.jpg

Original local: `obras/antifonas/2026-12-17.jpg`. Foco `50% 40%`, zoom `1.4`.

Janela original x=788.771889, y=433.371429, largura=2213.456221, altura=2708.571429 px; ampliação=0.274684.
Arquivo recortado: `saida/antifonas/2026-12-17/obra-1.jpg`. Prova: `saida/antifonas/2026-12-17/recorte-1.png`.
Dimensão do JPEG recortado: 1216 × 1488 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 139, "esquerda": 0, "direita": 0}, "faixas_descartadas": [{"lado": "topo", "largura": 235, "diferenca_cinza": 2.6350315276382474}], "margens_visiveis": []}`.

Capa e recorte-1.png finais conferidos individualmente. Os rostos de Maria e do Menino, suas mãos e o gesto de bênção ficam dentro do arco. A curva corta o alto da cabeça de Maria, e a base do nicho exclui parte inferior da veste, dos apoios do trono e do pedestal; portanto a escultura não está inteira. A margem fotográfica de 139 px na base do original fica fora da janela aprovada. O foco 50% 40% e zoom 1.4 foram mantidos no YAML.

Sugestão somente para avaliação, sem alterar o YAML: {"foco": "50% 55%", "zoom": 1.1, "janela_original": {"x": 486.9369501466276, "y": 189.60000000000016, "largura": 2817.1260997067448, "altura": 3447.272727272727}, "margens_visiveis": [], "nota": "Alternativa renderizada e inspecionada somente em work: recupera o alto da cabeça de Maria e abre a estátua quase toda, com o pedestal junto ao parapeito. Rostos, mãos e gesto de bênção continuam claros; a figura fica menor e há mais fundo cinzento. A inspeção geométrica tem margens_visiveis e avisos vazios. Não se propõe zoom 1, pois ele traz a margem fotográfica inferior. Sugestão apenas no relatório, sem alterar o YAML."}
### 2026-12-18 · card-1

Dieric Bouts (atrib.) · Moisés e a sarça ardente · Philadelphia Museum of Art — https://commons.wikimedia.org/wiki/File:Attributed_to_Dierick_Bouts_the_Elder,_Netherlandish_(active_Louvain),_first_securely_documented_1447,_died_1475_-_Moses_and_the_Burning_Bush,_with_Moses_Removing_His_Shoes_-_Google_Art_Project.jpg

Original local: `obras/antifonas/2026-12-18.jpg`. Foco `40% 50%`, zoom `1`.

Janela original x=0.000000, y=46.309211, largura=4289.000000, altura=5248.381579 px; ampliação=0.141758.
Arquivo recortado: `saida/antifonas/2026-12-18/obra-1.jpg`. Prova: `saida/antifonas/2026-12-18/recorte-1.png`.
Dimensão do JPEG recortado: 1216 × 1488 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 0, "esquerda": 0, "direita": 0}, "faixas_descartadas": [], "margens_visiveis": []}`.

Capa e recorte-1.png finais conferidos individualmente. Moisés ajoelhado, no primeiro plano, permanece inteiro na extensão pintada, com rosto, mãos, veste, joelhos e pés preservados. A aparição divina à esquerda mantém o rosto e os gestos legíveis; a curva intercepta parte das chamas e das extremidades do manto. A segunda cena de Moisés à direita preserva rosto, mãos, pernas e o gesto de tirar a sandália, até os limites já presentes na pintura. Nenhuma margem fotográfica aparece. O enquadramento aprovado foi mantido para priorizar o encontro na sarça.
### 2026-12-19 · card-1

Vitral alemão, séc. XIII · A Árvore de Jessé · The Met, Nova York — https://commons.wikimedia.org/wiki/File:Tree_of_Jesse_Window-_The_Reclining_Jesse,_King_David,_and_Scenes_from_the_Life_of_Jesus_MET_DP275861.jpg

Original local: `obras/antifonas/2026-12-19.jpg`. Janela aprovada `[584, 600, 845]`, tamanho original `[2000, 1683]`.

Janela original x=584.000000, y=600.000000, largura=845.000000, altura=1034.000000 px; ampliação=0.719527.
Arquivo recortado: `saida/antifonas/2026-12-19/obra-1.jpg`. Prova: `saida/antifonas/2026-12-19/recorte-1.png`.
Dimensão do JPEG recortado: 845 × 1034 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 0, "esquerda": 0, "direita": 0}, "faixas_descartadas": [{"lado": "direita", "largura": 6, "diferenca_cinza": 8.752797583679943}], "margens_visiveis": []}`.

Capa e recorte-1.png finais conferidos individualmente. Jessé reclinado fica inteiro na extensão representada: cabeça, mão junto ao rosto, veste e pés estão dentro do arco, junto ao tronco que brota de seu corpo. A janela isola a parte inferior do vitral; os painéis superiores e figuras periféricas aparecem parciais ou ficam fora por essa escolha. A fotografia e a armação externa do museu ficam fora do arco; nenhuma margem visível foi constatada. A janela aprovada [584, 600, 845] foi mantida.
### 2026-12-21 · card-1

Correggio · A Noite Santa · Gemäldegalerie Alte Meister, Dresden — https://commons.wikimedia.org/wiki/File:Correggio_-_The_Holy_Night_-_Google_Art_Project.jpg

Original local: `obras/antifonas/2026-12-21.jpg`. Foco `62% 60%`, zoom `1.2`.

Janela original x=328.496667, y=654.153947, largura=2649.166667, altura=3241.743421 px; ampliação=0.229506.
Arquivo recortado: `saida/antifonas/2026-12-21/obra-1.jpg`. Prova: `saida/antifonas/2026-12-21/recorte-1.png`.
Dimensão do JPEG recortado: 1216 × 1488 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 0, "esquerda": 0, "direita": 0}, "faixas_descartadas": [], "margens_visiveis": []}`.

Capa e recorte-1.png finais conferidos individualmente. Os rostos de Maria e do Menino, as mãos que o sustentam e o Menino na manjedoura permanecem preservados na extensão pintada; o foco mantém o núcleo luminoso do nascimento. Os rostos de José e das duas mulheres próximas também ficam legíveis. O grupo de anjos no alto fica fora, e o pastor à esquerda e outras partes periféricas são cortados pela curva e pelas laterais. Nenhuma margem fotográfica aparece. O foco e o zoom aprovados foram mantidos para priorizar Maria e o Menino, sem afirmar que a composição inteira está no arco.
### 2026-12-22 · card-1

Quentin Metsys · Salvator Mundi · Museo Correr, Veneza — https://commons.wikimedia.org/wiki/File:(Venice)_Salvator_Mundi_-_Quentin_Metsys_-_Museo_Correr.jpg

Original local: `obras/antifonas/2026-12-22.jpg`. Foco `50% 90%`, zoom `1`.

Janela original x=0.000000, y=553.156579, largura=4365.000000, altura=5341.381579 px; ampliação=0.139290.
Arquivo recortado: `saida/antifonas/2026-12-22/obra-1.jpg`. Prova: `saida/antifonas/2026-12-22/recorte-1.png`.
Dimensão do JPEG recortado: 1216 × 1488 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 0, "esquerda": 0, "direita": 0}, "faixas_descartadas": [], "margens_visiveis": []}`.

Capa e recorte-1.png finais conferidos individualmente. O rosto de Cristo e os dedos levantados no gesto de bênção ficam dentro do arco; os dedos que tocam o globo também permanecem legíveis. A curva corta parte do alto do cabelo e do resplendor; o globo e a extensão inferior das mãos/punhos ficam parciais no limite inferior, além dos limites já impostos pela própria fotografia da pintura. Portanto não se afirma que a auréola, as duas mãos completas e o orbe estejam integralmente contidos. Nenhuma margem fotográfica foi vista. Mantido o foco 50% 90% para o rosto e a bênção; não foi proposta uma correção integral não demonstrada.
### 2026-12-23 · card-1

Rafael · A Pequena Madona Cowper · National Gallery of Art, Washington — https://commons.wikimedia.org/wiki/File:Raphael,_The_Small_Cowper_Madonna,_c._1505,_NGA_1196.jpg

Original local: `obras/antifonas/2026-12-23.jpg`. Foco `50% 25%`, zoom `1.1`.

Janela original x=135.090909, y=173.456938, largura=2701.818182, altura=3306.172249 px; ampliação=0.225034.
Arquivo recortado: `saida/antifonas/2026-12-23/obra-1.jpg`. Prova: `saida/antifonas/2026-12-23/recorte-1.png`.
Dimensão do JPEG recortado: 1216 × 1488 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 0, "esquerda": 0, "direita": 0}, "faixas_descartadas": [], "margens_visiveis": []}`.

Capa e recorte-1.png finais conferidos individualmente. Os rostos de Maria e do Menino, suas mãos, o abraço e os dois pés do Menino ficam dentro do arco na extensão pintada. A auréola de Maria é interceptada pela curva superior; os extremos do manto e a parte inferior do colo também são recortados. Não há margem fotográfica visível. O enquadramento aprovado foi mantido para conservar os rostos e os gestos; a ressalva de integralidade refere-se principalmente à auréola e ao manto periférico.

## Avisos e pendências

Nenhum aviso.

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
saida/antifonas/
  2026-12-17/antifonas-2026-12-17.pdf
  2026-12-17/card-1.png
  2026-12-17/card-2.png
  2026-12-17/card-3.png
  2026-12-17/ficha.json
  2026-12-17/obra-1.jpg
  2026-12-17/recorte-1.png
  2026-12-18/antifonas-2026-12-18.pdf
  2026-12-18/card-1.png
  2026-12-18/card-2.png
  2026-12-18/card-3.png
  2026-12-18/ficha.json
  2026-12-18/obra-1.jpg
  2026-12-18/recorte-1.png
  2026-12-19/antifonas-2026-12-19.pdf
  2026-12-19/card-1.png
  2026-12-19/card-2.png
  2026-12-19/card-3.png
  2026-12-19/ficha.json
  2026-12-19/obra-1.jpg
  2026-12-19/recorte-1.png
  2026-12-21/antifonas-2026-12-21.pdf
  2026-12-21/card-1.png
  2026-12-21/card-2.png
  2026-12-21/card-3.png
  2026-12-21/ficha.json
  2026-12-21/obra-1.jpg
  2026-12-21/recorte-1.png
  2026-12-22/antifonas-2026-12-22.pdf
  2026-12-22/card-1.png
  2026-12-22/card-2.png
  2026-12-22/card-3.png
  2026-12-22/ficha.json
  2026-12-22/obra-1.jpg
  2026-12-22/recorte-1.png
  2026-12-23/antifonas-2026-12-23.pdf
  2026-12-23/card-1.png
  2026-12-23/card-2.png
  2026-12-23/card-3.png
  2026-12-23/ficha.json
  2026-12-23/obra-1.jpg
  2026-12-23/recorte-1.png
  NOTAS-DAS-OBRAS.json
  RELATORIO.md
  prancha.png
  verificacao.json
```
