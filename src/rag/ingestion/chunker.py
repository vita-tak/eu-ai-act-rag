import re


def chunk_document(text: str) -> list:
    """
    Split the EU AI Act text into chunks along article boundaries, so each
    chunk corresponds to exactly one article rather than a fixed size.

    Args:
        text: The cleaned EU AI Act text (see loader.clean_text).

    Returns:
        A list of dicts with "article" and "text" keys.
    """
    # Capturing group keeps the matched "Article N" headings in the result.
    chunks = re.split(r'(^Article \d+$)', text, flags=re.MULTILINE)

    combined_chunks = []
    for i in range(1, len(chunks), 2):
        heading = chunks[i]
        # Guard against a heading with no trailing content.
        content = chunks[i + 1] if i + 1 < len(chunks) else ""
        combined_chunks.append({"article": heading.strip(), "text": content.strip()})
    return combined_chunks