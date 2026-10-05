def build_chunk_metadata(document, chunk):
    return {
        "document_id": str(document.id),
        "filename": document.filename,
        "relative_path": document.relative_path,
        "file_type": document.file_type,
        "subject": document.subject or "",
        "topic": document.topic or "",
        "chunk_index": chunk.chunk_index,
        "page_number": chunk.page_number or 0,
    }
