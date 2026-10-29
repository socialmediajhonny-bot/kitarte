# Conferência do prompt 7

Baseline: `main` no commit `8b602bf36f06147284f124482e2475cd5d612ff2`. Somente os stories foram regenerados.

Aprovado: nenhuma diferença fora das áreas autorizadas.

72 PNGs comparados pixel a pixel: 63 idênticos e 9 alterados somente nos textos autorizados e na prancha correspondente.
As máscaras usam separadamente as caixas DOM antigas e novas do subtítulo, da invocação e da resposta, com 1 px para o antialias e o overhang do itálico. Selos, nichos, obras, títulos, ornamentos e assinaturas ficam protegidos. As miniaturas da prancha incluem somente os 3 px necessários ao filtro Lanczos.
Todas as saídas das demais séries e dos componentes foram comparadas byte a byte, assim como os dois recortes dos stories. Os demais geradores, todos os YAMLs, o ZIP e as obras originais também continuam idênticos.

## Distâncias no navegador

48 px entre o título e o subtítulo e entre a invocação e a resposta, para o Canva importar cada texto em sua caixa (importação de 29/10/2026).

| Story | Título → subtítulo | Invocação → resposta | Último texto → assinatura |
| --- | --- | --- | --- |
| `stories/advento/angelus.png` | 48 px | 48 px | 63 px |
| `stories/advento/misericordia.png` | 48 px | — | 37 px |
| `stories/natal/angelus.png` | 48 px | 48 px | 63 px |
| `stories/natal/misericordia.png` | 48 px | — | 37 px |
| `stories/quaresma/angelus.png` | 48 px | 48 px | 63 px |
| `stories/quaresma/misericordia.png` | 48 px | — | 37 px |
| `stories/tempo-comum/angelus.png` | 48 px | 48 px | 63 px |
| `stories/tempo-comum/misericordia.png` | 48 px | — | 37 px |

O subtítulo e a invocação descem 32 px; a resposta desce 64 px. O ornamento permanece em y=1286 px mediante redistribuição de suas margens inline, sem mover selo, nicho, obra, título ou assinatura.

## PDFs

18 PDFs conferidos: os quatro dos stories foram rasterizados a 1080 px e comparados nas mesmas regiões; os demais mantêm os bytes originais. Texto integral, dimensões e tabelas das fontes embutidas permanecem iguais. As posições dos glifos também seguem apenas as translações autorizadas.

| PDF / página | Par | Aumento medido | Esperado |
| --- | --- | --- | --- |
| `stories/advento/stories-advento.pdf` · 1 | titulo → subtitulo | 32.00000 px | 32 px |
| `stories/advento/stories-advento.pdf` · 1 | invocacao → resposta | 32.00000 px | 32 px |
| `stories/advento/stories-advento.pdf` · 2 | titulo → subtitulo | 32.00000 px | 32 px |
| `stories/natal/stories-natal.pdf` · 1 | titulo → subtitulo | 32.00000 px | 32 px |
| `stories/natal/stories-natal.pdf` · 1 | invocacao → resposta | 32.00000 px | 32 px |
| `stories/natal/stories-natal.pdf` · 2 | titulo → subtitulo | 32.00000 px | 32 px |
| `stories/quaresma/stories-quaresma.pdf` · 1 | titulo → subtitulo | 32.00000 px | 32 px |
| `stories/quaresma/stories-quaresma.pdf` · 1 | invocacao → resposta | 32.00000 px | 32 px |
| `stories/quaresma/stories-quaresma.pdf` · 2 | titulo → subtitulo | 32.00000 px | 32 px |
| `stories/tempo-comum/stories-tempo-comum.pdf` · 1 | titulo → subtitulo | 32.00000 px | 32 px |
| `stories/tempo-comum/stories-tempo-comum.pdf` · 1 | invocacao → resposta | 32.00000 px | 32 px |
| `stories/tempo-comum/stories-tempo-comum.pdf` · 2 | titulo → subtitulo | 32.00000 px | 32 px |

Distâncias entre caixas reais das linhas extraídas pelo PyMuPDF, convertidas de pontos para pixels (4/3), com tolerância de ±0,5 px. O texto completo extraído coincide com a ficha gerada do YAML, ignorando somente espaços e quebras.

## Prévia e kit

A cópia local da prévia do kit recebe as mesmas margens de texto e a mesma preservação do ornamento. O `article` é rasterizado na origem (0,0): zero pixels diferentes fora da obra.
Os 44 arquivos de `kit/` continuam idênticos ao ZIP original. Nenhuma fonte ou obra foi alterada.

118 testes passaram.

A nova importação destes PDFs no Canva não foi realizada. O resultado informado pelo usuário em 29/10/2026 motivou os novos espaços. Evidência detalhada: [conferencia-prompt7.json](conferencia-prompt7.json).
