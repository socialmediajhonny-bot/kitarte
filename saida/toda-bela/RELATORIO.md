# Toda Bela

`python3 gerar.py toda-bela --data 2027-01-09`

## Conteúdo e composição

- Os textos foram escritos pela página. Aprovação por data: 2026-12-12 → 2026-11-12; 2026-12-26 → 2026-11-19; 2027-01-02 → 2026-11-23; 2027-01-09 → 2026-11-23. O YAML preserva pontuação, aspas, acentos e quebras manuais; nenhum texto é gerado automaticamente.
- Feed de 1080 × 1350. Os modelos existem apenas no gerador, sem prévia equivalente no kit v4. Nenhum módulo compartilhado ou arquivo do kit é modificado.
- O helper igreja_text_html é importado intacto: protege palavras de uma letra, referências bíblicas inteiras, ordinais ligados à palavra seguinte e palavras com hífen. As quebras do YAML são mantidas.
- O gap de 16 px do aqr-texto recebe margens inline em tokens: 48 px entre rótulo e texto e em volta do ornamento; 32 px entre texto e fonte/referência e entre nicho e crédito. Cada par é medido no navegador com tolerância de ±0,01 px.
- Os cards com obra no alto seguem o selo e deixam pelo menos 32 px entre o último texto e a assinatura. Os demais centralizam o bloco entre selo e assinatura, com pelo menos 60 px de cada lado e diferença de centralização até 0,1 px.
- A cruz e o filete recebem a cor do dia; o ornamento usa ouro. Nos cartões inteiros na cor do dia, fundo na cor litúrgica e textos, cruz, ornamento e logo em sobre-cor.
- A assinatura usa a variante do tema, ou sobre-cor no cartão inteiro na cor. Cores, fontes, caixas, limites de linhas e trechos protegidos são validados no DOM e por pixels.
- Cada nicho recebe um JPEG já recortado na janela visível, qualidade 95 e sem subamostragem de cor, usando LANCZOS e Image.resize com box fracionária. O card e o PDF usam esse arquivo com foco 50% 50% e zoom 1. Isso evita a ampliação que borrou a obra de 25/12 na importação do Canva.
- O recorte mantém a dimensão nativa, limitado a 2× a área interna do nicho, sem ampliar o arquivo. As janelas explícitas exigem dimensão original exata, contenção completa e ampliação de até 1,2. Nenhuma obra original é alterada ou baixada.
- Cada obra recebe uma prova da imagem inteira a 1080 px com o contorno da janela do arco. Margens fotográficas visíveis geram aviso e nunca alteram o YAML.
- PostTodaBela: três cards. Capa e raiz no tema capela; oração em cartão inteiro na cor do dia. A capa traz o info do YAML e os outros cards a contagem 2/3 e 3/3.
- A capa usa nicho 640 × 760, crédito em uma linha e invocação em titulo-capa. Se a invocação quebrar, é renderizada em titulo com até duas linhas; a assinatura continua a pelo menos 32 px. Não há apoio na capa.
- A raiz traz versículo de até três linhas, referência em uma linha, texto de até cinco e fonte em uma. A oração usa citacao-grande em até três linhas, com as quebras manuais do YAML, e convite em uma.

## Tabela medida no navegador

