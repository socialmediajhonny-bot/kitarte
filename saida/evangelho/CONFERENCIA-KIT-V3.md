# Conferência do Evangelho e dos componentes com o kit v3

Baseline das saídas: commit `cada2f9f9b678a62cfcd61b6fdbe819b78c92e25`. O kit v3 foi conferido byte a byte contra o ZIP rastreado: 44 arquivos e 11 ativos de logo; nenhuma alteração em `kit/`.

Comandos executados:

```bash
python gerar.py componentes
python gerar.py evangelho
```

- Componentes: 28 PNGs e 19 SVGs de elementos comparados com o HEAD. Todos idênticos em bytes.
- PDF de componentes: texto extraído, caixas dos textos, dimensões e tabelas das fontes embutidas idênticos (timestamp e checksum das fontes normalizados).

- Os seis TTF exportados mudam somente no carimbo `head.modified` e no checksum dependente dele. São cópias exatas das fontes do kit v3 reexportado; todas as tabelas de desenho, métricas, nomes e composição permanecem idênticas.

## Evangelho com as duas obras reais

O usuário autorizou a substituição das obras provisórias pelas obras locais. Portanto, as capas e as pranchas que as mostram mudam na região das imagens, e os rótulos deixam de indicar obra pendente. As demais comparações preservam composição, texto, tipografia e cores.

### 2026-11-29

- Obra: `obras/2026-11-29.jpg`; foco preservado em 50% 50%.
- Card 1: pixels fora da caixa da imagem idênticos; caixa x=216, y=168, 648 × 744 px.
- Cards 2, 3 e 4: idênticos em bytes.
- Textos, linhas, estilos, cores e caixas das fichas: idênticos.
- Na ficha, mudaram somente o estado de pendência, o caminho e as dimensões naturais da obra; portas efêmeras do servidor local foram normalizadas.
- PDF: 4 páginas de 810 × 1012,5 pt; texto, posições dos textos e tabelas de fontes idênticos (timestamp e checksum das fontes normalizados).
- Fontes embutidas: CormorantGaramond-MediumItalic, CormorantGaramond-SemiBold, Lato-Bold, Lato-Regular.
- Novo `recorte.png`: 1080 × 738 px, mostrando a obra inteira e o contorno do arco.

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

### 2026-12-13

- Obra: `obras/2026-12-13.jpg`; foco preservado em 50% 50%.
- Card 1: pixels fora da caixa da imagem idênticos; caixa x=216, y=168, 648 × 744 px.
- Cards 2, 3 e 4: idênticos em bytes.
- Textos, linhas, estilos, cores e caixas das fichas: idênticos.
- Na ficha, mudaram somente o estado de pendência, o caminho e as dimensões naturais da obra; portas efêmeras do servidor local foram normalizadas.
- PDF: 4 páginas de 810 × 1012,5 pt; texto, posições dos textos e tabelas de fontes idênticos (timestamp e checksum das fontes normalizados).
- Fontes embutidas: CormorantGaramond-MediumItalic, CormorantGaramond-SemiBold, Lato-Bold, Lato-Regular.
- Novo `recorte.png`: 1080 × 770 px, mostrando a obra inteira e o contorno do arco.

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

## Resultado

Todas as verificações passaram. As diferenças visuais são as obras reais nas capas e suas pranchas; foram gerados os dois recortes.

Obras pendentes no Evangelho: nenhuma.

As duas pranchas e os dois recortes foram abertos e inspecionados visualmente. As pranchas também foram comparadas por pixels: fora das capas e dos rótulos atualizados, permanecem idênticas. Os focos 50% 50% fornecidos foram preservados.

O ajuste local redundante de `text-wrap: balance` da reflexão foi removido: o kit v3 agora fornece o mesmo valor. A medição demonstra que suas linhas, posições e PDF foram preservados.

Os bytes completos dos PDFs não são usados como critério: além da obra substituída, há metadados de criação. As fontes reexportadas no kit v3 diferem em `head.modified` e, em consequência, `head.checkSumAdjustment`; os subconjuntos TTF embutidos no PDF carregam a mesma diferença. A conferência neutraliza somente esses dois campos e compara todas as tabelas; os desenhos e as métricas das fontes permanecem iguais.

A importação no editor do Canva não foi executada. Não foi feito download de obras; foram utilizadas somente as imagens locais. Evidências detalhadas, hashes e campos comparados estão em `conferencia-kit-v3.json`.
