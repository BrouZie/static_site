import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_type(self):
        node = TextNode("This is a text node ", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node ", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("text", TextType.TEXT, "hello")
        node2 = TextNode("text", TextType.TEXT, "hello")
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode(
            "text",
            TextType.TEXT,
        )
        url = node.url
        node2 = TextNode(
            "text",
            TextType.TEXT,
        )
        url2 = node2.url
        self.assertEqual(url, url2)


if __name__ == "__main__":
    unittest.main()
