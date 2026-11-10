# Evangelho do Dia

`python gerar.py evangelho` · seleção: `python gerar.py evangelho --data AAAA-MM-DD`

## Decisões

- A composição vem de PostEvangelho/preview.html e bundle.css; a capa mantém a obra dentro do arco CSS e desenha somente o filete como uma faixa vetorial em U, com um único path preenchido. O parapeito permanece separado.
- 32 px entre o texto e a referência e 48 px entre o rótulo e o texto, para o Canva importar cada um em sua caixa (teste de 29/10/2026). O gerador acrescenta margens inline em tokens ao gap de 16 px do kit e mede os pares no navegador, com tolerância de ±0,01 px.
- O card final resolve a cor no tema pergaminho e usa o logo sobre-cor da versão 2. Os demais usam capela.
- Textos sem quebras manuais usam balanceamento do navegador, inclusive o corpo da reflexão. Quebras YAML são `<br>`; espaços após a, à, e, é e o são inseparáveis.
- O selo tem ficha separada para série e data porque as cores e pesos diferem. As caixas são do DOM e as linhas são medidas com Range, depois do carregamento das seis fontes locais.
- A prancha de cores usa ouro como alias de liturgico-branco. As miniaturas medem exatamente 360 × 450 px; etiquetas ficam fora dos cards. A prancha principal indexa todas as datas já geradas, preservando as demais ao usar --data.
- Só obras reais recebem recorte.png; nenhum recurso externo é acessado. Os HTML e PDFs de uma página usados na composição ficam em work/ e não são necessários para importar os PDFs finais.

- O zoom amplia somente a imagem depois de object-fit:cover, com transform-origin no foco. O arco e a composição permanecem fixos. A ficha e o recorte registram a janela em pixels originais; margens uniformes visíveis geram aviso sem bloquear.

## Linhas medidas no render

