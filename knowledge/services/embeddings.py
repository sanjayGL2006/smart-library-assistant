from functools import lru_cache

try:
    # pyrefly: ignore [missing-import]
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

MODEL_NAME = "all-MiniLM-L6-v2"

@lru_cache(maxsize=1)
def get_embedding_model():
    """
    Load the embedding model once and reuse it.
    """
    if not SentenceTransformer:
        return None
    return SentenceTransformer(MODEL_NAME)

def generate_embedding(text: str) -> list[float]:
    """
    Generate an embedding for a single piece of text.
    """
    model = get_embedding_model()
    if not model:
        return []

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for multiple chunks efficiently.
    """
    if not texts:
        return []

    model = get_embedding_model()
    if not model:
        return []

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    return embeddings.tolist()
