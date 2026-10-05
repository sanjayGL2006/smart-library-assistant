from pathlib import Path
from django.conf import settings

try:
    import chromadb
except ImportError:
    chromadb = None

COLLECTION_NAME = "olms_knowledge"

def get_chroma_path():
    path = Path(
        getattr(
            settings,
            "CHROMA_DB_PATH",
            Path(settings.BASE_DIR) / "data" / "chroma"
        )
    )

    path.mkdir(parents=True, exist_ok=True)
    return str(path)

def get_client():
    if not chromadb:
        return None
    return chromadb.PersistentClient(
        path=get_chroma_path()
    )

def get_collection():
    client = get_client()
    if not client:
        return None

    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "description": "OLMS AI Knowledge Base"
        }
    )

def add_chunks(
    chunk_ids: list[str],
    documents: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict]
):
    if not documents:
        return

    collection = get_collection()
    if not collection:
        return

    collection.upsert(
        ids=chunk_ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

def search(
    query_embedding: list[float],
    limit: int = 5
):
    collection = get_collection()
    if not collection:
        return {"documents": [], "metadatas": [], "distances": [], "ids": []}

    if collection.count() == 0:
        return {
            "documents": [],
            "metadatas": [],
            "distances": [],
            "ids": []
        }

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=limit
    )

def delete_document_chunks(document_id: int):
    collection = get_collection()
    if not collection:
        return

    collection.delete(
        where={
            "document_id": str(document_id)
        }
    )

def get_collection_count():
    collection = get_collection()
    if not collection:
        return 0
    return collection.count()
