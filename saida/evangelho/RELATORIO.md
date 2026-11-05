# Evangelho do Dia

`python gerar.py evangelho` · seleção: `python gerar.py evangelho --data AAAA-MM-DD`

## Decisões

- A composição vem de PostEvangelho/preview.html e bundle.css; a capa usa um img dentro do arco CSS, sem SVG sobre a imagem.
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

## Obras e legendas

- **2026-11-29 — 1º Domingo do Advento:** obra local real; recorte.png gerado.
  James Tissot · A profecia da destruição do Templo · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4551
  Foco 45% 50%; zoom 1.1; janela original x=309.337, y=46.591, largura=811.584, altura=931.818px.
- **2026-11-30 — Santo André, apóstolo (Festa):** obra local real; recorte.png gerado.
  Duccio · A vocação dos apóstolos Pedro e André · National Gallery of Art — https://www.nga.gov/artworks/282-calling-apostles-peter-and-andrew
  Foco 22% 50%; zoom 1; janela original x=103.890, y=0.000, largura=2127.774, altura=2443.000px.
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
  Foco 33% 50%; zoom 1.1; janela original x=242.977, y=45.909, largura=799.707, altura=918.182px.
- **2026-12-06 — 2º Domingo do Advento:** obra local real; recorte.png gerado.
  James Tissot · A voz no deserto · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4447
  Foco 40% 15%; zoom 1.1; janela original x=33.091, y=87.925, largura=827.273, altura=949.832px.
- **2026-12-07 — Santo Ambrósio, bispo e doutor da Igreja (Memória):** obra local real; recorte.png gerado.
  James Tissot · O paralítico descido pelo telhado · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4504
  Foco 50% 20%; zoom 1.1; janela original x=49.500, y=79.867, largura=990.000, altura=1136.667px.
- **2026-12-08 — Imaculada Conceição da Bem-aventurada Virgem Maria (Solenidade):** obra local real; recorte.png gerado.
  Fra Angelico · A Anunciação · Museu do Prado — https://commons.wikimedia.org/wiki/File:La_Anunciación,_by_Fra_Angelico,_from_Prado_in_Google_Earth.jpg
  Foco 82% 40%; zoom 1.3; janela original x=1067.200, y=349.754, largura=2538.536, altura=2914.615px.
- **2026-12-09 — Quarta-feira da 2ª Semana do Advento:** obra local real; recorte.png gerado.
  Ary Scheffer · Cristo Consolador · Minneapolis Institute of Art — https://collections.artsmia.org/art/104894/christus-consolator-ary-scheffer
  Foco 48% 27%; zoom 3; janela original x=2382.705, y=910.800, largura=1469.032, altura=1686.667px.
- **2026-12-10 — Quinta-feira da 2ª Semana do Advento:** obra local real; recorte.png gerado.
  Geertgen tot Sint Jans · São João Batista no deserto · Gemäldegalerie — https://commons.wikimedia.org/wiki/File:Geertgen_tot_Sint_Jans_004.jpg
  Foco 50% 85%; zoom 1; janela original x=0.000, y=376.046, largura=1192.000, altura=1368.593px.
- **2026-12-11 — Sexta-feira da 2ª Semana do Advento:** obra local real; recorte.png gerado.
  James Tissot · A refeição na casa de Mateus · Brooklyn Museum — https://www.brooklynmuseum.org/objects/13405
  Foco 88% 25%; zoom 1.3; janela original x=683.098, y=65.423, largura=759.752, altura=872.308px.
- **2026-12-12 — Bem-aventurada Virgem Maria de Guadalupe, Padroeira principal da América (Festa):** obra local real; recorte.png gerado.
  Piero di Cosimo · A Visitação · National Gallery of Art — https://www.nga.gov/artworks/505-visitation-saint-nicholas-and-saint-anthony-abbot
  Foco 50% 8%; zoom 1.55; janela original x=598.169, y=70.911, largura=1403.663, altura=1611.613px.
- **2026-12-13 — 3º Domingo do Advento (Gaudete):** obra local real; recorte.png gerado.
  James Tissot · São João Batista e os fariseus · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4449
  Foco 50% 50%; zoom 1.1; janela original x=334.496, y=49.773, largura=867.009, altura=995.455px.
