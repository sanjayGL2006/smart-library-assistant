from .embeddings import generate_embeddings
from .metadata import build_chunk_metadata
from .vector_store import add_chunks

def index_document(document):
    chunks = list(
        document.chunks.all().order_by("chunk_index")
    )

    if not chunks:
        return 0

    texts = [
        chunk.content
        for chunk in chunks
        if chunk.content.strip()
    ]

    if not texts:
        return 0

    embeddings = generate_embeddings(texts)

    chunk_ids = []
    metadatas = []

    valid_chunks = [
        chunk
        for chunk in chunks
        if chunk.content.strip()
    ]

    for chunk in valid_chunks:
        chunk_ids.append(
            f"document-{document.id}-chunk-{chunk.chunk_index}"
        )

        metadatas.append(
            build_chunk_metadata(
                document,
                chunk
            )
        )

    add_chunks(
        chunk_ids=chunk_ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(valid_chunks)
