import re


def chunk_documents(documents: list[dict[str, str]]) -> list[dict]:
    """
    Split Markdown documents into chunks using level-2 (##) headings.

    Args:
        documents: List of documents produced by the document loader.

    Returns:
        A list of chunks containing:
            - source
            - chunk_id
            - content
    """
    chunks = []

    for document in documents:
        sections = re.split(r"\n## ", document["content"])

        chunk_id = 1

        for index, section in enumerate(sections):
            section = section.strip()

            if not section:
                continue

            if index != 0:
                section = "## " + section

            chunks.append(
                {
                    "source": document["source"],
                    "chunk_id": chunk_id,
                    "content": section,
                }
            )

            chunk_id += 1

    return chunks