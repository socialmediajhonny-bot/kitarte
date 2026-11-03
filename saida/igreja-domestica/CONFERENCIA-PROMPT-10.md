# Conferência do prompt 10

Baseline: `main` no commit `55428062a031da6a2c4be6328ea430d3fe7fbc8a`, que já contém as duas obras fornecidas.

Aprovado: Igreja Doméstica foi acrescentada sem alterar as saídas anteriores.

215 saídas antigas foram comparadas byte a byte e permanecem idênticas, incluindo as pastas completas de novenas e stories. Os modelos, conteúdos, obras e fontes anteriores também foram preservados. O roteiro do CLI e o README receberam a nova série; o teste de obras foi atualizado para reconhecer a faixa escura da nova Educação da Virgem como parte da pintura, sem mudar o detector compartilhado.
Os 44 arquivos de `kit/` continuam iguais ao ZIP original. O novo YAML é exatamente o bloco aprovado em 03/11/2026.

## Cards, medidas e textos

| Data | Card | Tipo | Folga medida | Folga prevista | Diferenças da previsão |
| --- | --- | --- | --- | --- | --- |
| 2026-11-29 | 1 | capa | 116 px | 116 px | nenhuma |
| 2026-11-29 | 2 | passos | 128.5 px | 128.5 px | nenhuma |
| 2026-11-29 | 3 | oracao | 103.5 px | 103.5 px | nenhuma |
| 2026-11-29 | 4 | conversa | 353.5 px | 353.5 px | nenhuma |
| 2026-12-06 | 1 | capa | 116 px | 116 px | nenhuma |
| 2026-12-06 | 2 | oracao | 103.5 px | 103.5 px | nenhuma |
| 2026-12-06 | 3 | conversa | 353.5 px | 353.5 px | nenhuma |

Os pares de 32 e 48 px foram recalculados diretamente das caixas de cada campo. Foram conferidos os limites de linhas, as cores, a proteção das referências e dos ordinais e a ausência de finais de linha em palavra de uma letra, hífen, ordinal ou Mc. Cada número da lista coincide com a primeira linha de base do item (±0,01 px). O texto extraído integral das sete páginas coincide com os campos do YAML, desconsiderando espaços e quebras.

## Obras e recortes

As duas obras reais já existentes no repositório foram usadas, sem downloads ou imagem provisória. As dimensões, o foco e o zoom do YAML foram conservados. Cada recorte foi reconstruído independentemente pela fórmula de cover, pela janela original e pelos dois traços em arco: comparação de pixels exata.
As notas visuais sobre rostos e vela estão no relatório da série. Esta auditoria objetiva verifica os arquivos e a geometria dos recortes.

## PDFs, prancha e filtro

Foram conferidos dois PDFs, com quatro e três páginas na ordem do YAML. Todas as fontes usadas estão embutidas; dimensões de 810 × 1012,5 pt e texto integral foram verificados com PyMuPDF e Poppler. Os PNGs finais são cópias exatas dos renders internos, e as páginas dos PDFs finais mantêm raster, glifos e tabelas TTF dos PDFs de uma página produzidos pelo mesmo HTML.
A prancha foi reconstruída independentemente: duas linhas, miniaturas de 360 × 450 px e rótulos fora das artes, com zero diferenças de pixels. O filtro de 29/11 foi exercitado numa cópia isolada em work; os arquivos de 6/12 permaneceram byte a byte iguais e seus hashes também coincidem com os arquivos publicados. A evidência detalhada está em [conferencia-prompt10.json](conferencia-prompt10.json).

175 testes passaram.

Pendente: importar os dois PDFs no Canva e conferir as caixas de texto, as obras nos arcos e as formas conforme o relatório da série.
