# Toda Bela

`python3 gerar.py toda-bela`

## Conteúdo e composição

- Os textos foram escritos pela página e aprovados em 12/11/2026. O YAML preserva pontuação, aspas, acentos e quebras manuais; nenhum texto é gerado automaticamente.
- Feed de 1080 × 1350. Os modelos existem apenas no gerador, sem prévia equivalente no kit v4. Nenhum módulo compartilhado ou arquivo do kit é modificado.
- O helper igreja_text_html é importado intacto: protege palavras de uma letra, referências bíblicas inteiras, ordinais ligados à palavra seguinte e palavras com hífen. As quebras do YAML são mantidas.
- O gap de 16 px do aqr-texto recebe margens inline em tokens: 48 px entre rótulo e texto e em volta do ornamento; 32 px entre texto e fonte/referência e entre nicho e crédito. Cada par é medido no navegador com tolerância de ±0,01 px.
- Os cards com obra no alto seguem o selo e deixam pelo menos 32 px entre o último texto e a assinatura. Os demais centralizam o bloco entre selo e assinatura, com pelo menos 60 px de cada lado e diferença de centralização até 0,1 px.
- A cruz e o filete recebem a cor do dia; o ornamento usa ouro. Nos cartões inteiros na cor do dia, fundo na cor litúrgica e textos, cruz, ornamento e logo em sobre-cor.
- A assinatura usa a variante do tema, ou sobre-cor no cartão inteiro na cor. Cores, fontes, caixas, limites de linhas e trechos protegidos são validados no DOM e por pixels.
- Cada nicho recebe um JPEG já recortado na janela visível, qualidade 95 e sem subamostragem de cor, usando LANCZOS e Image.resize com box fracionária. O card e o PDF usam esse arquivo com foco 50% 50% e zoom 1. Isso evita a ampliação que borrou a obra de 25/12 na importação do Canva.
- O recorte mantém a dimensão nativa, limitado a 2× a área interna do nicho, sem ampliar o arquivo. As janelas explícitas exigem dimensão original exata, contenção completa e ampliação de até 1,2. Nenhuma obra original é alterada ou baixada.
- Cada obra recebe uma prova da imagem inteira a 1080 px com o contorno da janela do arco. Margens fotográficas visíveis geram aviso e nunca alteram o YAML.
- PostTodaBela: três cards. Capa e raiz no tema capela; oração em cartão inteiro na cor do dia. A capa traz o info do YAML e os outros cards a contagem 2/3 e 3/3.
- A capa usa nicho 640 × 760, crédito em uma linha e invocação em titulo-capa. Se a invocação quebrar, é renderizada em titulo com até duas linhas; a assinatura continua a pelo menos 32 px. Não há apoio na capa.
- A raiz traz versículo de até três linhas, referência em uma linha, texto de até cinco e fonte em uma. A oração usa citacao-grande em até três linhas, com as quebras manuais do YAML, e convite em uma.

## Tabela medida no navegador

| Data | Card | Tipo | Linhas medidas | Distâncias e folgas medidas | Previsto |
| --- | --- | --- | --- | --- | --- |
| 2026-12-12 | 1 | capa | credito: 1; invocacao: 1 | selo_nicho_px: 32 px; nicho_credito_px: 32 px; credito_invocacao_px: 48 px; invocacao_assinatura_px: 98 px | credito: 1 linhas; invocacao: 1 linhas; selo_nicho_px: 32 px; invocacao_assinatura_px: 98 px |
| 2026-12-12 | 2 | raiz | rotulo: 1; versiculo: 1; referencia: 1; texto: 5; fonte: 1 | selo_texto_px: 219.5 px; texto_assinatura_px: 219.5 px; diferenca_centralizacao_px: 0 px; rotulo_versiculo_px: 48 px; versiculo_referencia_px: 32 px; referencia_ornamento_px: 48 px; ornamento_texto_px: 48 px; texto_fonte_px: 32 px | rotulo: 1 linhas; versiculo: 1 linhas; referencia: 1 linhas; texto: 5 linhas; fonte: 1 linhas; folga_px: 219.5 px |
| 2026-12-12 | 3 | oracao | rotulo: 1; frase: 2; convite: 1 | selo_texto_px: 333.5 px; texto_assinatura_px: 333.5 px; diferenca_centralizacao_px: 0 px; rotulo_frase_px: 48 px; frase_ornamento_px: 48 px; ornamento_convite_px: 48 px | rotulo: 1 linhas; frase: 2 linhas; convite: 1 linhas; folga_px: 333.5 px |

