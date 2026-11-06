# Santo do Dia

`python gerar.py santo`

## Decisões

- Os dois modelos seguem os previews do kit v4: pergaminho, logo pergaminho, obra trocável no recorte CSS do nicho e foco do YAML. O filete é uma faixa vetorial em U; o parapeito mantém o retângulo original.
- Dentro do santinho, o conjunto obra e textos fica centralizado como no justify-content:center do kit. Frases de uma e três linhas mudam a altura do conjunto e, por isso, os nichos dos dois santos ficam em alturas diferentes.
- Festa de santo permanece santinho, com Santo do Dia no selo e o grau à direita. A festa do Senhor ou de Nossa Senhora usa o grau como série, sem informação à direita.
- A moldura dupla e o ornamento dos santinhos ficam em ouro, inclusive no mártir; só a cruz do selo e o filete do nicho seguem a cor litúrgica.
- O crédito da obra dos santinhos fica na ficha e neste relatório para a legenda. Na festa, também aparece sob o nicho. As frases recebem aspas curvas sem modificar o YAML.
- Quebras manuais viram <br>; as demais seguem o balanceamento do bundle.css. O espaço depois de a, à, e, é e o é inseparável. As linhas vazias forçadas também contam para os limites.
- A ficha mantém o formato do Evangelho e acrescenta as caixas, o padding e os afastamentos da moldura do cartão. As linhas são medidas no DOM com Range, depois do carregamento das seis fontes locais.
- A prancha usa miniaturas exatas de 360 × 450 px, lado a lado, e inclui todas as datas já geradas; --data preserva os arquivos das outras datas. HTMLs de apoio ficam em work/santo-do-dia.
- Os PDFs mantêm texto extraível e as fontes usadas embutidas; a festa não recebe uma exigência artificial de fonte itálica.
- O zoom amplia somente a imagem no foco, depois do object-fit:cover. O arco, a moldura e a composição ficam fixos. A ficha e o recorte registram a janela em pixels originais; margens uniformes visíveis geram aviso sem bloquear.

## Linhas medidas