| Data | Card | Tipo | Linhas medidas | Distâncias e folgas medidas | Previsto |
| --- | --- | --- | --- | --- | --- |
| 2026-12-12 | 1 | capa | credito: 1; invocacao: 1 | selo_nicho_px: 32 px; nicho_credito_px: 32 px; credito_invocacao_px: 48 px; invocacao_assinatura_px: 98 px | credito: 1 linhas; invocacao: 1 linhas; selo_nicho_px: 32 px; invocacao_assinatura_px: 98 px |
| 2026-12-12 | 2 | raiz | rotulo: 1; versiculo: 1; referencia: 1; texto: 5; fonte: 1 | selo_texto_px: 219.5 px; texto_assinatura_px: 219.5 px; diferenca_centralizacao_px: 0 px; rotulo_versiculo_px: 48 px; versiculo_referencia_px: 32 px; referencia_ornamento_px: 48 px; ornamento_texto_px: 48 px; texto_fonte_px: 32 px | rotulo: 1 linhas; versiculo: 1 linhas; referencia: 1 linhas; texto: 5 linhas; fonte: 1 linhas; folga_px: 219.5 px |
| 2026-12-12 | 3 | oracao | rotulo: 1; frase: 2; convite: 1 | selo_texto_px: 333.5 px; texto_assinatura_px: 333.5 px; diferenca_centralizacao_px: 0 px; rotulo_frase_px: 48 px; frase_ornamento_px: 48 px; ornamento_convite_px: 48 px | rotulo: 1 linhas; frase: 2 linhas; convite: 1 linhas; folga_px: 333.5 px |
| 2026-12-26 | 1 | capa | credito: 1; invocacao: 1 | selo_nicho_px: 32 px; nicho_credito_px: 32 px; credito_invocacao_px: 48 px; invocacao_assinatura_px: 98 px | credito: 1 linhas; invocacao: 1 linhas; selo_nicho_px: 32 px; invocacao_assinatura_px: 98 px |
| 2026-12-26 | 2 | raiz | rotulo: 1; versiculo: 2; referencia: 1; texto: 4; fonte: 1 | selo_texto_px: 210.5 px; texto_assinatura_px: 210.5 px; diferenca_centralizacao_px: 0 px; rotulo_versiculo_px: 48 px; versiculo_referencia_px: 32 px; referencia_ornamento_px: 48 px; ornamento_texto_px: 48 px; texto_fonte_px: 32 px | rotulo: 1 linhas; versiculo: 2 linhas; referencia: 1 linhas; texto: 4 linhas; fonte: 1 linhas; folga_px: 210.5 px |
| 2026-12-26 | 3 | oracao | rotulo: 1; frase: 2; convite: 1 | selo_texto_px: 333.5 px; texto_assinatura_px: 333.5 px; diferenca_centralizacao_px: 0 px; rotulo_frase_px: 48 px; frase_ornamento_px: 48 px; ornamento_convite_px: 48 px | rotulo: 1 linhas; frase: 2 linhas; convite: 1 linhas; folga_px: 333.5 px |
| 2027-01-02 | 1 | capa | credito: 1; invocacao: 1 | selo_nicho_px: 32 px; nicho_credito_px: 32 px; credito_invocacao_px: 48 px; invocacao_assinatura_px: 118 px | credito: 1 linhas; invocacao: 1 linhas; selo_nicho_px: 32 px; invocacao_assinatura_px: 98 px |
| 2027-01-02 | 2 | raiz | rotulo: 1; versiculo: 2; referencia: 1; texto: 4; fonte: 1 | selo_texto_px: 210.5 px; texto_assinatura_px: 210.5 px; diferenca_centralizacao_px: 0 px; rotulo_versiculo_px: 48 px; versiculo_referencia_px: 32 px; referencia_ornamento_px: 48 px; ornamento_texto_px: 48 px; texto_fonte_px: 32 px | rotulo: 1 linhas; versiculo: 1 linhas; referencia: 1 linhas; texto: 5 linhas; fonte: 1 linhas; folga_px: 219.5 px |
| 2027-01-02 | 3 | oracao | rotulo: 1; frase: 2; convite: 1 | selo_texto_px: 333.5 px; texto_assinatura_px: 333.5 px; diferenca_centralizacao_px: 0 px; rotulo_frase_px: 48 px; frase_ornamento_px: 48 px; ornamento_convite_px: 48 px | rotulo: 1 linhas; frase: 2 linhas; convite: 1 linhas; folga_px: 333.5 px |
| 2027-01-09 | 1 | capa | credito: 1; invocacao: 1 | selo_nicho_px: 32 px; nicho_credito_px: 32 px; credito_invocacao_px: 48 px; invocacao_assinatura_px: 98 px | credito: 1 linhas; invocacao: 1 linhas; selo_nicho_px: 32 px; invocacao_assinatura_px: 98 px |
| 2027-01-09 | 2 | raiz | rotulo: 1; versiculo: 2; referencia: 1; texto: 4; fonte: 1 | selo_texto_px: 210.5 px; texto_assinatura_px: 210.5 px; diferenca_centralizacao_px: 0 px; rotulo_versiculo_px: 48 px; versiculo_referencia_px: 32 px; referencia_ornamento_px: 48 px; ornamento_texto_px: 48 px; texto_fonte_px: 32 px | rotulo: 1 linhas; versiculo: 1 linhas; referencia: 1 linhas; texto: 5 linhas; fonte: 1 linhas; folga_px: 219.5 px |
| 2027-01-09 | 3 | oracao | rotulo: 1; frase: 2; convite: 1 | selo_texto_px: 333.5 px; texto_assinatura_px: 333.5 px; diferenca_centralizacao_px: 0 px; rotulo_frase_px: 48 px; frase_ornamento_px: 48 px; ornamento_convite_px: 48 px | rotulo: 1 linhas; frase: 2 linhas; convite: 1 linhas; folga_px: 333.5 px |

