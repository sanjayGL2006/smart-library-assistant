def chunk_text(text, page=1, max_chunk_size=1000, overlap=100):
    """Simple semantic chunker by paragraph, falling back to character chunking."""
    chunks = []
    if not text:
        return chunks
        
    paragraphs = text.split('\n\n')
    current_chunk = ""
    
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
            
        if len(current_chunk) + len(p) < max_chunk_size:
            current_chunk += p + "\n\n"
        else:
            if current_chunk:
                chunks.append({"text": current_chunk.strip(), "page": page})
            
            # If paragraph itself is too large, split it by characters
            if len(p) > max_chunk_size:
                for i in range(0, len(p), max_chunk_size - overlap):
                    chunks.append({"text": p[i:i + max_chunk_size], "page": page})
                current_chunk = ""
            else:
                current_chunk = p + "\n\n"
                
    if current_chunk:
        chunks.append({"text": current_chunk.strip(), "page": page})
        
    return chunks
