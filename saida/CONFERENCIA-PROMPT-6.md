# Conferência do prompt 6

Baseline: `main` no commit `333aaf716fe8c42c4b3d686cc39e8cfbc27280c4`. As cinco séries foram regeneradas: `evangelho`, `coragem`, `stories`, `santo` e `para-rezar`.

## Resultado

Aprovado: não há diferença fora das alterações autorizadas.

- 72 PNGs comparados pixel a pixel: 53 idênticos e 19 com alterações somente nas regiões autorizadas.
- O card 1 dos dois Evangelhos, os nichos e as obras do Coragem, os quatro Ângelus, o Santo do Dia, o Para Rezar e os componentes são idênticos.
- Nos demais cards do Evangelho e no Coragem, apenas o bloco de texto muda. As máscaras são a união das caixas DOM antigas e novas; selos, logos e fundos ficam protegidos.
- Na Misericórdia, somente a obra dentro do arco muda. Os textos, as caixas, o filete, o parapeito e a assinatura permanecem iguais.
- As pranchas mudam apenas nas miniaturas equivalentes; a máscara inclui os 3 px do suporte do filtro Lanczos. No recorte da Misericórdia mudam somente os contornos da janela.

## Espaços para o Canva

32 px entre o texto e a referência e 48 px entre o rótulo e o texto, para o Canva importar cada um em sua caixa (teste de 29/10/2026).

| Arte | Par | Distância DOM |
| --- | --- | --- |
| `evangelho/2026-11-29/card-2.png` | trecho → trecho_ref | 32 px |
| `evangelho/2026-11-29/card-3.png` | chamada_reflexao → reflexao.titulo | 48 px |
| `evangelho/2026-11-29/card-4.png` | chamada_oracao → pergunta | 48 px |
| `evangelho/2026-12-13/card-2.png` | trecho → trecho_ref | 32 px |
| `evangelho/2026-12-13/card-3.png` | chamada_reflexao → reflexao.titulo | 48 px |
| `evangelho/2026-12-13/card-4.png` | chamada_oracao → pergunta | 48 px |
| `coragem/2026-12-14/feed.png` | frase → referencia | 32 px |
| `coragem/2026-12-14/status.png` | frase → referencia | 32 px |
| `coragem/2026-12-28/feed.png` | frase → referencia | 32 px |
| `coragem/2026-12-28/status.png` | frase → referencia | 32 px |

Os blocos conservam o mesmo centro vertical. Textos, quebras de linha, fontes, tamanhos, cores e tracking são iguais; somente as translações de −8/+8 px nas referências e −16/+16 px nos rótulos foram permitidas.

| Coragem | Parapeito → frase | Referência → assinatura |
| --- | --- | --- |
| 14/12 e 28/12 · feed | 58 px | 61 px |
| 14/12 e 28/12 · status | 73 px | 76 px |

## PDFs

Os 18 PDFs preservam dimensões, texto extraível e tabelas das fontes embutidas. Os PDFs das cinco séries também foram rasterizados a 1080 px e comparados com as mesmas máscaras dos PNGs.

| PDF / página | Par | Aumento medido | Esperado |
| --- | --- | --- | --- |
| `coragem/2026-12-14/coragem-2026-12-14-feed.pdf` · 1 | frase → referencia | 16.00000 px | 16 px |
| `coragem/2026-12-14/coragem-2026-12-14-status.pdf` · 1 | frase → referencia | 16.00000 px | 16 px |
| `coragem/2026-12-28/coragem-2026-12-28-feed.pdf` · 1 | frase → referencia | 16.00000 px | 16 px |
| `coragem/2026-12-28/coragem-2026-12-28-status.pdf` · 1 | frase → referencia | 16.00000 px | 16 px |
| `evangelho/2026-11-29/evangelho-2026-11-29.pdf` · 2 | trecho → trecho_ref | 16.00000 px | 16 px |
| `evangelho/2026-11-29/evangelho-2026-11-29.pdf` · 3 | chamada_reflexao → reflexao.titulo | 32.00000 px | 32 px |
| `evangelho/2026-11-29/evangelho-2026-11-29.pdf` · 4 | chamada_oracao → pergunta | 32.00000 px | 32 px |
| `evangelho/2026-12-13/evangelho-2026-12-13.pdf` · 2 | trecho → trecho_ref | 16.00000 px | 16 px |
| `evangelho/2026-12-13/evangelho-2026-12-13.pdf` · 3 | chamada_reflexao → reflexao.titulo | 32.00000 px | 32 px |
| `evangelho/2026-12-13/evangelho-2026-12-13.pdf` · 4 | chamada_oracao → pergunta | 32.00000 px | 32 px |

As distâncias da tabela são entre as caixas reais das linhas extraídas pelo PyMuPDF, em pixels equivalentes (4/3 pt), com tolerância de ±0,5 px. O texto extraído completo também coincide com as fichas produzidas do YAML, ignorando somente espaços e quebras.
Os dois PDFs do teste do prompt 5 foram preservados byte a byte; o resultado da importação já executada pelo usuário foi registrado no LEIA-ME, sem regeneração.

## Misericórdia e margem da foto

Foco `50% 8%`, zoom `1.15`. Janela original: x=116.02, y=90.97, 1546.96 × 1862.88 px.

Na obra real desta entrega, o foco 50% 8% e o zoom 1.15 mantêm na janela o rosto, a auréola, as duas mãos, as mangas e o começo dos raios. As faixas uniformes escuras são parte do fundo da própria pintura; a comparação com as faixas interiores as descarta e não há aviso de margem da foto.

As faixas escuras da pintura são descartadas por contraste interior inferior a 10 níveis de cinza; não há aviso de margem. A ficha registra lado, largura e diferença. Os testes preservam os avisos antigos dos dois Tissot e cobrem borda branca sintética e continuação escura da própria pintura.

## Prévia, kit e originais

A prévia do StoryAngelus é conferida com o `article` na origem (0,0), nas mesmas coordenadas do card gerado: zero pixels diferentes fora da obra. O antigo aviso causado pela posição global foi retirado.

Os 44 arquivos de `kit/` são idênticos ao ZIP v4, que também permanece igual ao baseline. As obras originais e os elementos Canva do kit foram comparados byte a byte.

116 testes passaram.

O resultado do teste de importação de 29/10/2026 foi fornecido pelo usuário. Não há teste novo de importação no Canva realizado por esta conferência. Evidência detalhada em `verificacao/conferencia-prompt6.json`.
