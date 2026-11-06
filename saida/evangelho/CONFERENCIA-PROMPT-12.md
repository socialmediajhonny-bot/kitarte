# Conferência do prompt 12

Baseline: main em d8e738b5562fb2bf2ed62d0b86f55b9116be89a8.

Conferência aprovada.

Regra autorizada: qualquer intensidade de antialiasing somente até 2 pixels do contorno nos PNGs e até 4 pixels no raster PyMuPDF a 2× dos PDFs. Fora dessas faixas, exige-se igualdade absoluta. As posições são avaliadas pelo centro de cada pixel. A geometria dos PNGs usa o caminho em U; os PDFs usam as curvas e retas reais extraídas por PyMuPDF, em coordenadas do raster. Pranchas e imagens reduzidas derivadas dos cards estão excluídas da comparação por instrução explícita.

| Série | Tipo | Arquivos | Idênticos | Páginas | Pixels diferentes | Maior diferença por canal | Maior distância ao contorno (px do raster) | Pixels fora da faixa |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| componentes | PNG | 28 | 26 | — | 11286 | 58 | 0.884076621 | 0 |
| componentes | PDF | 1 | 0 | 3 | 244 | 26 | 1.590213407 | 0 |
| coragem | PNG | 8 | 4 | — | 7267 | 62 | 0.825183372 | 0 |
| coragem | PDF | 4 | 0 | 4 | 4714 | 47 | 2.098640619 | 0 |
| evangelho | PNG | 63 | 48 | — | 26832 | 51 | 0.820843801 | 0 |
| evangelho | PDF | 15 | 0 | 48 | 3745 | 35 | 1.590213407 | 0 |
| igreja-domestica | PNG | 9 | 7 | — | 3090 | 45 | 0.769845563 | 0 |
| igreja-domestica | PDF | 2 | 0 | 7 | 532 | 31 | 2.098640619 | 0 |
| novena | PNG | 23 | 23 | — | 0 | 0 | — | 0 |
| novena | PDF | 3 | 3 | 23 | 0 | 0 | — | 0 |
| para-rezar | PNG | 3 | 3 | — | 0 | 0 | — | 0 |
| para-rezar | PDF | 2 | 2 | 3 | 0 | 0 | — | 0 |
| santo-do-dia | PNG | 6 | 3 | — | 3337 | 45 | 1.282620103 | 0 |
| santo-do-dia | PDF | 3 | 0 | 3 | 491 | 32 | 2.098640619 | 0 |
| stories | PNG | 10 | 2 | — | 12448 | 43 | 0.769845563 | 0 |
| stories | PDF | 4 | 0 | 8 | 2108 | 32 | 2.098619040 | 0 |
| teste-canva | PNG | 0 | 0 | — | 0 | 0 | — | 0 |
| teste-canva | PDF | 2 | 2 | 16 | 0 | 0 | — | 0 |

Total: 150 PNGs e 36 PDFs, com 115 páginas renderizadas a 2×.

## Posições das maiores distâncias por série e modalidade

| Série | Tipo | Arquivo e página | Posição do pixel (x, y) | Distância no raster |
| --- | --- | --- | --- | ---: |
| componentes | PNG | previas/nichos.png | (1721, 158) | 0.884076621 |
| componentes | PDF | canva/teste-importacao.pdf · página1 | (450, 378) | 1.590213407 |
| coragem | PNG | coragem/2026-12-14/status.png | (759, 407) | 0.825183372 |
| coragem | PDF | coragem/2026-12-14/coragem-2026-12-14-feed.pdf · página1 | (1126, 385) | 2.098640619 |
| evangelho | PNG | evangelho/2026-11-29/card-1.png | (706, 196) | 0.820843801 |
| evangelho | PDF | evangelho/2026-11-29/evangelho-2026-11-29.pdf · página1 | (450, 378) | 1.590213407 |
| igreja-domestica | PNG | igreja-domestica/2026-11-29/card-1.png | (489, 155) | 0.769845563 |
| igreja-domestica | PDF | igreja-domestica/2026-11-29/igreja-domestica-2026-11-29.pdf · página1 | (1126, 361) | 2.098640619 |
| santo-do-dia | PNG | santo-do-dia/2026-11-30/card.png | (637, 311) | 1.282620103 |
| santo-do-dia | PDF | santo-do-dia/2026-12-08/santo-2026-12-08.pdf · página1 | (1126, 361) | 2.098640619 |
| stories | PNG | stories/advento/angelus.png | (489, 331) | 0.769845563 |
| stories | PDF | stories/advento/stories-advento.pdf · página1 | (1126, 625) | 2.098619040 |

## Pranchas excluídas da comparação

| Imagem reduzida | Tratamento | Bytes idênticos ao baseline |
| --- | --- | --- |
| coragem/prancha.png | Prancha regenerada a partir dos cards atuais | não; regenerada |
| evangelho/prancha-cores.png | Prancha regenerada a partir dos cards atuais | não; regenerada |
| evangelho/prancha.png | Prancha regenerada a partir dos cards atuais | não; regenerada |
| igreja-domestica/prancha.png | Prancha regenerada a partir dos cards atuais | não; regenerada |
| novena/imaculada/prancha.png | Registro anterior preservado byte a byte | sim |
| novena/natal/prancha.png | Registro anterior preservado byte a byte | sim |
| novena/teste-canva/prancha.png | Registro anterior preservado byte a byte | sim |
| para-rezar/prancha.png | Registro anterior preservado byte a byte | sim |
| santo-do-dia/prancha.png | Prancha regenerada a partir dos cards atuais | não; regenerada |
| stories/prancha.png | Prancha regenerada a partir dos cards atuais | não; regenerada |
| teste-canva/prancha.png | Registro anterior preservado byte a byte | sim |

Os seis índices das séries com nicho foram regenerados. As três pranchas da Novena, a prancha de Para Rezar e a prancha histórica de teste-canva foram preservadas junto com esses registros. Os recortes das obras originais continuam incluídos na comparação de pixels.

## Fichas

66 entradas do nicho foram conferidas. x, y, width, height, hex e token são preservados.

- nicho-filete: campos alterados: border_bottom_px, border_left_px, border_radius_px, border_right_px, border_top_px, font_family, font_size_px, font_style, font_weight, host, kind, letter_spacing_em, letter_spacing_px, letter_spacing_thousandths_em, line_height_multiple, line_height_px, measurement, pseudo, source.

Os valores anteriores e atuais dos campos alterados estão na evidência JSON. As imagens originais, todos os YAMLs, o ZIP e os 44 arquivos do kit permanecem preservados. Novena e Para Rezar não foram regenerados e continuam idênticos byte a byte.

194 testes passaram.

Pendente: teste de importação no Canva dos dois PDFs de 30/11 e 10/12.

Evidência: [conferencia-prompt12.json](conferencia-prompt12.json).
