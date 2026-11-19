# Stories avulsos

`python gerar.py stories-avulsos`

## Composição

- Textos e obras aprovados pela página em 19/11/2026. Os seis stories usam StoryAngelus, capela, 1080 × 1920, sem laço por tempo litúrgico.
- O selo é serie · apoio; o nicho tem 600 × 700 px. A cruz e o filete seguem a cor do YAML; ornamento ouro e assinatura capela sem @.
- Posições fixas: selo y=240; nicho y=328, base=1028; título y=1076; ornamento y=1286; assinatura y=1628.
- 48 px entre título e subtítulo e, havendo resposta, entre invocação e resposta; mínimo de 32 px do último texto à assinatura. As margens inline mantêm o gap de 16 px do kit.
- Limites: título e subtítulo em uma linha, invocação até três e resposta até duas. Só o nome fixo Antífonas do Ó no selo de uma linha é isento da regra de palavra de uma letra no fim.
- O grupo recebe um PDF com as páginas na ordem do YAML. --grupo preserva os outros grupos e a prancha reúne todos os já gerados.

## Medidas no navegador

| Grupo | Story | Título / subtítulo / invocação / resposta: linhas | Título → subtítulo | Invocação → resposta | Último texto → assinatura | Assinatura y |
| --- | --- | --- | --- | --- | --- | --- |
| terco-2026-12-12 | terco-2026-12-12 | 1 / 1 / 3 / — | 48 | — | 37 | 1628 |
| chave-de-davi-2026-12-20 | chave-de-davi-1 | 1 / 1 / 3 / — | 48 | — | 37 | 1628 |
| chave-de-davi-2026-12-20 | chave-de-davi-2 | 1 / 1 / 3 / — | 48 | — | 37 | 1628 |
| comece-aqui | comece-aqui-1 | 1 / 1 / 3 / — | 48 | — | 37 | 1628 |
| comece-aqui | comece-aqui-2 | 1 / 1 / 3 / — | 48 | — | 37 | 1628 |
| comece-aqui | comece-aqui-3 | 1 / 1 / 3 / — | 48 | — | 37 | 1628 |

## Obras, janelas e notas visuais

### terco-2026-12-12

Bartolomé Esteban Murillo · A Virgem do Rosário · Museu do Prado — https://commons.wikimedia.org/wiki/File:Virgen_del_Rosario_(Murillo).jpg

Original: `obras/stories/terco.jpg`; foco `50% 35%`, zoom `1.15`. Janela x=118.826087, y=283.180863, largura=1584.347826, altura=1907.911819 px; ampliação=0.358507.
Prova do recorte: `terco-2026-12-12/recorte-terco-2026-12-12.png`.
Margens: `{"topo": 0, "base": 0, "esquerda": 0, "direita": 0}`; faixas descartadas: `[{"lado": "base", "largura": 10, "diferenca_cinza": 0.49814077936333945}]`; margens visíveis: `[]`.

Story final e recorte-terco-2026-12-12.png conferidos individualmente. Os rostos de Maria e do Menino, os braços e as mãos, o terço e os pés visíveis do Menino ficam dentro do arco. A curva passa acima dos cabelos e não corta esses elementos. A base recorta a extensão inferior do manto e do assento de Maria; portanto não se afirma que a pintura inteira esteja contida. A faixa escura inferior foi descartada pelo detector como parte da pintura, e não há margem fotográfica visível. O foco 50% 35% e o zoom 1.15 aprovados foram mantidos.
### chave-de-davi-1

Fra Angelico · Cristo desce à mansão dos mortos · Museu de San Marco, Florença — https://commons.wikimedia.org/wiki/File:Fra_Angelico_024.jpg

Original: `obras/stories/chave-de-davi.jpg`; foco `91% 90%`, zoom `1.36`. Janela x=745.851589, y=669.679412, largura=1716.382869, altura=2066.911765 px; ampliação=0.330928.
Prova do recorte: `chave-de-davi-2026-12-20/recorte-chave-de-davi-1.png`.
Margens: `{"topo": 0, "base": 0, "esquerda": 0, "direita": 0}`; faixas descartadas: `[{"lado": "topo", "largura": 19, "diferenca_cinza": 7.976773929105093}]`; margens visíveis: `[]`.