## Diferenças da tabela prevista

- 2027-01-02, card 1: invocacao_assinatura_px: 118px; previsto 98px
- 2027-01-02, card 2: versiculo: 2 linhas; previsto 1; texto: 4 linhas; previsto 5; selo_texto_px: 210.5px; previsto 219.5px; texto_assinatura_px: 210.5px; previsto 219.5px
- 2027-01-09, card 2: versiculo: 2 linhas; previsto 1; texto: 4 linhas; previsto 5; selo_texto_px: 210.5px; previsto 219.5px; texto_assinatura_px: 210.5px; previsto 219.5px

## Obras, janelas e recortes

### 2026-12-12 · card-1

Sassoferrato · A Virgem em oração · National Gallery, Londres — https://www.nationalgallery.org.uk/paintings/sassoferrato-the-virgin-in-prayer

Original local: `obras/toda-bela/2026-12-12.jpg`. Foco `50% 30%`, zoom `1.08`.

Janela original x=124.481481, y=125.354825, largura=3112.037037, altura=3808.150585 px; ampliação=0.195370.
Arquivo recortado: `saida/toda-bela/2026-12-12/obra-1.jpg`. Prova: `saida/toda-bela/2026-12-12/recorte-1.png`.
Dimensão do JPEG recortado: 1216 × 1488 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 0, "esquerda": 0, "direita": 0}, "faixas_descartadas": [], "margens_visiveis": []}`.

Card 1 final e recorte-1.png, com a obra inteira e o contorno da janela, conferidos visualmente. O rosto de Maria fica inteiro dentro do arco, com testa, olhos, nariz, boca e queixo preservados; a cabeça e o véu também não encontram a curva. As duas mãos em oração permanecem inteiras, incluindo as pontas dos dedos e os punhos. O arco e a base recortam apenas partes laterais e inferiores do manto, sem atingir o rosto ou as mãos pedidos. Não há margem fotográfica visível. O foco aprovado 50% 30%, zoom 1.08, foi mantido; não é necessário sugerir correção para os elementos principais desta capa.
### 2026-12-26 · card-1

Ícone bizantino, séc. XII · Virgem de Vladimir · Galeria Tretyakov, Moscou — https://commons.wikimedia.org/wiki/File:Vladimirskaja_ikona_Bo%C5%BEiej_Materi.jpg

Original local: `obras/toda-bela/2026-12-26.jpg`. Foco `53% 38%`, zoom `1.9`.

Janela original x=487.293158, y=634.565789, largura=1021.578947, altura=1250.090028 px; ampliação=0.595157.
Arquivo recortado: `saida/toda-bela/2026-12-26/obra-1.jpg`. Prova: `saida/toda-bela/2026-12-26/recorte-1.png`.
Dimensão do JPEG recortado: 1022 × 1250 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 0, "esquerda": 12, "direita": 19}, "faixas_descartadas": [{"lado": "topo", "largura": 7, "diferenca_cinza": 4.883965371310811}], "margens_visiveis": []}`.

Capa e recorte-1.png finais conferidos no ícone de Vladimir. Os rostos de Maria e do Menino e os gestos das mãos junto do colo ficam preservados. A curva recorta a região externa do véu e parte da auréola; a base fecha a composição sobre as vestes, deixando parte inferior do corpo e os pés do Menino fora da janela. Não há margem fotográfica dentro do arco: as bordas de 12 e 19 px do original ficam excluídas pelo foco 53% 38% e zoom 1.9 aprovados. Nenhuma mudança aplicada ao YAML.
### 2027-01-02 · card-1

