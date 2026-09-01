from src.config import DATA_PATH

def clean_text(text: str) -> str:
    lines = text.split('\n')
    cleaned = [line for line in lines if 'OJ L' not in line 
               and 'ELI:' not in line 
               and 'europa.eu' not in line]
    return '\n'.join(cleaned)

def load_document() -> str:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    return clean_text(text)