Nenhuma margem uniforme da foto está visível nos enquadramentos selecionados.

## Conferência

PNG exatos; limites de linhas; palavras de uma letra; afastamento de 32 px do logo; pares de 32 e 48 px para o Canva; centralização vertical; cruz, fundo e filete por pixel; páginas PDF de 810 × 1012,5 pt; quatro variantes embutidas por pdffonts; título e convite extraíveis. Os valores estão em verificacao.json e ficha.json.

A regra dos espaços foi aprovada no teste de importação no Canva de 29/10/2026, registrado em saida/teste-canva/LEIA-ME.md. Esta geração valida os novos PDFs; sua importação no editor permanece uma conferência manual.

Todas as obras selecionadas foram encontradas localmente e receberam prova de recorte.

<!-- inicio-relatorio-lote-1 -->
## Lote 1 · 30/11 a 12/12

Trechos retirados da Liturgia Diária da CNBB, conferidos e aprovados em 05/11/2026. Foram acrescentados treze carrosséis; os dias 29/11 e 13/12 foram preservados.

### Tabela medida no navegador

| Data | Capa: crédito, título | Versículo: estilo, linhas | Para a Missa de hoje | Para rezar hoje: pergunta, convite |
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

### Comparação com a tabela prevista

Nenhuma diferença em relação à tabela do prompt.

### Obras, janelas e inspeção visual

As imagens originais foram preservadas. Borda do museu é aceita quando fica fora do arco e recebe teste próprio. Os recortes mostram a pintura inteira com o contorno do arco; as notas se referem ao interior desse contorno.

#### 2026-11-30

Duccio · A vocação dos apóstolos Pedro e André · National Gallery of Art — https://www.nga.gov/artworks/282-calling-apostles-peter-and-andrew

Foco 22% 50%, zoom 1; janela original x=103.890, y=0.000, largura=2127.774, altura=2443.000 px.
Margens uniformes visíveis: nenhuma.

Cristo, Pedro e André preservam os corpos, rostos, mãos e, no caso de Cristo, os pés; as partes inferiores dos apóstolos já são ocultadas pelo barco na obra original. A curva do arco intercepta apenas a borda superior esquerda da auréola de Cristo, por isso a composição não está estritamente integral. O barco e parte das redes também saem à direita, sem cortar os corpos. Não há margem fotográfica dentro do arco.

A figura ou o grupo principal aparece parcialmente no recorte.

Sugestão registrada, sem alterar o YAML: foco 10% 50%, zoom 1. Alternativa renderizada e inspecionada no card e no respectivo recorte: libera a auréola e mantém os três personagens na extensão em que aparecem na pintura. Sugestão somente; YAML aprovado 22% 50%, zoom 1 preservado.

#### 2026-12-01

James Tissot · Deixai vir a mim as criancinhas · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4539

Foco 20% 45%, zoom 1.1; janela original x=124.930, y=47.086, largura=911.349, altura=1046.364 px.
Margens uniformes visíveis: nenhuma.

Cristo, a mulher que apresenta a criança e a menina de roupa clara ao seu lado ficam inteiros na extensão em que estão pintados, com mãos e pés preservados. Participantes periféricos são recortados nas laterais e pela curva superior; a mãe sentada à direita aparece parcialmente. O papel da fotografia do museu fica inteiramente fora do arco.

#### 2026-12-02

James Tissot · A multiplicação dos pães · Brooklyn Museum — https://www.brooklynmuseum.org/objects/13423

Foco 50% 50%, zoom 1.1; janela original x=348.352, y=48.182, largura=839.296, altura=963.636 px.
Margens uniformes visíveis: nenhuma.

O núcleo central da distribuição dos pães, incluindo as duas figuras que servem e o grupo imediatamente diante delas, permanece preservado na extensão visível na obra; pernas já ocultadas por outros participantes não são um corte novo. Vários integrantes periféricos da multidão são cortados nas laterais, pela curva e na base. Nenhuma borda de papel do museu entra no arco.

#### 2026-12-03

