# Evangelho do Dia

`python gerar.py evangelho` · seleção: `python gerar.py evangelho --data AAAA-MM-DD`

## Decisões

- Composição, medidas e espaços seguem PostEvangelho/preview.html e bundle.css; a capa usa um img dentro do arco CSS, sem SVG sobre a imagem.
- O card final resolve a cor no tema pergaminho e usa o logo sobre-cor da versão 2. Os demais usam capela.
- Textos sem quebras manuais usam balanceamento do navegador, inclusive o corpo da reflexão. Quebras YAML são `<br>`; espaços após a, à, e, é e o são inseparáveis.
- O selo tem ficha separada para série e data porque as cores e pesos diferem. As caixas são do DOM e as linhas são medidas com Range, depois do carregamento das seis fontes locais.
- A prancha de cores usa ouro como alias de liturgico-branco. As miniaturas medem exatamente 360 × 450 px; etiquetas ficam fora dos cards. A prancha principal indexa todas as datas já geradas, preservando as demais ao usar --data.
- Só obras reais recebem recorte.png; nenhum recurso externo é acessado. Os HTML e PDFs de uma página usados na composição ficam em work/ e não são necessários para importar os PDFs finais.

## Linhas medidas no render

| Data | Card | Campo | Estilo | Linhas | Limite |
| --- | --- | --- | --- | --- | --- |
| 2026-11-29 | 1 | selo | selo | 1 | — |
| 2026-11-29 | 1 | data | selo | 1 | — |
| 2026-11-29 | 1 | referencia | selo | 1 | — |
| 2026-11-29 | 1 | credito | credito | 1 | 1 |
| 2026-11-29 | 1 | titulo | titulo | 2 | 2 |
| 2026-11-29 | 2 | selo | selo | 1 | — |
| 2026-11-29 | 2 | data | selo | 1 | — |
| 2026-11-29 | 2 | referencia | selo | 1 | — |
| 2026-11-29 | 2 | trecho | citacao-grande | 2 | 3 |
| 2026-11-29 | 2 | trecho_ref | referencia | 1 | — |
| 2026-11-29 | 3 | selo | selo | 1 | — |
| 2026-11-29 | 3 | data | selo | 1 | — |
| 2026-11-29 | 3 | referencia | selo | 1 | — |
| 2026-11-29 | 3 | chamada_reflexao | selo | 1 | — |
| 2026-11-29 | 3 | reflexao.titulo | titulo | 1 | 2 |
| 2026-11-29 | 3 | reflexao.texto | corpo | 5 | 6 |
| 2026-11-29 | 4 | selo | selo | 1 | — |
| 2026-11-29 | 4 | data | selo | 1 | — |
| 2026-11-29 | 4 | referencia | selo | 1 | — |
| 2026-11-29 | 4 | chamada_oracao | selo | 1 | — |
| 2026-11-29 | 4 | pergunta | citacao | 2 | 4 |
| 2026-11-29 | 4 | convite | corpo | 1 | 1 |
| 2026-12-13 | 1 | selo | selo | 1 | — |
| 2026-12-13 | 1 | data | selo | 1 | — |
| 2026-12-13 | 1 | referencia | selo | 1 | — |
| 2026-12-13 | 1 | credito | credito | 1 | 1 |
| 2026-12-13 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-13 | 2 | selo | selo | 1 | — |
| 2026-12-13 | 2 | data | selo | 1 | — |
| 2026-12-13 | 2 | referencia | selo | 1 | — |
| 2026-12-13 | 2 | trecho | citacao-grande | 2 | 3 |
| 2026-12-13 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-13 | 3 | selo | selo | 1 | — |
| 2026-12-13 | 3 | data | selo | 1 | — |
| 2026-12-13 | 3 | referencia | selo | 1 | — |
| 2026-12-13 | 3 | chamada_reflexao | selo | 1 | — |
| 2026-12-13 | 3 | reflexao.titulo | titulo | 1 | 2 |
| 2026-12-13 | 3 | reflexao.texto | corpo | 4 | 6 |
| 2026-12-13 | 4 | selo | selo | 1 | — |
| 2026-12-13 | 4 | data | selo | 1 | — |
| 2026-12-13 | 4 | referencia | selo | 1 | — |
| 2026-12-13 | 4 | chamada_oracao | selo | 1 | — |
| 2026-12-13 | 4 | pergunta | citacao | 2 | 4 |
| 2026-12-13 | 4 | convite | corpo | 1 | 1 |

## Obras e legendas

- **2026-11-29 — 1º Domingo do Advento:** obra local real; recorte.png gerado.
  James Tissot · A profecia da destruição do Templo · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4551
- **2026-12-13 — 3º Domingo do Advento (Gaudete):** obra local real; recorte.png gerado.
  James Tissot · São João Batista e os fariseus · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4449

## Conferência

PNG exatos; limites de linhas; palavras de uma letra; afastamento de 32 px; centralização vertical; cruz, fundo e filete por pixel; páginas PDF de 810 × 1012,5 pt; quatro variantes embutidas por pdffonts; título e convite extraíveis. Os valores estão em verificacao.json e ficha.json.

A importação dentro do editor do Canva não foi executada; a validação cobre o arquivo produzido (texto, fontes e dimensões), não o comportamento do editor.

Todas as obras selecionadas foram encontradas localmente e receberam prova de recorte.

## Árvore

```text
saida/evangelho/
  2026-11-29/card-1.png
  2026-11-29/card-2.png
  2026-11-29/card-3.png
  2026-11-29/card-4.png
  2026-11-29/evangelho-2026-11-29.pdf
  2026-11-29/ficha.json
  2026-11-29/recorte.png
  2026-12-13/card-1.png
  2026-12-13/card-2.png
  2026-12-13/card-3.png
  2026-12-13/card-4.png
  2026-12-13/evangelho-2026-12-13.pdf
  2026-12-13/ficha.json
  2026-12-13/recorte.png
  CONFERENCIA-KIT-V3.md
  RELATORIO.md
  conferencia-kit-v3.json
  prancha-cores.png
  prancha.png
  verificacao.json
```
