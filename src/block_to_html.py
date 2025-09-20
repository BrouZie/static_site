import re

from converter import text_node_to_html_node
from htmlnode import LeafNode, ParentNode
from inline import text_to_textnodes
from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks

md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.
After a while `this is code`
This is image ![image](https://i.imgur.com/zjjcJKZ.png) and a link [link](https://google.com)

- This is the first list item in a list block
- This is a list item
- This is another list item

1. This is first ordered in list
2. This is second ordered in list
3. This is third ordered in list

```
# this is a code block
print("Hello suckers")
```

> some insightful quote
> this is also a quote
> should still be a quote
"""
md_ulist = """- This is the first list item in a list block
- This is a list item
- This is another list item
"""
md_code = """
```
# this is a code block
print("Hello suckers")
```
"""

md_olist = """1. This is the first list item in a list block
2. This is a **list** item
3. This is another list item
"""


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
            block_nodes.append(ParentNode("p", _text_to_children(block)))

        elif btype == BlockType.HEADING:
            # match 1–6 #'s then space, capture level and text
            if (m := re.match(r"^(#{1,6})\s+(.*)$", block)) is None:
                raise ValueError("Invalid regex value")

            level = len(m.group(1))
            content = m.group(2)
            block_nodes.append(ParentNode(f"h{level}", _text_to_children(content)))

        elif btype == BlockType.CODE:
            inner = block[3:3]

            if inner.startswith("\n"):
                inner = inner[1:]
            block_nodes.append(ParentNode("pre", [LeafNode("code", inner)]))

        elif btype == BlockType.QUOTE:
            lines = []
            for line in block.split("\n"):
                if line.startswith("< "):
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
