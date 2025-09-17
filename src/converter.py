from textnode import TextType, TextNode
from htmlnode import LeafNode

def text_node_to_html_node(tn: TextNode):
    match tn.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=tn.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=tn.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=tn.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=tn.text)
        case TextType.LINK if tn.url is not None:
            return LeafNode(tag="a", value=tn.text, props={"href": tn.url})
        case TextType.IMAGE if tn.url is not None:
            return LeafNode("img", "", {"src": tn.url, "alt": tn.text})
        case _:
            raise ValueError("Unsupported or missing data for TextNode")
