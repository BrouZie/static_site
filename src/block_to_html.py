import re
import textwrap

from converter import text_node_to_html_node
from htmlnode import LeafNode, ParentNode
from inline import text_to_textnodes
from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks

def _text_to_children(text: str):
    text_nodes = text_to_textnodes(text)

    children = []
    for tn in text_nodes:
        child = text_node_to_html_node(tn)
        children.append(child)

    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.PARAGRAPH:
            lines = [ln.strip() for ln in block.split("\n")]
            para_text = " ".join(lines)
            block_nodes.append(ParentNode("p", _text_to_children(para_text)))

        elif btype == BlockType.HEADING:
            # match 1–6 #'s then space, capture level and text
            if (m := re.match(r"^(#{1,6})\s+(.*)$", block)) is None:
                raise ValueError("Invalid regex value")

            level = len(m.group(1))
            content = m.group(2)
            block_nodes.append(ParentNode(f"h{level}", _text_to_children(content)))

        elif btype == BlockType.CODE:
            blk = block.strip()
            inner = blk[3:-3]
            if inner.startswith("\n"):
                inner = inner[1:]
            inner = textwrap.dedent(inner)   # <-- remove common indent
            block_nodes.append(ParentNode("pre", [LeafNode("code", inner)]))

        elif btype == BlockType.QUOTE:
            lines = []
            for line in block.split("\n"):
                if line.startswith("> "):
                    lines.append(line[2:])
                else:
                    lines.append(line[1:])

            content = "\n".join(lines)
            block_nodes.append(ParentNode("blockquote", _text_to_children(content)))

        elif btype == BlockType.UNORDERED_LIST:
            nodes = []
            for line in block.split("\n"):
                item = line[2:]
                nodes.append(ParentNode("li", _text_to_children(item)))
            block_nodes.append(ParentNode("ul", nodes))

        elif btype == BlockType.ORDERED_LIST:
            nodes = []
            for i, line in enumerate(block.split("\n"), start=1):
                prefix = f"{i}. "
                # assume block_to_block_type already validated the prefix
                item_text = line[len(prefix):]
                nodes.append(ParentNode("li", _text_to_children(item_text)))
            block_nodes.append(ParentNode("ol", nodes))

        else:
            raise TypeError("BlockType is not recognized")

    return ParentNode(tag="div", children=block_nodes)
