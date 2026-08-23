class Retriever:
    """
    Retrieve the most relevant document chunks from the vector store.
    """

    def __init__(self, vector_store) -> None:
        self._vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Retrieve the top matching document chunks.

        Args:
            query: User query.
            top_k: Number of chunks to retrieve.

        Returns:
            A list of retrieved chunks containing:
                - source
                - chunk_id
                - content
                - distance
        """

        query_embedding = (
            self._vector_store.embedding_model
            .encode(query)
            .tolist()
        )

        results = self._vector_store.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        retrieved_chunks = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            retrieved_chunks.append(
                {
                    "source": metadata["source"],
                    "chunk_id": metadata["chunk_id"],
                    "content": document,
                    "distance": distance,
                }
            )

        return retrieved_chunks