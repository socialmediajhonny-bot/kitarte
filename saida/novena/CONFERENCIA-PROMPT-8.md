# Conferência do prompt 8

Baseline: `main` no commit `2369956b11958ae8f4936b19373feb79f195e7c1`.

Aprovado: só foram acrescentados os arquivos da Novena e o novo comando/documentação.

177 saídas anteriores foram comparadas byte a byte e permanecem intactas, incluindo todos os stories corrigidos no Canva. Os 72 PNGs e 18 PDFs anteriores não foram regenerados.
Os arquivos compartilhados de composição, fontes, cores, conteúdo e renderização permanecem iguais; o CLI recebeu somente o novo comando e suas opções. Todos os YAMLs anteriores e as obras originais foram preservados.
Os 44 arquivos extraídos do kit são idênticos ao ZIP original. O ZIP também foi comparado com o baseline.

## Conteúdo e validação dos vinte cards

O YAML corresponde exatamente ao bloco aprovado em 03/11/2026. Os vinte cards foram renderizados somente em `work/novena/`, usando os mesmos documentos HTML e PDFs da geração final.
| Novena | Card | Título | Oração e refrão | Folga acima / abaixo |
| --- | --- | --- | --- | --- |
| imaculada | dia-1 | 1 | 6 | 153.5 / 153.5 px |
| imaculada | dia-2 | 1 | 6 | 153.5 / 153.5 px |
| imaculada | dia-3 | 1 | 6 | 153.5 / 153.5 px |
| imaculada | dia-4 | 1 | 6 | 153.5 / 153.5 px |
| imaculada | dia-5 | 1 | 6 | 153.5 / 153.5 px |
| imaculada | dia-6 | 1 | 6 | 153.5 / 153.5 px |
| imaculada | dia-7 | 1 | 6 | 153.5 / 153.5 px |
| imaculada | dia-8 | 2 | 6 | 115.5 / 115.5 px |
| imaculada | dia-9 | 1 | 6 | 153.5 / 153.5 px |
| imaculada | encerramento | 1 | 7 | 158.5 / 158.5 px |
| natal | dia-1 | 1 | 5 | 184.5 / 184.5 px |
| natal | dia-2 | 2 | 5 | 146.5 / 146.5 px |
| natal | dia-3 | 1 | 5 | 184.5 / 184.5 px |
| natal | dia-4 | 1 | 6 | 153.5 / 153.5 px |
| natal | dia-5 | 1 | 5 | 184.5 / 184.5 px |
| natal | dia-6 | 1 | 5 | 184.5 / 184.5 px |
| natal | dia-7 | 1 | 5 | 184.5 / 184.5 px |
| natal | dia-8 | 1 | 5 | 184.5 / 184.5 px |
| natal | dia-9 | 1 | 5 | 184.5 / 184.5 px |
| natal | encerramento | 1 | 5 | 184.5 / 184.5 px |

Foram conferidos os pares de 48/32/48/48/48 px (±0,01), títulos de até duas linhas, oração com refrão até oito, folgas iguais de pelo menos 60 px, refrão em linha própria e itálico, quebra mariana após a vírgula, ausência de linha terminada em hífen, geometria/preenchimento/cor das nove contas, cruz roxa nos dias e encerramento em ouro com texto sobre-cor.

## Entrega para testar no Canva

A entrega contém somente três PNGs, a prancha e o PDF de três páginas, nesta ordem: Imaculada dia 1, dia 8 e encerramento. Nenhuma pasta final com os vinte cards foi publicada.
Os três PNGs são cópias byte a byte dos cards finais validados em work. Cada página do PDF de teste também conserva exatamente o raster, o texto, a posição dos glifos e os programas TTF do PDF final correspondente. Texto integral e dimensões foram conferidos por PyMuPDF, e o texto foi conferido também por pdftotext. As cinco fontes usadas estão embutidas.

Os dois PDFs completos de dez páginas também foram reunidos e validados somente em work, com texto e fontes embutidas corretos em todas as páginas. Eles não fazem parte da entrega desta rodada.

28 novos testes do schema e do layout das Novenas passaram. As demais séries não foram renderizadas.

Pendente: importar o PDF de três páginas no Canva e conferir os pontos do relatório da série. Os vinte cards finais serão publicados somente depois dessa conferência.
Evidência detalhada: [conferencia-prompt8.json](conferencia-prompt8.json).
