from src.config import DATA_PATH


def clean_text(text: str) -> str:
    """
    Strip administrative boilerplate (OJ references, ELI identifiers, URLs)
    from the raw EU AI Act text.

    Runs before chunking: leftover boilerplate mixed into a chunk
    dilutes the embedding's semantic signal and can interfere with the
    article-boundary detection used in the chunking step.
    """
    lines = text.split('\n')
    cleaned = [line for line in lines if 'OJ L' not in line
               and 'ELI:' not in line
               and 'europa.eu' not in line]
    return '\n'.join(cleaned)


def load_document() -> str:
    """Load the EU AI Act source file and strip administrative boilerplate."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    return clean_text(text)