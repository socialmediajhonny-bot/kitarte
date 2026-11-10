# Arte que Reza — componentes e séries diárias

Gera Selo, Nicho e Assinatura, prévias PNG, SVGs para Canva, PDF de prova e ficha técnica a partir do ZIP do kit. O conteúdo de `kit/` é extraído sem alterações e conferido contra o arquivo do commit. Nenhum recurso externo é carregado durante os renders.

O kit versão 4 final tem 44 arquivos e precisa citar o Nicho no LEIA-ME. Tokens, CSS, logos e fontes continuam idênticos aos da versão 3. Os comandos das séries e stories usam o leitor estrito de YAML, as peças compartilhadas e a mesma receita de PDF. Não edite `kit/`; extraia novamente o ZIP quando atualizar a versão.

## Uso neste ambiente

```bash
python gerar.py componentes
python gerar.py evangelho
python gerar.py evangelho --data 2026-11-29
python gerar.py santo
python gerar.py santo --data 2026-12-08
python gerar.py para-rezar
python gerar.py para-rezar --data 2026-12-15
python gerar.py coragem
python gerar.py coragem --data 2026-12-14
python gerar.py stories
python gerar.py stories --tempo advento
python gerar.py novena --teste-canva
python gerar.py igreja-domestica
python gerar.py igreja-domestica --data 2026-11-29
```

O comando usa automaticamente `.venv` se uma dependência não estiver no Python atual. As saídas ficam em `saida/`, com as evidências em `saida/verificacao/resultados.json` e as decisões em `saida/RELATORIO.md`.

## Conteúdo do Evangelho

Edite somente `conteudo/evangelho.yaml` e os arquivos locais em `obras/`. A referência do kit permanece intacta em `kit/`. Cada data gera `saida/evangelho/<data>/evangelho-<data>.pdf`, os PNGs de 1080 × 1350 e `ficha.json` com linhas e medidas reais do navegador. As pranchas e o relatório ficam em `saida/evangelho/`.

Domingos exigem reflexão e geram quatro cards. Sem reflexão são três cards; reflexão em dia de semana emite aviso. Campos desconhecidos, conteúdo inválido, texto acima do limite ou falha nas verificações interrompem a geração. As quebras manuais são preservadas, e palavras de uma letra ficam ligadas à palavra seguinte.

O Lote 1 acrescenta os treze carrosséis de 30/11 a 12/12/2026: doze dias de semana com três cards e o domingo de 6/12 com quatro. Os trechos foram tirados da Liturgia Diária da CNBB e aprovados em 05/11/2026; pontuação, acentos e quebras manuais foram preservados, assim como o conteúdo de 29/11 e 13/12.

O Lote 3 acrescenta os dezoito carrosséis de 14 a 31/12/2026, com trechos retirados da Liturgia Diária da CNBB e aprovados em 09/11/2026. São dezesseis dias com três cards e os domingos 20 e 27/12 com quatro; o Natal de 25/12 não recebe reflexão.

Somente `referencia` pode terminar com um espaço e o nome de uma das quatro missas do Natal: `(Missa da vigília)`, `(Missa da noite)`, `(Missa da aurora)` ou `(Missa do dia)`. Esse nome também aparece no convite, com a referência inteira em negrito; `trecho_ref` continua sem sufixo.

Uma obra com borda do museu é aceita quando a borda fica fora do arco no foco e zoom aprovados. As imagens originais são preservadas; um teste próprio registra as margens e faixas descartadas e exige ausência de margem visível nos enquadramentos do lote. Cada data recebe sua prova de recorte.

As cores aceitas são `verde`, `roxo`, `ouro` (ou `branco`), `vermelho` e `rosa`. `celebracao` e `obra.pagina` são metadados do relatório, sem aparecer nos cards. Nenhuma obra é baixada: quando `obra.arquivo` não existe, usa-se `saida/obra-provisoria.png`, com indicação de obra pendente. Uma obra local real também gera `recorte.png` para ajustar o foco do arco.

O PDF mantém texto e fontes embutidas para importar um carrossel como um design no Canva. Nos cards 2, 3 e 4, o gerador aplica margens inline em tokens: 32 px entre o texto e a referência e 48 px entre o rótulo e o texto, para o Canva importar cada um em sua caixa (teste de 29/10/2026). O bloco permanece centralizado entre o selo e o logo. A validação mede esses pares no navegador e interrompe a geração se diferirem mais de 0,01 px.

