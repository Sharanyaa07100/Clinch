from pathlib import Path

from parser import extract_text

from llm import (
    classify_document,
    extract_career_profile,
    extract_certification,
    extract_project
)


def ingest_document(file_path):
    """
    Extract, classify and structure a career document.
    """

    file_path = Path(file_path)

    text = extract_text(file_path)

    classification = classify_document(text)

    document_type = classification.document_type

    if document_type == "resume":

        data = extract_career_profile(text)

    elif document_type == "certification":

        data = extract_certification(text)

    elif document_type == "project":

        data = extract_project(text)

    else:

        data = None

    return {
        "file_name": file_path.name,
        "document_type": document_type,
        "confidence": classification.confidence,
        "data": data
    }
def ingest_folder(folder_path):
    """
    Ingest all supported documents in a folder.
    """

    folder_path = Path(folder_path)

    supported_extensions = {".pdf", ".docx"}

    documents = []

    for file_path in folder_path.iterdir():

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in supported_extensions:
            continue

        print(f"Processing: {file_path.name}")

        try:
            document = ingest_document(file_path)
            documents.append(document)

        except Exception as error:
            print(f"Failed to process {file_path.name}: {error}")

    return documents