| Data | Campo | Estilo | Linhas | Limite |
| --- | --- | --- | --- | --- |
| 2026-11-30 | selo | selo | 1 | — |
| 2026-11-30 | data | selo | 1 | — |
| 2026-11-30 | grau | selo | 1 | — |
| 2026-11-30 | nome | titulo | 1 | 1 |
| 2026-11-30 | titulo | corpo | 1 | 1 |
| 2026-11-30 | frase | citacao | 1 | 3 |
| 2026-11-30 | fonte | credito | 1 | 1 |
| 2026-12-01 | selo | selo | 1 | — |
| 2026-12-01 | data | selo | 1 | — |
| 2026-12-01 | grau | selo | 1 | — |
| 2026-12-01 | nome | titulo | 1 | 1 |
| 2026-12-01 | titulo | corpo | 1 | 1 |
| 2026-12-01 | frase | citacao | 2 | 3 |
| 2026-12-01 | fonte | credito | 1 | 1 |
| 2026-12-02 | selo | selo | 1 | — |
| 2026-12-02 | data | selo | 1 | — |
| 2026-12-02 | grau | selo | 1 | — |
| 2026-12-02 | nome | titulo | 1 | 1 |
| 2026-12-02 | titulo | corpo | 1 | 1 |
| 2026-12-02 | frase | citacao | 3 | 3 |
| 2026-12-02 | fonte | credito | 1 | 1 |
| 2026-12-03 | selo | selo | 1 | — |
| 2026-12-03 | data | selo | 1 | — |
| 2026-12-03 | grau | selo | 1 | — |
| 2026-12-03 | nome | titulo | 1 | 1 |
| 2026-12-03 | titulo | corpo | 1 | 1 |
| 2026-12-03 | frase | citacao | 3 | 3 |
| 2026-12-03 | fonte | credito | 1 | 1 |
| 2026-12-04 | selo | selo | 1 | — |
| 2026-12-04 | data | selo | 1 | — |
| 2026-12-04 | grau | selo | 1 | — |
| 2026-12-04 | nome | titulo | 1 | 1 |
| 2026-12-04 | titulo | corpo | 1 | 1 |
| 2026-12-04 | frase | citacao | 3 | 3 |
| 2026-12-04 | fonte | credito | 1 | 1 |
| 2026-12-05 | selo | selo | 1 | — |
| 2026-12-05 | data | selo | 1 | — |
| 2026-12-05 | credito | credito | 1 | 1 |
| 2026-12-05 | nome | titulo-capa | 1 | 2 |
| 2026-12-07 | selo | selo | 1 | — |
| 2026-12-07 | data | selo | 1 | — |
| 2026-12-07 | grau | selo | 1 | — |
| 2026-12-07 | nome | titulo | 1 | 1 |
| 2026-12-07 | titulo | corpo | 1 | 1 |
| 2026-12-07 | frase | citacao | 1 | 3 |
| 2026-12-07 | fonte | credito | 1 | 1 |
| 2026-12-08 | selo | selo | 1 | — |
| 2026-12-08 | data | selo | 1 | — |
| 2026-12-08 | credito | credito | 1 | 1 |
| 2026-12-08 | nome | titulo-capa | 2 | 2 |
| 2026-12-09 | selo | selo | 1 | — |
| 2026-12-09 | data | selo | 1 | — |
| 2026-12-09 | grau | selo | 1 | — |
| 2026-12-09 | nome | titulo | 1 | 1 |
| 2026-12-09 | titulo | corpo | 1 | 1 |
| 2026-12-09 | frase | citacao | 2 | 3 |
| 2026-12-09 | fonte | credito | 1 | 1 |
| 2026-12-10 | selo | selo | 1 | — |
| 2026-12-10 | data | selo | 1 | — |
| 2026-12-10 | grau | selo | 1 | — |
| 2026-12-10 | nome | titulo | 1 | 1 |
| 2026-12-10 | titulo | corpo | 1 | 1 |
| 2026-12-10 | frase | citacao | 3 | 3 |
| 2026-12-10 | fonte | credito | 1 | 1 |
| 2026-12-11 | selo | selo | 1 | — |
| 2026-12-11 | data | selo | 1 | — |
| 2026-12-11 | grau | selo | 1 | — |
| 2026-12-11 | nome | titulo | 1 | 1 |
| 2026-12-11 | titulo | corpo | 1 | 1 |
| 2026-12-11 | frase | citacao | 2 | 3 |
| 2026-12-11 | fonte | credito | 1 | 1 |
| 2026-12-12 | selo | selo | 1 | — |
| 2026-12-12 | data | selo | 1 | — |
| 2026-12-12 | credito | credito | 1 | 1 |
| 2026-12-12 | nome | titulo-capa | 2 | 2 |
| 2026-12-14 | selo | selo | 1 | — |
| 2026-12-14 | data | selo | 1 | — |
| 2026-12-14 | grau | selo | 1 | — |
| 2026-12-14 | nome | titulo | 1 | 1 |
| 2026-12-14 | titulo | corpo | 1 | 1 |
| 2026-12-14 | frase | citacao | 2 | 3 |
| 2026-12-14 | fonte | credito | 1 | 1 |
| 2026-12-15 | selo | selo | 1 | — |
| 2026-12-15 | data | selo | 1 | — |
| 2026-12-15 | grau | selo | 1 | — |
| 2026-12-15 | nome | titulo | 1 | 1 |
| 2026-12-15 | titulo | corpo | 1 | 1 |
| 2026-12-15 | frase | citacao | 3 | 3 |
| 2026-12-15 | fonte | credito | 1 | 1 |
| 2026-12-16 | selo | selo | 1 | — |
| 2026-12-16 | data | selo | 1 | — |
| 2026-12-16 | grau | selo | 1 | — |
| 2026-12-16 | nome | titulo | 1 | 1 |
| 2026-12-16 | titulo | corpo | 1 | 1 |
| 2026-12-16 | frase | citacao | 3 | 3 |
| 2026-12-16 | fonte | credito | 1 | 1 |
| 2026-12-24 | selo | selo | 1 | — |
| 2026-12-24 | data | selo | 1 | — |
| 2026-12-24 | grau | selo | 1 | — |
| 2026-12-24 | nome | titulo | 1 | 1 |
| 2026-12-24 | titulo | corpo | 1 | 1 |
| 2026-12-24 | frase | citacao | 1 | 3 |
| 2026-12-24 | fonte | credito | 1 | 1 |
| 2026-12-25 | selo | selo | 1 | — |
| 2026-12-25 | data | selo | 1 | — |
| 2026-12-25 | credito | credito | 1 | 1 |
| 2026-12-25 | nome | titulo-capa | 1 | 2 |
| 2026-12-26 | selo | selo | 1 | — |
| 2026-12-26 | data | selo | 1 | — |
| 2026-12-26 | grau | selo | 1 | — |
| 2026-12-26 | nome | titulo | 1 | 1 |
| 2026-12-26 | titulo | corpo | 1 | 1 |
| 2026-12-26 | frase | citacao | 3 | 3 |
| 2026-12-26 | fonte | credito | 1 | 1 |
| 2026-12-28 | selo | selo | 1 | — |
| 2026-12-28 | data | selo | 1 | — |
| 2026-12-28 | grau | selo | 1 | — |
| 2026-12-28 | nome | titulo | 1 | 1 |
| 2026-12-28 | titulo | corpo | 1 | 1 |
| 2026-12-28 | frase | citacao | 2 | 3 |
| 2026-12-28 | fonte | credito | 1 | 1 |
| 2026-12-29 | selo | selo | 1 | — |
| 2026-12-29 | data | selo | 1 | — |
| 2026-12-29 | grau | selo | 1 | — |
| 2026-12-29 | nome | titulo | 1 | 1 |
| 2026-12-29 | titulo | corpo | 1 | 1 |
| 2026-12-29 | frase | citacao | 2 | 3 |
| 2026-12-29 | fonte | credito | 1 | 1 |
| 2026-12-30 | selo | selo | 1 | — |
| 2026-12-30 | data | selo | 1 | — |
| 2026-12-30 | credito | credito | 1 | 1 |
| 2026-12-30 | nome | titulo-capa | 1 | 2 |
| 2026-12-31 | selo | selo | 1 | — |
| 2026-12-31 | data | selo | 1 | — |
| 2026-12-31 | credito | credito | 1 | 1 |
| 2026-12-31 | nome | titulo-capa | 1 | 2 |

