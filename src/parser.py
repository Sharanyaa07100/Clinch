import pymupdf
from docx import Document
from extractor import clean_text

def extract_pdf_text(file_path):
    document = pymupdf.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def extract_docx_text(file_path):
    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_text(file_path):

    if file_path.suffix.lower() == ".pdf":
        text = extract_pdf_text(file_path)

    elif file_path.suffix.lower() == ".docx":
        text = extract_docx_text(file_path)

    else:
        raise ValueError(f"Unsupported file type: {file_path.suffix}")

    return clean_text(text)