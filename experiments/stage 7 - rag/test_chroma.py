from pathlib import Path
import re

import chromadb
from sentence_transformers import SentenceTransformer


KB_PATH = Path("knowledge_base")


def load_documents():
    documents = []

    for file_path in KB_PATH.glob("*.md"):
        with open(file_path, "r", encoding="utf-8") as f:
            documents.append(
                {
                    "source": file_path.name,
                    "content": f.read(),
                }
            )

    return documents



def chunk_documents(documents):

    chunks = []

    for doc in documents:

        sections = re.split(
            r"\n## ",
            doc["content"]
        )

        chunk_id = 1

        for idx, section in enumerate(sections):

            section = section.strip()

            if not section:
                continue

            if idx != 0:
                section = "## " + section

            chunks.append(
                {
                    "source": doc["source"],
                    "chunk_id": chunk_id,
                    "content": section,
                }
            )

            chunk_id += 1

    return chunks


def main():

    print("Loading documents...")
    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")

    print("Chunking documents...")
    chunks = chunk_documents(documents)

    print("\nSample Chunks")
    print("=" * 60)

    for chunk in chunks[:3]:

        print("\nChunk ID:", chunk["chunk_id"])
        print("-" * 60)
        print(chunk["content"][:500])

    print(f"Chunks created: {len(chunks)}")

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Creating Chroma client...")
    client = chromadb.PersistentClient(
    path="chroma_db"
    )

    collection = client.get_or_create_collection(
    name="inventory_knowledge_base"
    )

    print("Generating embeddings and storing in Chroma...")

    for chunk in chunks:

        embedding = model.encode(
            chunk["content"]
        ).tolist()

        collection.add(
            ids=[
                f"{chunk['source']}_{chunk['chunk_id']}"
            ],
            documents=[
                chunk["content"]
            ],
            embeddings=[
                embedding
            ],
            metadatas=[
                {
                    "source": chunk["source"],
                    "chunk_id": chunk["chunk_id"],
                }
            ],
        )

    print("\n" + "=" * 50)
    print("CHROMA VALIDATION")
    print("=" * 50)

    print(f"\nChunks Stored: {collection.count()}")

    results = collection.get(
        include=[
            "documents",
            "embeddings",
            "metadatas",
        ]
    )

    print("\nSample ID:")
    print(results["ids"][0])

    print("\nSample Metadata:")
    print(results["metadatas"][0])

    print("\nEmbedding Dimension:")
    print(len(results["embeddings"][0]))

    print("\nSample Document:")
    print(results["documents"][0][:300])

if __name__ == "__main__":
    main()