## Diferenças da tabela prevista

Nenhuma diferença.

## Obras, janelas e recortes

### 2026-12-12 · card-1

Sassoferrato · A Virgem em oração · National Gallery, Londres — https://www.nationalgallery.org.uk/paintings/sassoferrato-the-virgin-in-prayer

Original local: `obras/toda-bela/2026-12-12.jpg`. Foco `50% 30%`, zoom `1.08`.

Janela original x=124.481481, y=125.354825, largura=3112.037037, altura=3808.150585 px; ampliação=0.195370.
Arquivo recortado: `saida/toda-bela/2026-12-12/obra-1.jpg`. Prova: `saida/toda-bela/2026-12-12/recorte-1.png`.
Dimensão do JPEG recortado: 1216 × 1488 px.

Margens e faixas detectadas: `{"margens_detectadas": {"topo": 0, "base": 0, "esquerda": 0, "direita": 0}, "faixas_descartadas": [], "margens_visiveis": []}`.

Card 1 final e recorte-1.png, com a obra inteira e o contorno da janela, conferidos visualmente. O rosto de Maria fica inteiro dentro do arco, com testa, olhos, nariz, boca e queixo preservados; a cabeça e o véu também não encontram a curva. As duas mãos em oração permanecem inteiras, incluindo as pontas dos dedos e os punhos. O arco e a base recortam apenas partes laterais e inferiores do manto, sem atingir o rosto ou as mãos pedidos. Não há margem fotográfica visível. O foco aprovado 50% 30%, zoom 1.08, foi mantido; não é necessário sugerir correção para os elementos principais desta capa.

## Avisos e pendências

Nenhum aviso.

## PDF e conferências

Um PDF por data, com todos os cards na ordem do YAML e páginas de 810 × 1012,5 pt. PyMuPDF, pdffonts e pdftotext verificam fontes TTF embutidas e texto integral igual ao YAML. Cada nicho tem o filete em U e o parapeito vetoriais conferidos, inclusive os dois nichos do card 4 do Olhe de Novo.
As fichas registram caixas de cada linha de texto, tema, cores, conteúdos aprovados, janela original, ampliação e arquivo recortado de cada obra. Os renders usam somente recursos e seis fontes locais.

## O que conferir no Canva

- Cada texto na sua caixa: selo, data, contagem ou info, rótulo, título ou pergunta, crédito, texto, fonte, versículo, referência, frase e convite.
- A obra dentro do arco, sem borrão, usando o arquivo já recortado.
- O filete, o parapeito e o ornamento como formas.
- No card 4 de 9/12, os dois nichos lado a lado, com os parapeitos encostados.
- Nenhuma caixa solta, nem contendo só um espaço; conferir que dois textos não foram fundidos.

A importação destes PDFs no editor do Canva permanece uma conferência manual.
A evidência da geração está em [verificacao.json](verificacao.json).

## Árvore

```text
saida/toda-bela/
  2026-12-12/card-1.png
  2026-12-12/card-2.png
  2026-12-12/card-3.png
  2026-12-12/ficha.json
  2026-12-12/obra-1.jpg
  2026-12-12/recorte-1.png
  2026-12-12/toda-bela-2026-12-12.pdf
  NOTAS-DAS-OBRAS.json
  RELATORIO.md
  prancha.png
  verificacao.json
```

<!-- inicio-prova-prompt15 -->
## Prova de preservação do prompt 15

BASE: `109d8c8f6fbb69ab6cae37ce8459658e3f863379`. Nenhum download foi feito nesta execução. As cinco imagens locais têm os tamanhos exigidos; as quatro novas não têm margens fotográficas ou faixas uniformes descartadas.

**Controle inicial:** os oito comandos foram executados na BASE limpa, com `git status` vazio antes de cada um. Cada arquivo modificado foi comparado: PNG por pixel, páginas PDF a 2× por PyMuPDF e JSON/Markdown normalizando apenas a porta local. **Prova após as alterações:** os sete comandos das outras séries foram executados novamente, antes da geração das novas pastas. Nenhum PNG, PDF ou ficha mudou além da porta local prevista. Todos os seus arquivos foram restaurados à BASE.

