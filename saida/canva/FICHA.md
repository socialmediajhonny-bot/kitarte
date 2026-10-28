# Ficha técnica

| Token | Pergaminho | Capela | Alias |
| --- | --- | --- | --- |
| fundo | #f2eadb | #16110d | — |
| papel | #faf6ee | #211a15 | — |
| tinta | #241b14 | #f3eadb | — |
| tinta-suave | #665647 | #bbad98 | — |
| linha | #d3c3a9 | #3d3229 | — |
| ouro | #866420 | #cfa956 | — |
| liturgico-verde | #2e5b3b | #74aa82 | — |
| liturgico-roxo | #5b2e70 | #ac8bc6 | — |
| liturgico-branco | #866420 | #cfa956 | ouro |
| liturgico-vermelho | #8e2020 | #d86e60 | — |
| liturgico-rosa | #99476a | #de9eb5 | — |
| cor-do-dia | #2e5b3b | #74aa82 | liturgico-verde |
| sobre-cor | #faf6ee | #16110d | — |

## Página 1 · Capa CSS

| Tema | Largura (px) | Altura (px) | Cor do dia |
| --- | --- | --- | --- |
| capela | 1080 | 1350 | var(--liturgico-verde) |

| Elemento | Arquivo | Texto | Fonte / peso / estilo | x (px) | y (px) | Largura (px) | Altura (px) | Texto (px) | Entrelinha (px) | Entrelinha (×) | Letras (em) | Letras (‰ de em) | Cor: token / hex |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arte-fundo | — | — | — | 0 | 0 | 1080 | 1350 | — | — | — | — | — | fundo / #16110d |
| topo | — | — | — | 80 | 80 | 920 | 40 | — | — | — | — | — | — |
| selo-cruz | — | — | — | 80 | 85 | 18 | 30 | — | — | — | — | — | cor-do-dia / #74aa82 |
| selo-serie | — | Evangelho do Dia | Lato / 700 / normal | 114 | 80 | 252.359375 | 39 | 32 | 40 | 1.25 | 0.01 | 10 | tinta / #f3eadb |
| selo-data | — | · sex, 16 out | Lato / 400 / normal | 374.46875 | 80 | 175.390625 | 39 | 32 | 40 | 1.25 | 0.01 | 10 | tinta-suave / #bbad98 |
| selo-info | — | Lc 12,1-7 | Lato / 400 / normal | 864.984375 | 80 | 135.015625 | 40 | 32 | 40 | 1.25 | 0.01 | 10 | tinta-suave / #bbad98 |
| nicho | — | — | — | 200 | 152 | 680 | 760 | — | — | — | — | — | — |
| nicho-filete | — | — | — | 200 | 152 | 680 | 760 | — | — | — | — | — | cor-do-dia / #74aa82 |
| nicho-parapeito | — | — | — | 152 | 912 | 776 | 3 | — | — | — | — | — | cor-do-dia / #74aa82 |
| nicho-recorte | — | — | — | 216 | 168 | 648 | 744 | — | — | — | — | — | papel / #211a15 |
| nicho-obra | obra-provisoria.png | — | — | 216 | 168 | 648 | 744 | — | — | — | — | — | — |
| credito-obra | — | Artista · Título da obra · Museu | Lato / 400 / normal | 377.8125 | 944 | 324.375 | 32 | 24 | 32 | 1.333333 | 0 | 0 | tinta-suave / #bbad98 |
| titulo | — | Nem um pardal é esquecido por Deus | Cormorant Garamond / 600 / normal | 100 | 1024 | 880 | 152 | 68 | 76 | 1.117647 | 0 | 0 | tinta / #f3eadb |
| assinatura | — | — | — | 394.328125 | 1218 | 291.328125 | 52 | — | — | — | — | — | — |
| logo | kit/logos/logo-horizontal-capela.svg | — | — | 394.328125 | 1218 | 291.328125 | 52 | — | — | — | — | — | ouro [capela] / #cfa956; tinta [capela] / #f3eadb |

