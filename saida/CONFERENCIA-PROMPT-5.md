# Conferência do prompt 5 — saídas aprovadas e Isaías

Baseline: commit `99492d584f06aef42b65fb57a140ae97f408c270`, com 144 arquivos de saída preservados em `work/prompt5-baseline`.

Esta conferência cobre as saídas anteriores e o ajuste de Isaías. Stories e teste de importação têm suas verificações próprias.

## Resultado

Aprovado: somente as duas artes de publicação de Isaías mudaram, dentro da obra em arco.

- 55 PNGs anteriores são idênticos em pixels, incluindo componentes, Evangelho, Santo do Dia, Para Rezar e todas as imagens de Coragem de 28/12.
- Em 14/12, feed e status têm zero diferença fora do arco da obra. Textos, linhas, cores, caixas e assinaturas permanecem iguais.
- A prancha do Coragem muda somente nas duas miniaturas da obra de 14/12; os recortes acompanham a nova janela.
- Os 12 PDFs anteriores preservam texto extraído, posições de texto e fontes embutidas. Os PDFs do Coragem também foram rasterizados a 1080px para conferir a região permitida.

## Isaías

`python gerar.py coragem` executado para as duas datas. Em 14/12 foi aplicado foco `50% 0%`, sem zoom. O foco de 28/12 foi preservado.

| Formato | Parapeito → frase | Referência → assinatura | Margem uniforme |
| --- | --- | --- | --- |
| Feed | 66 px | 69 px | Nenhuma |
| Status | 81 px | 84 px | Nenhuma |

Feed, status e os dois recortes de Isaías foram abertos: a cabeça está inteira nos dois formatos; nenhum aviso de margem uniforme.
A nota anterior sobre o corte da cabeça foi substituída em `coragem/NOTAS-DE-ENQUADRAMENTO.md`.

## Regra de Ó e ó

A nova regra liga Ó/ó à palavra seguinte com espaço inseparável e rejeita linhas que terminem com essas palavras isoladas. Os demais validadores e a composição do Evangelho não foram alterados.

Os 18 documentos HTML das quatro séries de texto foram construídos com `text_html` do HEAD e com a função atual: todos são idênticos em bytes. Assim, a ampliação da regra não muda nenhum documento de render anterior. Os arquivos aprovados das outras quatro séries foram preservados, sem regeneração desnecessária.

Os testes cobrem Ó/ó ligados à palavra seguinte, preservação das quebras manuais e rejeição de fim de linha nas quatro séries existentes. As comparações detalhadas, hashes e diferenças permitidas estão em `verificacao/conferencia-prompt5.json`.

Não houve alteração no kit nem nas obras originais. A importação no editor do Canva é uma conferência externa e não foi executada nesta prova de regressão.
