# Stories por tempo litúrgico

`python gerar.py stories`

## Composição e decisões

- A composição segue StoryAngelus: tema capela, formato 1080 × 1920, 240 px no topo e na base, selo Para Rezar com a hora e assinatura capela sem @.
- O Nicho 600 × 700 fica a espaco-4 do selo. O bloco de texto fica a espaco-4 do nicho, alinhado ao topo; margin-top:auto não foi aplicado a ele.
- Só a cruz do selo e o filete do nicho recebem a cor do tempo. O ornamento permanece ouro. Os créditos das obras estão nas fichas e não entram na arte.
- Quebras manuais são preservadas e palavras de uma letra, incluindo Ó e ó, ficam ligadas à seguinte. As linhas são medidas com Range, após carregar as seis fontes locais.
- A ordem de stories no YAML é a ordem das páginas. Os recortes são globais porque foco, zoom e imagem são iguais nos quatro tempos. --tempo preserva os outros tempos e a prancha indexa todos os já gerados.

## Linhas e posições

| Tempo | Story | Campo | Linhas | Limite |
| --- | --- | --- | --- | --- |
| advento | angelus | selo | 1 | — |
| advento | angelus | hora | 1 | — |
| advento | angelus | titulo | 1 | 1 |
| advento | angelus | subtitulo | 1 | 1 |
| advento | angelus | invocacao | 1 | 3 |
| advento | angelus | resposta | 1 | 2 |
| advento | misericordia | selo | 1 | — |
| advento | misericordia | hora | 1 | — |
| advento | misericordia | titulo | 1 | 1 |
| advento | misericordia | subtitulo | 1 | 1 |
| advento | misericordia | invocacao | 3 | 3 |
| natal | angelus | selo | 1 | — |
| natal | angelus | hora | 1 | — |
| natal | angelus | titulo | 1 | 1 |
| natal | angelus | subtitulo | 1 | 1 |
| natal | angelus | invocacao | 1 | 3 |
| natal | angelus | resposta | 1 | 2 |
| natal | misericordia | selo | 1 | — |
| natal | misericordia | hora | 1 | — |
| natal | misericordia | titulo | 1 | 1 |
| natal | misericordia | subtitulo | 1 | 1 |
| natal | misericordia | invocacao | 3 | 3 |
| tempo-comum | angelus | selo | 1 | — |
| tempo-comum | angelus | hora | 1 | — |
| tempo-comum | angelus | titulo | 1 | 1 |
| tempo-comum | angelus | subtitulo | 1 | 1 |
| tempo-comum | angelus | invocacao | 1 | 3 |
| tempo-comum | angelus | resposta | 1 | 2 |
| tempo-comum | misericordia | selo | 1 | — |
| tempo-comum | misericordia | hora | 1 | — |
| tempo-comum | misericordia | titulo | 1 | 1 |
| tempo-comum | misericordia | subtitulo | 1 | 1 |
| tempo-comum | misericordia | invocacao | 3 | 3 |
| quaresma | angelus | selo | 1 | — |
| quaresma | angelus | hora | 1 | — |
| quaresma | angelus | titulo | 1 | 1 |
| quaresma | angelus | subtitulo | 1 | 1 |
| quaresma | angelus | invocacao | 1 | 3 |
| quaresma | angelus | resposta | 1 | 2 |
| quaresma | misericordia | selo | 1 | — |
| quaresma | misericordia | hora | 1 | — |
| quaresma | misericordia | titulo | 1 | 1 |
| quaresma | misericordia | subtitulo | 1 | 1 |
| quaresma | misericordia | invocacao | 3 | 3 |

| Tempo | Story | Selo y | Nicho y / base | Título y | Assinatura y | Último texto → assinatura |
| --- | --- | --- | --- | --- | --- | --- |
| advento | angelus | 240 | 328 / 1028 | 1076 | 1628 | 127 px |
| advento | misericordia | 240 | 328 / 1028 | 1076 | 1628 | 69 px |
| natal | angelus | 240 | 328 / 1028 | 1076 | 1628 | 127 px |
| natal | misericordia | 240 | 328 / 1028 | 1076 | 1628 | 69 px |
| tempo-comum | angelus | 240 | 328 / 1028 | 1076 | 1628 | 127 px |
| tempo-comum | misericordia | 240 | 328 / 1028 | 1076 | 1628 | 69 px |
| quaresma | angelus | 240 | 328 / 1028 | 1076 | 1628 | 127 px |
| quaresma | misericordia | 240 | 328 / 1028 | 1076 | 1628 | 69 px |

## Obras, recortes e notas visuais

### angelus

Jan van Eyck · A Anunciação · National Gallery of Art — https://www.nga.gov/artworks/46-annunciation

Obra real local; recorte global gerado.
Foco `50% 55%`, zoom `1.0`; janela original x=0, y=896.938, largura=1137, altura=1369.2 px.

Na obra real desta entrega, o arco com foco 50% 55% mostra os rostos de Gabriel, à esquerda, e de Maria, à direita. O recorte concentra a cena nas duas figuras e deixa partes superiores da arquitetura e inferiores da pintura fora da janela. Os elementos essenciais estão preservados; não foi necessário recomendar outro foco ou zoom.
### misericordia

Eugeniusz Kazimirowski · Jesus Misericordioso · Santuário da Divina Misericórdia, Vilnius — https://en.wikipedia.org/wiki/Divine_Mercy_image

Obra real local; recorte global gerado.
Foco `50% 8%`, zoom `1.15`; janela original x=116.022, y=90.9693, largura=1546.96, altura=1862.88 px.

Na obra real desta entrega, o foco 50% 8% e o zoom 1.15 mantêm na janela o rosto, a auréola, as duas mãos, as mangas e o começo dos raios. As faixas uniformes escuras são parte do fundo da própria pintura; a comparação com as faixas interiores as descarta e não há aviso de margem da foto.

## Conferência da prévia

Prévia do StoryAngelus com o article na origem (0,0), contra tempo-comum/angelus: 0 pixels diferentes fora da janela (256,344)–(824,1028).

## Avisos e pendências

Nenhum aviso.
Obras pendentes: nenhuma.

## PDF e limites

Duas páginas de 810 × 1440 pt por tempo na ordem do YAML. As cinco fontes usadas foram conferidas como TTF embutidos por pdffonts; o texto integral de cada página foi comparado por PyMuPDF e pdftotext -layout, ignorando apenas espaços e quebras.

A importação no editor do Canva não foi executada. Avisos de tamanho acima de 4 MB por obra, largura abaixo de 1000 px ou PDF acima de 12 MB são informativos. Nenhum recurso externo foi baixado.

## Árvore

```text
saida/stories/
  RELATORIO.md
  advento/angelus.png
  advento/ficha.json
  advento/misericordia.png
  advento/stories-advento.pdf
  natal/angelus.png
  natal/ficha.json
  natal/misericordia.png
  natal/stories-natal.pdf
  prancha.png
  quaresma/angelus.png
  quaresma/ficha.json
  quaresma/misericordia.png
  quaresma/stories-quaresma.pdf
  recorte-angelus.png
  recorte-misericordia.png
  tempo-comum/angelus.png
  tempo-comum/ficha.json
  tempo-comum/misericordia.png
  tempo-comum/stories-tempo-comum.pdf
  verificacao.json
```