| Elemento | Propriedade | Valor |
| --- | --- | --- |
| arte-fundo | Fundo | #16110d |
| nicho-filete | Raio top_left (rx, ry; px) | [340,340] |
| nicho-filete | Raio top_right (rx, ry; px) | [340,340] |
| nicho-filete | Raio bottom_right (rx, ry; px) | [0,0] |
| nicho-filete | Raio bottom_left (rx, ry; px) | [0,0] |
| nicho-filete | Medição | getComputedStyle(::before) + host.getBoundingClientRect |
| nicho-filete | Borda top (px) | 3 |
| nicho-filete | Borda right (px) | 3 |
| nicho-filete | Borda bottom (px) | 0 |
| nicho-filete | Borda left (px) | 3 |
| nicho-parapeito | Fundo | #74aa82 |
| nicho-parapeito | Medição | getComputedStyle(::after) + host.getBoundingClientRect |
| nicho-parapeito | Borda top (px) | 0 |
| nicho-parapeito | Borda right (px) | 0 |
| nicho-parapeito | Borda bottom (px) | 0 |
| nicho-parapeito | Borda left (px) | 0 |
| nicho-recorte | Fundo | #211a15 |
| nicho-recorte | Raio top_left (rx, ry; px) | [324,324] |
| nicho-recorte | Raio top_right (rx, ry; px) | [324,324] |
| nicho-recorte | Raio bottom_right (rx, ry; px) | [0,0] |
| nicho-recorte | Raio bottom_left (rx, ry; px) | [0,0] |
| nicho-obra | Origem | http://127.0.0.1:35891/saida/obra-provisoria.png |
| nicho-obra | Imagem: largura original (px) | 1080 |
| nicho-obra | Imagem: altura original (px) | 1350 |
| nicho-obra | object-fit | cover |
| nicho-obra | object-position | 50% 50% |
| logo | Origem | kit/logos/logo-horizontal-capela.svg |
| logo | Imagem: largura original (px) | 2510 |
| logo | Imagem: altura original (px) | 448 |
| logo | object-fit | fill |
| logo | object-position | 50% 50% |

## Página 2 · Capa Canva

| Tema | Largura (px) | Altura (px) | Cor do dia |
| --- | --- | --- | --- |
| capela | 1080 | 1350 | var(--liturgico-verde) |

| Elemento | Arquivo | Texto | Fonte / peso / estilo | x (px) | y (px) | Largura (px) | Altura (px) | Texto (px) | Entrelinha (px) | Entrelinha (×) | Letras (em) | Letras (‰ de em) | Cor: token / hex |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arte-fundo | — | — | — | 0 | 0 | 1080 | 1350 | — | — | — | — | — | fundo / #16110d |
| topo | — | — | — | 80 | 80 | 920 | 40 | — | — | — | — | — | — |
| selo-cruz | — | — | — | 80 | 85 | 18 | 30 | — | — | — | — | — | cor-do-dia / #74aa82 |
| selo-serie | — | Evangelho do Dia | Lato / 700 / normal | 114 | 80 | 252.359375 | 39 | 32 | 40 | 1.25 | 0.01 | 10 | tinta / #f3eadb |
| selo-data | — | · sex, 16 out | Lato / 400 / normal | 374.46875 | 80 | 175.390625 | 39 | 32 | 40 | 1.25 | 0.01 | 10 | tinta-suave / #bbad98 |
| selo-info | — | Lc 12,1-7 | Lato / 400 / normal | 864.984375 | 80 | 135.015625 | 40 | 32 | 40 | 1.25 | 0.01 | 10 | tinta-suave / #bbad98 |
| nicho-canva | — | — | — | 200 | 152 | 680 | 760 | — | — | — | — | — | — |
| nicho-obra-retangular | obra-provisoria.png | — | — | 216 | 168 | 648 | 744 | — | — | — | — | — | — |
| nicho-mascara | canva/elementos/variantes/nicho-680x760-capela-verde.svg | — | — | 152 | 152 | 776 | 763 | — | — | — | — | — | fundo [capela] / #16110d; liturgico-verde [capela] / #74aa82 |
| credito-obra | — | Artista · Título da obra · Museu | Lato / 400 / normal | 377.8125 | 944 | 324.375 | 32 | 24 | 32 | 1.333333 | 0 | 0 | tinta-suave / #bbad98 |
| titulo | — | Nem um pardal é esquecido por Deus | Cormorant Garamond / 600 / normal | 100 | 1024 | 880 | 152 | 68 | 76 | 1.117647 | 0 | 0 | tinta / #f3eadb |
| assinatura | — | — | — | 394.328125 | 1218 | 291.328125 | 52 | — | — | — | — | — | — |
| logo | kit/logos/logo-horizontal-capela.svg | — | — | 394.328125 | 1218 | 291.328125 | 52 | — | — | — | — | — | ouro [capela] / #cfa956; tinta [capela] / #f3eadb |

| Elemento | Propriedade | Valor |
| --- | --- | --- |
| arte-fundo | Fundo | #16110d |
| nicho-obra-retangular | Origem | http://127.0.0.1:35891/saida/obra-provisoria.png |
| nicho-obra-retangular | Imagem: largura original (px) | 1080 |
| nicho-obra-retangular | Imagem: altura original (px) | 1350 |
| nicho-obra-retangular | object-fit | cover |
| nicho-obra-retangular | object-position | 50% 50% |
| nicho-mascara | Origem | saida/canva/elementos/variantes/nicho-680x760-capela-verde.svg |
| nicho-mascara | Imagem: largura original (px) | 776 |
| nicho-mascara | Imagem: altura original (px) | 763 |
| nicho-mascara | object-fit | fill |
| nicho-mascara | object-position | 50% 50% |
| logo | Origem | kit/logos/logo-horizontal-capela.svg |
| logo | Imagem: largura original (px) | 2510 |
| logo | Imagem: altura original (px) | 448 |
| logo | object-fit | fill |
| logo | object-position | 50% 50% |

