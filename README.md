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
python gerar.py teste-canva
```

O comando usa automaticamente `.venv` se uma dependência não estiver no Python atual. As saídas ficam em `saida/`, com as evidências em `saida/verificacao/resultados.json` e as decisões em `saida/RELATORIO.md`.

## Conteúdo do Evangelho

Edite somente `conteudo/evangelho.yaml` e os arquivos locais em `obras/`. A referência do kit permanece intacta em `kit/`. Cada data gera `saida/evangelho/<data>/evangelho-<data>.pdf`, os PNGs de 1080 × 1350 e `ficha.json` com linhas e medidas reais do navegador. As pranchas e o relatório ficam em `saida/evangelho/`.

Domingos exigem reflexão e geram quatro cards. Sem reflexão são três cards; reflexão em dia de semana emite aviso. Campos desconhecidos, conteúdo inválido, texto acima do limite ou falha nas verificações interrompem a geração. As quebras manuais são preservadas, e palavras de uma letra ficam ligadas à palavra seguinte.

As cores aceitas são `verde`, `roxo`, `ouro` (ou `branco`), `vermelho` e `rosa`. `celebracao` e `obra.pagina` são metadados do relatório, sem aparecer nos cards. Nenhuma obra é baixada: quando `obra.arquivo` não existe, usa-se `saida/obra-provisoria.png`, com indicação de obra pendente. Uma obra local real também gera `recorte.png` para ajustar o foco do arco.

O PDF mantém texto e fontes embutidas para importar um carrossel como um design no Canva. A conferência no editor do Canva continua necessária para avaliar o resultado da importação.

O filtro `--data` preserva os arquivos das outras datas. A prancha geral inclui todas as datas já geradas; a prancha de cores sempre usa o conteúdo de 29/11. As variantes de cor ficam em `work/`, sem substituir os cards finais.

## Conteúdo do Santo do Dia

`conteudo/santo-do-dia.yaml` escolhe entre `santinho` e `festa`, cada um com seus campos obrigatórios. Domingos, campos desconhecidos ou ausentes são erros. O santinho usa nome, título, frase sem aspas e fonte; o gerador acrescenta as aspas curvas. O card de festa usa o nome da celebração e a obra, com o grau no selo.

`python gerar.py santo` gera um `card.png` de 1080 × 1350, um `santo-<data>.pdf` de uma página e `ficha.json` por data em `saida/santo-do-dia/`. Cada obra real recebe `recorte.png`, com a imagem inteira a 1080 px de largura e o contorno do que aparece no arco. A prancha mostra os cards lado a lado a 1/3 do tamanho; `--data` preserva as demais datas já geradas.

As obras vêm exclusivamente dos caminhos locais do YAML. O crédito da obra do santinho fica na ficha e no relatório para uso na legenda. A moldura do santinho permanece ouro, inclusive para mártires; a cruz e o filete do nicho seguem a cor litúrgica. Limites de linhas, transbordamento, área interna da moldura e distância ao logo são conferidos no render. A ausência de uma imagem usa a provisória e marca a pendência.

## Foco, zoom e recortes

O bloco `obra` aceita `zoom` opcional, número entre 1 e 3, com padrão 1. A ampliação acontece depois de `object-fit: cover`, com a origem e o `object-position` no `foco`. A moldura e o arco permanecem fixos. As fichas registram a janela visível em pixels da imagem original; o contorno em `recorte.png` usa a mesma geometria.

Uma borda uniforme da foto gera aviso quando ainda aparece no enquadramento: pelo menos quatro linhas ou colunas inteiras consecutivas a partir da borda com desvio-padrão de cinza menor que 6. O aviso não interrompe a geração. O gerador não modifica o YAML para corrigir o enquadramento.

## Para Rezar e Coragem

`conteudo/para-rezar.yaml` define um card por item de `partes`, sem divisão automática. A intenção vai no primeiro topo; nos seguintes entra a contagem; a origem fica no último card. São permitidas até 10 linhas de oração no primeiro e 14 nos seguintes. Partes não finais precisam terminar com ponto, ponto e vírgula, exclamação ou interrogação. Card único acima de 400 caracteres recebe aviso. O PDF de cada data reúne todos os cards em um único design.

`conteudo/coragem.yaml` gera feed 1080 × 1350 e status 1080 × 1920, com PDFs separados e a assinatura com @. A frase tem até duas linhas, a referência livre tem uma e os afastamentos do nicho e da assinatura precisam ser de pelo menos 32 px. Obras reais geram `recorte-feed.png` e `recorte-status.png`; crédito, foco, zoom e janela ficam na ficha. Se uma margem uniforme aparecer, o relatório sugere foco e zoom sem mudar o conteúdo.

As saídas ficam em `saida/para-rezar/` e `saida/coragem/`, cada qual com prancha, relatório, verificações e pastas por data. O filtro `--data` preserva os demais dias. As provas da prévia original do Para Rezar e eventuais diferenças de pixels ficam em `work/para-rezar/conferencia-kit/`; o resultado é documentado no relatório.

## Stories por tempo litúrgico

`conteudo/stories.yaml` contém os tempos e os stories fixos do Ângelus às 12h e da Hora da Misericórdia às 15h. O tema capela e a composição de `StoryAngelus` permanecem iguais; entre tempos muda somente a cor da cruz do selo e do filete do nicho. `python gerar.py stories` gera oito PNGs de 1080 × 1920 e um PDF de duas páginas por tempo, na ordem dos stories do YAML.

As saídas ficam em `saida/stories/<tempo>/`, com ficha de texto, obra, foco, zoom, janela original e distâncias. Os recortes das duas obras reais, a prancha de todos os tempos já gerados e o relatório ficam em `saida/stories/`. `--tempo advento` preserva os outros tempos; `--data` não é aceito neste comando. O schema rejeita campos desconhecidos, IDs repetidos ou inseguros, horas fora de `0h` a `23h`, textos vazios e zoom fora de 1 a 3.

Os títulos e subtítulos têm uma linha; a invocação aceita três e a resposta opcional, duas. O bloco segue alinhado ao topo, como no kit, com pelo menos 32 px até a assinatura. A regra de espaços inseparáveis inclui `Ó` e `ó`. Obras acima de 4 MB ou abaixo de 1000 px de largura e PDFs acima de 12 MB recebem aviso; obras ausentes usam a provisória. As notas visuais registram o que aparece no arco e eventuais sugestões sem mudar o YAML.

## Teste de importação no Canva

`python gerar.py teste-canva` reutiliza os cards 2 e 4 do Evangelho de 29/11 para gerar `saida/teste-canva/teste-canva-a.pdf` (14 páginas, sem marcação) e `teste-canva-b.pdf` (dois controles, marcado). Cada documento sai de uma única chamada de impressão do Chromium; a correção das caixas preserva a estrutura do PDF marcado.

O A compara controle, transparência `opacity:0.999`, giro de `0.5deg` e respiros de 32, 48, 80 e 128 px, alterando somente o estilo inline da referência ou do rótulo. A ficha registra variante e distâncias, e a prancha mostra as páginas do A rasterizadas a 1/4. São conferidos estrutura marcada, transparência em Form XObject, giro, caixas, texto, fontes e identidade visual dos controles.

O comando prepara os arquivos para o teste manual; não os importa nem edita um design no Canva. O `LEIA-ME.md` traz a tabela de páginas e pede a importação dos dois PDFs sem editar nada, para comparar o agrupamento das caixas.

Os testes verificam o schema e os limites medidos no Chromium, incluindo linhas vazias, transbordamento e a troca do tamanho do versículo na mesma página:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

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

A pasta `kit/` é derivada do ZIP e ignorada pelo Git. A pasta `saida/` é versionada integralmente para permitir baixar os arquivos gerados pelo GitHub. A importação e a editabilidade no Canva precisam ser verificadas no editor com `saida/canva/teste-importacao.pdf`.