James Tissot · O sermão das bem-aventuranças · Brooklyn Museum — https://www.brooklynmuseum.org/objects/13418

Foco 50% 15%, zoom 1.1; janela original x=48.455, y=63.501, largura=969.091, altura=1112.660 px.
Margens uniformes visíveis: nenhuma.

Cristo, que é a figura principal no alto do monte, fica inteiro: capuz, mãos erguidas, vestes e pés dentro do arco. A plateia periférica, especialmente os ouvintes em primeiro plano, é cortada na base e à direita. A borda fotográfica do museu fica fora do recorte.

#### 2026-12-04

James Tissot · Os cegos de Cafarnaum · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4505

Foco 50% 80%, zoom 1.2; janela original x=71.500, y=572.059, largura=715.000, altura=820.926 px.
Margens uniformes visíveis: nenhuma.

Cristo e os dois cegos ficam inteiros na extensão em que aparecem no original: rostos, mãos erguidas ou estendidas, vestes e pés preservados. O pé do cego em primeiro plano está muito próximo da base, mas permanece dentro dela. O observador atrás de Cristo já aparece parcialmente oculto na própria pintura. As faixas cinzentas externas da fotografia ficam fora do arco.

#### 2026-12-05

James Tissot · A escolha dos doze apóstolos · Brooklyn Museum — https://www.brooklynmuseum.org/objects/13407

Foco 33% 50%, zoom 1.1; janela original x=242.977, y=45.909, largura=799.707, altura=918.182 px.
Margens uniformes visíveis: nenhuma.

No foco aprovado 33% 50%, zoom 1.1, a mão de Cristo que se estende para a esquerda fica fora do arco, embora rosto, outra mão e pés estejam preservados. A maior parte do grupo dos Doze, à direita, também fica fora; alguns apóstolos são interceptados pela curva e pela lateral. Não há borda do museu dentro do arco. A composição horizontal de Cristo até o último apóstolo não cabe inteira no nicho fixo com zoom igual ou superior a 1.

A figura ou o grupo principal aparece parcialmente no recorte.

Sugestão registrada, sem alterar o YAML: foco 25% 50%, zoom 1.1. Alternativa renderizada e inspecionada: recupera Cristo inteiro, inclusive a mão à esquerda, sem trazer o papel do museu. Os apóstolos da direita continuam parcialmente fora; não resolve a integralidade de todo o grupo. Sugestão somente; YAML aprovado preservado.

#### 2026-12-06

James Tissot · A voz no deserto · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4447

Foco 40% 15%, zoom 1.1; janela original x=33.091, y=87.925, largura=827.273, altura=949.832 px.
Margens uniformes visíveis: nenhuma.

Card 1 e recorte conferidos: o rosto de João Batista, os braços e as duas mãos erguidas ficam inteiros dentro do arco. A base corta a figura logo abaixo da túnica, deixando as pernas inferiores e os pés de fora. O foco e o zoom aprovados foram preservados.

A figura ou o grupo principal aparece parcialmente no recorte.

Sugestão registrada, sem alterar o YAML: foco 40% 15%, zoom 1.05. Alternativa verificada em render isolado: abre um pouco o enquadramento, preserva rosto e mãos e continua sem margem fotográfica visível. As pernas ainda ficam parciais; não resolve a figura de corpo inteiro. Abrir até zoom 1 mostra as bordas laterais da foto, e descer o foco para tentar incluir os pés compromete as mãos junto à curva. Recomenda-se priorizar o rosto e o gesto, como no enquadramento aprovado. Não aplicada ao YAML.

#### 2026-12-07

James Tissot · O paralítico descido pelo telhado · Brooklyn Museum — https://www.brooklynmuseum.org/objects/4504

Foco 50% 20%, zoom 1.1; janela original x=49.500, y=79.867, largura=990.000, altura=1136.667 px.
Margens uniformes visíveis: nenhuma.

Card 1 e recorte conferidos: o paralítico suspenso, seu rosto e seus dois braços ficam preservados, assim como o rosto e o gesto de Jesus. A base faz um corte leve na parte inferior da figura sentada de Jesus, junto ao pé. Ajudantes no telhado e figurantes periféricos também são parciais, alguns já no original. O foco e o zoom aprovados foram preservados.

