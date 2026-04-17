import fitz

def extract_text(file_bytes):
    pdf = fitz.open(stream=file_bytes, filetype="pdf")

    text = ""
    for page in pdf:
        text += page.get_text()

    if not text.strip():
        raise ValueError("Empty PDF")

    return text[:3000]