## Obras e legendas

- **2026-11-30 — Santo André:** obra real local; recorte.png gerado.
  Simone Martini · Santo André · Metropolitan Museum — https://www.metmuseum.org/art/collection/search/437675
  Foco 45% 15%; zoom 1.05; janela original x=37.350, y=59.790, largura=1660.000, altura=2177.403px.
- **2026-12-01 — São Carlos de Foucauld:** obra real local; recorte.png gerado.
  Fotógrafo desconhecido · Carlos de Foucauld · Wikimedia Commons — https://commons.wikimedia.org/wiki/File:St_Charles_de_Foucauld.jpg
  Foco 50% 40%; zoom 1; janela original x=0.000, y=82.426, largura=1620.000, altura=2124.935px.
- **2026-12-02 — São Habacuque:** obra real local; recorte.png gerado.
  Juan Correa de Vivar · O profeta Habacuque · Museu do Prado — https://commons.wikimedia.org/wiki/File:El_profeta_Habacuc,_de_Juan_Correa_de_Vivar_(Museo_del_Prado).jpg
  Foco 52% 18%; zoom 1.22; janela original x=88.613, y=162.716, largura=774.590, altura=1016.021px.
- **2026-12-03 — São Francisco Xavier:** obra real local; recorte.png gerado.
  Autor desconhecido · São Francisco Xavier · Museu Municipal de Kobe — https://commons.wikimedia.org/wiki/File:Franciscus_de_Xabier.jpg
  Foco 50% 0%; zoom 1.3; janela original x=242.193, y=0.000, largura=1435.613, altura=1883.077px.
