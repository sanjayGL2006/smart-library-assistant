from .embeddings import generate_embedding
from .vector_store import search

def semantic_search(
    query: str,
    limit: int = 5
):
    """
    Search the OLMS knowledge base using semantic similarity.
    """
    query_embedding = generate_embedding(query)

    results = search(
        query_embedding=query_embedding,
        limit=limit
    )

    output = []

    documents = results.get("documents", [[]])[0] if results.get("documents") else []
    metadatas = results.get("metadatas", [[]])[0] if results.get("metadatas") else []
    distances = results.get("distances", [[]])[0] if results.get("distances") else []
    ids = results.get("ids", [[]])[0] if results.get("ids") else []

    for index, document in enumerate(documents):
        output.append({
            "id": ids[index],
            "content": document,
            "metadata": metadatas[index],
            "distance": distances[index],
        })

    return output
