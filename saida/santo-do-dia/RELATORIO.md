# Santo do Dia

`python gerar.py santo`

## Decisões

- Os dois modelos seguem os previews do kit v4: pergaminho, logo pergaminho, Nicho CSS com imagem trocável, foco do YAML e nenhuma sobreposição SVG.
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
| 2026-12-03 | selo | selo | 1 | — |
| 2026-12-03 | data | selo | 1 | — |
| 2026-12-03 | grau | selo | 1 | — |
| 2026-12-03 | nome | titulo | 1 | 1 |
| 2026-12-03 | titulo | corpo | 1 | 1 |
| 2026-12-03 | frase | citacao | 3 | 3 |
| 2026-12-03 | fonte | credito | 1 | 1 |
| 2026-12-08 | selo | selo | 1 | — |
| 2026-12-08 | data | selo | 1 | — |
| 2026-12-08 | credito | credito | 1 | 1 |
| 2026-12-08 | nome | titulo-capa | 2 | 2 |

## Obras e legendas

- **2026-11-30 — Santo André:** obra real local; recorte.png gerado.
  Simone Martini · Santo André · Metropolitan Museum — https://www.metmuseum.org/art/collection/search/437675
  Foco 45% 15%; zoom 1.05; janela original x=37.350, y=59.790, largura=1660.000, altura=2177.403px.
- **2026-12-03 — São Francisco Xavier:** obra real local; recorte.png gerado.
  Autor desconhecido · São Francisco Xavier · Museu Municipal de Kobe — https://commons.wikimedia.org/wiki/File:Franciscus_de_Xabier.jpg
  Foco 50% 0%; zoom 1.3; janela original x=242.193, y=0.000, largura=1435.613, altura=1883.077px.
- **2026-12-08 — Imaculada Conceição de Nossa Senhora:** obra real local; recorte.png gerado.
  Bartolomé Esteban Murillo · Imaculada dos Veneráveis · Museu do Prado — https://en.wikipedia.org/wiki/The_Immaculate_Conception_of_Los_Venerables
  Foco 50% 20%; zoom 1; janela original x=0.000, y=104.642, largura=1756.000, altura=2052.789px.
Nenhuma margem uniforme da foto está visível nos enquadramentos selecionados.

Obras pendentes: nenhuma.

## Conferências

PNG 1080 × 1350; PDF de uma página em 810 × 1012,5 pt; textos extraíveis; TTF embutidos e pdffonts; limites de linhas e largura; palavras de uma letra; área interna e afastamento do filete; cruz, nicho e moldura por pixel. Os dados completos estão em verificacao.json e nas fichas.

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

## Árvore

```text
saida/santo-do-dia/
  2026-11-30/card.png
  2026-11-30/ficha.json
  2026-11-30/recorte.png
  2026-11-30/santo-2026-11-30.pdf
  2026-12-03/card.png
  2026-12-03/ficha.json
  2026-12-03/recorte.png
  2026-12-03/santo-2026-12-03.pdf
  2026-12-08/card.png
  2026-12-08/ficha.json
  2026-12-08/recorte.png
  2026-12-08/santo-2026-12-08.pdf
  RELATORIO.md
  prancha.png
  verificacao.json
```
