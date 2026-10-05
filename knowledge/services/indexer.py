from django.utils import timezone
from knowledge.models import KnowledgeDocument, KnowledgeChunk
from knowledge.services.scanner import scan_notes_directory
from knowledge.services.extractor import extract_document
from knowledge.services.chunker import chunk_text

def index_all_notes(notes_dir):
    stats = {
        "files_found": 0,
        "new": 0,
        "already_indexed": 0,
        "modified": 0,
        "unsupported": 0,
        "processed": 0,
        "chunks_created": 0,
        "failed": 0
    }
    
    discovered = scan_notes_directory(notes_dir)
    stats["files_found"] = len(discovered)
    
    for file_info in discovered:
        print(f"Indexing: {file_info['relative_path']}")
        # Check DB
        doc = KnowledgeDocument.objects.filter(relative_path=file_info['relative_path']).first()
        
        is_new = False
        is_modified = False
        
        if not doc:
            is_new = True
            doc = KnowledgeDocument.objects.create(
                filename=file_info['filename'],
                relative_path=file_info['relative_path'],
                file_type=file_info['file_type'],
                file_size=file_info['file_size']
            )
        elif doc.content_hash != file_info['hash']:
            is_modified = True
            # Clear old chunks
            doc.chunks.all().delete()
        else:
            stats["already_indexed"] += 1
            continue
            
        if is_new:
            stats["new"] += 1
        if is_modified:
            stats["modified"] += 1
            
        # Extract & Chunk
        doc.content_hash = file_info['hash']
        
        extracted_pages = extract_document(file_info['filepath'], file_info['file_type'])
        if not extracted_pages:
            stats["failed"] += 1
            continue
            
        final_chunks = []
        for page_data in extracted_pages:
            final_chunks.extend(chunk_text(page_data['text'], page=page_data['page']))
            
        # Save Doc first
        doc.chunk_count = len(final_chunks)
        doc.indexed = True
        doc.last_indexed_at = timezone.now()
        doc.save()
        
        # Save Chunks
        for i, c in enumerate(final_chunks):
            KnowledgeChunk.objects.create(
                document=doc,
                chunk_index=i,
                content=c['text'],
                page_number=c['page']
            )
            
        stats["processed"] += 1
        stats["chunks_created"] += len(final_chunks)
        
    return stats
