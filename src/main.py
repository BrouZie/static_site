from textnode import TextNode, TextType

def main():
    node1 = TextNode("First node", TextType.BOLD, "~/workspace/boot_dev/static_site/src/text.py")
    node2 = TextNode("Sub header or something", TextType.ITALIC, "~/workspace/boot_dev/static_site/src/text.py")
    node3 = TextNode("Link to this cool thing", TextType.LINK, "~/workspace/boot_dev/static_site/src/text.py")
    print(node1)
    print(node2)
    print(node3)
    print(node1.text_type)

if __name__ == "__main__":
    main()
