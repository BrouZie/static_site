import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

props_dict = {
    "href": "https://www.google.com",
    "target": "_blank",
}
node_default = HTMLNode()
node_default2 = HTMLNode()
node3 = HTMLNode(props=props_dict)
node4 = HTMLNode(props=props_dict)


class TestHTMLNode(unittest.TestCase):
    def test_default_props(self):
        props = node_default.props
        props2 = node_default2.props
        self.assertEqual(props, props2)

    def test_not_equal_props(self):
        props = node_default.props
        props2 = node3.props
        self.assertNotEqual(props, props2)

    def test_equal_props(self):
        props = node3.props
        props2 = node4.props
        self.assertEqual(props, props2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "")
        self.assertEqual(node.to_html(), "<a></a>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "this is bold!")
        self.assertEqual(node.to_html(), "<b>this is bold!</b>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        self.assertEqual(
            ParentNode("p", [LeafNode(None, "a"), LeafNode("em", "b")]).to_html(),
            "<p>a<em>b</em></p>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
