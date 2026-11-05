# Conferência do prompt 11

Baseline: main no commit d086e793d9d0c3b2dbd47a2455776e2e0cd64c8d.

Aprovado: treze carrosséis novos sem alterar o modelo nem as saídas anteriores protegidas.

216 saídas anteriores permanecem idênticas byte a byte. Os dez PNGs dos dois Evangelhos anteriores e a prancha de cores também mantêm os mesmos pixels.
Os PDFs anteriores preservam texto, posições dos glifos, tabelas das fontes embutidas e raster em 1080 px. Metadados internos como a data de criação podem variar.
Todos os arquivos de geração, o kit, as obras originais e os outros YAMLs continuam idênticos ao baseline. O conteúdo novo foi inserido literalmente, preservando comentários e os dois dias anteriores.

## Conteúdo e arquivos

Quinze datas em ordem, com 48 cards: 40 novos entre 30/11 e 12/12 e os oito dos dois domingos anteriores. Cada data tem seus PNGs, um PDF na ordem, recorte da obra e ficha.
Os quinze PDFs foram conferidos por PyMuPDF e pdftotext: dimensões de 810 × 1012,5 pt, texto integral derivado do YAML e quatro variantes de fontes embutidas.
A comparação preserva os espaços entre palavras: sequências de espaços, espaços inseparáveis e quebras de linha são normalizadas para um único espaço. As 48 páginas coincidem com os campos do YAML sem unir palavras.
Os recortes foram reconstruídos pela geometria cover/foco/zoom. As margens uniformes detectadas do museu ficam fora da janela aprovada.
A prancha geral foi reconstruída com as quinze datas a 1/3 do tamanho, em 1576 × 7982 px.

## Tabela de linhas do lote

| Data | Capa | Versículo | Reflexão | Pergunta/convite |
| --- | --- | --- | --- | --- |
| 2026-11-30 | 1, 2 | citacao-grande, 3 | — | 2, 1 |
| 2026-12-01 | 1, 1 | citacao, 3 | — | 2, 1 |
| 2026-12-02 | 1, 2 | citacao, 3 | — | 2, 1 |
| 2026-12-03 | 1, 1 | citacao, 3 | — | 2, 1 |
| 2026-12-04 | 1, 2 | citacao-grande, 1 | — | 2, 1 |
| 2026-12-05 | 1, 2 | citacao-grande, 2 | — | 2, 1 |
| 2026-12-06 | 1, 2 | citacao-grande, 2 | título 1, texto 5 | 2, 1 |
| 2026-12-07 | 1, 2 | citacao-grande, 2 | — | 2, 1 |
| 2026-12-08 | 1, 1 | citacao-grande, 2 | — | 2, 1 |
| 2026-12-09 | 1, 2 | citacao, 3 | — | 2, 1 |
| 2026-12-10 | 1, 1 | citacao-grande, 2 | — | 2, 1 |
| 2026-12-11 | 1, 2 | citacao, 3 | — | 2, 1 |
| 2026-12-12 | 1, 2 | citacao, 2 | — | 2, 1 |

Diferenças da tabela prevista: nenhuma.

## Inspeção das obras

A inspeção visual das capas e dos contornos está registrada em NOTAS-DAS-OBRAS-LOTE-1.json. Objetos visíveis fora do contorno na prova de recorte ficam fora do arco do card.
Em 9/12, o homem com punhal, a mãe com o filho morto e a moldura foram confirmados fora do arco.
Ressalva de 12/12: pequenos fragmentos dos mantos dos santos à frente ainda aparecem nas quinas inferiores; a sugestão está no relatório, sem alterar o YAML.

177 testes passaram.

Pendente: conferir a importação dos treze PDFs no Canva. Recortes parciais e sugestões de foco/zoom estão documentados sem alterar o YAML. Evidência: [conferencia-prompt11.json](conferencia-prompt11.json).
