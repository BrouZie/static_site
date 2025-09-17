import unittest

from split_nodes import split_nodes_delimiter, split_nodes_link, split_nodes_image
from textnode import TextNode, TextType


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
        node = TextNode("This is a LINK [link](https://bitches.com) - Meet the sweetest bitches!", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                    TextNode("This is a LINK ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://bitches.com"),
                    TextNode(" - Meet the sweetest bitches!", TextType.TEXT)
            ],
            new_nodes,
        )



if __name__ == "__main__":
    unittest.main()