O filete do nicho é um único caminho vetorial preenchido em forma de U, para o Canva importá-lo como forma. A borda CSS arredondada anterior chegava ao Canva como imagem e podia incorporar o parapeito. A obra mantém seu recorte CSS; o parapeito continua sendo um retângulo separado. Em cada PDF com nicho, PyMuPDF exige um preenchimento curvo na caixa e na cor do filete, ausência da assinatura antiga feita apenas de retângulos recortados e um parapeito retangular separado de 3 px. Falhas interrompem a geração e ficam registradas em `nicho_vetorial`, na verificação do PDF e no relatório da série. O gerador aplica essa mudança sem editar o kit ou seu ZIP.

A comparação do prompt 12 aceita diferenças de antialiasing de qualquer intensidade somente na faixa de 2 px do contorno do filete nos cards PNG e de 4 px nos PDFs rasterizados por PyMuPDF a 2×. Fora dessas faixas, a diferença precisa ser zero. Pranchas e imagens reduzidas a partir dos cards são regeneradas e ficam fora da comparação pixel a pixel; os registros históricos protegidos permanecem intactos. A tabela por série, as maiores distâncias e a prova estão no relatório do Evangelho.

O filtro `--data` preserva os arquivos das outras datas. A prancha geral inclui todas as datas já geradas; a prancha de cores sempre usa o conteúdo de 29/11. As variantes de cor ficam em `work/`, sem substituir os cards finais.

## Conteúdo do Santo do Dia

`conteudo/santo-do-dia.yaml` escolhe entre `santinho` e `festa`, cada um com seus campos obrigatórios. Domingos, campos desconhecidos ou ausentes são erros. O santinho usa nome, título, frase sem aspas e fonte; o gerador acrescenta as aspas curvas. O card de festa usa o nome da celebração e a obra, com o grau no selo.

`python gerar.py santo` gera um `card.png` de 1080 × 1350, um `santo-<data>.pdf` de uma página e `ficha.json` por data em `saida/santo-do-dia/`. Cada obra real recebe `recorte.png`, com a imagem inteira a 1080 px de largura e o contorno do que aparece no arco. A prancha mostra os cards lado a lado a 1/3 do tamanho; `--data` preserva as demais datas já geradas.

As obras vêm exclusivamente dos caminhos locais do YAML. O crédito da obra do santinho fica na ficha e no relatório para uso na legenda. A moldura do santinho permanece ouro, inclusive para mártires; a cruz e o filete do nicho seguem a cor litúrgica. Limites de linhas, transbordamento, área interna da moldura e distância ao logo são conferidos no render. A ausência de uma imagem usa a provisória e marca a pendência.

## Foco, zoom e recortes

O bloco `obra` aceita `zoom` opcional, número entre 1 e 3, com padrão 1. A ampliação acontece depois de `object-fit: cover`, com a origem e o `object-position` no `foco`. A moldura e o arco permanecem fixos. As fichas registram a janela visível em pixels da imagem original; o contorno em `recorte.png` usa a mesma geometria.

Uma faixa uniforme é encontrada quando há pelo menos quatro linhas ou colunas inteiras consecutivas a partir da borda com desvio-padrão de cinza menor que 6. Ela só conta como margem da foto se sua média de cinza diferir em pelo menos 10 níveis da média das 16 linhas ou colunas imediatamente interiores. Faixas com diferença menor são parte da pintura e ficam registradas na ficha como descartadas, com lado, largura e diferença. Margens verdadeiras ainda visíveis no enquadramento geram aviso sem interromper a geração. O gerador não modifica o YAML para corrigir o enquadramento.

## Para Rezar e Coragem

`conteudo/para-rezar.yaml` define um card por item de `partes`, sem divisão automática. A intenção vai no primeiro topo; nos seguintes entra a contagem; a origem fica no último card. São permitidas até 10 linhas de oração no primeiro e 14 nos seguintes. Partes não finais precisam terminar com ponto, ponto e vírgula, exclamação ou interrogação. Card único acima de 400 caracteres recebe aviso. O PDF de cada data reúne todos os cards em um único design.

