import os
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None
try:
    import docx
except ImportError:
    docx = None

def extract_pdf(filepath):
    if not PdfReader:
        return []
    chunks = []
    try:
        reader = PdfReader(filepath)
        for i, page in enumerate(reader.pages):
            try:
                t = page.extract_text()
                if t and t.strip():
                    chunks.append({"text": t.strip(), "page": i + 1})
            except Exception as e:
                print(f"Skipping page {i + 1} due to extraction error")
    except Exception:
        pass
    return chunks

def extract_docx(filepath):
    if not docx:
        return []
    text = ""
    try:
        doc = docx.Document(filepath)
        for p in doc.paragraphs:
            text += p.text + "\n"
    except Exception:
        pass
    if text.strip():
        return [{"text": text.strip(), "page": 1}]
    return []

def extract_text_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            t = f.read()
            if t.strip():
                return [{"text": t.strip(), "page": 1}]
    except Exception:
        pass
    return []

def extract_document(filepath, file_type):
    """Returns a list of dicts: [{'text': '...', 'page': 1}]"""
    if file_type == 'pdf':
        return extract_pdf(filepath)
    elif file_type == 'docx':
        return extract_docx(filepath)
    else:
        return extract_text_file(filepath)
