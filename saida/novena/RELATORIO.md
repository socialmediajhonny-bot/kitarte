# Novenas

`python gerar.py novena --teste-canva`

## Conteúdo e composição

- As orações foram escritas pela página e aprovadas em 03/11/2026. O YAML mantém os vinte textos e os refrões aprovados, sem composição automática de orações.
- PostNovena usa feed 1080 × 1350, tema pergaminho, sem obra. O bloco inteiro fica centralizado entre o selo e a assinatura, com pelo menos 60 px de folga dos dois lados.
- O selo traz o nome da novena e a data, sem apoio à direita. A cruz segue a cor da novena nos nove dias: roxo #5b2e70, inclusive em 30/11, 3/12 e 7/12.
- Dia N de 9 → título: 48 px; título → fonte: 32 px; fonte → ornamento e ornamento → oração: 48 px; oração → contas: 48 px. No encerramento sem fonte, título → ornamento: 48 px. Os espaços são o gap de 16 px do kit somado às margens inline em tokens e são medidos no navegador com tolerância de ±0,01 px.
- Título em titulo, até duas linhas e 820 px. A oração usa oracao a 880 px, com entrelinha de 62 px, e contém o refrão em um único parágrafo, depois de uma quebra de linha. O refrão usa Cormorant Garamond Medium Italic e tinta-suave; a Imaculada mantém duas linhas, com a primeira terminando em `pecado,`.
- Palavras com hífen recebem white-space:nowrap apenas nessa palavra. As palavras de uma letra seguem a regra compartilhada de espaços inseparáveis, sem modificar o helper usado pelas outras séries.
- As nove contas formam um SVG de 306 × 18 px, centros x=9+36·i e y=9. Até o dia N, raio 9 e preenchimento ouro; as demais têm raio 7,75, traço de 2,5 px em ouro e nenhum preenchimento.
- O encerramento usa cartão inteiro em ouro litúrgico (#866420), todos os elementos em sobre-cor (#faf6ee), logo-horizontal-sobre-cor.svg e nove contas cheias. O final do YAML substitui o refrão quando existe; no Natal, Glória a Deus nas alturas!.

## Tabela prevista no prompt

| Cards | Título | Oração com refrão | Folga prevista |
| --- | --- | --- | --- |
| Imaculada · dias 1 a 7 e 9 | 1 linha | 6 linhas | 154 px |
| Imaculada · dia 8 | 2 linhas | 6 linhas | 116 px |
| Imaculada · encerramento | 1 linha | 7 linhas | 158 px |
| Natal · dias 1, 3 e 5 a 9 e encerramento | 1 linha | 5 linhas | 184 px |
| Natal · dia 2 | 2 linhas | 5 linhas | 146 px |
| Natal · dia 4 | 1 linha | 6 linhas | 154 px |

## 20 cards medidos no navegador

Os 20 cards selecionados foram renderizados e validados em work/novena/. Os números abaixo são medidas reais do DOM; diferenças da tabela prevista são informativas quando todos os limites continuam satisfeitos.

| Novena | Data | Card | Título: medido / previsto | Oração: medido / previsto | Selo → bloco | Bloco → assinatura | Folga prevista |
| --- | --- | --- | --- | --- | --- | --- | --- |
| imaculada | 2026-11-29 | Dia 1 | 1 / 1 | 6 / 6 | 153.5 px | 153.5 px | 154 px |
| imaculada | 2026-11-30 | Dia 2 | 1 / 1 | 6 / 6 | 153.5 px | 153.5 px | 154 px |
| imaculada | 2026-12-01 | Dia 3 | 1 / 1 | 6 / 6 | 153.5 px | 153.5 px | 154 px |
| imaculada | 2026-12-02 | Dia 4 | 1 / 1 | 6 / 6 | 153.5 px | 153.5 px | 154 px |
| imaculada | 2026-12-03 | Dia 5 | 1 / 1 | 6 / 6 | 153.5 px | 153.5 px | 154 px |
| imaculada | 2026-12-04 | Dia 6 | 1 / 1 | 6 / 6 | 153.5 px | 153.5 px | 154 px |
| imaculada | 2026-12-05 | Dia 7 | 1 / 1 | 6 / 6 | 153.5 px | 153.5 px | 154 px |
| imaculada | 2026-12-06 | Dia 8 | 2 / 2 | 6 / 6 | 115.5 px | 115.5 px | 116 px |
| imaculada | 2026-12-07 | Dia 9 | 1 / 1 | 6 / 6 | 153.5 px | 153.5 px | 154 px |
| imaculada | 2026-12-08 | Encerramento | 1 / 1 | 7 / 7 | 158.5 px | 158.5 px | 158 px |
| natal | 2026-12-16 | Dia 1 | 1 / 1 | 5 / 5 | 184.5 px | 184.5 px | 184 px |
| natal | 2026-12-17 | Dia 2 | 2 / 2 | 5 / 5 | 146.5 px | 146.5 px | 146 px |
| natal | 2026-12-18 | Dia 3 | 1 / 1 | 5 / 5 | 184.5 px | 184.5 px | 184 px |
| natal | 2026-12-19 | Dia 4 | 1 / 1 | 6 / 6 | 153.5 px | 153.5 px | 154 px |
| natal | 2026-12-20 | Dia 5 | 1 / 1 | 5 / 5 | 184.5 px | 184.5 px | 184 px |
| natal | 2026-12-21 | Dia 6 | 1 / 1 | 5 / 5 | 184.5 px | 184.5 px | 184 px |
| natal | 2026-12-22 | Dia 7 | 1 / 1 | 5 / 5 | 184.5 px | 184.5 px | 184 px |
| natal | 2026-12-23 | Dia 8 | 1 / 1 | 5 / 5 | 184.5 px | 184.5 px | 184 px |
| natal | 2026-12-24 | Dia 9 | 1 / 1 | 5 / 5 | 184.5 px | 184.5 px | 184 px |
| natal | 2026-12-25 | Encerramento | 1 / 1 | 5 / 5 | 184.5 px | 184.5 px | 184 px |

## Diferenças da tabela prevista

- imaculada, dia-1: selo_texto_px: medido 153.5px, previsto 154px; texto_assinatura_px: medido 153.5px, previsto 154px
- imaculada, dia-2: selo_texto_px: medido 153.5px, previsto 154px; texto_assinatura_px: medido 153.5px, previsto 154px
- imaculada, dia-3: selo_texto_px: medido 153.5px, previsto 154px; texto_assinatura_px: medido 153.5px, previsto 154px
- imaculada, dia-4: selo_texto_px: medido 153.5px, previsto 154px; texto_assinatura_px: medido 153.5px, previsto 154px
- imaculada, dia-5: selo_texto_px: medido 153.5px, previsto 154px; texto_assinatura_px: medido 153.5px, previsto 154px
- imaculada, dia-6: selo_texto_px: medido 153.5px, previsto 154px; texto_assinatura_px: medido 153.5px, previsto 154px
- imaculada, dia-7: selo_texto_px: medido 153.5px, previsto 154px; texto_assinatura_px: medido 153.5px, previsto 154px
- imaculada, dia-8: selo_texto_px: medido 115.5px, previsto 116px; texto_assinatura_px: medido 115.5px, previsto 116px
- imaculada, dia-9: selo_texto_px: medido 153.5px, previsto 154px; texto_assinatura_px: medido 153.5px, previsto 154px
- imaculada, encerramento: selo_texto_px: medido 158.5px, previsto 158px; texto_assinatura_px: medido 158.5px, previsto 158px
- natal, dia-1: selo_texto_px: medido 184.5px, previsto 184px; texto_assinatura_px: medido 184.5px, previsto 184px
- natal, dia-2: selo_texto_px: medido 146.5px, previsto 146px; texto_assinatura_px: medido 146.5px, previsto 146px
- natal, dia-3: selo_texto_px: medido 184.5px, previsto 184px; texto_assinatura_px: medido 184.5px, previsto 184px
- natal, dia-4: selo_texto_px: medido 153.5px, previsto 154px; texto_assinatura_px: medido 153.5px, previsto 154px
- natal, dia-5: selo_texto_px: medido 184.5px, previsto 184px; texto_assinatura_px: medido 184.5px, previsto 184px
- natal, dia-6: selo_texto_px: medido 184.5px, previsto 184px; texto_assinatura_px: medido 184.5px, previsto 184px
- natal, dia-7: selo_texto_px: medido 184.5px, previsto 184px; texto_assinatura_px: medido 184.5px, previsto 184px
- natal, dia-8: selo_texto_px: medido 184.5px, previsto 184px; texto_assinatura_px: medido 184.5px, previsto 184px
- natal, dia-9: selo_texto_px: medido 184.5px, previsto 184px; texto_assinatura_px: medido 184.5px, previsto 184px
- natal, encerramento: selo_texto_px: medido 184.5px, previsto 184px; texto_assinatura_px: medido 184.5px, previsto 184px

## Verificações

- As distâncias, o limite de oito linhas da oração com refrão, as linhas próprias e a variante itálica do refrão, as palavras com hífen e a geometria e as cores das contas foram conferidos no navegador.
- Cada PDF interno de uma página passa pelas verificações de texto e fontes. Os PDFs reunidos são conferidos novamente: páginas de 810 × 1012,5 pt, fontes TTF embutidas e texto integral igual ao conteúdo aprovado, desconsiderando apenas espaços e quebras.
- Os renders carregam somente os seis arquivos de fonte e demais recursos locais do projeto. O ZIP e os 44 arquivos de kit/ são conferidos antes e depois. Nenhuma outra série é regenerada por este comando.

## Entrega desta rodada

Somente os três cards da Imaculada foram gravados em saida/novena/teste-canva/: dia 1 (29/11), dia 8 (6/12) e encerramento (8/12), nessa ordem. O HTML e o PDF usam exatamente a composição dos cards finais; os arquivos internos dos vinte cards permanecem em work/novena/.

- [novena-teste-canva.pdf](teste-canva/novena-teste-canva.pdf)
- [prancha.png](teste-canva/prancha.png)
- [ficha.json](teste-canva/ficha.json)

## O que conferir no Canva

- Cada texto na sua caixa: selo, data, Dia N de 9 ou Encerramento, título e fonte.
- A oração e o refrão numa caixa só, com entrelinha de 62 px, o refrão em itálico e na cor certa, e a quebra depois da vírgula.
- As nove contas como formas.
- Nenhuma caixa solta.

## Pendências

A importação deste PDF no Canva ainda precisa ser conferida. Após essa conferência, gerar os vinte cards finais em saida/novena/imaculada/ e saida/novena/natal/, com os PDFs novena-imaculada.pdf e novena-natal.pdf. Nesta rodada, esses vinte cards não foram publicados.

A evidência da geração está em [verificacao.json](verificacao.json).

A preservação das saídas anteriores em relação à main no commit 2369956 e a conferência independente das novas artes estão documentadas em [CONFERENCIA-PROMPT-8.md](CONFERENCIA-PROMPT-8.md), com [evidência detalhada](conferencia-prompt8.json).

## Árvore

```text
saida/novena/
  CONFERENCIA-PROMPT-8.md
  RELATORIO.md
  conferencia-prompt8.json
  teste-canva/dia-1.png
  teste-canva/dia-8.png
  teste-canva/encerramento.png
  teste-canva/ficha.json
  teste-canva/novena-teste-canva.pdf
  teste-canva/prancha.png
  verificacao.json
```
