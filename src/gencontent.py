import re
from pathlib import Path
import os
from block_to_html import markdown_to_html_node

def generate_pages_recursive(content_dir, template_path, out_dir, basepath="/"):
    for name in os.listdir(content_dir):
        from_path = os.path.join(content_dir, name)
        this_dest = os.path.join(out_dir, name)     # <-- don't overwrite out_dir

        if os.path.isfile(from_path):
            out_html = Path(this_dest).with_suffix(".html")
            generate_page(from_path, template_path, out_html, basepath)
        else:
            generate_pages_recursive(from_path, template_path, this_dest, basepath)

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f" * {from_path} {template_path} -> {dest_path}")

    md = Path(from_path).read_text(encoding="utf8")
    template = Path(template_path).read_text(encoding="utf8")

    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    full = (
        template
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", html)
        .replace('href="/', f'href="{basepath}')   # <-- use basepath
        .replace('src="/',  f'src="{basepath}')
    )

    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(full, encoding="utf8")

def extract_title(markdown: str) -> str:
    if (m := re.search(r"(?m)^# (.+)$", markdown)) is None:
        raise Exception("No header (h1) in file")
    else:
        return m.group(1).strip()
