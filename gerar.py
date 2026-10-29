#!/usr/bin/env python3
"""CLI do gerador Arte que Reza. Não altera o kit exportado."""
from __future__ import annotations

import argparse
from datetime import date
import importlib.util
import os
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parent


def dependencies() -> None:
    required = {"playwright": "playwright", "picosvg": "picosvg", "fontTools": "fonttools", "PIL": "Pillow", "pypdf": "pypdf", "fitz": "PyMuPDF", "yaml": "PyYAML"}
    missing = [package for module, package in required.items() if importlib.util.find_spec(module) is None]
    if missing:
        local_python = ROOT / ".venv/bin/python"
        if local_python.exists() and Path(sys.prefix) != ROOT / ".venv":
            os.execv(str(local_python), [str(local_python), str(Path(__file__).resolve()), *sys.argv[1:]])
        raise SystemExit("Dependências ausentes: " + ", ".join(missing) + ". Instale requirements.txt; nenhuma ferramenta será substituída.")


def ensure_kit() -> None:
    """Extraia apenas arquivos ausentes e recuse diferenças na fonte da verdade."""
    with zipfile.ZipFile(ROOT / "kit-arte-que-reza.zip") as archive:
        if archive.testzip() is not None:
            raise RuntimeError("O ZIP do kit falhou na verificação de integridade.")
        entries = archive.infolist()
        names = [item.filename for item in entries]
        if len(set(names)) != len(names):
            raise RuntimeError("O ZIP contém caminhos repetidos.")
        files = [item for item in entries if not item.is_dir()]
        if len(files) != 44 or not {"kit/logos/logo-horizontal-sobre-cor.svg", "kit/design-system/componentes/PostFesta/preview.html", "kit/design-system/componentes/PostFesta/README.md"}.issubset(names):
            raise RuntimeError("É necessário o kit versão 4, com 44 arquivos e o modelo PostFesta.")
        readme = archive.read("kit/LEIA-ME.md").decode("utf-8")
        if not readme.startswith("# Kit Arte que Reza · versão 4\n"):
            raise RuntimeError("O LEIA-ME do kit não identifica a versão 4.")
        changes = readme.split("## O que mudou desde a versão 3", 1)
        if len(changes) != 2 or "Nicho" not in changes[1].split("\n## ", 1)[0]:
            raise RuntimeError("Kit v4 antigo: falta a mudança do Nicho no LEIA-ME. Use a versão 4 final.")
        for item in entries:
            path = Path(item.filename)
            if path.is_absolute() or ".." in path.parts or path.parts[0] != "kit" or "\\" in item.filename or ((item.external_attr >> 16) & 0o170000) == 0o120000:
                raise RuntimeError(f"Caminho não permitido no kit: {item.filename}")
            target = ROOT / path
            if target.is_symlink() or not target.resolve().is_relative_to(ROOT):
                raise RuntimeError(f"Link não permitido no kit: {item.filename}")
            if not item.is_dir() and target.exists() and target.read_bytes() != archive.read(item):
                raise RuntimeError(f"O arquivo {item.filename} difere do ZIP. O gerador não sobrescreve o kit.")
        extras = {p.relative_to(ROOT).as_posix() for p in (ROOT / "kit").rglob("*") if p.is_file()} - set(names)
        if extras:
            raise RuntimeError("Arquivos fora do kit versão 4: " + ", ".join(sorted(extras)))
        for item in entries:
            target = ROOT / item.filename
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            elif not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(item))


def main() -> None:
    parser = argparse.ArgumentParser(description="Gere as séries e stories, preservando kit/.")
    parser.add_argument("alvo", choices=["componentes", "evangelho", "santo", "para-rezar", "coragem", "stories"])
    parser.add_argument("--data", help="Gere só a data ISO informada nas séries de feed.")
    parser.add_argument("--tempo", help="Gere só o tempo litúrgico informado (stories), por exemplo advento.")
    args = parser.parse_args()
    if args.tempo is not None and args.alvo != "stories":
        parser.error("--tempo só vale para stories.")
    if args.data is not None:
        if args.alvo in {"componentes", "stories"}:
            parser.error("--data só vale para evangelho, santo, para-rezar ou coragem.")
        try:
            if date.fromisoformat(args.data).isoformat() != args.data:
                raise ValueError
        except ValueError:
            parser.error("--data deve estar no formato AAAA-MM-DD.")
    dependencies()
    try:
        ensure_kit()
        if args.alvo == "stories":
            from arteque_reza.stories import generate
            result = generate(ROOT / "saida", ROOT / "conteudo/stories.yaml", args.tempo)
            print("Pronto: stories gerados.")
            if result.get('obras_pendentes'):
                print("Obras pendentes: " + ", ".join(result['obras_pendentes']))
            print(f"Relatório: {ROOT / 'saida/stories/RELATORIO.md'}")
            return
        if args.alvo != "componentes":
            if args.alvo == "evangelho":
                from arteque_reza.evangelho import generate
                content = "evangelho"
            elif args.alvo == "santo":
                from arteque_reza.santo import generate
                content = "santo-do-dia"
            elif args.alvo == "para-rezar":
                from arteque_reza.para_rezar import generate
                content = "para-rezar"
            else:
                from arteque_reza.coragem import generate
                content = "coragem"
            result = generate(ROOT / "saida", ROOT / f"conteudo/{content}.yaml", args.data)
            print(f"Pronto: {result['dias']} dia(s), {result['cards']} cards, {result['pdfs']} PDF(s) e {result['pngs']} PNGs.")
            if result['obras_pendentes']:
                print("Obras pendentes: " + ", ".join(result['obras_pendentes']))
            print(f"Relatório: {ROOT / f'saida/{content}/RELATORIO.md'}")
            return
        from arteque_reza.renderizacao import generate
        result = generate(ROOT / "saida")
    except Exception as error:
        raise SystemExit(f"Geração interrompida: {error}") from error
    print(f"Pronto: {result['pngs']} PNGs, {result['svgs']} SVGs e PDF de três páginas.")
    print("Validações: dimensões, fontes, texto do PDF, pixels dos arcos e regras dos SVGs.")
    print(f"Relatório: {ROOT / 'saida/RELATORIO.md'}")


if __name__ == "__main__":
    main()
