import sys
import os
import shutil
from pathlib import Path
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive


def _normalize_basepath(bp: str | None) -> str:
    if not bp or bp == "/":
        return "/"
    if not bp.startswith("/"):
        bp = "/" + bp
    if not bp.endswith("/"):
        bp = bp + "/"
    return bp


def main() -> None:
    cwd = Path(os.getcwd())
    static_dir = cwd / "static"
    content_dir = cwd / "content"
    template_path = cwd / "template.html"
    docs_dir = cwd / "docs"

    basepath = _normalize_basepath(sys.argv[1] if len(sys.argv) > 1 else "/")

    if docs_dir.exists():
        shutil.rmtree(docs_dir)
    docs_dir.mkdir(parents=True, exist_ok=True)

    copy_files_recursive(static_dir, docs_dir)
    generate_pages_recursive(content_dir, template_path, docs_dir, basepath)


if __name__ == "__main__":
    main()
