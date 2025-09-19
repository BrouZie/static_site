import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str):
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("-") for line in lines):
        return BlockType.UNORDERED_LIST

    ok = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            ok = False
            break
    if ok:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    # Normalize Windows newlines
    md = markdown.replace("\r\n", "\n").replace("\r", "\n")
    # Split on blank lines, trim each block, and drop empties
    return [block.strip() for block in md.split("\n\n") if block.strip()]