A figura ou o grupo principal aparece parcialmente no recorte.

Sugestão registrada, sem alterar o YAML: foco 50% 20%, zoom 1.04. Alternativa verificada no contorno e no render isolado: inclui o pé e a parte inferior de Jesus e mantém o paralítico e seus gestos dentro do arco, sem margem fotográfica visível. Os figurantes periféricos e os ajudantes já cortados no original continuam parciais. Não aplicada ao YAML.

#### 2026-12-08

Fra Angelico · A Anunciação · Museu do Prado — https://commons.wikimedia.org/wiki/File:La_Anunciación,_by_Fra_Angelico,_from_Prado_in_Google_Earth.jpg

Foco 82% 40%, zoom 1.3; janela original x=1067.200, y=349.754, largura=2538.536, altura=2914.615 px.
Margens uniformes visíveis: nenhuma.

Card 1 e recorte conferidos: os rostos, halos e mãos de Maria e Gabriel ficam inteiros, e as vestes principais são legíveis. O arco corta a extremidade esquerda da asa de Gabriel e a ponta lateral de sua veste. Maria permanece inteira no enquadramento aprovado, com a veste próxima da borda direita. O foco e o zoom aprovados foram preservados.

A figura ou o grupo principal aparece parcialmente no recorte.

Sugestão registrada, sem alterar o YAML: foco 82% 20%, zoom 1.12. Alternativa verificada no contorno e no render isolado: inclui a ponta da asa e a veste de Gabriel, preservando Maria, rostos, halos e mãos. Não mostra margem fotográfica, mas inclui mais arquitetura, moldura interna e uma faixa da predela na base; esse é o custo de abrir o recorte. Não aplicada ao YAML.

#### 2026-12-09

Ary Scheffer · Cristo Consolador · Minneapolis Institute of Art — https://collections.artsmia.org/art/104894/christus-consolator-ary-scheffer

Foco 48% 27%, zoom 3; janela original x=2382.705, y=910.800, largura=1469.032, altura=1686.667 px.
Margens uniformes visíveis: nenhuma.

Card 1 e recorte conferidos: o enquadramento fechado preserva a cabeça e o rosto de Cristo, a mão aberta e o rosto da mulher encostado na mão dele. Os corpos são parciais pela base e pela lateral direita, intencionalmente. O suicida com punhal, a mãe com o filho morto e toda a moldura ficam fora do arco; o topo vermelho da mãe chega perto, mas permanece abaixo da linha inferior do contorno. O recorte mostra essas figuras apenas na parte do original fora do arco. Nenhuma condição de parada foi acionada. Revisão confirmada também pelo revisor principal.

A figura ou o grupo principal aparece parcialmente no recorte.

Sugestão registrada, sem alterar o YAML: foco 48% 27%, zoom 3. Recomendação: manter o enquadramento aprovado, verificado no card e no recorte. Mostrar os corpos inteiros exigiria abrir a janela em direção às figuras que devem ficar excluídas. Não se recomenda abrir este recorte; priorizar os rostos e o gesto e manter o YAML intacto.

Conferência especial de 9/12: o arco está fechado em Cristo e na mulher junto à mão dele. O homem com punhal, a mãe com o filho morto e a moldura estão fora do arco e fora do contorno indicado no recorte.

#### 2026-12-10

Geertgen tot Sint Jans · São João Batista no deserto · Gemäldegalerie — https://commons.wikimedia.org/wiki/File:Geertgen_tot_Sint_Jans_004.jpg

Foco 50% 85%, zoom 1; janela original x=0.000, y=376.046, largura=1192.000, altura=1368.593 px.
Margens uniformes visíveis: nenhuma.

Card 1 e recorte conferidos: o rosto, as duas mãos, as pernas e os pés de João Batista ficam dentro do arco, assim como o cordeiro. A única parte da figura cortada é a extremidade inferior do manto azul, que ultrapassa a base. O foco e o zoom aprovados foram preservados.

A figura ou o grupo principal aparece parcialmente no recorte.