Story final e recorte-chave-de-davi-1.png conferidos individualmente. Cristo e Adão preservam os rostos, as mãos que se encontram, as vestes e os pés na extensão em que aparecem na pintura. A porta derrubada também permanece legível. A parte superior do estandarte e da cruz e alguns personagens do grupo à esquerda ficam parciais ou fora do arco; o demônio e boa parte da arquitetura lateral do original são excluídos. O recorte prioriza o encontro de Cristo com Adão e não contém toda a cena. A faixa superior foi descartada pelo detector; nenhuma margem fotográfica fica visível. Foco 91% 90% e zoom 1.36 mantidos.
### chave-de-davi-2

Fra Angelico · Cristo desce à mansão dos mortos · Museu de San Marco, Florença — https://commons.wikimedia.org/wiki/File:Fra_Angelico_024.jpg

Original: `obras/stories/chave-de-davi.jpg`; foco `91% 90%`, zoom `1.36`. Janela x=745.851589, y=669.679412, largura=1716.382869, altura=2066.911765 px; ampliação=0.330928.
Prova do recorte: `chave-de-davi-2026-12-20/recorte-chave-de-davi-2.png`.
Margens: `{"topo": 0, "base": 0, "esquerda": 0, "direita": 0}`; faixas descartadas: `[{"lado": "topo", "largura": 19, "diferenca_cinza": 7.976773929105093}]`; margens visíveis: `[]`.

O segundo story e recorte-chave-de-davi-2.png foram conferidos individualmente. A obra usa o mesmo enquadramento do primeiro: os rostos, o gesto de Cristo que liberta Adão, as vestes e os pés visíveis e a porta derrubada ficam preservados. O alto do estandarte e da cruz e os personagens periféricos à esquerda continuam parciais ou fora; a cena inteira não cabe nesse detalhe. Nenhuma margem fotográfica visível. O foco 91% 90% e o zoom 1.36 foram mantidos, iguais aos do primeiro story.
### comece-aqui-1

Rogier van der Weyden · São Lucas desenhando a Virgem · Museum of Fine Arts, Boston — https://commons.wikimedia.org/wiki/File:Saint_Luke_Drawing_the_Virgin_MFA_Boston.jpg

Original: `obras/stories/comece-aqui-1.jpg`; foco `50% 60%`, zoom `1`. Janela x=0.000000, y=38.159155, largura=1941.000000, altura=2337.401408 px; ampliação=0.292633.
Prova do recorte: `comece-aqui/recorte-comece-aqui-1.png`.
Margens: `{"topo": 0, "base": 4, "esquerda": 0, "direita": 5}`; faixas descartadas: `[]`; margens visíveis: `["direita"]`.

Story final e recorte-comece-aqui-1.png conferidos individualmente. Os rostos de Maria, do Menino e de São Lucas, as mãos, o gesto de desenhar e os pés visíveis do Menino ficam dentro do arco. A curva recorta o dossel e a arquitetura superior, sem atingir esses protagonistas. O detector registra 5 px de margem fotográfica à direita, incluídos no limite vertical da janela e percebidos como uma faixa escura muito fina junto à direita; a margem de 4 px na base fica fora da janela. O enquadramento aprovado 50% 60%, zoom 1 foi preservado.

Sugestão somente no relatório, sem mudar o YAML: {"foco": "50% 60%", "zoom": 1.01, "janela_original": {"x": 9.608910891089181, "y": 52.044707851066775, "largura": 1921.7821782178216, "altura": 2314.258820248222}, "margens_visiveis": [], "nota": "Alternativa renderizada e inspecionada somente em work: zoom 1.01, mantendo o foco 50% 60%, exclui a margem fotográfica detectada e preserva os três rostos, as mãos, o gesto de desenhar e o Menino. O recorte fica discretamente mais fechado na arquitetura e nos extremos dos mantos; não é uma proposta para incluir a pintura inteira. O detector fica com margens_visiveis vazias. Sugestão apenas no relatório; o YAML e os PNGs/PDFs publicados permanecem com o enquadramento aprovado."}
### comece-aqui-2

Jean-François Millet · O Ângelus · Musée d'Orsay, Paris — https://commons.wikimedia.org/wiki/File:Jean-Fran%C3%A7ois_Millet_-_The_Angelus_-_Google_Art_Project.jpg