**Exceções de relatórios, autorizadas pelo usuário:**

| Relatório restaurado e excluído do commit | Evidência |
| --- | --- |
| `saida/RELATORIO.md` | Mesma desatualização e árvore regenerada nas duas execuções, com texto idêntico salvo a porta local. |
| `saida/evangelho/RELATORIO.md` | A regeneração remove o apêndice manual do prompt 14 igualmente na BASE limpa; nenhum PNG/PDF/ficha é alterado além da porta. |
| `saida/santo-do-dia/RELATORIO.md` | Mesma remoção das 72 linhas do apêndice do prompt 13, de 427 para 355 linhas. |

Para cada relatório, o texto gerado com o código novo foi comparado ao texto gerado no controle da BASE limpa; as diferenças são iguais. Os três arquivos foram restaurados byte a byte e ficam fora do commit. Não foi aplicada exceção a outra diferença. Nenhum auxiliar em `work/` integra a entrega.

**Igreja Doméstica:** as duas datas anteriores foram comparadas e restauradas byte a byte, incluindo cards, PDFs, recortes e fichas. As notas dessas datas e os arquivos `CONFERENCIA-PROMPT-10.md` e `conferencia-prompt10.json` foram preservados. Só a data 13/12 e os quatro arquivos gerais autorizados mudam.

**Testes:** 240 testes passaram (105,707 s): 201 anteriores e 39 novos. `test_conteudo_noite.py` acrescenta 17 testes dos leitores estritos, janelas e referências; `test_layout_noite.py` acrescenta 22 testes de layout, cores, PDF, próximos títulos, uma obra e recortes. Na Igreja, apenas os dois testes autorizados foram ajustados para três datas, 12 cards e a cor do dia. O teste de `--data` também demonstrou preservação byte a byte de PNG, PDF e ficha de outra data.

**Escopo:** os módulos compartilhados, o kit, o ZIP e as obras originais permanecem intactos. O uso dos helpers existentes foi conferido pelas importações abaixo; na Igreja, as alterações ficaram limitadas à previsão de 13/12 e à aprovação por data e relatório.

```text
arteque_reza/conteudo_noite.py:8:import yaml
arteque_reza/conteudo_noite.py:10:from .conteudo import (
arteque_reza/conteudo_noite.py:14:from .igreja_domestica import BOOKS
arteque_reza/noite.py:7:import re
arteque_reza/noite.py:8:import shutil
arteque_reza/noite.py:9:import subprocess
arteque_reza/noite.py:14:from .base import PROJECT, assinatura, color, html_document, montar_arte, nicho, selo
arteque_reza/noite.py:15:from .conteudo import color_token, date_label
arteque_reza/noite.py:16:from .evangelho import _measure as measure_evangelho, _ornament, _text
arteque_reza/noite.py:17:from .igreja_domestica import BOOK_PATTERN, igreja_text_html
arteque_reza/noite.py:18:from .obras import artwork_geometry, crop_proof, inspect_artwork, uniform_margins
arteque_reza/noite.py:19:from .pdf_nicho import niches_from_elements, validate_niche_pdf
arteque_reza/noite.py:20:from .validacao import validate_niche_pixels
arteque_reza/serie_noite.py:9:import json
arteque_reza/serie_noite.py:11:import shutil
arteque_reza/serie_noite.py:18:from .base import PROJECT, KIT, color, generate_tokens_css, render_arte
arteque_reza/serie_noite.py:19:from .canva import niche_svg, validate_svg
arteque_reza/serie_noite.py:20:from .conteudo_noite import LOADERS
arteque_reza/serie_noite.py:21:from .noite import (_document, _measure, _pdf_check, _pixels, _validate_layout,
arteque_reza/serie_noite.py:23:from .renderizacao import local_server
arteque_reza/serie_noite.py:24:from .validacao import validate_kit, validate_pngs
```

A prova completa por arquivo PNG e página PDF está no [relatório de Olhe de Novo](../olhe-de-novo/RELATORIO.md).

<!-- fim-prova-prompt15 -->