Sugestão registrada, sem alterar o YAML: foco 50% 98%, zoom 1. Alternativa verificada no contorno e no render isolado: inclui a ponta inferior do manto e mantém rosto, mãos, pés e cordeiro dentro do arco, sem margem fotográfica visível. Não aplicada ao YAML.

#### 2026-12-11

James Tissot · A refeição na casa de Mateus · Brooklyn Museum — https://www.brooklynmuseum.org/objects/13405

Foco 88% 25%, zoom 1.3; janela original x=683.098, y=65.423, largura=759.752, altura=872.308 px.
Margens uniformes visíveis: nenhuma.

Card 1 e recorte conferidos: Cristo sentado e os dois interlocutores de pé no centro ficam inteiros, incluindo seus rostos, mãos, vestes e pés visíveis na pintura. O figurante sentado de azul na borda inferior esquerda fica parcial, e outros figurantes periféricos são excluídos, sem cortar as figuras principais. O foco e o zoom aprovados foram preservados.

#### 2026-12-12

Piero di Cosimo · A Visitação · National Gallery of Art — https://www.nga.gov/artworks/505-visitation-saint-nicholas-and-saint-anthony-abbot

Foco 50% 8%, zoom 1.55; janela original x=598.169, y=70.911, largura=1403.663, altura=1611.613 px.
Margens uniformes visíveis: nenhuma.

Card 1 e recorte conferidos: Maria e Isabel ficam no centro, com rostos, halos e mãos inteiros; a base corta as partes inferiores das saias e os pés. Os rostos e corpos identificáveis de São Nicolau e Santo Antão ficam fora. Contudo, duas pequenas pontas vermelhas de seus mantos aparecem nas quinas inferiores internas do arco: à esquerda de Maria e à direita de Isabel; junto da ponta direita também há uma extremidade clara ligada ao objeto que o santo segura. Portanto, os santos não estão integralmente excluídos. Essa ressalva foi confirmada também pelo revisor principal. O foco e o zoom aprovados foram preservados; o STOP obrigatório de 9/12 não se aplica a esta data.

A figura ou o grupo principal aparece parcialmente no recorte.

Sugestão registrada, sem alterar o YAML: foco 50% 3%, zoom 1.6. Alternativa verificada em render real isolado e confirmada por dois revisores: elimina as duas pontas dos mantos e a extremidade clara, preservando os halos, rostos e mãos de Maria e Isabel. Saias inferiores e pés continuam fora; o recorte não torna as figuras de corpo inteiro. Não aplicada ao YAML.

Ressalva de 12/12: os santos da frente não ficam completamente fora do arco. Fragmentos dos mantos aparecem nas quinas inferiores; a nota visual registra a extensão visível e a sugestão de enquadramento, sem mudar o YAML.

## O que conferir no Canva

- Cada texto na sua caixa: selo, data, referência, crédito, título, trecho, referência do trecho, a chamada, o título e o texto da reflexão de 6/12, a pergunta e o convite, com a referência em negrito.
- A obra dentro do arco.
- O filete, o parapeito e o ornamento como formas.
- Nenhuma caixa solta, inclusive caixas contendo somente um espaço, como observado na importação da Igreja Doméstica.

A conferência independente está em [CONFERENCIA-PROMPT-11.md](CONFERENCIA-PROMPT-11.md), com [evidência detalhada](conferencia-prompt11.json).

O texto integral de todas as páginas foi comparado por PyMuPDF e pdftotext, preservando as fronteiras entre palavras. Espaços comuns, espaços inseparáveis e quebras são normalizados para um espaço, sem descartar os espaços entre palavras.
Os treze PDFs novos ainda precisam da conferência de importação no Canva. As notas registram os recortes parciais e as sugestões, sem alterar foco e zoom aprovados.
<!-- fim-relatorio-lote-1 -->

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
  CONFERENCIA-KIT-V3.md
  CONFERENCIA-PROMPT-11.md
  NOTAS-DAS-OBRAS-LOTE-1.json
  RELATORIO.md
  conferencia-kit-v3.json
  conferencia-prompt11.json
  prancha-cores.png
  prancha.png
  verificacao.json
```