Original: `obras/stories/comece-aqui-2.jpg`; foco `50% 50%`, zoom `1`. Janela x=1091.739766, y=0.000000, largura=4869.520468, altura=5864.000000 px; ampliação=0.116644.
Prova do recorte: `comece-aqui/recorte-comece-aqui-2.png`.
Margens: `{"topo": 0, "base": 0, "esquerda": 0, "direita": 0}`; faixas descartadas: `[]`; margens visíveis: `[]`.

Story final e recorte-comece-aqui-2.png conferidos individualmente. Os dois camponeses ficam inteiros na extensão pintada, com cabeças, mãos em oração, vestes e pés preservados dentro do arco. A igreja ao fundo permanece reconhecível. O arco exclui partes laterais do campo e das ferramentas, sem cortar os protagonistas; a iluminação escura dos rostos é a do original. Nenhuma margem fotográfica detectada ou vista. Mantido foco 50% 50%, zoom 1.
### comece-aqui-3

Johannes Vermeer · Cristo na casa de Marta e Maria · National Galleries of Scotland, Edimburgo — https://commons.wikimedia.org/wiki/File:Johannes_(Jan)_Vermeer_-_Christ_in_the_House_of_Martha_and_Mary_-_Google_Art_Project.jpg

Original: `obras/stories/comece-aqui-3.jpg`; foco `40% 45%`, zoom `1`. Janela x=54.612865, y=0.000000, largura=3322.467836, altura=4001.000000 px; ampliação=0.170957.
Prova do recorte: `comece-aqui/recorte-comece-aqui-3.png`.
Margens: `{"topo": 0, "base": 0, "esquerda": 0, "direita": 0}`; faixas descartadas: `[]`; margens visíveis: `[]`.

Story final e recorte-comece-aqui-3.png conferidos individualmente. Os rostos de Cristo, Marta e Maria, as mãos e os gestos centrais, o cesto com o pão e os pés visíveis de Maria ficam dentro do arco. A lateral direita recorta parte do manto de Cristo e da cadeira, e a curva limita o fundo superior; não se afirma que todos os corpos ou a composição inteira estejam integralmente visíveis. Partes encobertas pela mesa e pelas vestes já são assim no original. Nenhuma margem fotográfica detectada ou vista. Foco 40% 45%, zoom 1 mantidos.

## Avisos e pendências

- terco-2026-12-12: obra com 4250021 bytes, acima de 4 MB; o PDF incorpora a imagem inteira.
- comece-aqui-1: margem da foto visível à direita; aumente o zoom
- comece-aqui-2: obra com 7099454 bytes, acima de 4 MB; o PDF incorpora a imagem inteira.
Obras pendentes: nenhuma.

## PDF e Canva

Cada página tem 810 × 1440 pt. PyMuPDF, pdffonts e pdftotext verificam texto integral e fontes TTF embutidas; o filete em U e o parapeito de cada nicho são vetoriais e validados.
A importação no Canva permanece manual: conferir cada texto em sua caixa, a obra dentro do arco, o filete e o parapeito como formas e nenhuma caixa solta ou contendo só um espaço.

## Árvore

```text
saida/stories-avulsos/
  NOTAS-DAS-OBRAS.json
  RELATORIO.md
  chave-de-davi-2026-12-20/chave-de-davi-1.png
  chave-de-davi-2026-12-20/chave-de-davi-2.png
  chave-de-davi-2026-12-20/chave-de-davi-2026-12-20.pdf
  chave-de-davi-2026-12-20/ficha.json
  chave-de-davi-2026-12-20/recorte-chave-de-davi-1.png
  chave-de-davi-2026-12-20/recorte-chave-de-davi-2.png
  comece-aqui/comece-aqui-1.png
  comece-aqui/comece-aqui-2.png
  comece-aqui/comece-aqui-3.png
  comece-aqui/comece-aqui.pdf
  comece-aqui/ficha.json
  comece-aqui/recorte-comece-aqui-1.png
  comece-aqui/recorte-comece-aqui-2.png
  comece-aqui/recorte-comece-aqui-3.png
  prancha.png
  terco-2026-12-12/ficha.json
  terco-2026-12-12/recorte-terco-2026-12-12.png
  terco-2026-12-12/terco-2026-12-12.pdf
  terco-2026-12-12/terco-2026-12-12.png
  verificacao.json
```
