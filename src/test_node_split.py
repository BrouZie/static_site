import unittest

from split_nodes import split_nodes_delimiter, split_nodes_link, split_nodes_image
from textnode import TextNode, TextType
from inline import text_to_textnodes
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from block_to_html import markdown_to_html_node


class TestNodeSplit(unittest.TestCase):
    def test_code_single(self):
        node = TextNode("This is `code` here", TextType.TEXT)
        out = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [
                ("This is ", TextType.TEXT),
                ("code", TextType.CODE),
                (" here", TextType.TEXT),
            ],
        )

    def test_code_multiple(self):
        node = TextNode("a `x` and `y`.", TextType.TEXT)
        out = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual([n.text for n in out], ["a ", "x", " and ", "y", "."])

    def test_italic_underscore(self):
        node = TextNode("pre _ital_ post", TextType.TEXT)
        out = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [
                ("pre ", TextType.TEXT),
                ("ital", TextType.ITALIC),
                (" post", TextType.TEXT),
            ],
        )

    def test_no_delimiter_unchanged(self):
        node = TextNode("plain text", TextType.TEXT)
        out = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].text, "plain text")
        self.assertIs(out[0].text_type, TextType.TEXT)

    def test_unmatched_raises(self):
        node = TextNode("oops `no close", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_pass_through_non_text(self):
        link = TextNode("Boot", TextType.LINK, "https://boot.dev")
        out = split_nodes_delimiter([link], "`", TextType.CODE)
        self.assertIs(out[0], link)  # same object, unchanged

    """
    Tests for image and link node splitting
    """

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is a LINK [link](https://bitches.com) - Meet the sweetest bitches!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a LINK ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://bitches.com"),
                TextNode(" - Meet the sweetest bitches!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT, None),
                TextNode("text", TextType.BOLD, None),
                TextNode(" with an ", TextType.TEXT, None),
                TextNode("italic", TextType.ITALIC, None),
                TextNode(" word and a ", TextType.TEXT, None),
                TextNode("code block", TextType.CODE, None),
                TextNode(" and an ", TextType.TEXT, None),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT, None),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

        """
        Tests for markdown block splitting
        """

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_block_types(self):
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
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.HEADING)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[2]), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(blocks[3]), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(blocks[4]), BlockType.CODE)
        self.assertEqual(block_to_block_type(blocks[5]), BlockType.QUOTE)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