- **2026-12-04 — São João Damasceno:** obra real local; recorte.png gerado.
  Autor desconhecido · São João Damasceno · Afresco do Monte Athos — https://commons.wikimedia.org/wiki/File:Athonite_Fresco_Icon_of_Saint_John_of_Damascus_2.jpg
  Foco 50% 3%; zoom 1; janela original x=0.000, y=7.079, largura=1200.000, altura=1574.026px.
- **2026-12-05 — São Sabas:** obra real local; recorte.png gerado.
  Menológio de Basílio II · São Sabas · Biblioteca Apostólica Vaticana — https://commons.wikimedia.org/wiki/File:Sabbas_the_Sanctified_(Menologion_of_Basil_II).jpg
  Foco 28% 50%; zoom 1.12; janela original x=141.448, y=40.179, largura=572.827, altura=669.643px.
- **2026-12-07 — Santo Ambrósio:** obra real local; recorte.png gerado.
  Francisco de Zurbarán · Santo Ambrósio · Museu de Belas Artes de Sevilha — https://commons.wikimedia.org/wiki/File:Francisco_de_Zurbar%C3%A1n_032.jpg
  Foco 55% 0%; zoom 1.1; janela original x=62.800, y=0.000, largura=1141.818, altura=1497.710px.
- **2026-12-08 — Imaculada Conceição de Nossa Senhora:** obra real local; recorte.png gerado.
  Bartolomé Esteban Murillo · Imaculada dos Veneráveis · Museu do Prado — https://en.wikipedia.org/wiki/The_Immaculate_Conception_of_Los_Venerables
  Foco 50% 20%; zoom 1; janela original x=0.000, y=104.642, largura=1756.000, altura=2052.789px.
- **2026-12-09 — São João Diego:** obra real local; recorte.png gerado.
  Autor desconhecido · São João Diego com a tilma · 1737 — https://commons.wikimedia.org/wiki/File:San_Juan_Diego_con_el_ayate.jpg
  Foco 50% 30%; zoom 1.4; janela original x=314.571, y=266.671, largura=1572.857, altura=2063.098px.
- **2026-12-10 — Nossa Senhora de Loreto:** obra real local; recorte.png gerado.
  Lorenzo Lotto · A Anunciação · Museu Villa Colloredo Mels, Recanati — https://commons.wikimedia.org/wiki/File:Lorenzo_Lotto_066.jpg
  Foco 40% 100%; zoom 1.12; janela original x=105.814, y=597.430, largura=2204.464, altura=2891.570px.
- **2026-12-11 — São Dâmaso I:** obra real local; recorte.png gerado.
  Bíblia de São Marcial de Limoges · O papa Dâmaso · Biblioteca Nacional da França — https://commons.wikimedia.org/wiki/File:Pope_Damasus_-_Biblia_Sancti_Martialis_Lemovicensis,_Folio_4v.png
  Foco 50% 3%; zoom 1.05; janela original x=14.857, y=13.634, largura=594.286, altura=779.518px.
- **2026-12-12 — Nossa Senhora de Guadalupe:** obra real local; recorte.png gerado.
  Antonio e Manuel de Arellano · Virgem de Guadalupe · LACMA — https://collections.lacma.org/object/148372
  Foco 50% 40%; zoom 1; janela original x=0.000, y=301.859, largura=2777.000, altura=3246.352px.
- **2026-12-14 — São João da Cruz:** obra real local; recorte.png gerado.
  Atribuído a Francisco de Zurbarán · São João da Cruz · Museu Arquidiocesano de Katowice — https://commons.wikimedia.org/wiki/File:Zurbar%C3%A1n_(atribuido)-John_of_the_Cross-1656.jpg
  Foco 40% 5%; zoom 1.35; janela original x=70.785, y=10.422, largura=454.037, altura=595.556px.
