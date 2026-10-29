# Coragem

`python gerar.py coragem`

## Composição e decisões

- Tema pergaminho; o feed segue PostCoragem e o status usa a mesma composição com aqr-post--story, sem substituir os 240 px de padding superior e inferior do kit.
- Nichos de 600 × 680 no feed e 720 × 900 no status, com img dentro do arco, object-fit:cover, foco e zoom depois do cover. O crédito da obra permanece somente na ficha para uso na legenda.
- Frase em citacao-grande e referência livre em referencia/ouro, centralizadas entre nicho e assinatura; a assinatura inclui @artequereza.oficial nos dois formatos.
- Quebras manuais são preservadas; as demais linhas são equilibradas pelo CSS do kit. Palavras de uma letra ficam ligadas à seguinte. As linhas vazias também contam para o limite.
- Cada formato recebe seu PDF, porque os designs do Canva têm um tamanho único. Os recortes mostram a obra inteira a 1080 px de largura com a janela do arco, já considerando o zoom.
- As obras reais fornecidas no repositório foram usadas sem downloads. Avisos e recomendações abaixo não alteram coragem.yaml nem o enquadramento pedido.

## Linhas e distâncias

| Data | Formato | Frase (limite 2) | Referência (limite 1) | Parapeito → frase | Referência → assinatura |
| --- | --- | --- | --- | --- | --- |
| 2026-12-14 | feed | 2 | 1 | 66 px | 69 px |
| 2026-12-14 | status | 2 | 1 | 81 px | 84 px |
| 2026-12-28 | feed | 2 | 1 | 66 px | 69 px |
| 2026-12-28 | status | 2 | 1 | 81 px | 84 px |

## Obras, foco e zoom

- **2026-12-14:** obra real local; recortes de feed e status gerados.
  Michelangelo · O profeta Isaías · Capela Sistina — https://en.wikipedia.org/wiki/Prophet_Isaiah_(Michelangelo)
  - feed: foco `50% 0%`, zoom `1.0`; janela original x=0, y=0, largura=1500, altura=1753.52 px.
  - status: foco `50% 0%`, zoom `1.0`; janela original x=0, y=0, largura=1500, altura=1927.33 px.
- **2026-12-28:** obra real local; recortes de feed e status gerados.
  Jacopo Bassano · A Anunciação aos pastores · National Gallery of Art — https://www.nga.gov/artworks/267-annunciation-shepherds
  - feed: foco `50% 50%`, zoom `1.0`; janela original x=0, y=133.782, largura=1961, altura=2292.44 px.
  - status: foco `50% 50%`, zoom `1.0`; janela original x=1.13687e-13, y=20.1715, largura=1961, altura=2519.66 px.

## Revisão visual das obras

As duas obras reais do Coragem foram usadas nos formatos feed e status. O foco de Isaías em 14/12 foi atualizado para `50% 0%`, sem zoom, conforme o prompt 5. Em 28/12, o foco permanece `50% 50%`, sem zoom. Nenhum dos quatro enquadramentos disparou o detector de margem uniforme da foto.

- **14/12 — Isaías:** o foco recomendado `50% 0%`, zoom `1`, foi aplicado ao `coragem.yaml` e às artes finais de feed e status. A cabeça aparece inteira nos dois formatos; a observação anterior sobre seu corte não se aplica mais. Os dois recortes finais mostram a janela atual, sem margem uniforme visível.
- **28/12 — Anunciação aos pastores:** os enquadramentos foram inspecionados; o foco original foi mantido nos dois formatos.

A revisão da cabeça de Isaías é uma avaliação visual do recorte, distinta do aviso técnico de margem uniforme. A comparação com a main está em `saida/CONFERENCIA-PROMPT-5.md`: apenas a obra de 14/12 pode mudar; texto, cores, geometria e todas as artes de 28/12 são preservados.

Obras pendentes: nenhuma.
Avisos de margem: nenhum nos dois formatos das obras reais fornecidas.

## Conferências e limites

Foram conferidos dimensões dos PNGs, cores da cruz e do filete por pixel, linhas reais com Range, limites e distâncias. PDFs com uma página em 810 × 1012,5 pt no feed e 810 × 1440 pt no status; fontes TTF usadas embutidas por pdffonts e texto do YAML verificado por pdftotext desconsiderando espaços e quebras.

A importação no editor do Canva não foi executada. As margens são diagnosticadas pelo critério objetivo de linhas/colunas uniformes da foto; a recomendação conserva a arte gerada e serve para ajuste posterior.

## Árvore

```text
saida/coragem/
  2026-12-14/coragem-2026-12-14-feed.pdf
  2026-12-14/coragem-2026-12-14-status.pdf
  2026-12-14/feed.png
  2026-12-14/ficha.json
  2026-12-14/recorte-feed.png
  2026-12-14/recorte-status.png
  2026-12-14/status.png
  2026-12-28/coragem-2026-12-28-feed.pdf
  2026-12-28/coragem-2026-12-28-status.pdf
  2026-12-28/feed.png
  2026-12-28/ficha.json
  2026-12-28/recorte-feed.png
  2026-12-28/recorte-status.png
  2026-12-28/status.png
  NOTAS-DE-ENQUADRAMENTO.md
  RELATORIO.md
  prancha.png
  verificacao.json
```
