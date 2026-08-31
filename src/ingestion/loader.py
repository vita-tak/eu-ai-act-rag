from src.config import DATA_PATH

def load_document() -> str:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return f.read()