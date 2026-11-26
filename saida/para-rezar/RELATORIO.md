# Para Rezar

`python gerar.py para-rezar --data 2026-12-31`

## Decisões

- Composição dos três artigos do PostOracao do kit v4: mesmas classes, estilos inline, fontes, bundle.css e espaços. O confronto solicitado renderiza a vitrine original inteira e recorta cada article. O isolamento do article na origem 0,0 é só um diagnóstico adicional, sem substituir o resultado da vitrine.
- Cada item de partes gera um card; não há divisão automática. Título e ornamento ficam no primeiro, origem somente no último e a intenção dá lugar à contagem nos seguintes.
- O bloco inteiro usa margin-top:auto junto à assinatura, como a prévia, deixando respiros iguais acima e abaixo. As distâncias medidas estão também em cada ficha.
- Quebras manuais são preservadas; os demais textos seguem o balanceamento do bundle. Espaços após a, à, e, é e o são inseparáveis. Linhas vazias forçadas também entram na contagem.
- A ficha mantém o formato das séries anteriores, com linhas recuperadas por Range. A prancha usa miniaturas de 360 × 450 px e indexa todas as datas já geradas; --data preserva as demais.
- São Miguel de 20/10 é uma prova do design system e não é publicação. Não há obras nesta série.
- As palavras hifenizadas permanecem inteiras pelo helper da Igreja Doméstica, importado sem modificações. Os textos de 29 e 31/12 foram aprovados em 19/11/2026.

## Linhas medidas no render

| Data | Card | Campo | Linhas | Limite |
| --- | --- | --- | --- | --- |
| 2026-12-31 | 1 | selo | 1 | — |
| 2026-12-31 | 1 | data | 1 | — |
| 2026-12-31 | 1 | intencao | 1 | — |
| 2026-12-31 | 1 | titulo | 1 | 2 |
| 2026-12-31 | 1 | oracao | 8 | 10 |
| 2026-12-31 | 2 | selo | 1 | — |
| 2026-12-31 | 2 | data | 1 | — |
| 2026-12-31 | 2 | contagem | 1 | — |
| 2026-12-31 | 2 | oracao | 11 | 14 |
| 2026-12-31 | 3 | selo | 1 | — |
| 2026-12-31 | 3 | data | 1 | — |
| 2026-12-31 | 3 | contagem | 1 | — |
| 2026-12-31 | 3 | oracao | 12 | 14 |
| 2026-12-31 | 3 | origem | 1 | — |

## Distâncias

| Data | Card | Selo → texto | Texto → assinatura |
| --- | --- | --- | --- |
| 2026-12-31 | 1 | 204.5 px | 204.5 px |
| 2026-12-31 | 2 | 208 px | 208 px |
| 2026-12-31 | 3 | 137 px | 137 px |

## Conferência da prévia

- **2026-10-20, card 1: vitrine inteira — 125 pixels diferentes; diagnóstico isolado — 0.**
  Diferença: `work/para-rezar/conferencia-kit/vitrine-diferenca-1.png`; caixa [404, 1221, 533, 1259]. Rasterização do SVG em posições globais diferentes na vitrine e no PNG; nenhum ajuste foi aplicado à composição.
- **2026-12-15, card 1: vitrine inteira — 93 pixels diferentes; diagnóstico isolado — 0.**
  Diferença: `work/para-rezar/conferencia-kit/vitrine-diferenca-2.png`; caixa [404, 1221, 533, 1259]. Rasterização do SVG em posições globais diferentes na vitrine e no PNG; nenhum ajuste foi aplicado à composição.
- **2026-12-15, card 2: vitrine inteira — 114 pixels diferentes; diagnóstico isolado — 0.**
  Diferença: `work/para-rezar/conferencia-kit/vitrine-diferenca-3.png`; caixa [404, 1221, 533, 1259]. Rasterização do SVG em posições globais diferentes na vitrine e no PNG; nenhum ajuste foi aplicado à composição.

O confronto literal solicitado não deu zero. As diferenças ficaram confinadas ao SVG do logo; nenhum outro pixel mudou. O diagnóstico com cada article original intacto na mesma origem do PNG deu zero, indicando rasterização do SVG em posições globais diferentes. Os PNGs de referência e diferenças estão em work/para-rezar/conferencia-kit/.

## Avisos e pendências

- 2026-10-20, card 1: confronto da vitrine inteira tem 125 pixels diferentes, confinados ao SVG do logo; o article isolado na origem 0,0 tem zero. Diferença salva em work/para-rezar/conferencia-kit/vitrine-diferenca-1.png.
- 2026-12-15, card 1: confronto da vitrine inteira tem 93 pixels diferentes, confinados ao SVG do logo; o article isolado na origem 0,0 tem zero. Diferença salva em work/para-rezar/conferencia-kit/vitrine-diferenca-2.png.
- 2026-12-15, card 2: confronto da vitrine inteira tem 114 pixels diferentes, confinados ao SVG do logo; o article isolado na origem 0,0 tem zero. Diferença salva em work/para-rezar/conferencia-kit/vitrine-diferenca-3.png.

## PDF e limites da verificação

Páginas de 810 × 1012,5 pt (1080 × 1350 px), uma por parte; fontes TTF usadas embutidas e listadas por pdffonts. O texto integral extraído por pdftotext -layout corresponde aos campos do YAML, desconsiderando espaços e quebras. A opção -layout mantém o contador do topo na ordem visual; a heurística padrão de colunas podia movê-lo para o fim da página.

A importação no editor do Canva não foi executada. A validação cobre o arquivo produzido, suas fontes, textos, cores, dimensões e geometria.

## Árvore

```text
saida/para-rezar/
  2026-10-20/card-1.png
  2026-10-20/ficha.json
  2026-10-20/para-rezar-2026-10-20.pdf
  2026-12-15/card-1.png
  2026-12-15/card-2.png
  2026-12-15/ficha.json
  2026-12-15/para-rezar-2026-12-15.pdf
  2026-12-29/card-1.png
  2026-12-29/card-2.png
  2026-12-29/ficha.json
  2026-12-29/para-rezar-2026-12-29.pdf
  2026-12-31/card-1.png
  2026-12-31/card-2.png
  2026-12-31/card-3.png
  2026-12-31/ficha.json
  2026-12-31/para-rezar-2026-12-31.pdf
  RELATORIO.md
  prancha.png
  verificacao.json
```

## Compatibilidade dos cards aprovados

As datas de 20/10 e 15/12 preservam seu HTML histórico, cujos hífens já cabem inteiros. As datas novas e futuras usam o helper intacto da Igreja Doméstica. A validação rejeita hífen no fim da linha em todas as datas. A regeneração dos três cards antigos deu zero pixels diferentes nos PNGs e nas páginas PDF a 2×; a ocorrência inicial de 318 pixels foi resolvida, sem tolerância de antialiasing.

### Janeiro de 2027: 1º a 10/1

Gerado em 23/11/2026 com `python gerar.py para-rezar --data 2027-01-05`: À vossa proteção (Sub tuum praesidium, a mais antiga oração a Nossa Senhora), um card, sem obra. Texto autorizado em 23/11/2026.

A conferência da prévia do kit compara a vitrine com as provas de 20/10 e 15/12, renderizadas em outro ambiente; por isso essas duas pastas foram afastadas só durante a geração e devolvidas intactas. A prancha foi recomposta com todas as datas: as faixas de 29 e 31/12 da nova geração são idênticas, pixel a pixel, às da main.