| Data | Card | Campo | Estilo | Linhas | Limite |
| --- | --- | --- | --- | --- | --- |
| 2026-11-29 | 1 | selo | selo | 1 | — |
| 2026-11-29 | 1 | data | selo | 1 | — |
| 2026-11-29 | 1 | referencia | selo | 1 | — |
| 2026-11-29 | 1 | credito | credito | 1 | 1 |
| 2026-11-29 | 1 | titulo | titulo | 2 | 2 |
| 2026-11-29 | 2 | selo | selo | 1 | — |
| 2026-11-29 | 2 | data | selo | 1 | — |
| 2026-11-29 | 2 | referencia | selo | 1 | — |
| 2026-11-29 | 2 | trecho | citacao-grande | 2 | 3 |
| 2026-11-29 | 2 | trecho_ref | referencia | 1 | — |
| 2026-11-29 | 3 | selo | selo | 1 | — |
| 2026-11-29 | 3 | data | selo | 1 | — |
| 2026-11-29 | 3 | referencia | selo | 1 | — |
| 2026-11-29 | 3 | chamada_reflexao | selo | 1 | — |
| 2026-11-29 | 3 | reflexao.titulo | titulo | 1 | 2 |
| 2026-11-29 | 3 | reflexao.texto | corpo | 5 | 6 |
| 2026-11-29 | 4 | selo | selo | 1 | — |
| 2026-11-29 | 4 | data | selo | 1 | — |
| 2026-11-29 | 4 | referencia | selo | 1 | — |
| 2026-11-29 | 4 | chamada_oracao | selo | 1 | — |
| 2026-11-29 | 4 | pergunta | citacao | 2 | 4 |
| 2026-11-29 | 4 | convite | corpo | 1 | 1 |
| 2026-11-30 | 1 | selo | selo | 1 | — |
| 2026-11-30 | 1 | data | selo | 1 | — |
| 2026-11-30 | 1 | referencia | selo | 1 | — |
| 2026-11-30 | 1 | credito | credito | 1 | 1 |
| 2026-11-30 | 1 | titulo | titulo | 2 | 2 |
| 2026-11-30 | 2 | selo | selo | 1 | — |
| 2026-11-30 | 2 | data | selo | 1 | — |
| 2026-11-30 | 2 | referencia | selo | 1 | — |
| 2026-11-30 | 2 | trecho | citacao-grande | 3 | 3 |
| 2026-11-30 | 2 | trecho_ref | referencia | 1 | — |
| 2026-11-30 | 3 | selo | selo | 1 | — |
| 2026-11-30 | 3 | data | selo | 1 | — |
| 2026-11-30 | 3 | referencia | selo | 1 | — |
| 2026-11-30 | 3 | chamada_oracao | selo | 1 | — |
| 2026-11-30 | 3 | pergunta | citacao | 2 | 4 |
| 2026-11-30 | 3 | convite | corpo | 1 | 1 |
| 2026-12-01 | 1 | selo | selo | 1 | — |
| 2026-12-01 | 1 | data | selo | 1 | — |
| 2026-12-01 | 1 | referencia | selo | 1 | — |
| 2026-12-01 | 1 | credito | credito | 1 | 1 |
| 2026-12-01 | 1 | titulo | titulo | 1 | 2 |
| 2026-12-01 | 2 | selo | selo | 1 | — |
| 2026-12-01 | 2 | data | selo | 1 | — |
| 2026-12-01 | 2 | referencia | selo | 1 | — |
| 2026-12-01 | 2 | trecho | citacao | 3 | 4 |
| 2026-12-01 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-01 | 3 | selo | selo | 1 | — |
| 2026-12-01 | 3 | data | selo | 1 | — |
| 2026-12-01 | 3 | referencia | selo | 1 | — |
| 2026-12-01 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-01 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-01 | 3 | convite | corpo | 1 | 1 |
| 2026-12-02 | 1 | selo | selo | 1 | — |
| 2026-12-02 | 1 | data | selo | 1 | — |
| 2026-12-02 | 1 | referencia | selo | 1 | — |
| 2026-12-02 | 1 | credito | credito | 1 | 1 |
| 2026-12-02 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-02 | 2 | selo | selo | 1 | — |
| 2026-12-02 | 2 | data | selo | 1 | — |
| 2026-12-02 | 2 | referencia | selo | 1 | — |
| 2026-12-02 | 2 | trecho | citacao | 3 | 4 |
| 2026-12-02 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-02 | 3 | selo | selo | 1 | — |
| 2026-12-02 | 3 | data | selo | 1 | — |
| 2026-12-02 | 3 | referencia | selo | 1 | — |
| 2026-12-02 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-02 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-02 | 3 | convite | corpo | 1 | 1 |
| 2026-12-03 | 1 | selo | selo | 1 | — |
| 2026-12-03 | 1 | data | selo | 1 | — |
| 2026-12-03 | 1 | referencia | selo | 1 | — |
| 2026-12-03 | 1 | credito | credito | 1 | 1 |
| 2026-12-03 | 1 | titulo | titulo | 1 | 2 |
| 2026-12-03 | 2 | selo | selo | 1 | — |
| 2026-12-03 | 2 | data | selo | 1 | — |
| 2026-12-03 | 2 | referencia | selo | 1 | — |
| 2026-12-03 | 2 | trecho | citacao | 3 | 4 |
| 2026-12-03 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-03 | 3 | selo | selo | 1 | — |
| 2026-12-03 | 3 | data | selo | 1 | — |
| 2026-12-03 | 3 | referencia | selo | 1 | — |
| 2026-12-03 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-03 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-03 | 3 | convite | corpo | 1 | 1 |
| 2026-12-04 | 1 | selo | selo | 1 | — |
| 2026-12-04 | 1 | data | selo | 1 | — |
| 2026-12-04 | 1 | referencia | selo | 1 | — |
| 2026-12-04 | 1 | credito | credito | 1 | 1 |
| 2026-12-04 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-04 | 2 | selo | selo | 1 | — |
| 2026-12-04 | 2 | data | selo | 1 | — |
| 2026-12-04 | 2 | referencia | selo | 1 | — |
| 2026-12-04 | 2 | trecho | citacao-grande | 1 | 3 |
| 2026-12-04 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-04 | 3 | selo | selo | 1 | — |
| 2026-12-04 | 3 | data | selo | 1 | — |
| 2026-12-04 | 3 | referencia | selo | 1 | — |
| 2026-12-04 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-04 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-04 | 3 | convite | corpo | 1 | 1 |
| 2026-12-05 | 1 | selo | selo | 1 | — |
| 2026-12-05 | 1 | data | selo | 1 | — |
| 2026-12-05 | 1 | referencia | selo | 1 | — |
| 2026-12-05 | 1 | credito | credito | 1 | 1 |
| 2026-12-05 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-05 | 2 | selo | selo | 1 | — |
| 2026-12-05 | 2 | data | selo | 1 | — |
| 2026-12-05 | 2 | referencia | selo | 1 | — |
| 2026-12-05 | 2 | trecho | citacao-grande | 2 | 3 |
| 2026-12-05 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-05 | 3 | selo | selo | 1 | — |
| 2026-12-05 | 3 | data | selo | 1 | — |
| 2026-12-05 | 3 | referencia | selo | 1 | — |
| 2026-12-05 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-05 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-05 | 3 | convite | corpo | 1 | 1 |
| 2026-12-06 | 1 | selo | selo | 1 | — |
| 2026-12-06 | 1 | data | selo | 1 | — |
| 2026-12-06 | 1 | referencia | selo | 1 | — |
| 2026-12-06 | 1 | credito | credito | 1 | 1 |
| 2026-12-06 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-06 | 2 | selo | selo | 1 | — |
| 2026-12-06 | 2 | data | selo | 1 | — |
| 2026-12-06 | 2 | referencia | selo | 1 | — |
| 2026-12-06 | 2 | trecho | citacao-grande | 2 | 3 |
| 2026-12-06 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-06 | 3 | selo | selo | 1 | — |
| 2026-12-06 | 3 | data | selo | 1 | — |
| 2026-12-06 | 3 | referencia | selo | 1 | — |
| 2026-12-06 | 3 | chamada_reflexao | selo | 1 | — |
| 2026-12-06 | 3 | reflexao.titulo | titulo | 1 | 2 |
| 2026-12-06 | 3 | reflexao.texto | corpo | 5 | 6 |
| 2026-12-06 | 4 | selo | selo | 1 | — |
| 2026-12-06 | 4 | data | selo | 1 | — |
| 2026-12-06 | 4 | referencia | selo | 1 | — |
| 2026-12-06 | 4 | chamada_oracao | selo | 1 | — |
| 2026-12-06 | 4 | pergunta | citacao | 2 | 4 |
| 2026-12-06 | 4 | convite | corpo | 1 | 1 |
| 2026-12-07 | 1 | selo | selo | 1 | — |
| 2026-12-07 | 1 | data | selo | 1 | — |
| 2026-12-07 | 1 | referencia | selo | 1 | — |
| 2026-12-07 | 1 | credito | credito | 1 | 1 |
| 2026-12-07 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-07 | 2 | selo | selo | 1 | — |
| 2026-12-07 | 2 | data | selo | 1 | — |
| 2026-12-07 | 2 | referencia | selo | 1 | — |
| 2026-12-07 | 2 | trecho | citacao-grande | 2 | 3 |
| 2026-12-07 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-07 | 3 | selo | selo | 1 | — |
| 2026-12-07 | 3 | data | selo | 1 | — |
| 2026-12-07 | 3 | referencia | selo | 1 | — |
| 2026-12-07 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-07 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-07 | 3 | convite | corpo | 1 | 1 |
| 2026-12-08 | 1 | selo | selo | 1 | — |
| 2026-12-08 | 1 | data | selo | 1 | — |
| 2026-12-08 | 1 | referencia | selo | 1 | — |
| 2026-12-08 | 1 | credito | credito | 1 | 1 |
| 2026-12-08 | 1 | titulo | titulo | 1 | 2 |
| 2026-12-08 | 2 | selo | selo | 1 | — |
| 2026-12-08 | 2 | data | selo | 1 | — |
| 2026-12-08 | 2 | referencia | selo | 1 | — |
| 2026-12-08 | 2 | trecho | citacao-grande | 2 | 3 |
| 2026-12-08 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-08 | 3 | selo | selo | 1 | — |
| 2026-12-08 | 3 | data | selo | 1 | — |
| 2026-12-08 | 3 | referencia | selo | 1 | — |
| 2026-12-08 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-08 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-08 | 3 | convite | corpo | 1 | 1 |
| 2026-12-09 | 1 | selo | selo | 1 | — |
| 2026-12-09 | 1 | data | selo | 1 | — |
| 2026-12-09 | 1 | referencia | selo | 1 | — |
| 2026-12-09 | 1 | credito | credito | 1 | 1 |
| 2026-12-09 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-09 | 2 | selo | selo | 1 | — |
| 2026-12-09 | 2 | data | selo | 1 | — |
| 2026-12-09 | 2 | referencia | selo | 1 | — |
| 2026-12-09 | 2 | trecho | citacao | 3 | 4 |
| 2026-12-09 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-09 | 3 | selo | selo | 1 | — |
| 2026-12-09 | 3 | data | selo | 1 | — |
| 2026-12-09 | 3 | referencia | selo | 1 | — |
| 2026-12-09 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-09 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-09 | 3 | convite | corpo | 1 | 1 |
| 2026-12-10 | 1 | selo | selo | 1 | — |
| 2026-12-10 | 1 | data | selo | 1 | — |
| 2026-12-10 | 1 | referencia | selo | 1 | — |
| 2026-12-10 | 1 | credito | credito | 1 | 1 |
| 2026-12-10 | 1 | titulo | titulo | 1 | 2 |
| 2026-12-10 | 2 | selo | selo | 1 | — |
| 2026-12-10 | 2 | data | selo | 1 | — |
| 2026-12-10 | 2 | referencia | selo | 1 | — |
| 2026-12-10 | 2 | trecho | citacao-grande | 2 | 3 |
| 2026-12-10 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-10 | 3 | selo | selo | 1 | — |
| 2026-12-10 | 3 | data | selo | 1 | — |
| 2026-12-10 | 3 | referencia | selo | 1 | — |
| 2026-12-10 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-10 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-10 | 3 | convite | corpo | 1 | 1 |
| 2026-12-11 | 1 | selo | selo | 1 | — |
| 2026-12-11 | 1 | data | selo | 1 | — |
| 2026-12-11 | 1 | referencia | selo | 1 | — |
| 2026-12-11 | 1 | credito | credito | 1 | 1 |
| 2026-12-11 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-11 | 2 | selo | selo | 1 | — |
| 2026-12-11 | 2 | data | selo | 1 | — |
| 2026-12-11 | 2 | referencia | selo | 1 | — |
| 2026-12-11 | 2 | trecho | citacao | 3 | 4 |
| 2026-12-11 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-11 | 3 | selo | selo | 1 | — |
| 2026-12-11 | 3 | data | selo | 1 | — |
| 2026-12-11 | 3 | referencia | selo | 1 | — |
| 2026-12-11 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-11 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-11 | 3 | convite | corpo | 1 | 1 |
| 2026-12-12 | 1 | selo | selo | 1 | — |
| 2026-12-12 | 1 | data | selo | 1 | — |
| 2026-12-12 | 1 | referencia | selo | 1 | — |
| 2026-12-12 | 1 | credito | credito | 1 | 1 |
| 2026-12-12 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-12 | 2 | selo | selo | 1 | — |
| 2026-12-12 | 2 | data | selo | 1 | — |
| 2026-12-12 | 2 | referencia | selo | 1 | — |
| 2026-12-12 | 2 | trecho | citacao | 2 | 4 |
| 2026-12-12 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-12 | 3 | selo | selo | 1 | — |
| 2026-12-12 | 3 | data | selo | 1 | — |
| 2026-12-12 | 3 | referencia | selo | 1 | — |
| 2026-12-12 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-12 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-12 | 3 | convite | corpo | 1 | 1 |
| 2026-12-13 | 1 | selo | selo | 1 | — |
| 2026-12-13 | 1 | data | selo | 1 | — |
| 2026-12-13 | 1 | referencia | selo | 1 | — |
| 2026-12-13 | 1 | credito | credito | 1 | 1 |
| 2026-12-13 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-13 | 2 | selo | selo | 1 | — |
| 2026-12-13 | 2 | data | selo | 1 | — |
| 2026-12-13 | 2 | referencia | selo | 1 | — |
| 2026-12-13 | 2 | trecho | citacao-grande | 2 | 3 |
| 2026-12-13 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-13 | 3 | selo | selo | 1 | — |
| 2026-12-13 | 3 | data | selo | 1 | — |
| 2026-12-13 | 3 | referencia | selo | 1 | — |
| 2026-12-13 | 3 | chamada_reflexao | selo | 1 | — |
| 2026-12-13 | 3 | reflexao.titulo | titulo | 1 | 2 |
| 2026-12-13 | 3 | reflexao.texto | corpo | 4 | 6 |
| 2026-12-13 | 4 | selo | selo | 1 | — |
| 2026-12-13 | 4 | data | selo | 1 | — |
| 2026-12-13 | 4 | referencia | selo | 1 | — |
| 2026-12-13 | 4 | chamada_oracao | selo | 1 | — |
| 2026-12-13 | 4 | pergunta | citacao | 2 | 4 |
| 2026-12-13 | 4 | convite | corpo | 1 | 1 |
| 2026-12-14 | 1 | selo | selo | 1 | — |
| 2026-12-14 | 1 | data | selo | 1 | — |
| 2026-12-14 | 1 | referencia | selo | 1 | — |
| 2026-12-14 | 1 | credito | credito | 1 | 1 |
| 2026-12-14 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-14 | 2 | selo | selo | 1 | — |
| 2026-12-14 | 2 | data | selo | 1 | — |
| 2026-12-14 | 2 | referencia | selo | 1 | — |
| 2026-12-14 | 2 | trecho | citacao-grande | 3 | 3 |
| 2026-12-14 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-14 | 3 | selo | selo | 1 | — |
| 2026-12-14 | 3 | data | selo | 1 | — |
| 2026-12-14 | 3 | referencia | selo | 1 | — |
| 2026-12-14 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-14 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-14 | 3 | convite | corpo | 1 | 1 |
| 2026-12-15 | 1 | selo | selo | 1 | — |
| 2026-12-15 | 1 | data | selo | 1 | — |
| 2026-12-15 | 1 | referencia | selo | 1 | — |
| 2026-12-15 | 1 | credito | credito | 1 | 1 |
| 2026-12-15 | 1 | titulo | titulo | 1 | 2 |
| 2026-12-15 | 2 | selo | selo | 1 | — |
| 2026-12-15 | 2 | data | selo | 1 | — |
| 2026-12-15 | 2 | referencia | selo | 1 | — |
| 2026-12-15 | 2 | trecho | citacao-grande | 3 | 3 |
| 2026-12-15 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-15 | 3 | selo | selo | 1 | — |
| 2026-12-15 | 3 | data | selo | 1 | — |
| 2026-12-15 | 3 | referencia | selo | 1 | — |
| 2026-12-15 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-15 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-15 | 3 | convite | corpo | 1 | 1 |
| 2026-12-16 | 1 | selo | selo | 1 | — |
| 2026-12-16 | 1 | data | selo | 1 | — |
| 2026-12-16 | 1 | referencia | selo | 1 | — |
| 2026-12-16 | 1 | credito | credito | 1 | 1 |
| 2026-12-16 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-16 | 2 | selo | selo | 1 | — |
| 2026-12-16 | 2 | data | selo | 1 | — |
| 2026-12-16 | 2 | referencia | selo | 1 | — |
| 2026-12-16 | 2 | trecho | citacao-grande | 2 | 3 |
| 2026-12-16 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-16 | 3 | selo | selo | 1 | — |
| 2026-12-16 | 3 | data | selo | 1 | — |
| 2026-12-16 | 3 | referencia | selo | 1 | — |
| 2026-12-16 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-16 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-16 | 3 | convite | corpo | 1 | 1 |
| 2026-12-17 | 1 | selo | selo | 1 | — |
| 2026-12-17 | 1 | data | selo | 1 | — |
| 2026-12-17 | 1 | referencia | selo | 1 | — |
| 2026-12-17 | 1 | credito | credito | 1 | 1 |
| 2026-12-17 | 1 | titulo | titulo | 1 | 2 |
| 2026-12-17 | 2 | selo | selo | 1 | — |
| 2026-12-17 | 2 | data | selo | 1 | — |
| 2026-12-17 | 2 | referencia | selo | 1 | — |
| 2026-12-17 | 2 | trecho | citacao-grande | 3 | 3 |
| 2026-12-17 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-17 | 3 | selo | selo | 1 | — |
| 2026-12-17 | 3 | data | selo | 1 | — |
| 2026-12-17 | 3 | referencia | selo | 1 | — |
| 2026-12-17 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-17 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-17 | 3 | convite | corpo | 1 | 1 |
| 2026-12-18 | 1 | selo | selo | 1 | — |
| 2026-12-18 | 1 | data | selo | 1 | — |
| 2026-12-18 | 1 | referencia | selo | 1 | — |
| 2026-12-18 | 1 | credito | credito | 1 | 1 |
| 2026-12-18 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-18 | 2 | selo | selo | 1 | — |
| 2026-12-18 | 2 | data | selo | 1 | — |
| 2026-12-18 | 2 | referencia | selo | 1 | — |
| 2026-12-18 | 2 | trecho | citacao | 3 | 4 |
| 2026-12-18 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-18 | 3 | selo | selo | 1 | — |
| 2026-12-18 | 3 | data | selo | 1 | — |
| 2026-12-18 | 3 | referencia | selo | 1 | — |
| 2026-12-18 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-18 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-18 | 3 | convite | corpo | 1 | 1 |
| 2026-12-19 | 1 | selo | selo | 1 | — |
| 2026-12-19 | 1 | data | selo | 1 | — |
| 2026-12-19 | 1 | referencia | selo | 1 | — |
| 2026-12-19 | 1 | credito | credito | 1 | 1 |
| 2026-12-19 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-19 | 2 | selo | selo | 1 | — |
| 2026-12-19 | 2 | data | selo | 1 | — |
| 2026-12-19 | 2 | referencia | selo | 1 | — |
| 2026-12-19 | 2 | trecho | citacao-grande | 2 | 3 |
| 2026-12-19 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-19 | 3 | selo | selo | 1 | — |
| 2026-12-19 | 3 | data | selo | 1 | — |
| 2026-12-19 | 3 | referencia | selo | 1 | — |
| 2026-12-19 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-19 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-19 | 3 | convite | corpo | 1 | 1 |
| 2026-12-20 | 1 | selo | selo | 1 | — |
| 2026-12-20 | 1 | data | selo | 1 | — |
| 2026-12-20 | 1 | referencia | selo | 1 | — |
| 2026-12-20 | 1 | credito | credito | 1 | 1 |
| 2026-12-20 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-20 | 2 | selo | selo | 1 | — |
| 2026-12-20 | 2 | data | selo | 1 | — |
| 2026-12-20 | 2 | referencia | selo | 1 | — |
| 2026-12-20 | 2 | trecho | citacao-grande | 1 | 3 |
| 2026-12-20 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-20 | 3 | selo | selo | 1 | — |
| 2026-12-20 | 3 | data | selo | 1 | — |
| 2026-12-20 | 3 | referencia | selo | 1 | — |
| 2026-12-20 | 3 | chamada_reflexao | selo | 1 | — |
| 2026-12-20 | 3 | reflexao.titulo | titulo | 1 | 2 |
| 2026-12-20 | 3 | reflexao.texto | corpo | 5 | 6 |
| 2026-12-20 | 4 | selo | selo | 1 | — |
| 2026-12-20 | 4 | data | selo | 1 | — |
| 2026-12-20 | 4 | referencia | selo | 1 | — |
| 2026-12-20 | 4 | chamada_oracao | selo | 1 | — |
| 2026-12-20 | 4 | pergunta | citacao | 2 | 4 |
| 2026-12-20 | 4 | convite | corpo | 1 | 1 |
| 2026-12-21 | 1 | selo | selo | 1 | — |
| 2026-12-21 | 1 | data | selo | 1 | — |
| 2026-12-21 | 1 | referencia | selo | 1 | — |
| 2026-12-21 | 1 | credito | credito | 1 | 1 |
| 2026-12-21 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-21 | 2 | selo | selo | 1 | — |
| 2026-12-21 | 2 | data | selo | 1 | — |
| 2026-12-21 | 2 | referencia | selo | 1 | — |
| 2026-12-21 | 2 | trecho | citacao | 3 | 4 |
| 2026-12-21 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-21 | 3 | selo | selo | 1 | — |
| 2026-12-21 | 3 | data | selo | 1 | — |
| 2026-12-21 | 3 | referencia | selo | 1 | — |
| 2026-12-21 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-21 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-21 | 3 | convite | corpo | 1 | 1 |
| 2026-12-22 | 1 | selo | selo | 1 | — |
| 2026-12-22 | 1 | data | selo | 1 | — |
| 2026-12-22 | 1 | referencia | selo | 1 | — |
| 2026-12-22 | 1 | credito | credito | 1 | 1 |
| 2026-12-22 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-22 | 2 | selo | selo | 1 | — |
| 2026-12-22 | 2 | data | selo | 1 | — |
| 2026-12-22 | 2 | referencia | selo | 1 | — |
| 2026-12-22 | 2 | trecho | citacao-grande | 3 | 3 |
| 2026-12-22 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-22 | 3 | selo | selo | 1 | — |
| 2026-12-22 | 3 | data | selo | 1 | — |
| 2026-12-22 | 3 | referencia | selo | 1 | — |
| 2026-12-22 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-22 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-22 | 3 | convite | corpo | 1 | 1 |
| 2026-12-23 | 1 | selo | selo | 1 | — |
| 2026-12-23 | 1 | data | selo | 1 | — |
| 2026-12-23 | 1 | referencia | selo | 1 | — |
| 2026-12-23 | 1 | credito | credito | 1 | 1 |
| 2026-12-23 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-23 | 2 | selo | selo | 1 | — |
| 2026-12-23 | 2 | data | selo | 1 | — |
| 2026-12-23 | 2 | referencia | selo | 1 | — |
| 2026-12-23 | 2 | trecho | citacao-grande | 3 | 3 |
| 2026-12-23 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-23 | 3 | selo | selo | 1 | — |
| 2026-12-23 | 3 | data | selo | 1 | — |
| 2026-12-23 | 3 | referencia | selo | 1 | — |
| 2026-12-23 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-23 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-23 | 3 | convite | corpo | 1 | 1 |
| 2026-12-24 | 1 | selo | selo | 1 | — |
| 2026-12-24 | 1 | data | selo | 1 | — |
| 2026-12-24 | 1 | referencia | selo | 1 | — |
| 2026-12-24 | 1 | credito | credito | 1 | 1 |
| 2026-12-24 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-24 | 2 | selo | selo | 1 | — |
| 2026-12-24 | 2 | data | selo | 1 | — |
| 2026-12-24 | 2 | referencia | selo | 1 | — |
| 2026-12-24 | 2 | trecho | citacao-grande | 3 | 3 |
| 2026-12-24 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-24 | 3 | selo | selo | 1 | — |
| 2026-12-24 | 3 | data | selo | 1 | — |
| 2026-12-24 | 3 | referencia | selo | 1 | — |
| 2026-12-24 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-24 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-24 | 3 | convite | corpo | 1 | 1 |
| 2026-12-25 | 1 | selo | selo | 1 | — |
| 2026-12-25 | 1 | data | selo | 1 | — |
| 2026-12-25 | 1 | referencia | selo | 1 | — |
| 2026-12-25 | 1 | credito | credito | 1 | 1 |
| 2026-12-25 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-25 | 2 | selo | selo | 1 | — |
| 2026-12-25 | 2 | data | selo | 1 | — |
| 2026-12-25 | 2 | referencia | selo | 1 | — |
| 2026-12-25 | 2 | trecho | citacao-grande | 3 | 3 |
| 2026-12-25 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-25 | 3 | selo | selo | 1 | — |
| 2026-12-25 | 3 | data | selo | 1 | — |
| 2026-12-25 | 3 | referencia | selo | 1 | — |
| 2026-12-25 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-25 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-25 | 3 | convite | corpo | 1 | 1 |
| 2026-12-26 | 1 | selo | selo | 1 | — |
| 2026-12-26 | 1 | data | selo | 1 | — |
| 2026-12-26 | 1 | referencia | selo | 1 | — |
| 2026-12-26 | 1 | credito | credito | 1 | 1 |
| 2026-12-26 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-26 | 2 | selo | selo | 1 | — |
| 2026-12-26 | 2 | data | selo | 1 | — |
| 2026-12-26 | 2 | referencia | selo | 1 | — |
| 2026-12-26 | 2 | trecho | citacao | 3 | 4 |
| 2026-12-26 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-26 | 3 | selo | selo | 1 | — |
| 2026-12-26 | 3 | data | selo | 1 | — |
| 2026-12-26 | 3 | referencia | selo | 1 | — |
| 2026-12-26 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-26 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-26 | 3 | convite | corpo | 1 | 1 |
| 2026-12-27 | 1 | selo | selo | 1 | — |
| 2026-12-27 | 1 | data | selo | 1 | — |
| 2026-12-27 | 1 | referencia | selo | 1 | — |
| 2026-12-27 | 1 | credito | credito | 1 | 1 |
| 2026-12-27 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-27 | 2 | selo | selo | 1 | — |
| 2026-12-27 | 2 | data | selo | 1 | — |
| 2026-12-27 | 2 | referencia | selo | 1 | — |
| 2026-12-27 | 2 | trecho | citacao | 2 | 4 |
| 2026-12-27 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-27 | 3 | selo | selo | 1 | — |
| 2026-12-27 | 3 | data | selo | 1 | — |
| 2026-12-27 | 3 | referencia | selo | 1 | — |
| 2026-12-27 | 3 | chamada_reflexao | selo | 1 | — |
| 2026-12-27 | 3 | reflexao.titulo | titulo | 1 | 2 |
| 2026-12-27 | 3 | reflexao.texto | corpo | 5 | 6 |
| 2026-12-27 | 4 | selo | selo | 1 | — |
| 2026-12-27 | 4 | data | selo | 1 | — |
| 2026-12-27 | 4 | referencia | selo | 1 | — |
| 2026-12-27 | 4 | chamada_oracao | selo | 1 | — |
| 2026-12-27 | 4 | pergunta | citacao | 2 | 4 |
| 2026-12-27 | 4 | convite | corpo | 1 | 1 |
| 2026-12-28 | 1 | selo | selo | 1 | — |
| 2026-12-28 | 1 | data | selo | 1 | — |
| 2026-12-28 | 1 | referencia | selo | 1 | — |
| 2026-12-28 | 1 | credito | credito | 1 | 1 |
| 2026-12-28 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-28 | 2 | selo | selo | 1 | — |
| 2026-12-28 | 2 | data | selo | 1 | — |
| 2026-12-28 | 2 | referencia | selo | 1 | — |
| 2026-12-28 | 2 | trecho | citacao-grande | 2 | 3 |
| 2026-12-28 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-28 | 3 | selo | selo | 1 | — |
| 2026-12-28 | 3 | data | selo | 1 | — |
| 2026-12-28 | 3 | referencia | selo | 1 | — |
| 2026-12-28 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-28 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-28 | 3 | convite | corpo | 1 | 1 |
| 2026-12-29 | 1 | selo | selo | 1 | — |
| 2026-12-29 | 1 | data | selo | 1 | — |
| 2026-12-29 | 1 | referencia | selo | 1 | — |
| 2026-12-29 | 1 | credito | credito | 1 | 1 |
| 2026-12-29 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-29 | 2 | selo | selo | 1 | — |
| 2026-12-29 | 2 | data | selo | 1 | — |
| 2026-12-29 | 2 | referencia | selo | 1 | — |
| 2026-12-29 | 2 | trecho | citacao | 3 | 4 |
| 2026-12-29 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-29 | 3 | selo | selo | 1 | — |
| 2026-12-29 | 3 | data | selo | 1 | — |
| 2026-12-29 | 3 | referencia | selo | 1 | — |
| 2026-12-29 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-29 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-29 | 3 | convite | corpo | 1 | 1 |
| 2026-12-30 | 1 | selo | selo | 1 | — |
| 2026-12-30 | 1 | data | selo | 1 | — |
| 2026-12-30 | 1 | referencia | selo | 1 | — |
| 2026-12-30 | 1 | credito | credito | 1 | 1 |
| 2026-12-30 | 1 | titulo | titulo | 2 | 2 |
| 2026-12-30 | 2 | selo | selo | 1 | — |
| 2026-12-30 | 2 | data | selo | 1 | — |
| 2026-12-30 | 2 | referencia | selo | 1 | — |
| 2026-12-30 | 2 | trecho | citacao | 3 | 4 |
| 2026-12-30 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-30 | 3 | selo | selo | 1 | — |
| 2026-12-30 | 3 | data | selo | 1 | — |
| 2026-12-30 | 3 | referencia | selo | 1 | — |
| 2026-12-30 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-30 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-30 | 3 | convite | corpo | 1 | 1 |
| 2026-12-31 | 1 | selo | selo | 1 | — |
| 2026-12-31 | 1 | data | selo | 1 | — |
| 2026-12-31 | 1 | referencia | selo | 1 | — |
| 2026-12-31 | 1 | credito | credito | 1 | 1 |
| 2026-12-31 | 1 | titulo | titulo | 1 | 2 |
| 2026-12-31 | 2 | selo | selo | 1 | — |
| 2026-12-31 | 2 | data | selo | 1 | — |
| 2026-12-31 | 2 | referencia | selo | 1 | — |
| 2026-12-31 | 2 | trecho | citacao-grande | 2 | 3 |
| 2026-12-31 | 2 | trecho_ref | referencia | 1 | — |
| 2026-12-31 | 3 | selo | selo | 1 | — |
| 2026-12-31 | 3 | data | selo | 1 | — |
| 2026-12-31 | 3 | referencia | selo | 1 | — |
| 2026-12-31 | 3 | chamada_oracao | selo | 1 | — |
| 2026-12-31 | 3 | pergunta | citacao | 2 | 4 |
| 2026-12-31 | 3 | convite | corpo | 1 | 1 |