- **2026-12-15 — Santa Virgínia Bracelli:** obra real local; recorte.png gerado.
  Mestre de Alkmaar · Dar de comer a quem tem fome · Rijksmuseum — https://commons.wikimedia.org/wiki/File:De_zeven_werken_van_barmhartigheid_Rijksmuseum_SK-A-2815-1.jpeg
  Foco 20% 62%; zoom 1.3; janela original x=146.954, y=1781.491, largura=2449.231, altura=3212.627px.
- **2026-12-16 — São Ageu:** obra real local; recorte.png gerado.
  Moretto da Brescia · O profeta Ageu · San Giovanni Evangelista, Brescia — https://commons.wikimedia.org/wiki/File:Profeta_Aggeo_(Moretto).jpg
  Foco 35% 50%; zoom 1.2; janela original x=269.056, y=188.000, largura=1433.267, altura=1880.000px.
- **2026-12-24 — Santos antepassados de Cristo:** obra real local; recorte.png gerado.
  Círculo de Geertgen tot Sint Jans · A árvore de Jessé · Rijksmuseum — https://www.rijksmuseum.nl/en/collection/SK-A-3901
  Foco 50% 0%; zoom 1.5; janela original x=320.000, y=0.000, largura=1280.000, altura=1678.961px.
- **2026-12-25 — Natal do Senhor:** obra real local; recorte.png gerado.
  Georges de La Tour · A adoração dos pastores · Museu do Louvre — https://collections.louvre.fr/ark:/53355/cl010065555
  Foco 28% 50%; zoom 1; janela original x=344.127, y=0.000, largura=2780.976, altura=3251.000px.
- **2026-12-26 — Santo Estêvão:** obra real local; recorte.png gerado.
  Carlo Crivelli · Santo Estêvão · National Gallery, Londres — https://www.nationalgallery.org.uk/paintings/carlo-crivelli-saint-stephen
  Foco 50% 5%; zoom 1.1; janela original x=87.273, y=32.425, largura=1745.455, altura=2289.492px.
- **2026-12-28 — Santos Inocentes:** obra real local; recorte.png gerado.
  Vittore Carpaccio · A fuga para o Egito · National Gallery of Art — https://www.nga.gov/collection/art-object-page.32.html
  Foco 26% 50%; zoom 1; janela original x=252.617, y=0.000, largura=948.396, altura=1244.000px.
- **2026-12-29 — São Tomás Becket:** obra real local; recorte.png gerado.
  Autor desconhecido · Cena da vida de São Tomás Becket · Harvard Art Museums — https://harvardartmuseums.org/art/231842
  Foco 50% 55%; zoom 1.35; janela original x=418.995, y=273.207, largura=1082.010, altura=1419.259px.
- **2026-12-30 — Sexto dia do Natal:** obra real local; recorte.png gerado.
  Bartolomé Esteban Murillo · A Sagrada Família do passarinho · Museu do Prado — https://commons.wikimedia.org/wiki/File:Sagrada_Familia_del_pajarito_(Murillo).jpg
  Foco 16% 50%; zoom 1; janela original x=175.007, y=0.000, largura=1957.205, altura=2288.000px.
- **2026-12-31 — São Silvestre I:** obra real local; recorte.png gerado.
  Autor desconhecido · São Silvestre · Biblioteca Nacional da França — https://commons.wikimedia.org/wiki/File:Pape_St_Sylvestre_%E2%80%93_BnF,_ms_16251,_fol._87.jpg
  Foco 50% 5%; zoom 1; janela original x=0.000, y=22.962, largura=963.000, altura=1125.761px.
Nenhuma margem uniforme da foto está visível nos enquadramentos selecionados.

Obras pendentes: nenhuma.

## Conferências

