import fitz  # PyMuPDF
import docx
import tempfile


def extract_pdf(file_bytes: bytes) -> str:
    """Extracts text from PDF resumes."""
    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp.flush()
        doc = fitz.open(tmp.name)
        return " ".join(page.get_text() for page in doc)


def extract_docx(file_bytes: bytes) -> str:
    """Extracts text from .docx resumes."""
    with tempfile.NamedTemporaryFile(suffix=".docx") as tmp:
        tmp.write(file_bytes)
        tmp.flush()
        document = docx.Document(tmp.name)
        return " ".join(p.text for p in document.paragraphs)


def parse_resume(file_bytes: bytes, filename: str):
    ext = filename.lower().split(".")[-1]

    if ext == "pdf":
        text = extract_pdf(file_bytes)
    elif ext == "docx":
        text = extract_docx(file_bytes)
    else:
        text = file_bytes.decode("utf-8", errors="ignore")

    # Smooth whitespace for better processing
    clean_text = " ".join(text.split())
    return {"filename": filename, "text": clean_text}