`conteudo/coragem.yaml` gera feed 1080 × 1350 e status 1080 × 1920, com PDFs separados e a assinatura com @. A frase tem até duas linhas, a referência livre tem uma e os afastamentos do nicho e da assinatura precisam ser de pelo menos 32 px. Obras reais geram `recorte-feed.png` e `recorte-status.png`; crédito, foco, zoom e janela ficam na ficha. Se uma margem uniforme aparecer, o relatório sugere foco e zoom sem mudar o conteúdo.

No Coragem, a referência recebe `margin-top: var(--espaco-2)` e fica a 32 px da frase. O bloco continua centralizado entre o nicho e a assinatura, e a validação exige 32 px com tolerância de 0,01 px. A regra aprovada é: 32 px entre o texto e a referência e 48 px entre o rótulo e o texto, para o Canva importar cada um em sua caixa (teste de 29/10/2026).

As saídas ficam em `saida/para-rezar/` e `saida/coragem/`, cada qual com prancha, relatório, verificações e pastas por data. O filtro `--data` preserva os demais dias. As provas da prévia original do Para Rezar e eventuais diferenças de pixels ficam em `work/para-rezar/conferencia-kit/`; o resultado é documentado no relatório.

## Stories por tempo litúrgico

`conteudo/stories.yaml` contém os tempos e os stories fixos do Ângelus às 12h e da Hora da Misericórdia às 15h. O tema capela e a estrutura seguem `StoryAngelus`, com os espaços para o Canva descritos abaixo; entre tempos muda somente a cor da cruz do selo e do filete do nicho. `python gerar.py stories` gera oito PNGs de 1080 × 1920 e um PDF de duas páginas por tempo, na ordem dos stories do YAML.

As saídas ficam em `saida/stories/<tempo>/`, com ficha de texto, obra, foco, zoom, janela original e distâncias. Os recortes das duas obras reais, a prancha de todos os tempos já gerados e o relatório ficam em `saida/stories/`. `--tempo advento` preserva os outros tempos; `--data` não é aceito neste comando. O schema rejeita campos desconhecidos, IDs repetidos ou inseguros, horas fora de `0h` a `23h`, textos vazios e zoom fora de 1 a 3.

Os títulos e subtítulos têm uma linha; a invocação aceita três e a resposta opcional, duas. O bloco segue alinhado ao topo, como no kit, com pelo menos 32 px até a assinatura. A regra de espaços inseparáveis inclui `Ó` e `ó`. Obras acima de 4 MB ou abaixo de 1000 px de largura e PDFs acima de 12 MB recebem aviso; obras ausentes usam a provisória. As notas visuais registram o que aparece no arco e eventuais sugestões sem mudar o YAML.

48 px entre o título e o subtítulo e entre a invocação e a resposta, para o Canva importar cada texto em sua caixa (importação de 29/10/2026). O gerador soma `margin-top: var(--espaco-3)` no subtítulo e na resposta ao `gap` de 16 px do kit. Cada par é medido no navegador e precisa ter 48 px (±0,01). As margens inline do ornamento são redistribuídas entre o topo e a base para conservar sua posição; selo, nicho, obra, título e assinatura também permanecem fixos. A cópia da prévia recebe os mesmos ajustes antes da comparação na origem (0,0), sem editar `kit/`.

| Story · todos os tempos | Título → subtítulo | Invocação → resposta | Último texto → assinatura |
| --- | --- | --- | --- |
| Ângelus | 48 px | 48 px | 63 px |
| Hora da Misericórdia | 48 px | — | 37 px |

O teste de importação realizado em 29/10/2026 e seus PDFs originais ficam registrados em [saida/teste-canva/LEIA-ME.md](saida/teste-canva/LEIA-ME.md); o comando experimental `teste-canva` foi retirado após a aprovação dos espaços.

Os testes verificam o schema e os limites medidos no Chromium, incluindo linhas vazias, transbordamento e a troca do tamanho do versículo na mesma página:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

## Novenas

`conteudo/novenas.yaml` contém a Novena da Imaculada e a Novena de Natal: nove dias consecutivos e o encerramento no dia seguinte. As orações foram escritas pela página e aprovadas em 03/11/2026. O leitor preserva esses textos, exige fonte nos nove dias e limita cada oração a 240 caracteres, sem contar o refrão.

Nesta rodada, execute `python gerar.py novena --teste-canva`: os 20 cards são renderizados e validados somente em `work/novena/`, e `saida/novena/teste-canva/` recebe os dias 1 e 8 e o encerramento da Imaculada, reunidos em um PDF de três páginas, com PNGs, prancha e ficha. O relatório da série registra as medidas dos 20 e o que conferir no Canva. Os arquivos corrigidos dos stories e as outras séries são preservados.