PNG 1080 × 1350; PDF de uma página em 810 × 1012,5 pt; textos extraíveis; TTF embutidos e pdffonts; limites de linhas e largura; palavras de uma letra; área interna e afastamento do filete; cruz, nicho e moldura por pixel. Os dados completos estão em verificacao.json e nas fichas.
Em cada PDF, PyMuPDF exige um único preenchimento curvo na caixa do nicho, ausência da borda antiga feita de retângulos recortados e um parapeito retangular separado de 3 px. Uma falha interrompe a geração; o resultado está em nicho_vetorial, dentro da verificação do PDF.

### Regressão dos modelos com o kit v4

Conferência aprovada.

Base: `8365dc125c76e859633026c949322966fd111e29`.

Componentes: 28/28 PNGs com pixels idênticos.

evangelho, 2026-11-29: textos, linhas, estilos e caixas idênticos; cards 2, 3, 4 com pixels idênticos; o foco/zoom mudou somente a área da obra.

evangelho, 2026-12-13: textos, linhas, estilos e caixas idênticos; cards 2, 3, 4 com pixels idênticos; o foco/zoom mudou somente a área da obra.

santo-do-dia, 2026-11-30: textos, linhas, estilos e caixas idênticos; o foco/zoom mudou somente a área da obra.

santo-do-dia, 2026-12-03: textos, linhas, estilos e caixas idênticos; o foco/zoom mudou somente a área da obra.

santo-do-dia, 2026-12-08: textos, linhas, estilos e caixas idênticos; o foco/zoom mudou somente a área da obra.

Detalhes: [`CONFERENCIA-KIT-V4.md`](../CONFERENCIA-KIT-V4.md) e [`conferencia-kit-v4.json`](../verificacao/conferencia-kit-v4.json).

### Limites da verificação

A importação no editor do Canva não foi executada. A validação confere os arquivos produzidos, suas fontes, textos, cores e geometria. As obras foram usadas como entregues no repositório, sem downloads.

<!-- inicio-prompt13 -->
## Prompt 13 · 19 cards novos de dezembro

Baseline: main no commit `d927cff3137544b10db92fe90b930acb793c69a9`. O gerador, os modelos, o kit, o ZIP e as obras não foram alterados. A série contém 22 dias: 19 novos e os três anteriores preservados.

SHA-256 do YAML copiado literalmente do anexo: `6771584f26af24d19b573c0627c5224139ccbbd6d6386910839acc22ab6506fa`. O diff contém somente 269 linhas acrescentadas.

### Controle do ambiente e prova final

PNG comparado pixel a pixel; PDFs comparados página a página com PyMuPDF a 2×. Todos os arquivos abaixo têm zero pixel diferente nas duas etapas.

| Arquivo | Controle: pixels diferentes | Prova final: pixels diferentes | Maior diferença por canal nas duas etapas |
| --- | ---: | ---: | ---: |
| 2026-11-30/card.png | 0 | 0 | 0 |
| 2026-11-30/recorte.png | 0 | 0 | 0 |
| 2026-11-30/santo-2026-11-30.pdf · página 1 a 2× | 0 | 0 | 0 |
| 2026-12-03/card.png | 0 | 0 | 0 |
| 2026-12-03/recorte.png | 0 | 0 | 0 |
| 2026-12-03/santo-2026-12-03.pdf · página 1 a 2× | 0 | 0 | 0 |
| 2026-12-08/card.png | 0 | 0 | 0 |
| 2026-12-08/recorte.png | 0 | 0 | 0 |
| 2026-12-08/santo-2026-12-08.pdf · página 1 a 2× | 0 | 0 | 0 |

As três fichas são iguais nas duas etapas, exceto pelo campo `source` da obra, que registra a porta do servidor local. Após a prova, as pastas de 30/11, 3/12 e 8/12 foram restauradas ao commit de referência; nenhum de seus arquivos faz parte da alteração entregue.

412 arquivos anteriores protegidos permanecem idênticos byte a byte. Isso inclui as outras séries, o código fora dos três testes autorizados, os três dias antigos, as obras e o ZIP. Os 44 arquivos de kit/ também coincidem com o ZIP.

