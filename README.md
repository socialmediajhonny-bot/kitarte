# Arte que Reza — gerador de componentes

Gera Selo, Nicho e Assinatura, prévias PNG, SVGs para Canva, PDF de prova e ficha técnica a partir do ZIP do kit. O conteúdo de `kit/` é extraído sem alterações e conferido contra o arquivo do commit. Nenhum recurso externo é carregado durante os renders.

## Uso neste ambiente

```bash
python gerar.py componentes
```

O comando usa automaticamente `.venv` se uma dependência não estiver no Python atual. As saídas ficam em `saida/`, com as evidências em `saida/verificacao/resultados.json` e as decisões em `saida/RELATORIO.md`.

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
