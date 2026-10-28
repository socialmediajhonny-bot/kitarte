# Conferência do kit v4 e das artes aprovadas

Baseline das saídas: commit `8365dc125c76e859633026c949322966fd111e29` (main antes da implementação).

## Kit final

- ZIP v4 final com 44 arquivos. O LEIA-ME começa por `# Kit Arte que Reza · versão 4` e cita o Nicho na seção de mudanças desde a v3.
- Mudaram exatamente os cinco arquivos previstos:

- `kit/LEIA-ME.md`
- `kit/design-system/componentes/Nicho/README.md`
- `kit/design-system/componentes/PostCoragem/README.md`
- `kit/design-system/componentes/PostOracao/README.md`
- `kit/design-system/componentes/PostOracao/preview.html`

- Os outros 39 arquivos são idênticos em bytes, incluindo tokens.json, bundle.css, os logos e os seis TTF. Os hashes constam no JSON. `kit/` permanece idêntico ao ZIP.

## Comandos executados

```bash
python gerar.py componentes
python gerar.py evangelho
python gerar.py santo
```

## Componentes

28 PNGs comparados pixel a pixel, 19 SVGs e 6 fontes comparados em bytes.
O PDF de componentes mantém texto, caixas de texto, dimensões e tabelas de fontes.

## Cinco enquadramentos autorizados

Em cada PNG completo, somente a caixa interna da obra pode mudar; uma segunda máscara em arco também protege seus cantos. Selos, textos, filetes, parapeitos, molduras, assinaturas e fundos ficam fora da região permitida. Nas pranchas, a região equivalente recebe uma folga de 3 px para o suporte do filtro Lanczos; os rótulos não são liberados.

Uma máscara inicial de 2 px deixou apenas halos de 1–2 níveis RGB da reamostragem. Com o suporte correto de 3 px, não há diferença fora das regiões das obras nas pranchas. Não houve mudança de composição.

### evangelho · 2026-11-29

- Foco: `45% 50%`; zoom: `1.1`.
- PNG: somente a obra mudou.
- Textos, linhas, estilos e caixas: idênticos.
- Ficha antiga preservada fora do foco/zoom e da geometria do IMG; metadados novos de janela são registrados.
- PDF: texto extraído, caixas de texto, dimensões e tabelas de fontes idênticos.
- Recorte: `evangelho/2026-11-29/recorte.png`, 1080 × 738 px.
- Janela na imagem original: `{"x": 309.33739002932555, "y": 46.59090909090912, "largura": 811.5835777126099, "altura": 931.8181818181818}`.
- Avisos de margem com o enquadramento novo: nenhum.

| Card | Campo | Linhas |
| --- | --- | --- |
| 1 | selo | 1 |
| 1 | data | 1 |
| 1 | referencia | 1 |
| 1 | credito | 1 |
| 1 | titulo | 2 |
| 2 | selo | 1 |
| 2 | data | 1 |
| 2 | referencia | 1 |
| 2 | trecho | 2 |
| 2 | trecho_ref | 1 |
| 3 | selo | 1 |
| 3 | data | 1 |
| 3 | referencia | 1 |
| 3 | chamada_reflexao | 1 |
| 3 | reflexao.titulo | 1 |
| 3 | reflexao.texto | 5 |
| 4 | selo | 1 |
| 4 | data | 1 |
| 4 | referencia | 1 |
| 4 | chamada_oracao | 1 |
| 4 | pergunta | 2 |
| 4 | convite | 1 |

### evangelho · 2026-12-13

- Foco: `50% 50%`; zoom: `1.1`.
- PNG: somente a obra mudou.
- Textos, linhas, estilos e caixas: idênticos.
- Ficha antiga preservada fora do foco/zoom e da geometria do IMG; metadados novos de janela são registrados.
- PDF: texto extraído, caixas de texto, dimensões e tabelas de fontes idênticos.
- Recorte: `evangelho/2026-12-13/recorte.png`, 1080 × 770 px.
- Janela na imagem original: `{"x": 334.4956011730206, "y": 49.77272727272731, "largura": 867.0087976539588, "altura": 995.4545454545454}`.
- Avisos de margem com o enquadramento novo: nenhum.

