from pathlib import Path


def load_documents(knowledge_base_path: str) -> list[dict[str, str]]:
    """
    Load all Markdown documents from the knowledge base.

    Args:
        knowledge_base_path: Path to the knowledge base directory.

    Returns:
        A list of documents, where each document contains:
            - source: File name
            - content: Markdown content
    """
    documents = []

    for file_path in sorted(Path(knowledge_base_path).glob("*.md")):
        documents.append(
            {
                "source": file_path.name,
                "content": file_path.read_text(encoding="utf-8"),
            }
        )

    return documents