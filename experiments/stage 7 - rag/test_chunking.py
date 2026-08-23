from pathlib import Path
import re


def load_document(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")


def split_by_sections(text: str, source: str):
    """
    Split markdown document by ## headings.
    Return chunk metadata.
    """

    sections = re.split(r"\n## ", text)

    chunks = []

    for idx, section in enumerate(sections):

        if idx == 0:
            chunk_text = section.strip()
        else:
            chunk_text = "## " + section.strip()

        chunks.append(
            {
                "source": source,
                "chunk_id": idx + 1,
                "content": chunk_text,
            }
        )

    return chunks


if __name__ == "__main__":

    source = "inventory_risk_policy.md"

    text = load_document(
        f"knowledge_base/{source}"
    )

    chunks = split_by_sections(
        text=text,
        source=source
    )

    print(f"Chunks Created: {len(chunks)}\n")

    for chunk in chunks:
        print("=" * 60)
        print(f"Source   : {chunk['source']}")
        print(f"Chunk ID : {chunk['chunk_id']}")
        print(chunk["content"][:300])
        print()

    for chunk in chunks:
        if "CRITICAL Stockout Risk" in chunk["content"]:
            print(chunk["content"])