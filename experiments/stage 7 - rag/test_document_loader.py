from pathlib import Path


def load_documents(kb_path: str):
    """
    Load all markdown files from the knowledge base.
    """

    documents = []

    for file_path in Path(kb_path).glob("*.md"):
        documents.append(
            {
                "source": file_path.name,
                "content": file_path.read_text(encoding="utf-8")
            }
        )

    return documents


if __name__ == "__main__":

    docs = load_documents("knowledge_base")

    print(f"Loaded {len(docs)} documents\n")

    for doc in docs:
        print("=" * 50)
        print(doc["source"])
        print(doc["content"][:200])
        print()