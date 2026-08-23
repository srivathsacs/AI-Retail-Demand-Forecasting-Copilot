from sentence_transformers import SentenceTransformer
import chromadb


def main():

    # -------------------------
    # Load embedding model
    # -------------------------

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    # -------------------------
    # Connect to Chroma
    # -------------------------

    client = chromadb.PersistentClient(
    path="chroma_db"
    )

    collection = client.get_collection(
        name="inventory_knowledge_base"
    )

    # -------------------------
    # User question
    # -------------------------

    question = (
    "CRITICAL Stockout Risk"
    )



    print("\nQuestion:")
    print(question)

    # -------------------------
    # Create query embedding
    # -------------------------

    query_embedding = model.encode(
        question
    ).tolist()

    print(
        f"\nQuery Embedding Size: "
        f"{len(query_embedding)}"
    )

    # -------------------------
    # Retrieve top matches
    # -------------------------

    results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10,
    )

    # -------------------------
    # Display results
    # -------------------------

    print("\n" + "=" * 60)
    print("TOP MATCHES")
    print("=" * 60)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i in range(len(documents)):

        print(f"\nMatch {i + 1}")

        print(
            f"Distance: "
            f"{distances[i]:.4f}"
        )

        print(
            f"Source: "
            f"{metadatas[i]['source']}"
        )

        print(
            f"Chunk ID: "
            f"{metadatas[i]['chunk_id']}"
        )

        print("\nContent:")

        print(documents[i])

        print("-" * 60)


if __name__ == "__main__":
    main()