Antonello da Messina · A Virgem da Anunciação · Palazzo Abatellis, Palermo — https://commons.wikimedia.org/wiki/File:Antonello_da_Messina,_Annunciata_di_Palermo,_circa_1475-77_-FG2.jpg

Original local: `obras/toda-bela/2027-01-02.jpg`. Foco `50% 32%`, zoom `1.1`.

Janela original x=168.636364, y=231.311005, largura=3372.727273, altura=4127.153110 px; ampliação=0.180270.
Arquivo recortado: `saida/toda-bela/2027-01-02/obra-1.jpg`. Prova: `saida/toda-bela/2027-01-02/recorte-1.png`.
Dimensão do JPEG recortado: 1216 × 1488 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 0, "esquerda": 0, "direita": 0}, "faixas_descartadas": [], "margens_visiveis": []}`.

Card 1 final e recorte-1.png conferidos. O rosto de Maria, o véu azul inteiro e as duas mãos, a erguida e a que segura o véu, ficam dentro do arco; o atril com o livro aberto aparece na base. A curva passa acima do véu sem cortar a cabeça, e as bordas escuras do painel ficam fora. Não há margem fotográfica visível. Foco 50% 32% e zoom 1.1 mantidos.
### 2027-01-09 · card-1

Rafael · Madona della Seggiola · Palazzo Pitti, Florença — https://commons.wikimedia.org/wiki/File:Raphael_Madonna_della_seggiola.jpg

Original local: `obras/toda-bela/2027-01-09.jpg`. Foco `45% 40%`, zoom `1.3`.

Janela original x=257.493797, y=150.923077, largura=1027.791563, altura=1257.692308 px; ampliação=0.591560.
Arquivo recortado: `saida/toda-bela/2027-01-09/obra-1.jpg`. Prova: `saida/toda-bela/2027-01-09/recorte-1.png`.
Dimensão do JPEG recortado: 1028 × 1258 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 13, "base": 12, "esquerda": 13, "direita": 16}, "faixas_descartadas": [], "margens_visiveis": []}`.

Card 1 final e recorte-1.png conferidos. Os rostos de Maria e do Menino, o abraço e as pernas do Menino ficam dentro do arco, com o pilar entalhado da cadeira à esquerda. São João menino, à direita, aparece só em parte junto da curva, e a borda do tondo fica fora do arco. Não há margem fotográfica visível. Foco 45% 40% e zoom 1.3 mantidos.

## Avisos e pendências

- 2027-01-02, card 1: invocacao_assinatura_px: 118px; previsto 98px
- 2027-01-02, card 2: versiculo: 2 linhas; previsto 1; texto: 4 linhas; previsto 5; selo_texto_px: 210.5px; previsto 219.5px; texto_assinatura_px: 210.5px; previsto 219.5px
- 2027-01-09, card 2: versiculo: 2 linhas; previsto 1; texto: 4 linhas; previsto 5; selo_texto_px: 210.5px; previsto 219.5px; texto_assinatura_px: 210.5px; previsto 219.5px

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
saida/toda-bela/
  2026-12-12/card-1.png
  2026-12-12/card-2.png
  2026-12-12/card-3.png
  2026-12-12/ficha.json
  2026-12-12/obra-1.jpg
  2026-12-12/recorte-1.png
  2026-12-12/toda-bela-2026-12-12.pdf
  2026-12-26/card-1.png
  2026-12-26/card-2.png
  2026-12-26/card-3.png
  2026-12-26/ficha.json
  2026-12-26/obra-1.jpg
  2026-12-26/recorte-1.png
  2026-12-26/toda-bela-2026-12-26.pdf
  2027-01-02/card-1.png
  2027-01-02/card-2.png
  2027-01-02/card-3.png
  2027-01-02/ficha.json
  2027-01-02/obra-1.jpg
  2027-01-02/recorte-1.png
  2027-01-02/toda-bela-2027-01-02.pdf
  2027-01-09/card-1.png
  2027-01-09/card-2.png
  2027-01-09/card-3.png
  2027-01-09/ficha.json
  2027-01-09/obra-1.jpg
  2027-01-09/recorte-1.png
  2027-01-09/toda-bela-2027-01-09.pdf
  NOTAS-DAS-OBRAS.json
  RELATORIO.md
  prancha.png
  verificacao.json
```
