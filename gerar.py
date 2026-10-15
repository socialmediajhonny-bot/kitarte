#!/usr/bin/env python3
"""CLI do gerador Arte que Reza. Não altera o kit exportado."""
from __future__ import annotations

import argparse
import importlib.util
import os
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parent


def dependencies() -> None:
    required = {"playwright": "playwright", "picosvg": "picosvg", "fontTools": "fonttools", "PIL": "Pillow", "pypdf": "pypdf", "fitz": "PyMuPDF"}
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
        for item in entries:
            path = Path(item.filename)
            if path.is_absolute() or ".." in path.parts or path.parts[0] != "kit" or "\\" in item.filename or ((item.external_attr >> 16) & 0o170000) == 0o120000:
                raise RuntimeError(f"Caminho não permitido no kit: {item.filename}")
            target = ROOT / path
            if target.is_symlink() or not target.resolve().is_relative_to(ROOT):
                raise RuntimeError(f"Link não permitido no kit: {item.filename}")
            if not item.is_dir() and target.exists() and target.read_bytes() != archive.read(item):
                raise RuntimeError(f"O arquivo {item.filename} difere do ZIP. O gerador não sobrescreve o kit.")
        for item in entries:
            target = ROOT / item.filename
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            elif not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(item))


def main() -> None:
    parser = argparse.ArgumentParser(description="Gere componentes e elementos do Canva, preservando kit/.")
    parser.add_argument("alvo", choices=["componentes"])
    parser.parse_args()
    dependencies()
    ensure_kit()
    from arteque_reza.renderizacao import generate
    try:
        result = generate(ROOT / "saida")
    except Exception as error:
        raise SystemExit(f"Geração interrompida: {error}") from error
    print(f"Pronto: {result['pngs']} PNGs, {result['svgs']} SVGs e PDF de três páginas.")
    print("Validações: dimensões, fontes, texto do PDF, pixels dos arcos e regras dos SVGs.")
    print(f"Relatório: {ROOT / 'saida/RELATORIO.md'}")


if __name__ == "__main__":
    main()