## Obras e legendas

- **2026-11-29 — 1º Domingo do Advento:** obra local real; recorte.png gerado.
  James Tissot · A profecia da destruição do Templo · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4551
  Foco 45% 50%; zoom 1.1; janela original x=309.337, y=46.591, largura=811.584, altura=931.818px.
- **2026-11-30 — Santo André, apóstolo (Festa):** obra local real; recorte.png gerado.
  Duccio · A vocação dos apóstolos Pedro e André · National Gallery of Art — https://www.nga.gov/artworks/282-calling-apostles-peter-and-andrew
  Foco 10% 50%; zoom 1; janela original x=47.223, y=0.000, largura=2127.774, altura=2443.000px.
- **2026-12-01 — Terça-feira da 1ª Semana do Advento:** obra local real; recorte.png gerado.
  James Tissot · Deixai vir a mim as criancinhas · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4539
  Foco 20% 45%; zoom 1.1; janela original x=124.930, y=47.086, largura=911.349, altura=1046.364px.
- **2026-12-02 — Quarta-feira da 1ª Semana do Advento:** obra local real; recorte.png gerado.
  James Tissot · A multiplicação dos pães · Brooklyn Museum — https://www.brooklynmuseum.org/objects/13423
  Foco 50% 50%; zoom 1.1; janela original x=348.352, y=48.182, largura=839.296, altura=963.636px.
- **2026-12-03 — São Francisco Xavier, presbítero (Memória):** obra local real; recorte.png gerado.
  James Tissot · O sermão das bem-aventuranças · Brooklyn Museum — https://www.brooklynmuseum.org/objects/13418
  Foco 50% 15%; zoom 1.1; janela original x=48.455, y=63.501, largura=969.091, altura=1112.660px.
- **2026-12-04 — Sexta-feira da 1ª Semana do Advento:** obra local real; recorte.png gerado.
  James Tissot · Os cegos de Cafarnaum · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4505
  Foco 50% 80%; zoom 1.2; janela original x=71.500, y=572.059, largura=715.000, altura=820.926px.
- **2026-12-05 — Sábado da 1ª Semana do Advento:** obra local real; recorte.png gerado.
  James Tissot · A escolha dos doze apóstolos · Brooklyn Museum — https://www.brooklynmuseum.org/objects/13407
  Foco 25% 50%; zoom 1.1; janela original x=184.073, y=45.909, largura=799.707, altura=918.182px.
- **2026-12-06 — 2º Domingo do Advento:** obra local real; recorte.png gerado.
  James Tissot · A voz no deserto · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4447
  Foco 40% 15%; zoom 1.1; janela original x=33.091, y=87.925, largura=827.273, altura=949.832px.
- **2026-12-07 — Santo Ambrósio, bispo e doutor da Igreja (Memória):** obra local real; recorte.png gerado.
  James Tissot · O paralítico descido pelo telhado · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4504
  Foco 50% 20%; zoom 1.04; janela original x=20.942, y=66.751, largura=1047.115, altura=1202.244px.
- **2026-12-08 — Imaculada Conceição da Bem-aventurada Virgem Maria (Solenidade):** obra local real; recorte.png gerado.
  Fra Angelico · A Anunciação · Museu do Prado — https://commons.wikimedia.org/wiki/File:La_Anunciación,_by_Fra_Angelico,_from_Prado_in_Google_Earth.jpg
  Foco 82% 40%; zoom 1.3; janela original x=1067.200, y=349.754, largura=2538.536, altura=2914.615px.
- **2026-12-09 — Quarta-feira da 2ª Semana do Advento:** obra local real; recorte.png gerado.
  Ary Scheffer · Cristo Consolador · Minneapolis Institute of Art — https://collections.artsmia.org/art/104894/christus-consolator-ary-scheffer
  Foco 48% 27%; zoom 3; janela original x=2382.705, y=910.800, largura=1469.032, altura=1686.667px.
- **2026-12-10 — Quinta-feira da 2ª Semana do Advento:** obra local real; recorte.png gerado.
  Geertgen tot Sint Jans · São João Batista no deserto · Gemäldegalerie — https://commons.wikimedia.org/wiki/File:Geertgen_tot_Sint_Jans_004.jpg
  Foco 50% 98%; zoom 1; janela original x=0.000, y=433.559, largura=1192.000, altura=1368.593px.
- **2026-12-11 — Sexta-feira da 2ª Semana do Advento:** obra local real; recorte.png gerado.
  James Tissot · A refeição na casa de Mateus · Brooklyn Museum — https://www.brooklynmuseum.org/objects/13405
  Foco 88% 25%; zoom 1.3; janela original x=683.098, y=65.423, largura=759.752, altura=872.308px.
- **2026-12-12 — Bem-aventurada Virgem Maria de Guadalupe, Padroeira principal da América (Festa):** obra local real; recorte.png gerado.
  Piero di Cosimo · A Visitação · National Gallery of Art — https://www.nga.gov/artworks/505-visitation-saint-nicholas-and-saint-anthony-abbot
  Foco 50% 3%; zoom 1.6; janela original x=620.101, y=28.103, largura=1359.798, altura=1561.250px.
- **2026-12-13 — 3º Domingo do Advento (Gaudete):** obra local real; recorte.png gerado.
  James Tissot · São João Batista e os fariseus · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4449
  Foco 50% 50%; zoom 1.1; janela original x=334.496, y=49.773, largura=867.009, altura=995.455px.