## Página 3 · Cartão final

| Tema | Largura (px) | Altura (px) | Cor do dia |
| --- | --- | --- | --- |
| pergaminho | 1080 | 1350 | var(--liturgico-verde) |

| Elemento | Arquivo | Texto | Fonte / peso / estilo | x (px) | y (px) | Largura (px) | Altura (px) | Texto (px) | Entrelinha (px) | Entrelinha (×) | Letras (em) | Letras (‰ de em) | Cor: token / hex |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arte-fundo | — | — | — | 0 | 0 | 1080 | 1350 | — | — | — | — | — | cor-do-dia / #2e5b3b |
| topo | — | — | — | 80 | 80 | 920 | 40 | — | — | — | — | — | — |
| selo-cruz | — | — | — | 80 | 85 | 18 | 30 | — | — | — | — | — | sobre-cor / #faf6ee |
| selo-serie | — | Evangelho do Dia | Lato / 700 / normal | 114 | 80 | 252.359375 | 39 | 32 | 40 | 1.25 | 0.01 | 10 | sobre-cor / #faf6ee |
| selo-data | — | · sex, 16 out | Lato / 400 / normal | 374.46875 | 80 | 175.390625 | 39 | 32 | 40 | 1.25 | 0.01 | 10 | sobre-cor / #faf6ee |
| selo-info | — | Lc 12,1-7 | Lato / 400 / normal | 864.984375 | 80 | 135.015625 | 40 | 32 | 40 | 1.25 | 0.01 | 10 | sobre-cor / #faf6ee |
| convite-oracao | — | Para rezar hoje | Lato / 700 / normal | 431.84375 | 489.5 | 216.296875 | 40 | 32 | 40 | 1.25 | 0.01 | 10 | sobre-cor / #faf6ee |
| pergunta | — | Se Deus conta até os cabelos da minha cabeça, do que eu ainda tenho medo? | Cormorant Garamond / 500 / italic | 110 | 545.5 | 860 | 136 | 54 | 68 | 1.259259 | 0 | 0 | sobre-cor / #faf6ee |
| ornamento | — | — | — | 445 | 729.5 | 190 | 21 | — | — | — | — | — | — |
| ornamento-filete-esquerdo | — | — | — | 445 | 739 | 72 | 2 | — | — | — | — | — | sobre-cor / #faf6ee |
| ornamento-filete-direito | — | — | — | 563 | 739 | 72 | 2 | — | — | — | — | — | sobre-cor / #faf6ee |
| ornamento-cruz | — | — | — | 533 | 729.5 | 14 | 21 | — | — | — | — | — | sobre-cor / #faf6ee |
| convite-biblia | — | Abra sua Bíblia em | Lato / 400 / normal | 301.34375 | 802.5 | 284.8125 | 41 | 34 | 50 | 1.470588 | 0 | 0 | sobre-cor / #faf6ee |
| referencia-biblia | — | Lucas 12,1-7 | Lato / 700 / normal | 586.15625 | 802.5 | 192.5 | 41 | 34 | 50 | 1.470588 | 0 | 0 | sobre-cor / #faf6ee |
| assinatura | — | — | — | 394.328125 | 1218 | 291.328125 | 52 | — | — | — | — | — | — |
| logo | kit/logos/logo-horizontal-sobre-cor.svg | — | — | 394.328125 | 1218 | 291.328125 | 52 | — | — | — | — | — | papel [pergaminho] / #faf6ee |

| Elemento | Propriedade | Valor |
| --- | --- | --- |
| arte-fundo | Fundo | #2e5b3b |
| ornamento-filete-esquerdo | Fundo | #faf6ee |
| ornamento-filete-esquerdo | Medição | getComputedStyle(::before) + host.getBoundingClientRect |
| ornamento-filete-esquerdo | Borda top (px) | 0 |
| ornamento-filete-esquerdo | Borda right (px) | 0 |
| ornamento-filete-esquerdo | Borda bottom (px) | 0 |
| ornamento-filete-esquerdo | Borda left (px) | 0 |
| ornamento-filete-direito | Fundo | #faf6ee |
| ornamento-filete-direito | Medição | getComputedStyle(::after) + host.getBoundingClientRect |
| ornamento-filete-direito | Borda top (px) | 0 |
| ornamento-filete-direito | Borda right (px) | 0 |
| ornamento-filete-direito | Borda bottom (px) | 0 |
| ornamento-filete-direito | Borda left (px) | 0 |
| logo | Origem | kit/logos/logo-horizontal-sobre-cor.svg |
| logo | Imagem: largura original (px) | 2510 |
| logo | Imagem: altura original (px) | 448 |
| logo | object-fit | fill |
| logo | object-position | 50% 50% |
