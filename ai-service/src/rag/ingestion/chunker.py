import re


def chunk_document(text: str) -> list:
    """
    Split the EU AI Act Markdown into chunks on heading boundaries.

    Docling exports the document as Markdown with ## headings for articles
    and annexes. Each chunk corresponds to one heading section.

    Args:
        text: The EU AI Act as Markdown from Docling (see loader.py).

    Returns:
        A list of dicts with "article" and "text" keys.
    """
    # Split on ## headings that start with Article or ANNEX.
    # Capturing group keeps the heading in the result.
    chunks = re.split(r'(^## (?:Article\s+\d+|ANNEX\s+[IVX]+).*$)', text, flags=re.MULTILINE)

    combined_chunks = []
    for i in range(1, len(chunks), 2):
        heading = chunks[i]
        content = chunks[i + 1] if i + 1 < len(chunks) else ""
        # Strip ## prefix to keep article key consistent with metadata.
        article = heading.replace('## ', '').strip()
        combined_chunks.append({"article": article, "text": content.strip()})
    return combined_chunks