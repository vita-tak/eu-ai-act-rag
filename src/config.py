from dotenv import load_dotenv
import os

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_WORKSPACE_ID = os.getenv("ANTHROPIC_WORKSPACE_ID")

# Paths
DATA_PATH = "data/eu_ai_act.txt"
CHROMA_PATH = "chroma_db"

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Retrieval
TOP_K = 5