O modelo `PostNovena` usa feed 1080 × 1350 e o bloco centralizado entre selo e assinatura. A cruz permanece roxa nos nove dias de cada novena, inclusive nas festas de 30/11, 3/12 e 7/12. As nove contas mostram o progresso: as do dia 1 até o dia N ficam cheias, e as restantes, vazadas. A oração e o refrão formam um único parágrafo com entrelinha de 62 px; o refrão começa em linha própria, em itálico, e preserva suas quebras. Palavras com hífen ficam inteiras. Espaços de 48 px acima do título e de 32 px abaixo dele separam as caixas para o Canva, sem alterar o kit.

O encerramento ocupa o cartão inteiro em ouro, com textos, cruz, contas cheias e logo em `sobre-cor`. Ele usa o refrão da novena ou o campo `final` quando houver; a fonte é opcional.

Depois da conferência da importação no Canva, `python gerar.py novena` gera as duas novenas completas em `saida/novena/imaculada/` e `saida/novena/natal/`, com dez PNGs e um PDF de dez páginas por novena. `python gerar.py novena --novena imaculada` e `--novena natal` filtram a série; `--teste-canva` aceita a Imaculada e não combina com o filtro de Natal. Esses comandos finais não fazem parte da geração desta rodada.

## Igreja Doméstica

`conteudo/igreja-domestica.yaml` define carrosséis de domingo para pais e casais rezarem em casa. Os textos foram escritos pela página e aprovados em 03/11/2026. `python gerar.py igreja-domestica` gera as duas datas; `--data AAAA-MM-DD` filtra uma delas e preserva as outras já geradas.

Cada carrossel tem de dois a cinco cards: uma capa com obra, crédito, título e apoio; passos opcionais com itens numerados; oração em família com rubricas, oração e aclamação na ordem do YAML; e conversa opcional, sempre no final, com o cartão inteiro na cor indicada. A capa segue alinhada abaixo do selo; os blocos dos cards de texto ficam centralizados entre o selo e a assinatura. Os espaços de 48 px entre instrução e texto e de 32 px até a fonte são medidos no navegador.

As regras de texto desta série preservam as palavras com hífen, mantêm a referência bíblica inteira (como `Mc 13,33-37`) e ligam ordinais à palavra seguinte (como `3º domingo`). As duas regras novas são locais à série; o `text_html` compartilhado continua intacto. Quebras manuais são preservadas e as palavras de uma letra seguem a regra já usada nas outras séries.

As obras são lidas dos caminhos locais do YAML, sem downloads. Cada data recebe PNGs, um PDF com os cards na ordem, `ficha.json` e `recorte.png` em `saida/igreja-domestica/<data>/`. A prancha geral mostra cada data numa linha, a 1/3 do tamanho. O relatório traz medidas, notas dos enquadramentos e a lista do que conferir no Canva; obras ausentes usam a provisória e ficam marcadas como pendentes.

## Instalação em outra máquina

Use Python 3.12+, Chromium e Poppler (`pdffonts`/`pdftotext`). Neste ambiente Chromium está em `/usr/bin/chromium`.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
python gerar.py componentes
```

Se faltar acesso à rede ou algum pacote, instale os requisitos indicados antes de gerar. O código não substitui Playwright, Chromium ou picosvg por ferramentas alternativas. As verificações do PDF também usam PyMuPDF para conferir os próprios programas TTF embutidos.

## Reúso

`arteque_reza/base.py` fornece `selo(serie, data, info=None)`, `nicho(largura, altura, obra)`, `assinatura(tema, arroba=False, curta=False)`, `montar_arte(...)`, `html_document(...)`, `await_fonts(page)` e `render_arte(...)`. `renderizacao.local_server()` fornece a origem HTTP local para o Playwright, sem depender de navegação `file://`. Os recursos precisam ficar dentro do projeto.

O CSS de composição é o `bundle.css` original, carregado por referência. `tokens.css` é gerado do JSON e aponta para os TTF locais. Para alterar identidade ou composição do kit, faça a mudança no design system e substitua o ZIP por um novo export; não edite `kit/`.

A pasta `kit/` é derivada do ZIP e ignorada pelo Git. A pasta `saida/` é versionada integralmente para permitir baixar os arquivos gerados pelo GitHub.
