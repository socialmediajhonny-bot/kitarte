# Teste de importação no Canva

Gerado por `python gerar.py teste-canva` a partir dos cards 2 e 4 do Evangelho de 29/11/2026, usando o mesmo `_document` do gerador.

O teste consistiu em importar **os dois PDFs no Canva, sem editar nada**, comparando as caixas e o tamanho da referência Mc 13,37 e do rótulo Para rezar hoje. Os resultados informados pelo usuário estão registrados abaixo; os PDFs originais foram preservados sem regeneração, e o comando experimental foi retirado.

- [teste-canva-a.pdf](teste-canva-a.pdf): 14 páginas, sem marcação.
- [teste-canva-b.pdf](teste-canva-b.pdf): 2 controles, com marcação estrutural.
- [prancha.png](prancha.png): as páginas do A rasterizadas a 1/4, com a variante fora das artes (270 × 338 px; 1350/4 resulta em meio pixel, arredondado pelo rasterizador).

| Páginas do A | Variante | Estilo na referência (card 2) | Estilo no rótulo (card 4) | Distância DOM do par |
| --- | --- | --- | --- | --- |
| 1 e 2 | controle | `nenhum` | `nenhum` | 16 / 16 px |
| 3 e 4 | camada | `opacity: 0.999` | `opacity: 0.999` | 16 / 16 px |
| 5 e 6 | giro | `transform: rotate(0.5deg)` | `transform: rotate(0.5deg)` | 15.3906 / 15.0571 px |
| 7 e 8 | respiro 32 | `margin-top: 16px` | `margin-bottom: 16px` | 32 / 32 px |
| 9 e 10 | respiro 48 | `margin-top: 32px` | `margin-bottom: 32px` | 48 / 48 px |
| 11 e 12 | respiro 80 | `margin-top: 64px` | `margin-bottom: 64px` | 80 / 80 px |
| 13 e 14 | respiro 128 | `margin-top: 112px` | `margin-bottom: 112px` | 128 / 128 px |

As páginas 1 e 2 do B correspondem às páginas 1 e 2 do A. Não há nomes de variantes dentro de nenhuma arte.

Cada PDF foi produzido por um documento HTML próprio e uma única chamada de `page.pdf`; o A usa `tagged=False` e o B `tagged=True`. A correção das caixas usa `PdfWriter(clone_from=reader)`, preservando o catálogo e a árvore estrutural do B.

No respiro, só a margem do elemento muda. O `gap` de 16 px do kit se soma a ela, e o bloco continua centralizado. Os controles e as demais variantes mantêm os estilos originais do Evangelho.

A validação automática está em [verificacao.json](verificacao.json): páginas e dimensões, fontes embutidas, texto integral, estrutura marcada, comparação visual dos controles e da camada, Form XObject de transparência, direção das linhas e crescimento dos espaços no PDF.

A igualdade do texto usa a ordem geométrica de leitura (`PyMuPDF sort=True` e `pdftotext -layout`), desconsiderando espaços e quebras. A camada e o giro podem pintar o alvo por último no fluxo interno do PDF; a ordem visual e o conteúdo continuam os mesmos.

## Resultado no Canva (29/10/2026)

| Páginas | Variante | Card 2 (referência embaixo) | Card 4 (rótulo em cima) |
| --- | --- | --- | --- |
| A 1 e 2 | controle (16 px) | fundiu | fundiu |
| A 3 e 4 | camada | fundiu | fundiu |
| A 5 e 6 | giro | fundiu | fundiu |
| A 7 e 8 | 32 px | separou | fundiu |
| A 9 e 10 | 48 px | separou | separou |
| A 11 a 14 | 80 e 128 px | separou | separou |
| B 1 e 2 | PDF marcado | fundiu | fundiu |

Quando separa, o Canva importa a fonte, o tamanho, a cor e a posição certos (menos de 1 px de diferença) e a entrelinha certa. Foram aprovados 32 px entre o texto e a referência e 48 px entre o rótulo e o texto.

## Arquivos

```text
saida/teste-canva/
  LEIA-ME.md
  ficha.json
  prancha.png
  teste-canva-a.pdf
  teste-canva-b.pdf
  verificacao.json
```