| Card | Campo | Linhas |
| --- | --- | --- |
| 1 | selo | 1 |
| 1 | data | 1 |
| 1 | referencia | 1 |
| 1 | credito | 1 |
| 1 | titulo | 2 |
| 2 | selo | 1 |
| 2 | data | 1 |
| 2 | referencia | 1 |
| 2 | trecho | 2 |
| 2 | trecho_ref | 1 |
| 3 | selo | 1 |
| 3 | data | 1 |
| 3 | referencia | 1 |
| 3 | chamada_reflexao | 1 |
| 3 | reflexao.titulo | 1 |
| 3 | reflexao.texto | 4 |
| 4 | selo | 1 |
| 4 | data | 1 |
| 4 | referencia | 1 |
| 4 | chamada_oracao | 1 |
| 4 | pergunta | 2 |
| 4 | convite | 1 |

### santo-do-dia · 2026-11-30

- Foco: `45% 15%`; zoom: `1.05`.
- PNG: somente a obra mudou.
- Textos, linhas, estilos e caixas: idênticos.
- Ficha antiga preservada fora do foco/zoom e da geometria do IMG; metadados novos de janela são registrados.
- PDF: texto extraído, caixas de texto, dimensões e tabelas de fontes idênticos.
- Recorte: `santo-do-dia/2026-11-30/recorte.png`, 1080 × 1596 px.
- Janela na imagem original: `{"x": 37.35, "y": 59.789610389610424, "largura": 1660.0, "altura": 2177.402597402597}`.
- Avisos de margem com o enquadramento novo: nenhum.

| Card | Campo | Linhas |
| --- | --- | --- |
| 1 | selo | 1 |
| 1 | data | 1 |
| 1 | grau | 1 |
| 1 | nome | 1 |
| 1 | titulo | 1 |
| 1 | frase | 1 |
| 1 | fonte | 1 |

### santo-do-dia · 2026-12-03

- Foco: `50% 0%`; zoom: `1.3`.
- PNG: somente a obra mudou.
- Textos, linhas, estilos e caixas: idênticos.
- Ficha antiga preservada fora do foco/zoom e da geometria do IMG; metadados novos de janela são registrados.
- PDF: texto extraído, caixas de texto, dimensões e tabelas de fontes idênticos.
- Recorte: `santo-do-dia/2026-12-03/recorte.png`, 1080 × 1377 px.
- Janela na imagem original: `{"x": 242.1934501142423, "y": 0.0, "largura": 1435.6130997715154, "altura": 1883.0769230769229}`.
- Avisos de margem com o enquadramento novo: nenhum.

| Card | Campo | Linhas |
| --- | --- | --- |
| 1 | selo | 1 |
| 1 | data | 1 |
| 1 | grau | 1 |
| 1 | nome | 1 |
| 1 | titulo | 1 |
| 1 | frase | 3 |
| 1 | fonte | 1 |

### santo-do-dia · 2026-12-08

- Foco: `50% 20%`; zoom: `1`.
- PNG: somente a obra mudou.
- Textos, linhas, estilos e caixas: idênticos.
- Ficha antiga preservada fora do foco/zoom e da geometria do IMG; metadados novos de janela são registrados.
- PDF: texto extraído, caixas de texto, dimensões e tabelas de fontes idênticos.
- Recorte: `santo-do-dia/2026-12-08/recorte.png`, 1080 × 1584 px.
- Janela na imagem original: `{"x": 0.0, "y": 104.6422535211268, "largura": 1756.0, "altura": 2052.788732394366}`.
- Avisos de margem com o enquadramento novo: nenhum.

| Card | Campo | Linhas |
| --- | --- | --- |
| 1 | selo | 1 |
| 1 | data | 1 |
| 1 | credito | 1 |
| 1 | nome | 2 |

## Resultado

Todas as verificações passaram: fora das cinco obras, as artes aprovadas permanecem iguais.

As comparações dos PDFs removem apenas metadados de criação do documento e normalizam timestamp/checksum da tabela head dos subconjuntos TTF; desenhos, métricas, nomes e demais tabelas continuam sendo comparados. Os TTF fornecidos pelo kit são comparados byte a byte.

A importação no editor do Canva não foi executada. Evidências completas em `verificacao/conferencia-kit-v4.json`.
