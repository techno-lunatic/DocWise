from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
# Points to DocWise/

UPLOAD_DIR = BASE_DIR / "data" / "uploads"
# Points to DocWise/data/uploads/

CHROMA_DIR = BASE_DIR / "data" / "chroma_db"
# Points to chromadb storage


UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

# LLM model and Embedding model selection
LLM_MODEL = "llama3.2:3b"
EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-0.6B" # make sure ots the same for indexing and querying


# Parameter Tuning (change later if want to)
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120
TOP_K = 5