- **2026-12-14 — São João da Cruz, presbítero e doutor da Igreja (Memória):** obra local real; recorte.png gerado.
  James Tissot · Os sumos sacerdotes interrogam Jesus · Brooklyn Museum — https://www.brooklynmuseum.org/objects/13456
  Foco 18% 50%; zoom 1.08; janela original x=115.932, y=40.963, largura=891.935, altura=1024.074px.
- **2026-12-15 — Terça-feira da 3ª Semana do Advento:** obra local real; recorte.png gerado.
  James Tissot · A volta do filho pródigo · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4538
  Foco 60% 45%; zoom 1.15; janela original x=76.070, y=254.504, largura=845.217, altura=970.435px.
- **2026-12-16 — Quarta-feira da 3ª Semana do Advento:** obra local real; recorte.png gerado.
  James Tissot · Jesus cura cegos e coxos no monte · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4482
  Foco 85% 45%; zoom 1.2; janela original x=603.527, y=85.350, largura=825.968, altura=948.333px.
- **2026-12-17 — Quinta-feira da 3ª Semana do Advento:** obra local real; recorte.png gerado.
  Livro de Kells · Início do Evangelho de Mateus · Trinity College Dublin — https://commons.wikimedia.org/wiki/File:KellsFol029rIncipitMatthew.jpg
  Foco 50% 30%; zoom 1; janela original x=0.000, y=71.822, largura=1354.000, altura=1554.593px.
- **2026-12-18 — Sexta-feira da 3ª Semana do Advento:** obra local real; recorte.png gerado.
  Philippe de Champaigne · O sonho de São José · National Gallery, Londres — https://commons.wikimedia.org/wiki/File:Philippe_de_Champaigne_(1602-1674)_-_The_Dream_of_Saint_Joseph_-_NG6276_-_National_Gallery.jpg
  Foco 45% 40%; zoom 1; janela original x=0.000, y=320.844, largura=3840.000, altura=4408.889px.
- **2026-12-19 — Sábado da 3ª Semana do Advento:** obra local real; recorte.png gerado.
  James Tissot · A visão de Zacarias · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4419
  Foco 50% 25%; zoom 1.1; janela original x=40.727, y=150.195, largura=814.545, altura=935.219px.
- **2026-12-20 — 4º Domingo do Advento:** obra local real; recorte.png gerado.
  Henry Ossawa Tanner · A Anunciação · Philadelphia Museum of Art — https://commons.wikimedia.org/wiki/File:The_Annunciation,_Philadelphia_Museum_of_Art,_W1899-1-1-pma,_by_Henry_Ossawa_Tanner.jpg
  Foco 25% 50%; zoom 1; janela original x=289.137, y=0.000, largura=2683.452, altura=3081.000px.
- **2026-12-21 — Segunda-feira da 4ª Semana do Advento:** obra local real; recorte.png gerado.
  James Tissot · A Visitação · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4424
  Foco 45% 40%; zoom 1.1; janela original x=43.936, y=165.996, largura=976.364, altura=1121.010px.
- **2026-12-22 — Terça-feira da 4ª Semana do Advento:** obra local real; recorte.png gerado.
  James Tissot · O Magnificat · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4425
  Foco 60% 30%; zoom 1.1; janela original x=40.255, y=229.709, largura=670.909, altura=770.303px.
- **2026-12-23 — Quarta-feira da 4ª Semana do Advento:** obra local real; recorte.png gerado.
  Fra Angelico · A imposição do nome a João Batista · Museu de San Marco, Florença — https://commons.wikimedia.org/wiki/File:Fra_Angelico_002.jpg
  Foco 40% 60%; zoom 1.2; janela original x=153.471, y=226.000, largura=1640.323, altura=1883.333px.
- **2026-12-24 — Quinta-feira da 4ª Semana do Advento:** obra local real; recorte.png gerado.
  James Tissot · Zacarias e Isabel · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4418
  Foco 40% 50%; zoom 1.1; janela original x=41.164, y=177.226, largura=1029.091, altura=1181.549px.
- **2026-12-25 — Natal de Nosso Senhor Jesus Cristo (Solenidade):** obra local real; recorte.png gerado.
  Duccio · A Natividade · National Gallery of Art — https://commons.wikimedia.org/wiki/File:Duccio_di_Buoninsegna_-_The_Nativity_with_the_Prophets_Isaiah_and_Ezekiel_-_Google_Art_Project.jpg
  Foco 50% 20%; zoom 1.9; janela original x=1430.424, y=202.358, largura=979.151, altura=1124.211px.
- **2026-12-26 — Santo Estêvão, protomártir (Festa):** obra local real; recorte.png gerado.
  James Tissot · Recomendações aos apóstolos · Brooklyn Museum — https://www.brooklynmuseum.org/objects/13422
  Foco 35% 50%; zoom 1.2; janela original x=241.398, y=97.167, largura=846.290, altura=971.667px.
- **2026-12-27 — Sagrada Família de Jesus, Maria e José (Festa):** obra local real; recorte.png gerado.
  Andrea Mantegna · A Apresentação no Templo · Gemäldegalerie, Berlim — https://commons.wikimedia.org/wiki/File:Andrea_Mantegna_-_The_Presentation_-_Google_Art_Project.jpg
  Foco 45% 50%; zoom 1.1; janela original x=646.614, y=137.955, largura=2403.079, altura=2759.091px.
- **2026-12-28 — Santos Inocentes, mártires (Festa):** obra local real; recorte.png gerado.
  Rembrandt e ateliê · O sonho de São José · Museu de Belas Artes de Budapeste — https://www.mfab.hu/artworks/8895/
  Foco 40% 45%; zoom 1; janela original x=0.000, y=159.300, largura=2781.000, altura=3193.000px.
- **2026-12-29 — 5º dia na Oitava do Natal:** obra local real; recorte.png gerado.
  James Tissot · O velho Simeão · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4434
  Foco 40% 45%; zoom 1.12; janela original x=55.157, y=97.495, largura=1149.107, altura=1319.345px.
- **2026-12-30 — 6º dia na Oitava do Natal:** obra local real; recorte.png gerado.
  Rembrandt · A profetisa Ana · Rijksmuseum — https://www.rijksmuseum.nl/en/collection/SK-A-3066
  Foco 40% 40%; zoom 1.1; janela original x=139.636, y=322.768, largura=3490.909, altura=4008.081px.
- **2026-12-31 — 7º dia na Oitava do Natal:** obra local real; recorte.png gerado.
  Autor desconhecido · Cristo Pantocrator · Mosteiro de Santa Catarina, Sinai — https://commons.wikimedia.org/wiki/File:CHRIST_PANTOCRATOR-SINAI(6th_Century).jpg
  Foco 50% 15%; zoom 1; janela original x=0.000, y=236.917, largura=2400.000, altura=2755.556px.
Nenhuma margem uniforme da foto está visível nos enquadramentos selecionados.

## Conferência

PNG exatos; limites de linhas; palavras de uma letra; afastamento de 32 px do logo; pares de 32 e 48 px para o Canva; centralização vertical; cruz, fundo e filete por pixel; páginas PDF de 810 × 1012,5 pt; quatro variantes embutidas por pdffonts; título e convite extraíveis. Os valores estão em verificacao.json e ficha.json.

Em cada PDF, PyMuPDF exige um único preenchimento curvo na cor e na caixa do nicho, nenhuma borda antiga feita apenas de retângulos recortados e um parapeito retangular separado de 3 px. Uma falha interrompe a geração. O resultado fica em nicho_vetorial na verificação de cada PDF.

No Canva, conferir o filete (forma em U, sem imagem por trás), o parapeito e o ornamento como formas.

A regra dos espaços foi aprovada no teste de importação no Canva de 29/10/2026, registrado em saida/teste-canva/LEIA-ME.md. Esta geração valida os novos PDFs; sua importação no editor permanece uma conferência manual.

Todas as obras selecionadas foram encontradas localmente e receberam prova de recorte.

<!-- inicio-prompt14 -->
## Prompt 14 — Lote 3, de 14 a 31/12

**Estado: todas as provas concluídas; entrega em um commit na main.**

Os 18 carrosséis novos foram gerados, com 56 cards, 18 PDFs, 18 recortes e suas fichas. A geração completa cobre 33 datas, 104 cards, 33 PDFs e 139 PNGs. A verificação nativa passou, sem obras provisórias, margens visíveis ou avisos. As sete séries foram regeneradas e conferidas. A auditoria final passou com a exceção expressamente autorizada para os relatórios reproduzidos na baseline limpa e restaurados antes da entrega.

### Conteúdo, código e testes

- YAML gravado com LF, preservando byte a byte os 15 dias anteriores; diff de 288 linhas acrescentadas e nenhuma removida.
- SHA-256 do YAML: `cfcb88b21f90e48e810ee11ea3fb60abe124a92495447d2171cf7e8f0670ebae`.
- Única mudança funcional: `referencia` aceita no fim, após um espaço, os quatro sufixos das missas do Natal. `trecho_ref` continua recusando sufixos; o padrão das referências anteriores permanece igual. `expanded_reference` expande só o livro e conserva o nome da missa.
- `git grep` confirmou o uso de `REFERENCE_PATTERN`, `_reference` e `expanded_reference` somente em `arteque_reza/conteudo.py` e `arteque_reza/evangelho.py`.
- Natal: referência `Lc 2,1-14 (Missa da noite)` nos três selos, com pelo menos 32 px até a data; convite em uma linha, com `Lucas 2,1-14 (Missa da noite)` inteiro em negrito. 25/12 mantém três cards, sem reflexão; 20 e 27/12 têm quatro cards.
- `tests/test_conteudo.py`: ordem das 33 datas, textos e aspas do anexo, reflexões sem quebra manual, foco de Tanner e aceitação/recusa dos sufixos, inclusive expansão e recusa em `trecho_ref`.
- `tests/test_obras.py`: nove obras com margens do museu separadas do teste geral; margens e faixas descartadas conferidas e os 18 enquadramentos aprovados sem margem visível ou aviso.
- `tests/test_layout_evangelho.py`: acrescentado somente o teste do convite do Natal, em uma linha e com a referência inteira em negrito; testes anteriores preservados.
- **Suíte completa: 201 testes passaram** (133,434 s). O texto das 104 páginas PDF confere com as fichas/YAML, preservados os espaços na extração, e todas as fontes utilizadas estão embutidas.

### Medidas dos 18 dias

Todos os valores medidos coincidem com a tabela prevista no passo 5. A janela é a região retangular da imagem original, antes da máscara do arco; não é o tamanho do card.

| Data | Capa: crédito, título | Versículo: estilo, linhas | Para a Missa de hoje | Para rezar hoje: pergunta, convite | Janela original: largura × altura (px) |
| --- | --- | --- | --- | --- | --- |
| 14/12 | 1, 2 | citacao-grande, 3 | — | 2, 1 | 891.935 × 1024.074 |
| 15/12 | 1, 1 | citacao-grande, 3 | — | 2, 1 | 845.217 × 970.435 |
| 16/12 | 1, 2 | citacao-grande, 2 | — | 2, 1 | 825.968 × 948.333 |
| 17/12 | 1, 1 | citacao-grande, 3 | — | 2, 1 | 1354.000 × 1554.593 |
| 18/12 | 1, 2 | citacao, 3 | — | 2, 1 | 3840.000 × 4408.889 |
| 19/12 | 1, 2 | citacao-grande, 2 | — | 2, 1 | 814.545 × 935.219 |
| 20/12 | 1, 2 | citacao-grande, 1 | título 1, texto 5 | 2, 1 | 2683.452 × 3081.000 |
| 21/12 | 1, 2 | citacao, 3 | — | 2, 1 | 976.364 × 1121.010 |
| 22/12 | 1, 2 | citacao-grande, 3 | — | 2, 1 | 670.909 × 770.303 |
| 23/12 | 1, 2 | citacao-grande, 3 | — | 2, 1 | 1640.323 × 1883.333 |
| 24/12 | 1, 2 | citacao-grande, 3 | — | 2, 1 | 1029.091 × 1181.549 |
| 25/12 | 1, 2 | citacao-grande, 3 | — | 2, 1 | 979.151 × 1124.211 |
| 26/12 | 1, 2 | citacao, 3 | — | 2, 1 | 846.290 × 971.667 |
| 27/12 | 1, 2 | citacao, 2 | título 1, texto 5 | 2, 1 | 2403.079 × 2759.091 |
| 28/12 | 1, 2 | citacao-grande, 2 | — | 2, 1 | 2781.000 × 3193.000 |
| 29/12 | 1, 2 | citacao, 3 | — | 2, 1 | 1149.107 × 1319.345 |
| 30/12 | 1, 2 | citacao, 3 | — | 2, 1 | 3490.909 × 4008.081 |
| 31/12 | 1, 1 | citacao-grande, 2 | — | 2, 1 | 2400.000 × 2755.556 |

### Obras: conferência visual do card 1 e do recorte

As 18 capas e seus `recorte.png` finais foram inspecionados individualmente. As observações abaixo distinguem o corte novo pelo arco das partes já ocultas ou fora da própria pintura. **Nenhum foco ou zoom do YAML foi alterado.** Sugestões são apenas para avaliação posterior; quando não houve alternativa que preservasse todo o grupo e excluísse a margem fotográfica, a limitação e a manutenção do enquadramento aprovado estão registradas.

#### 2026-12-14