### Medidas dos 19 cards novos

As janelas estão em pixels da imagem original, no formato largura × altura. O zoom omitido no YAML é 1. Os cards do tipo festa não têm frase.

| Data | Tipo | Linhas: nome | Linhas: frase | Foco | Zoom | Janela da obra (px) |
| --- | --- | ---: | ---: | --- | ---: | --- |
| 2026-12-01 | santinho | 1 | 2 | 50% 40% | 1 | 1620.00 × 2124.94 |
| 2026-12-02 | santinho | 1 | 3 | 52% 18% | 1.22 | 774.59 × 1016.02 |
| 2026-12-04 | santinho | 1 | 3 | 50% 3% | 1 | 1200.00 × 1574.03 |
| 2026-12-05 | festa | 1 | — | 28% 50% | 1.12 | 572.83 × 669.64 |
| 2026-12-07 | santinho | 1 | 1 | 55% 0% | 1.1 | 1141.82 × 1497.71 |
| 2026-12-09 | santinho | 1 | 2 | 50% 30% | 1.4 | 1572.86 × 2063.10 |
| 2026-12-10 | santinho | 1 | 3 | 40% 100% | 1.12 | 2204.46 × 2891.57 |
| 2026-12-11 | santinho | 1 | 2 | 50% 3% | 1.05 | 594.29 × 779.52 |
| 2026-12-12 | festa | 2 | — | 50% 40% | 1 | 2777.00 × 3246.35 |
| 2026-12-14 | santinho | 1 | 2 | 40% 5% | 1.35 | 454.04 × 595.56 |
| 2026-12-15 | santinho | 1 | 3 | 20% 62% | 1.3 | 2449.23 × 3212.63 |
| 2026-12-16 | santinho | 1 | 3 | 35% 50% | 1.2 | 1433.27 × 1880.00 |
| 2026-12-24 | santinho | 1 | 1 | 50% 0% | 1.5 | 1280.00 × 1678.96 |
| 2026-12-25 | festa | 1 | — | 28% 50% | 1 | 2780.98 × 3251.00 |
| 2026-12-26 | santinho | 1 | 3 | 50% 5% | 1.1 | 1745.45 × 2289.49 |
| 2026-12-28 | santinho | 1 | 2 | 26% 50% | 1 | 948.40 × 1244.00 |
| 2026-12-29 | santinho | 1 | 2 | 50% 55% | 1.35 | 1082.01 × 1419.26 |
| 2026-12-30 | festa | 1 | — | 16% 50% | 1 | 1957.20 × 2288.00 |
| 2026-12-31 | festa | 1 | — | 50% 5% | 1 | 963.00 × 1125.76 |

Os dias 10/12 e 26/12 mantêm as três linhas exatamente nas quebras manuais do YAML. Nenhuma obra está pendente, nenhuma margem uniforme está visível e todos os 22 PDFs passam na verificação de texto extraível, fontes embutidas e filete vetorial, sem alterar tolerâncias.

5/12 é o único enquadramento cuja janela é menor que a largura nominal do nicho: 572,83 px para um nicho de 600 px, conforme aprovado no prompt. Nenhuma outra obra apresenta essa condição. A fotografia de 1/12 permanece em seu JPEG original em tons de cinza.

Os tipos festa sem frase de 5/12, 30/12 e 31/12 foram mantidos literalmente. Graus, traduções bíblicas e exceções de fonte também foram preservados; o texto original de Decisões do gerador não foi modificado.

### Testes

- `tests/test_conteudo_santo.py`: espera as 22 datas e seus tipos; exemplos de santinho e festa são escolhidos por data, mantendo as verificações anteriores.
- `tests/test_layout_santo.py`: escolhe Santo André em 30/11 e a Imaculada em 8/12 por data; as verificações de limites e geometria permanecem iguais.
- `tests/test_obras.py`: separa as quatro obras com borda do teste geral; o novo teste confere as bordas detectadas e exige margens_visiveis e avisos vazios nos focos, zooms e tamanhos de nicho aprovados.

