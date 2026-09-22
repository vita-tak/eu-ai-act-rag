from pathlib import Path
from src.config import DATA_PATH


def load_document() -> str:
    """
    Parse the EU AI Act PDF with Docling and return it as Markdown.

    Docling preserves the document's hierarchical structure (headings,
    sections, lists) which makes downstream chunking on heading boundaries
    more reliable than splitting raw text with regex.

    Docling is a local build-time dependency and is not installed in
    production. The import is deferred inside the function so the module
    can be imported without Docling present.
    """
    from docling.document_converter import DocumentConverter

    converter = DocumentConverter()
    result = converter.convert(Path(DATA_PATH))
    return result.document.export_to_markdown()