[James Tissot · Os sumos sacerdotes interrogam Jesus · Brooklyn Museum](https://www.brooklynmuseum.org/objects/13456). Obra local: `obras/2026-12-14.jpg`.

Foco aprovado **18% 50%**, zoom **1.08**; janela original x=115.932, y=40.963, largura=891.935, altura=1024.074 px. Figuras principais inteiras na extensão pintada: **não; ver ressalvas**.

Card 1 e recorte finais conferidos: Cristo fica inteiro, com rosto, mãos, vestes e pés preservados, e o interlocutor inclinado sobre a divisória permanece dentro do arco na extensão em que é visível na pintura. O grupo de sumos sacerdotes à direita fica parcial ou fora, incluindo o personagem de manto dourado com o livro. A figura à esquerda de Cristo e parte da multidão também são cortadas. Nenhuma borda fotográfica entra no arco.

Sugestão: foco **18% 50%**, zoom **1.08**. Recomenda-se manter este enquadramento para priorizar Cristo e o interlocutor inclinado. O conjunto horizontal de Cristo até os sacerdotes da direita não cabe integralmente no nicho com zoom igual ou superior a 1. A abertura até zoom 1 foi testada e traz bordas do museu, por isso não é recomendada. Não há proposta que inclua todo o grupo sem esse compromisso; o YAML foi preservado.

#### 2026-12-15

[James Tissot · A volta do filho pródigo · Brooklyn Museum](https://www.brooklynmuseum.org/objects/4538). Obra local: `obras/2026-12-15.jpg`.

Foco aprovado **60% 45%**, zoom **1.15**; janela original x=76.070, y=254.504, largura=845.217, altura=970.435 px. Figuras principais inteiras na extensão pintada: **não; ver ressalvas**.

Card 1 e recorte finais conferidos: os rostos, o abraço e as mãos do pai e do filho ficam preservados, mas a base corta a parte inferior das vestes e os pés do pai, além das pernas e pés do filho ajoelhado. Figurantes periféricos também aparecem parcialmente. Nenhuma borda do museu fica visível.

Sugestão: foco **60% 80%**, zoom **1.04**. Alternativa renderizada e inspecionada no card e no contorno: inclui pai e filho inteiros na extensão em que aparecem na pintura, recuperando os pés e as vestes inferiores e mantendo os rostos e o abraço. A inspeção geométrica continua com margens_visiveis e avisos vazios. Figurantes periféricos continuam parciais. Sugestão somente; YAML aprovado preservado.

#### 2026-12-16

[James Tissot · Jesus cura cegos e coxos no monte · Brooklyn Museum](https://www.brooklynmuseum.org/objects/4482). Obra local: `obras/2026-12-16.jpg`.

Foco aprovado **85% 45%**, zoom **1.2**; janela original x=603.527, y=85.350, largura=825.968, altura=948.333 px. Figuras principais inteiras na extensão pintada: **sim**.

Card 1 e recorte finais conferidos: o núcleo do milagre em primeiro plano à direita, com Cristo em veste branca e os enfermos imediatamente diante dele, permanece preservado na extensão visível na pintura; rosto, gestos e pés de Cristo ficam dentro do arco. A multidão distante e personagens periféricos à esquerda são recortados ou excluídos. As partes já ocultadas por outros participantes no original não são cortes novos. Não há margem fotográfica visível.

#### 2026-12-17

[Livro de Kells · Início do Evangelho de Mateus · Trinity College Dublin](https://commons.wikimedia.org/wiki/File:KellsFol029rIncipitMatthew.jpg). Obra local: `obras/2026-12-17.jpg`.

Foco aprovado **50% 30%**, zoom **1**; janela original x=0.000, y=71.822, largura=1354.000, altura=1554.593 px. Figuras principais inteiras na extensão pintada: **não; ver ressalvas**.

Card 1 e recorte finais conferidos: as figuras humanas principais do fólio permanecem legíveis, incluindo a figura em pé com o livro e os pés; porém a curva intercepta a borda superior do anel em torno da figura no alto. A folha e seus ornamentos de canto não cabem integralmente no nicho e ficam parciais. A ressalva de integralidade refere-se ao anel e à composição do fólio, não a um rosto cortado. Não há margem fotográfica uniforme.

Sugestão: foco **50% 5%**, zoom **1**. Alternativa renderizada e inspecionada: libera o anel da figura superior e mantém a figura em pé, inclusive seus pés, dentro da base. Ornamentos periféricos e a folha completa continuam recortados; a proporção do fólio impede incluir toda a página no nicho com zoom igual ou superior a 1. Sugestão somente; YAML aprovado preservado.

#### 2026-12-18

[Philippe de Champaigne · O sonho de São José · National Gallery, Londres](https://commons.wikimedia.org/wiki/File:Philippe_de_Champaigne_(1602-1674)_-_The_Dream_of_Saint_Joseph_-_NG6276_-_National_Gallery.jpg). Obra local: `obras/2026-12-18.jpg`.

Foco aprovado **45% 40%**, zoom **1**; janela original x=0.000, y=320.844, largura=3840.000, altura=4408.889 px. Figuras principais inteiras na extensão pintada: **não; ver ressalvas**.

Card 1 e recorte finais conferidos: o rosto e as mãos de José, o rosto e o gesto do anjo e a figura de Maria à direita ficam preservados. A base corta o pé e uma parte inferior de José; a curva superior intercepta a extremidade do braço erguido e da veste do anjo. Portanto o conjunto de protagonistas não está integralmente contido, embora seus rostos e o sentido da cena permaneçam legíveis. Não há margem fotográfica.

Sugestão: foco **45% 70%**, zoom **1**. Alternativa renderizada e inspecionada: inclui o pé e a parte inferior de José e conserva Maria e os rostos, sem margem fotográfica. A extremidade superior do anjo continua cortada, com maior corte no braço erguido; é uma opção para priorizar José, não uma solução para integrar todas as figuras. O conjunto vertical completo não cabe simultaneamente no nicho fixo com zoom igual ou superior a 1. Sugestão somente; YAML aprovado preservado.

#### 2026-12-19

[James Tissot · A visão de Zacarias · Brooklyn Museum](https://www.brooklynmuseum.org/objects/4419). Obra local: `obras/2026-12-19.jpg`.

Foco aprovado **50% 25%**, zoom **1.1**; janela original x=40.727, y=150.195, largura=814.545, altura=935.219 px. Figuras principais inteiras na extensão pintada: **não; ver ressalvas**.

Card 1 e recorte finais conferidos: os rostos de Zacarias e do anjo, suas mãos e o encontro entre os gestos ficam dentro do arco. A base corta os pés e a parte inferior de ambas as vestes; a curva superior também corta as pontas das asas do anjo. O papel do museu permanece fora do arco.

Sugestão: foco **50% 25%**, zoom **1.1**. Recomenda-se manter estes valores para priorizar rostos e gestos dos dois protagonistas. O corpo inteiro de Zacarias junto das asas inteiras do anjo não cabe na proporção fixa do nicho; mover para baixo perde as asas e abrir até zoom 1 traz a borda fotográfica. Nenhum enquadramento integral adequado foi encontrado dentro dessas restrições. Sugestão de manutenção, sem alterar o YAML aprovado.

#### 2026-12-20

[Henry Ossawa Tanner · A Anunciação · Philadelphia Museum of Art](https://commons.wikimedia.org/wiki/File:The_Annunciation,_Philadelphia_Museum_of_Art,_W1899-1-1-pma,_by_Henry_Ossawa_Tanner.jpg). Obra local: `obras/2026-12-20.jpg`.

Foco aprovado **25% 50%**, zoom **1**; janela original x=289.137, y=0.000, largura=2683.452, altura=3081.000 px. Figuras principais inteiras na extensão pintada: **sim**.

Card 1 e recorte finais conferidos individualmente: Maria fica inteira na extensão pintada, incluindo rosto, mãos, vestes e pés. O anjo é representado pela coluna vertical de luz à esquerda; seu núcleo luminoso está dentro do arco e permanece legível até junto do piso. O brilho superior entra pela curva e é interceptado por ela, portanto não se afirma que toda a luminosidade da pintura esteja contida. A integridade da figura humana refere-se a Maria; o anjo não tem corpo antropomórfico delimitado. As duas presenças pedidas estão confirmadas com o foco aprovado 25% 50% e zoom 1. Não há margem fotográfica visível.

#### 2026-12-21

[James Tissot · A Visitação · Brooklyn Museum](https://www.brooklynmuseum.org/objects/4424). Obra local: `obras/2026-12-21.jpg`.

Foco aprovado **45% 40%**, zoom **1.1**; janela original x=43.936, y=165.996, largura=976.364, altura=1121.010 px. Figuras principais inteiras na extensão pintada: **não; ver ressalvas**.

Card 1 e recorte finais conferidos: Maria e Isabel preservam rostos, mãos e o gesto do encontro. Isabel, à esquerda, fica inteira com os dois pés; a base corta a parte inferior da saia e os pés de Maria, em primeiro plano. Zacarias à direita e os figurantes periféricos também aparecem parcialmente. Nenhuma borda de papel fica dentro do arco.

Sugestão: foco **45% 75%**, zoom **1.09**. Alternativa renderizada e inspecionada no card e no contorno: inclui os pés e as vestes inferiores de Maria, mantendo Maria e Isabel inteiras, com rostos e mãos preservados. O personagem secundário à direita perde mais da cabeça pela curva. A inspeção continua com margens_visiveis e avisos vazios. Sugestão somente; YAML aprovado preservado.

#### 2026-12-22

[James Tissot · O Magnificat · Brooklyn Museum](https://www.brooklynmuseum.org/objects/4425). Obra local: `obras/2026-12-22.jpg`.

Foco aprovado **60% 30%**, zoom **1.1**; janela original x=40.255, y=229.709, largura=670.909, altura=770.303 px. Figuras principais inteiras na extensão pintada: **não; ver ressalvas**.

Card 1 e recorte finais conferidos: Maria preserva rosto, mãos erguidas e tronco, mas a base corta a parte inferior de sua veste, as pernas e os pés. Os interlocutores à esquerda também ficam parcialmente interceptados pela curva e pela lateral. A borda da fotografia do museu não entra no arco.

Sugestão: foco **50% 30%**, zoom **1.07**. Alternativa renderizada e inspecionada: abre discretamente o conjunto e recupera mais veste e contexto lateral, mantendo o rosto e as mãos de Maria e sem margem fotográfica visível. As pernas inferiores e os pés continuam fora. A figura completa é alta demais para o nicho estreito mantendo a borda do museu excluída; a alternativa não resolve a integralidade corporal. Sugestão somente; YAML aprovado preservado.

#### 2026-12-23

[Fra Angelico · A imposição do nome a João Batista · Museu de San Marco, Florença](https://commons.wikimedia.org/wiki/File:Fra_Angelico_002.jpg). Obra local: `obras/2026-12-23.jpg`.

Foco aprovado **40% 60%**, zoom **1.2**; janela original x=153.471, y=226.000, largura=1640.323, altura=1883.333 px. Figuras principais inteiras na extensão pintada: **não; ver ressalvas**.

Card 1 e recorte finais conferidos. Os rostos, as mãos de Zacarias e o menino apresentado no grupo central ficam preservados. A lateral esquerda intercepta parte da veste vermelha de Zacarias, e a base corta a barra da veste azul da figura à direita. Portanto, o grupo não está integralmente dentro do arco. Não há margem fotográfica visível.

Sugestão: foco **40% 60%**, zoom **1**. Alternativa renderizada e inspecionada: abre a cena e inclui Zacarias e o grupo com o menino na extensão em que aparecem no original, inclusive as barras antes interceptadas. Inclui mais arquitetura acima. Não aplicada ao YAML.

#### 2026-12-24

[James Tissot · Zacarias e Isabel · Brooklyn Museum](https://www.brooklynmuseum.org/objects/4418). Obra local: `obras/2026-12-24.jpg`.

Foco aprovado **40% 50%**, zoom **1.1**; janela original x=41.164, y=177.226, largura=1029.091, altura=1181.549 px. Figuras principais inteiras na extensão pintada: **não; ver ressalvas**.

Card 1 e recorte finais conferidos. Os rostos e os gestos de Zacarias e Isabel ficam legíveis, mas a curva e a lateral esquerda interceptam parte do capuz e da veste de Zacarias; a base corta a parte inferior da veste de Isabel. Não há margem fotográfica visível.

Sugestão: foco **0% 45%**, zoom **1.04**. Alternativa renderizada e inspecionada sem margem uniforme visível: abre mais a lateral esquerda e preserva os dois rostos e gestos, com mais veste de Zacarias. A parte inferior de Isabel continua parcial; a sugestão não torna os dois corpos integralmente visíveis. Não aplicada ao YAML.

#### 2026-12-25

[Duccio · A Natividade · National Gallery of Art](https://commons.wikimedia.org/wiki/File:Duccio_di_Buoninsegna_-_The_Nativity_with_the_Prophets_Isaiah_and_Ezekiel_-_Google_Art_Project.jpg). Obra local: `obras/2026-12-25.jpg`.

Foco aprovado **50% 20%**, zoom **1.9**; janela original x=1430.424, y=202.358, largura=979.151, altura=1124.211 px. Figuras principais inteiras na extensão pintada: **não; ver ressalvas**.

Card 1 e recorte finais conferidos no zoom aprovado de 1.9. O menino deitado na manjedoura fica inteiro e o rosto de Maria permanece visível. A lateral esquerda corta parte da auréola e da figura de Maria, e a base corta a extensão de sua veste e da manjedoura. José, os profetas dos painéis laterais e a maior parte dos outros participantes ficam fora. Trata-se de um recorte fechado, sem margem fotográfica visível.

Sugestão: foco **50% 20%**, zoom **1.3**. Alternativa renderizada e inspecionada: inclui Maria e o menino inteiros na extensão pintada, com a longa veste azul e a manjedoura. Aparecem mais anjos, a cobertura e áreas douradas da composição; os demais participantes periféricos continuam parciais ou fora. O detector não aponta margem uniforme visível. Não aplicada ao YAML.

#### 2026-12-26

[James Tissot · Recomendações aos apóstolos · Brooklyn Museum](https://www.brooklynmuseum.org/objects/13422). Obra local: `obras/2026-12-26.jpg`.

Foco aprovado **35% 50%**, zoom **1.2**; janela original x=241.398, y=97.167, largura=846.290, altura=971.667 px. Figuras principais inteiras na extensão pintada: **não; ver ressalvas**.

Card 1 e recorte finais conferidos. Cristo sentado fica preservado, com rosto, mãos e a extensão de suas vestes e pés que a própria cena permite ver. Vários apóstolos à direita e participantes em primeiro plano são cortados pelo arco ou ficam fora da janela, de modo que o grupo não está inteiro. Não há borda do museu no enquadramento aprovado.

Sugestão: foco **35% 50%**, zoom **1.2**. Recomenda-se manter o enquadramento aprovado: ele preserva Cristo e os gestos centrais sem trazer a borda do museu. A alternativa já renderizada com foco 50% 50%, zoom 1 foi novamente inspecionada na capa e no recorte e mostra uma faixa cinzenta da fotografia na base, além de ainda cortar participantes à direita; por isso não deve ser adotada. Não foi demonstrado um enquadramento que inclua o grupo inteiro no nicho sem borda visível; o YAML permanece intacto.

#### 2026-12-27

[Andrea Mantegna · A Apresentação no Templo · Gemäldegalerie, Berlim](https://commons.wikimedia.org/wiki/File:Andrea_Mantegna_-_The_Presentation_-_Google_Art_Project.jpg). Obra local: `obras/2026-12-27.jpg`.

Foco aprovado **45% 50%**, zoom **1.1**; janela original x=646.614, y=137.955, largura=2403.079, altura=2759.091 px. Figuras principais inteiras na extensão pintada: **não; ver ressalvas**.

Card 1 e recorte finais conferidos. Os rostos de Maria, do menino, de José ao fundo e de Simeão, além das mãos e do menino envolto em faixas, ficam preservados. A curva intercepta as auréolas e os extremos superiores/laterais de Maria e Simeão; parte das vestes laterais também sai. A pintura original já representa os adultos em meio-corpo, portanto a ausência de pernas não é um corte novo. Não há margem fotográfica visível.

Sugestão: foco **45% 50%**, zoom **1**. Alternativa renderizada e inspecionada sem margem uniforme visível: abre as vestes e as laterais e mantém os rostos e gestos centrais. Ainda há interseção da curva com extremos das auréolas e com participantes periféricos; não resolve a integralidade de todos os personagens. Não aplicada ao YAML.

#### 2026-12-28

[Rembrandt e ateliê · O sonho de São José · Museu de Belas Artes de Budapeste](https://www.mfab.hu/artworks/8895/). Obra local: `obras/2026-12-28.jpg`.

Foco aprovado **40% 45%**, zoom **1**; janela original x=0.000, y=159.300, largura=2781.000, altura=3193.000 px. Figuras principais inteiras na extensão pintada: **não; ver ressalvas**.

Card 1 e recorte finais conferidos. José e Maria ficam preservados na extensão visível da pintura, e os rostos do anjo e de José e o gesto do anjo que aponta ficam claros. O extremo esquerdo do anjo já é interrompido na própria obra, e o arco exclui mais de sua extremidade superior à esquerda. O anjo, portanto, não fica inteiro. A figura de Maria permanece na zona escura da pintura, como no original. Não há margem uniforme visível.

Sugestão: foco **40% 45%**, zoom **1**. Recomenda-se manter o foco e o zoom aprovados para priorizar o conjunto de José, Maria e o gesto do anjo. Uma alternativa renderizada com foco 40% 0%, zoom 1 abre a parte superior, mas não recupera o extremo do anjo já fora do original e sacrifica a parte inferior da família. O zoom aprovado já é o mínimo aceito; não há proposta de corpo inteiro para o anjo sem trocar a composição. YAML preservado.

#### 2026-12-29

[James Tissot · O velho Simeão · Brooklyn Museum](https://www.brooklynmuseum.org/objects/4434). Obra local: `obras/2026-12-29.jpg`.

Foco aprovado **40% 45%**, zoom **1.12**; janela original x=55.157, y=97.495, largura=1149.107, altura=1319.345 px. Figuras principais inteiras na extensão pintada: **não; ver ressalvas**.

Card 1 e recorte finais conferidos. Os rostos de Simeão e do menino, assim como as mãos que o sustentam, ficam preservados. A base corta a extensão inferior da veste de Simeão. As figuras que aparecem ao fundo ou nas bordas já são parcialmente ocultadas na pintura. A borda fotográfica do museu fica fora do arco.

Sugestão: foco **40% 68%**, zoom **1.06**. Alternativa renderizada e inspecionada: abre mais a parte inferior das vestes e mantém os rostos, o menino e as mãos dentro do arco, sem trazer a margem uniforme da fotografia. Preserva a figura na extensão em que a própria pintura a apresenta; partes já ocultas ou cortadas no original não são recuperadas. Não aplicada ao YAML.

#### 2026-12-30

[Rembrandt · A profetisa Ana · Rijksmuseum](https://www.rijksmuseum.nl/en/collection/SK-A-3066). Obra local: `obras/2026-12-30.jpg`.

Foco aprovado **40% 40%**, zoom **1.1**; janela original x=139.636, y=322.768, largura=3490.909, altura=4008.081 px. Figuras principais inteiras na extensão pintada: **não; ver ressalvas**.

Card 1 e recorte finais conferidos. A cabeça, o rosto, as mãos e o livro de Ana ficam inteiros. A base corta a extensão inferior de suas vestes e do assento que ainda aparece no original. A figura não está integralmente preservada na extensão pintada. Não há margem fotográfica visível.

Sugestão: foco **50% 100%**, zoom **1**. Alternativa renderizada e inspecionada sem margem uniforme visível: inclui mais da parte inferior das vestes e do assento, mantendo cabeça, mãos e livro. A própria pintura já limita a figura e não mostra um corpo de pé completo. Não aplicada ao YAML.

#### 2026-12-31

[Autor desconhecido · Cristo Pantocrator · Mosteiro de Santa Catarina, Sinai](https://commons.wikimedia.org/wiki/File:CHRIST_PANTOCRATOR-SINAI(6th_Century).jpg). Obra local: `obras/2026-12-31.jpg`.

Foco aprovado **50% 15%**, zoom **1**; janela original x=0.000, y=236.917, largura=2400.000, altura=2755.556 px. Figuras principais inteiras na extensão pintada: **não; ver ressalvas**.

Card 1 e recorte finais conferidos. O rosto de Cristo, os cabelos e a barba ficam preservados, mas o arco intercepta a extensão da auréola e a base corta o busto e quase todo o livro; a mão em bênção fica fora. O ícone original já é uma representação de busto, e este recorte é ainda mais fechado no rosto. Não há margem uniforme visível.

Sugestão: foco **50% 15%**, zoom **1**. Recomenda-se manter os valores aprovados para priorizar o rosto. A janela no zoom mínimo tem aproximadamente 2756 px de altura para uma imagem de 4335 px; nenhum ajuste de foco mostra todo o ícone nessa escala. Uma alternativa renderizada com foco 50% 50%, zoom 1 traz mais do livro e da mão, mas corta o alto da cabeça e da auréola, portanto não é uma correção integral recomendada. YAML preservado.

### Controle e preservação das 15 datas anteriores

Na 8bb86f4 sem alterações e novamente após o código/conteúdo novos: **64 PNGs com zero pixel diferente, 48 páginas de PDF a 2× com zero pixel diferente e 15 fichas iguais**, ignorando somente `source` no elemento `nicho-obra`. As 15 pastas e `prancha-cores.png` foram restauradas byte a byte à 8bb86f4 depois da prova. Nas tabelas abaixo, toda caixa de diferença é vazia e a maior diferença por canal é zero.

| PNG | Controle: pixels diferentes | Após a mudança: pixels diferentes |
| --- | --- | --- |
| `saida/evangelho/2026-11-29/card-1.png` | 0 | 0 |
| `saida/evangelho/2026-11-29/card-2.png` | 0 | 0 |
| `saida/evangelho/2026-11-29/card-3.png` | 0 | 0 |
| `saida/evangelho/2026-11-29/card-4.png` | 0 | 0 |
| `saida/evangelho/2026-11-29/recorte.png` | 0 | 0 |
| `saida/evangelho/2026-11-30/card-1.png` | 0 | 0 |
| `saida/evangelho/2026-11-30/card-2.png` | 0 | 0 |
| `saida/evangelho/2026-11-30/card-3.png` | 0 | 0 |
| `saida/evangelho/2026-11-30/recorte.png` | 0 | 0 |
| `saida/evangelho/2026-12-01/card-1.png` | 0 | 0 |
| `saida/evangelho/2026-12-01/card-2.png` | 0 | 0 |
| `saida/evangelho/2026-12-01/card-3.png` | 0 | 0 |
| `saida/evangelho/2026-12-01/recorte.png` | 0 | 0 |
| `saida/evangelho/2026-12-02/card-1.png` | 0 | 0 |
| `saida/evangelho/2026-12-02/card-2.png` | 0 | 0 |
| `saida/evangelho/2026-12-02/card-3.png` | 0 | 0 |
| `saida/evangelho/2026-12-02/recorte.png` | 0 | 0 |
| `saida/evangelho/2026-12-03/card-1.png` | 0 | 0 |
| `saida/evangelho/2026-12-03/card-2.png` | 0 | 0 |
| `saida/evangelho/2026-12-03/card-3.png` | 0 | 0 |
| `saida/evangelho/2026-12-03/recorte.png` | 0 | 0 |
| `saida/evangelho/2026-12-04/card-1.png` | 0 | 0 |
| `saida/evangelho/2026-12-04/card-2.png` | 0 | 0 |
| `saida/evangelho/2026-12-04/card-3.png` | 0 | 0 |
| `saida/evangelho/2026-12-04/recorte.png` | 0 | 0 |
| `saida/evangelho/2026-12-05/card-1.png` | 0 | 0 |
| `saida/evangelho/2026-12-05/card-2.png` | 0 | 0 |
| `saida/evangelho/2026-12-05/card-3.png` | 0 | 0 |
| `saida/evangelho/2026-12-05/recorte.png` | 0 | 0 |
| `saida/evangelho/2026-12-06/card-1.png` | 0 | 0 |
| `saida/evangelho/2026-12-06/card-2.png` | 0 | 0 |
| `saida/evangelho/2026-12-06/card-3.png` | 0 | 0 |
| `saida/evangelho/2026-12-06/card-4.png` | 0 | 0 |
| `saida/evangelho/2026-12-06/recorte.png` | 0 | 0 |
| `saida/evangelho/2026-12-07/card-1.png` | 0 | 0 |
| `saida/evangelho/2026-12-07/card-2.png` | 0 | 0 |
| `saida/evangelho/2026-12-07/card-3.png` | 0 | 0 |
| `saida/evangelho/2026-12-07/recorte.png` | 0 | 0 |
| `saida/evangelho/2026-12-08/card-1.png` | 0 | 0 |
| `saida/evangelho/2026-12-08/card-2.png` | 0 | 0 |
| `saida/evangelho/2026-12-08/card-3.png` | 0 | 0 |
| `saida/evangelho/2026-12-08/recorte.png` | 0 | 0 |
| `saida/evangelho/2026-12-09/card-1.png` | 0 | 0 |
| `saida/evangelho/2026-12-09/card-2.png` | 0 | 0 |
| `saida/evangelho/2026-12-09/card-3.png` | 0 | 0 |
| `saida/evangelho/2026-12-09/recorte.png` | 0 | 0 |
| `saida/evangelho/2026-12-10/card-1.png` | 0 | 0 |
| `saida/evangelho/2026-12-10/card-2.png` | 0 | 0 |
| `saida/evangelho/2026-12-10/card-3.png` | 0 | 0 |
| `saida/evangelho/2026-12-10/recorte.png` | 0 | 0 |
| `saida/evangelho/2026-12-11/card-1.png` | 0 | 0 |
| `saida/evangelho/2026-12-11/card-2.png` | 0 | 0 |
| `saida/evangelho/2026-12-11/card-3.png` | 0 | 0 |
| `saida/evangelho/2026-12-11/recorte.png` | 0 | 0 |
| `saida/evangelho/2026-12-12/card-1.png` | 0 | 0 |
| `saida/evangelho/2026-12-12/card-2.png` | 0 | 0 |
| `saida/evangelho/2026-12-12/card-3.png` | 0 | 0 |
| `saida/evangelho/2026-12-12/recorte.png` | 0 | 0 |
| `saida/evangelho/2026-12-13/card-1.png` | 0 | 0 |
| `saida/evangelho/2026-12-13/card-2.png` | 0 | 0 |
| `saida/evangelho/2026-12-13/card-3.png` | 0 | 0 |
| `saida/evangelho/2026-12-13/card-4.png` | 0 | 0 |
| `saida/evangelho/2026-12-13/recorte.png` | 0 | 0 |
| `saida/evangelho/prancha-cores.png` | 0 | 0 |

| PDF a 2× | Páginas | Controle: pixels diferentes por página | Após a mudança: pixels diferentes por página |
| --- | --- | --- | --- |
| `saida/evangelho/2026-11-29/evangelho-2026-11-29.pdf` | 4 | p1: 0, p2: 0, p3: 0, p4: 0 | p1: 0, p2: 0, p3: 0, p4: 0 |
| `saida/evangelho/2026-11-30/evangelho-2026-11-30.pdf` | 3 | p1: 0, p2: 0, p3: 0 | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-01/evangelho-2026-12-01.pdf` | 3 | p1: 0, p2: 0, p3: 0 | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-02/evangelho-2026-12-02.pdf` | 3 | p1: 0, p2: 0, p3: 0 | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-03/evangelho-2026-12-03.pdf` | 3 | p1: 0, p2: 0, p3: 0 | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-04/evangelho-2026-12-04.pdf` | 3 | p1: 0, p2: 0, p3: 0 | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-05/evangelho-2026-12-05.pdf` | 3 | p1: 0, p2: 0, p3: 0 | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-06/evangelho-2026-12-06.pdf` | 4 | p1: 0, p2: 0, p3: 0, p4: 0 | p1: 0, p2: 0, p3: 0, p4: 0 |
| `saida/evangelho/2026-12-07/evangelho-2026-12-07.pdf` | 3 | p1: 0, p2: 0, p3: 0 | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-08/evangelho-2026-12-08.pdf` | 3 | p1: 0, p2: 0, p3: 0 | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-09/evangelho-2026-12-09.pdf` | 3 | p1: 0, p2: 0, p3: 0 | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-10/evangelho-2026-12-10.pdf` | 3 | p1: 0, p2: 0, p3: 0 | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-11/evangelho-2026-12-11.pdf` | 3 | p1: 0, p2: 0, p3: 0 | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-12/evangelho-2026-12-12.pdf` | 3 | p1: 0, p2: 0, p3: 0 | p1: 0, p2: 0, p3: 0 |
| `saida/evangelho/2026-12-13/evangelho-2026-12-13.pdf` | 4 | p1: 0, p2: 0, p3: 0, p4: 0 | p1: 0, p2: 0, p3: 0, p4: 0 |

### Outras séries: provas concluídas e relatórios restaurados

Comandos executados após a mudança: `python3 gerar.py componentes`, `santo`, `para-rezar`, `coragem`, `stories`, `novena` e `igreja-domestica`. Cada execução foi comparada separadamente com a 8bb86f4 antes de restaurar suas saídas. Nenhum PNG ou PDF dessas séries mudou sequer em bytes; portanto cada imagem e cada página no mesmo rasterizador têm zero pixel diferente, caixa de diferença vazia e maior diferença por canal zero. As fichas, quando alteradas, diferiram exclusivamente na porta local. Todos os arquivos públicos fora do Evangelho foram restaurados byte a byte ao final.

O inventário protegido abaixo inclui os registros de testes anteriores mantidos nas pastas. O total de **290 arquivos de saída fora do Evangelho** continua idêntico à 8bb86f4. A auditoria final também confirmou **504 arquivos anteriores protegidos** byte a byte, incluindo `kit/`, o ZIP, `obras/`, `gerar.py`, as 15 pastas antigas do Evangelho e a prancha de cores. O escopo final tem somente os nove arquivos permitidos modificados e os 110 arquivos novos nas 18 datas.

| Série | Arquivos preservados | PNGs: 0 pixels diferentes em cada | PDFs | Páginas: 0 pixels diferentes em cada | ficha.json |
| --- | --- | --- | --- | --- | --- |
| componentes | 91 | 29 | 3 | 19 | 1 |
| santo | 91 | 45 | 22 | 22 | 22 |
| para-rezar | 10 | 4 | 2 | 3 | 2 |
| coragem | 18 | 9 | 4 | 4 | 2 |
| stories | 23 | 11 | 4 | 8 | 4 |
| novena | 38 | 26 | 3 | 23 | 3 |
| igreja-domestica | 19 | 10 | 2 | 7 | 2 |

**Relatórios restaurados e excluídos do commit, por autorização expressa do usuário:**

| Arquivo | Diferença observada ao regenerar | Reprodução na 8bb86f4 limpa | Tratamento |
| --- | --- | --- | --- |
| `saida/RELATORIO.md` | Relatório global já desatualizado: muda a descrição/árvore; a execução com as novas datas também inclui suas pastas. | A desatualização também ocorre no controle limpo, no mesmo diretório. Mantida a autorização anterior específica deste arquivo. | Restaurado byte a byte à 8bb86f4; fora do commit. |
| `saida/santo-do-dia/RELATORIO.md` | Remove o apêndice manual do prompt 13: 72 linhas (260 a 331), de 427 para 355 linhas. | Mesma remoção; os relatórios regenerados com a proposta e na baseline limpa são byte a byte idênticos. Nenhum PNG/PDF mudou; 22 fichas diferiram só na porta local. | Restaurado byte a byte à 8bb86f4; fora do commit. |

Nenhum outro `RELATORIO.md` precisou da exceção ampliada. A regra continua estrita para qualquer outra diferença, inclusive ficha além da porta ou relatório que não se repita na baseline limpa. A comparação do Santo foi inicialmente interrompida conforme a regra original e só foi aceita após a autorização expressa para ampliar a exceção. Todos os 91 arquivos do Santo estão restaurados. Nenhum auxiliar de `work/` integra o commit.

### Arquivos PNG e PDF preservados nas outras séries

Prova por arquivo: todos os arquivos abaixo têm bytes idênticos à baseline. Nos PDFs, cada zero vale para cada página a 2×; não houve PDF modificado que exigisse nova comparação de rasters. As fichas foram comparadas antes da restauração permitindo apenas a porta e agora também estão idênticas byte a byte.

| Arquivo | Resultado por imagem/página |
| --- | --- |
| `saida/canva/elementos/logos/avatar-perfil.png` | 0 pixels |
| `saida/canva/pagina-1.png` | 0 pixels |
| `saida/canva/pagina-2.png` | 0 pixels |
| `saida/canva/pagina-3.png` | 0 pixels |
| `saida/canva/teste-importacao.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/obra-provisoria.png` | 0 pixels |
| `saida/previas/assinaturas.png` | 0 pixels |
| `saida/previas/nichos.png` | 0 pixels |
| `saida/previas/selos.png` | 0 pixels |
| `saida/teste-canva/prancha.png` | 0 pixels |
| `saida/teste-canva/teste-canva-a.pdf` | p1: 0, p2: 0, p3: 0, p4: 0, p5: 0, p6: 0, p7: 0, p8: 0, p9: 0, p10: 0, p11: 0, p12: 0, p13: 0, p14: 0 |
| `saida/teste-canva/teste-canva-b.pdf` | p1: 0, p2: 0 |
| `saida/verificacao/logos/avatar-perfil-convertido.png` | 0 pixels |
| `saida/verificacao/logos/avatar-perfil-original.png` | 0 pixels |
| `saida/verificacao/logos/logo-horizontal-capela-convertido.png` | 0 pixels |
| `saida/verificacao/logos/logo-horizontal-capela-original.png` | 0 pixels |
| `saida/verificacao/logos/logo-horizontal-pergaminho-convertido.png` | 0 pixels |
| `saida/verificacao/logos/logo-horizontal-pergaminho-original.png` | 0 pixels |
| `saida/verificacao/logos/logo-horizontal-sobre-cor-convertido.png` | 0 pixels |
| `saida/verificacao/logos/logo-horizontal-sobre-cor-original.png` | 0 pixels |
| `saida/verificacao/logos/logo-vertical-capela-convertido.png` | 0 pixels |
| `saida/verificacao/logos/logo-vertical-capela-original.png` | 0 pixels |
| `saida/verificacao/logos/logo-vertical-pergaminho-convertido.png` | 0 pixels |
| `saida/verificacao/logos/logo-vertical-pergaminho-original.png` | 0 pixels |
| `saida/verificacao/logos/simbolo-capela-convertido.png` | 0 pixels |
| `saida/verificacao/logos/simbolo-capela-original.png` | 0 pixels |
| `saida/verificacao/logos/simbolo-pergaminho-convertido.png` | 0 pixels |
| `saida/verificacao/logos/simbolo-pergaminho-original.png` | 0 pixels |
| `saida/verificacao/logos/simbolo-reduzido-capela-convertido.png` | 0 pixels |
| `saida/verificacao/logos/simbolo-reduzido-capela-original.png` | 0 pixels |
| `saida/verificacao/logos/simbolo-reduzido-pergaminho-convertido.png` | 0 pixels |
| `saida/verificacao/logos/simbolo-reduzido-pergaminho-original.png` | 0 pixels |
| `saida/santo-do-dia/2026-11-30/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-11-30/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-11-30/santo-2026-11-30.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-01/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-01/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-01/santo-2026-12-01.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-02/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-02/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-02/santo-2026-12-02.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-03/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-03/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-03/santo-2026-12-03.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-04/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-04/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-04/santo-2026-12-04.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-05/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-05/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-05/santo-2026-12-05.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-07/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-07/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-07/santo-2026-12-07.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-08/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-08/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-08/santo-2026-12-08.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-09/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-09/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-09/santo-2026-12-09.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-10/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-10/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-10/santo-2026-12-10.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-11/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-11/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-11/santo-2026-12-11.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-12/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-12/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-12/santo-2026-12-12.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-14/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-14/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-14/santo-2026-12-14.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-15/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-15/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-15/santo-2026-12-15.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-16/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-16/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-16/santo-2026-12-16.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-24/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-24/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-24/santo-2026-12-24.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-25/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-25/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-25/santo-2026-12-25.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-26/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-26/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-26/santo-2026-12-26.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-28/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-28/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-28/santo-2026-12-28.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-29/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-29/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-29/santo-2026-12-29.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-30/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-30/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-30/santo-2026-12-30.pdf` | p1: 0 |
| `saida/santo-do-dia/2026-12-31/card.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-31/recorte.png` | 0 pixels |
| `saida/santo-do-dia/2026-12-31/santo-2026-12-31.pdf` | p1: 0 |
| `saida/santo-do-dia/prancha.png` | 0 pixels |
| `saida/para-rezar/2026-10-20/card-1.png` | 0 pixels |
| `saida/para-rezar/2026-10-20/para-rezar-2026-10-20.pdf` | p1: 0 |
| `saida/para-rezar/2026-12-15/card-1.png` | 0 pixels |
| `saida/para-rezar/2026-12-15/card-2.png` | 0 pixels |
| `saida/para-rezar/2026-12-15/para-rezar-2026-12-15.pdf` | p1: 0, p2: 0 |
| `saida/para-rezar/prancha.png` | 0 pixels |
| `saida/coragem/2026-12-14/coragem-2026-12-14-feed.pdf` | p1: 0 |
| `saida/coragem/2026-12-14/coragem-2026-12-14-status.pdf` | p1: 0 |
| `saida/coragem/2026-12-14/feed.png` | 0 pixels |
| `saida/coragem/2026-12-14/recorte-feed.png` | 0 pixels |
| `saida/coragem/2026-12-14/recorte-status.png` | 0 pixels |
| `saida/coragem/2026-12-14/status.png` | 0 pixels |
| `saida/coragem/2026-12-28/coragem-2026-12-28-feed.pdf` | p1: 0 |
| `saida/coragem/2026-12-28/coragem-2026-12-28-status.pdf` | p1: 0 |
| `saida/coragem/2026-12-28/feed.png` | 0 pixels |
| `saida/coragem/2026-12-28/recorte-feed.png` | 0 pixels |
| `saida/coragem/2026-12-28/recorte-status.png` | 0 pixels |
| `saida/coragem/2026-12-28/status.png` | 0 pixels |
| `saida/coragem/prancha.png` | 0 pixels |
| `saida/stories/advento/angelus.png` | 0 pixels |
| `saida/stories/advento/misericordia.png` | 0 pixels |
| `saida/stories/advento/stories-advento.pdf` | p1: 0, p2: 0 |
| `saida/stories/natal/angelus.png` | 0 pixels |
| `saida/stories/natal/misericordia.png` | 0 pixels |
| `saida/stories/natal/stories-natal.pdf` | p1: 0, p2: 0 |
| `saida/stories/prancha.png` | 0 pixels |
| `saida/stories/quaresma/angelus.png` | 0 pixels |
| `saida/stories/quaresma/misericordia.png` | 0 pixels |
| `saida/stories/quaresma/stories-quaresma.pdf` | p1: 0, p2: 0 |
| `saida/stories/recorte-angelus.png` | 0 pixels |
| `saida/stories/recorte-misericordia.png` | 0 pixels |
| `saida/stories/tempo-comum/angelus.png` | 0 pixels |
| `saida/stories/tempo-comum/misericordia.png` | 0 pixels |
| `saida/stories/tempo-comum/stories-tempo-comum.pdf` | p1: 0, p2: 0 |
| `saida/novena/imaculada/dia-1.png` | 0 pixels |
| `saida/novena/imaculada/dia-2.png` | 0 pixels |
| `saida/novena/imaculada/dia-3.png` | 0 pixels |
| `saida/novena/imaculada/dia-4.png` | 0 pixels |
| `saida/novena/imaculada/dia-5.png` | 0 pixels |
| `saida/novena/imaculada/dia-6.png` | 0 pixels |
| `saida/novena/imaculada/dia-7.png` | 0 pixels |
| `saida/novena/imaculada/dia-8.png` | 0 pixels |
| `saida/novena/imaculada/dia-9.png` | 0 pixels |
| `saida/novena/imaculada/encerramento.png` | 0 pixels |
| `saida/novena/imaculada/novena-imaculada.pdf` | p1: 0, p2: 0, p3: 0, p4: 0, p5: 0, p6: 0, p7: 0, p8: 0, p9: 0, p10: 0 |
| `saida/novena/imaculada/prancha.png` | 0 pixels |
| `saida/novena/natal/dia-1.png` | 0 pixels |
| `saida/novena/natal/dia-2.png` | 0 pixels |
| `saida/novena/natal/dia-3.png` | 0 pixels |
| `saida/novena/natal/dia-4.png` | 0 pixels |
| `saida/novena/natal/dia-5.png` | 0 pixels |
| `saida/novena/natal/dia-6.png` | 0 pixels |
| `saida/novena/natal/dia-7.png` | 0 pixels |
| `saida/novena/natal/dia-8.png` | 0 pixels |
| `saida/novena/natal/dia-9.png` | 0 pixels |
| `saida/novena/natal/encerramento.png` | 0 pixels |
| `saida/novena/natal/novena-natal.pdf` | p1: 0, p2: 0, p3: 0, p4: 0, p5: 0, p6: 0, p7: 0, p8: 0, p9: 0, p10: 0 |
| `saida/novena/natal/prancha.png` | 0 pixels |
| `saida/novena/teste-canva/dia-1.png` | 0 pixels |
| `saida/novena/teste-canva/dia-8.png` | 0 pixels |
| `saida/novena/teste-canva/encerramento.png` | 0 pixels |
| `saida/novena/teste-canva/novena-teste-canva.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/novena/teste-canva/prancha.png` | 0 pixels |
| `saida/igreja-domestica/2026-11-29/card-1.png` | 0 pixels |
| `saida/igreja-domestica/2026-11-29/card-2.png` | 0 pixels |
| `saida/igreja-domestica/2026-11-29/card-3.png` | 0 pixels |
| `saida/igreja-domestica/2026-11-29/card-4.png` | 0 pixels |
| `saida/igreja-domestica/2026-11-29/igreja-domestica-2026-11-29.pdf` | p1: 0, p2: 0, p3: 0, p4: 0 |
| `saida/igreja-domestica/2026-11-29/recorte.png` | 0 pixels |
| `saida/igreja-domestica/2026-12-06/card-1.png` | 0 pixels |
| `saida/igreja-domestica/2026-12-06/card-2.png` | 0 pixels |
| `saida/igreja-domestica/2026-12-06/card-3.png` | 0 pixels |
| `saida/igreja-domestica/2026-12-06/igreja-domestica-2026-12-06.pdf` | p1: 0, p2: 0, p3: 0 |
| `saida/igreja-domestica/2026-12-06/recorte.png` | 0 pixels |
| `saida/igreja-domestica/prancha.png` | 0 pixels |

### Pendências e limites da entrega

Não há pendência de geração, teste ou prova de preservação. A importação dos 18 PDFs no Canva permanece manual. Várias cenas têm figuras ou elementos periféricos cortados pelo arco; as limitações e alternativas conferidas estão nas notas de cada obra. Onde não foi demonstrado um enquadramento integral sem borda fotográfica, o relatório recomenda manter o foco aprovado e registra o limite. Nenhuma sugestão foi aplicada ao YAML. Em 20/12, Maria e o núcleo da coluna de luz estão dentro do arco, mas o brilho superior encontra a curva.

### O que conferir no Canva

A importação destes 18 PDFs no Canva permanece pendente. Conferir:

- Cada texto na sua caixa: selo, data, referência, crédito, título, trecho, referência do trecho, a chamada e o título e o texto da reflexão (20 e 27/12), a pergunta e o convite, com a referência inteira em negrito.
- A obra dentro do arco; em 20/12, Maria e o núcleo da coluna de luz à esquerda. O brilho superior da luz é interceptado pela curva, conforme a nota visual.
- O filete em U, o parapeito e o ornamento como formas vetoriais separadas.
- Nenhuma caixa solta, nem caixa contendo só um espaço, e nenhum par de textos fundido.

<!-- fim-prompt14 -->

## Árvore

```text
saida/evangelho/
  2026-11-29/card-1.png
  2026-11-29/card-2.png
  2026-11-29/card-3.png
  2026-11-29/card-4.png
  2026-11-29/evangelho-2026-11-29.pdf
  2026-11-29/ficha.json
  2026-11-29/recorte.png
  2026-11-30/card-1.png
  2026-11-30/card-2.png
  2026-11-30/card-3.png
  2026-11-30/evangelho-2026-11-30.pdf
  2026-11-30/ficha.json
  2026-11-30/recorte.png
  2026-12-01/card-1.png
  2026-12-01/card-2.png
  2026-12-01/card-3.png
  2026-12-01/evangelho-2026-12-01.pdf
  2026-12-01/ficha.json
  2026-12-01/recorte.png
  2026-12-02/card-1.png
  2026-12-02/card-2.png
  2026-12-02/card-3.png
  2026-12-02/evangelho-2026-12-02.pdf
  2026-12-02/ficha.json
  2026-12-02/recorte.png
  2026-12-03/card-1.png
  2026-12-03/card-2.png
  2026-12-03/card-3.png
  2026-12-03/evangelho-2026-12-03.pdf
  2026-12-03/ficha.json
  2026-12-03/recorte.png
  2026-12-04/card-1.png
  2026-12-04/card-2.png
  2026-12-04/card-3.png
  2026-12-04/evangelho-2026-12-04.pdf
  2026-12-04/ficha.json
  2026-12-04/recorte.png
  2026-12-05/card-1.png
  2026-12-05/card-2.png
  2026-12-05/card-3.png
  2026-12-05/evangelho-2026-12-05.pdf
  2026-12-05/ficha.json
  2026-12-05/recorte.png
  2026-12-06/card-1.png
  2026-12-06/card-2.png
  2026-12-06/card-3.png
  2026-12-06/card-4.png
  2026-12-06/evangelho-2026-12-06.pdf
  2026-12-06/ficha.json
  2026-12-06/recorte.png
  2026-12-07/card-1.png
  2026-12-07/card-2.png
  2026-12-07/card-3.png
  2026-12-07/evangelho-2026-12-07.pdf
  2026-12-07/ficha.json
  2026-12-07/recorte.png
  2026-12-08/card-1.png
  2026-12-08/card-2.png
  2026-12-08/card-3.png
  2026-12-08/evangelho-2026-12-08.pdf
  2026-12-08/ficha.json
  2026-12-08/recorte.png
  2026-12-09/card-1.png
  2026-12-09/card-2.png
  2026-12-09/card-3.png
  2026-12-09/evangelho-2026-12-09.pdf
  2026-12-09/ficha.json
  2026-12-09/recorte.png
  2026-12-10/card-1.png
  2026-12-10/card-2.png
  2026-12-10/card-3.png
  2026-12-10/evangelho-2026-12-10.pdf
  2026-12-10/ficha.json
  2026-12-10/recorte.png
  2026-12-11/card-1.png
  2026-12-11/card-2.png
  2026-12-11/card-3.png
  2026-12-11/evangelho-2026-12-11.pdf
  2026-12-11/ficha.json
  2026-12-11/recorte.png
  2026-12-12/card-1.png
  2026-12-12/card-2.png
  2026-12-12/card-3.png
  2026-12-12/evangelho-2026-12-12.pdf
  2026-12-12/ficha.json
  2026-12-12/recorte.png
  2026-12-13/card-1.png
  2026-12-13/card-2.png
  2026-12-13/card-3.png
  2026-12-13/card-4.png
  2026-12-13/evangelho-2026-12-13.pdf
  2026-12-13/ficha.json
  2026-12-13/recorte.png
  2026-12-14/card-1.png
  2026-12-14/card-2.png
  2026-12-14/card-3.png
  2026-12-14/evangelho-2026-12-14.pdf
  2026-12-14/ficha.json
  2026-12-14/recorte.png
  2026-12-15/card-1.png
  2026-12-15/card-2.png
  2026-12-15/card-3.png
  2026-12-15/evangelho-2026-12-15.pdf
  2026-12-15/ficha.json
  2026-12-15/recorte.png
  2026-12-16/card-1.png
  2026-12-16/card-2.png
  2026-12-16/card-3.png
  2026-12-16/evangelho-2026-12-16.pdf
  2026-12-16/ficha.json
  2026-12-16/recorte.png
  2026-12-17/card-1.png
  2026-12-17/card-2.png
  2026-12-17/card-3.png
  2026-12-17/evangelho-2026-12-17.pdf
  2026-12-17/ficha.json
  2026-12-17/recorte.png
  2026-12-18/card-1.png
  2026-12-18/card-2.png
  2026-12-18/card-3.png
  2026-12-18/evangelho-2026-12-18.pdf
  2026-12-18/ficha.json
  2026-12-18/recorte.png
  2026-12-19/card-1.png
  2026-12-19/card-2.png
  2026-12-19/card-3.png
  2026-12-19/evangelho-2026-12-19.pdf
  2026-12-19/ficha.json
  2026-12-19/recorte.png
  2026-12-20/card-1.png
  2026-12-20/card-2.png
  2026-12-20/card-3.png
  2026-12-20/card-4.png
  2026-12-20/evangelho-2026-12-20.pdf
  2026-12-20/ficha.json
  2026-12-20/recorte.png
  2026-12-21/card-1.png
  2026-12-21/card-2.png
  2026-12-21/card-3.png
  2026-12-21/evangelho-2026-12-21.pdf
  2026-12-21/ficha.json
  2026-12-21/recorte.png
  2026-12-22/card-1.png
  2026-12-22/card-2.png
  2026-12-22/card-3.png
  2026-12-22/evangelho-2026-12-22.pdf
  2026-12-22/ficha.json
  2026-12-22/recorte.png
  2026-12-23/card-1.png
  2026-12-23/card-2.png
  2026-12-23/card-3.png
  2026-12-23/evangelho-2026-12-23.pdf
  2026-12-23/ficha.json
  2026-12-23/recorte.png
  2026-12-24/card-1.png
  2026-12-24/card-2.png
  2026-12-24/card-3.png
  2026-12-24/evangelho-2026-12-24.pdf
  2026-12-24/ficha.json
  2026-12-24/recorte.png
  2026-12-25/card-1.png
  2026-12-25/card-2.png
  2026-12-25/card-3.png
  2026-12-25/evangelho-2026-12-25.pdf
  2026-12-25/ficha.json
  2026-12-25/recorte.png
  2026-12-26/card-1.png
  2026-12-26/card-2.png
  2026-12-26/card-3.png
  2026-12-26/evangelho-2026-12-26.pdf
  2026-12-26/ficha.json
  2026-12-26/recorte.png
  2026-12-27/card-1.png
  2026-12-27/card-2.png
  2026-12-27/card-3.png
  2026-12-27/card-4.png
  2026-12-27/evangelho-2026-12-27.pdf
  2026-12-27/ficha.json
  2026-12-27/recorte.png
  2026-12-28/card-1.png
  2026-12-28/card-2.png
  2026-12-28/card-3.png
  2026-12-28/evangelho-2026-12-28.pdf
  2026-12-28/ficha.json
  2026-12-28/recorte.png
  2026-12-29/card-1.png
  2026-12-29/card-2.png
  2026-12-29/card-3.png
  2026-12-29/evangelho-2026-12-29.pdf
  2026-12-29/ficha.json
  2026-12-29/recorte.png
  2026-12-30/card-1.png
  2026-12-30/card-2.png
  2026-12-30/card-3.png
  2026-12-30/evangelho-2026-12-30.pdf
  2026-12-30/ficha.json
  2026-12-30/recorte.png
  2026-12-31/card-1.png
  2026-12-31/card-2.png
  2026-12-31/card-3.png
  2026-12-31/evangelho-2026-12-31.pdf
  2026-12-31/ficha.json
  2026-12-31/recorte.png
  CONFERENCIA-ENQUADRAMENTOS.md
  CONFERENCIA-KIT-V3.md
  CONFERENCIA-PROMPT-11.md
  CONFERENCIA-PROMPT-12.md
  NOTAS-DAS-OBRAS-LOTE-1.json
  RELATORIO.md
  conferencia-enquadramentos.json
  conferencia-kit-v3.json
  conferencia-prompt11.json
  conferencia-prompt12.json
  prancha-cores.png
  prancha.png
  verificacao.json
```
