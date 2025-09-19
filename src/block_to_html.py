from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import LeafNode

md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

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
>> this is also a quote
>>> should still be a quote
"""


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            node = LeafNode(tag="p", value=block)
            return node.to_html()


print(markdown_to_html_node(md))