Suíte completa: 195 testes passaram. Nenhum outro arquivo de teste foi alterado.

### Pendências

Nenhuma pendência técnica. Os 19 PDFs novos estão prontos para importar no Canva.
<!-- fim-prompt13 -->

## Árvore

```text
saida/santo-do-dia/
  2026-11-30/card.png
  2026-11-30/ficha.json
  2026-11-30/recorte.png
  2026-11-30/santo-2026-11-30.pdf
  2026-12-01/card.png
  2026-12-01/ficha.json
  2026-12-01/recorte.png
  2026-12-01/santo-2026-12-01.pdf
  2026-12-02/card.png
  2026-12-02/ficha.json
  2026-12-02/recorte.png
  2026-12-02/santo-2026-12-02.pdf
  2026-12-03/card.png
  2026-12-03/ficha.json
  2026-12-03/recorte.png
  2026-12-03/santo-2026-12-03.pdf
  2026-12-04/card.png
  2026-12-04/ficha.json
  2026-12-04/recorte.png
  2026-12-04/santo-2026-12-04.pdf
  2026-12-05/card.png
  2026-12-05/ficha.json
  2026-12-05/recorte.png
  2026-12-05/santo-2026-12-05.pdf
  2026-12-07/card.png
  2026-12-07/ficha.json
  2026-12-07/recorte.png
  2026-12-07/santo-2026-12-07.pdf
  2026-12-08/card.png
  2026-12-08/ficha.json
  2026-12-08/recorte.png
  2026-12-08/santo-2026-12-08.pdf
  2026-12-09/card.png
  2026-12-09/ficha.json
  2026-12-09/recorte.png
  2026-12-09/santo-2026-12-09.pdf
  2026-12-10/card.png
  2026-12-10/ficha.json
  2026-12-10/recorte.png
  2026-12-10/santo-2026-12-10.pdf
  2026-12-11/card.png
  2026-12-11/ficha.json
  2026-12-11/recorte.png
  2026-12-11/santo-2026-12-11.pdf
  2026-12-12/card.png
  2026-12-12/ficha.json
  2026-12-12/recorte.png
  2026-12-12/santo-2026-12-12.pdf
  2026-12-14/card.png
  2026-12-14/ficha.json
  2026-12-14/recorte.png
  2026-12-14/santo-2026-12-14.pdf
  2026-12-15/card.png
  2026-12-15/ficha.json
  2026-12-15/recorte.png
  2026-12-15/santo-2026-12-15.pdf
  2026-12-16/card.png
  2026-12-16/ficha.json
  2026-12-16/recorte.png
  2026-12-16/santo-2026-12-16.pdf
  2026-12-24/card.png
  2026-12-24/ficha.json
  2026-12-24/recorte.png
  2026-12-24/santo-2026-12-24.pdf
  2026-12-25/card.png
  2026-12-25/ficha.json
  2026-12-25/recorte.png
  2026-12-25/santo-2026-12-25.pdf
  2026-12-26/card.png
  2026-12-26/ficha.json
  2026-12-26/recorte.png
  2026-12-26/santo-2026-12-26.pdf
  2026-12-28/card.png
  2026-12-28/ficha.json
  2026-12-28/recorte.png
  2026-12-28/santo-2026-12-28.pdf
  2026-12-29/card.png
  2026-12-29/ficha.json
  2026-12-29/recorte.png
  2026-12-29/santo-2026-12-29.pdf
  2026-12-30/card.png
  2026-12-30/ficha.json
  2026-12-30/recorte.png
  2026-12-30/santo-2026-12-30.pdf
  2026-12-31/card.png
  2026-12-31/ficha.json
  2026-12-31/recorte.png
  2026-12-31/santo-2026-12-31.pdf
  RELATORIO.md
  prancha.png
  verificacao.json
```
