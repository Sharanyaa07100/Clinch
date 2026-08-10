import json
from pathlib import Path


KNOWLEDGE_BASE_PATH = Path("data/processed/career_knowledge.json")


def save_knowledge(documents):
    """
    Save processed career documents to the knowledge base.
    """

    KNOWLEDGE_BASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    data = []

    for document in documents:

        record = {
            "file_name": document["file_name"],
            "document_type": document["document_type"],
            "confidence": document["confidence"],
            "data": (
                document["data"].model_dump()
                if document["data"] is not None
                else None
            )
        }

        data.append(record)

    with open(
        KNOWLEDGE_BASE_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


def load_knowledge():
    """
    Load the stored career knowledge.
    """

    if not KNOWLEDGE_BASE_PATH.exists():
        return []

    with open(
        KNOWLEDGE_BASE_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)