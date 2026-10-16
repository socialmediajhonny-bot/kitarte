# Arte que Reza — componentes e Evangelho do Dia

Gera Selo, Nicho e Assinatura, prévias PNG, SVGs para Canva, PDF de prova e ficha técnica a partir do ZIP do kit. O conteúdo de `kit/` é extraído sem alterações e conferido contra o arquivo do commit. Nenhum recurso externo é carregado durante os renders.

O kit versão 2 tem 42 arquivos, incluindo o logo horizontal inteiramente em `sobre-cor`. O comando `evangelho` reaproveita essa base para gerar carrosséis a partir de `conteudo/evangelho.yaml`.

## Uso neste ambiente

```bash
python gerar.py componentes
python gerar.py evangelho
python gerar.py evangelho --data 2026-11-29
```

O comando usa automaticamente `.venv` se uma dependência não estiver no Python atual. As saídas ficam em `saida/`, com as evidências em `saida/verificacao/resultados.json` e as decisões em `saida/RELATORIO.md`.

## Conteúdo do Evangelho

Edite somente `conteudo/evangelho.yaml` e os arquivos locais em `obras/`. A referência do kit permanece intacta em `kit/`. Cada data gera `saida/evangelho/<data>/evangelho-<data>.pdf`, os PNGs de 1080 × 1350 e `ficha.json` com linhas e medidas reais do navegador. As pranchas e o relatório ficam em `saida/evangelho/`.

Domingos exigem reflexão e geram quatro cards. Sem reflexão são três cards; reflexão em dia de semana emite aviso. Campos desconhecidos, conteúdo inválido, texto acima do limite ou falha nas verificações interrompem a geração. As quebras manuais são preservadas, e palavras de uma letra ficam ligadas à palavra seguinte.

As cores aceitas são `verde`, `roxo`, `ouro` (ou `branco`), `vermelho` e `rosa`. `celebracao` e `obra.pagina` são metadados do relatório, sem aparecer nos cards. Nenhuma obra é baixada: quando `obra.arquivo` não existe, usa-se `saida/obra-provisoria.png`, com indicação de obra pendente. Uma obra local real também gera `recorte.png` para ajustar o foco do arco.

O PDF mantém texto e fontes embutidas para importar um carrossel como um design no Canva. A conferência no editor do Canva continua necessária para avaliar o resultado da importação.

O filtro `--data` preserva os arquivos das outras datas. A prancha geral inclui todas as datas já geradas; a prancha de cores sempre usa o conteúdo de 29/11. As variantes de cor ficam em `work/`, sem substituir os cards finais.

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
