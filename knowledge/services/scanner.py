import os
import hashlib

def get_file_hash(filepath):
    """Calculates SHA256 of the file content."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return None

def scan_notes_directory(notes_dir):
    """Scans directory and returns raw file metadata."""
    discovered = []
    
    if not os.path.exists(notes_dir):
        return discovered
        
    for root, _, filenames in os.walk(notes_dir):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            ext = os.path.splitext(filename)[1].lower().replace('.', '')
            if ext not in ['pdf', 'docx', 'txt', 'md', 'html', 'py', 'js', 'ts', 'csv', 'json']:
                continue
                
            rel_path = os.path.relpath(filepath, notes_dir).replace('\\', '/')
            file_hash = get_file_hash(filepath)
            
            if file_hash:
                path_parts = rel_path.split('/')
                subject = path_parts[0] if len(path_parts) > 1 else ""
                topic = path_parts[1] if len(path_parts) > 2 else ""

                discovered.append({
                    "filename": filename,
                    "filepath": filepath,
                    "relative_path": rel_path,
                    "file_type": ext,
                    "file_size": os.path.getsize(filepath),
                    "hash": file_hash,
                    "subject": subject,
                    "topic": topic
                })
                
    return discovered
