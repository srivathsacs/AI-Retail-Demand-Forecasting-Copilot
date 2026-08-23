from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer


class VectorStore:
    """
    Manage embeddings and storage in a Chroma vector database.
    """

    def __init__(
        self,
        db_path: str,
        collection_name: str,
        embedding_model: str = "all-MiniLM-L6-v2",
    ) -> None:
        self._model = SentenceTransformer(embedding_model)

        self._client = PersistentClient(path=db_path)

        self._collection = self._client.get_or_create_collection(
            name=collection_name
        )

    def index_documents(
        self,
        chunks: list[dict],
    ) -> None:
        """
        Generate embeddings and store document chunks.
        Existing documents are removed before indexing to ensure
        repeatable execution.
        """

        existing = self._collection.get()

        if existing["ids"]:
            self._collection.delete(ids=existing["ids"])

        for chunk in chunks:
            embedding = self._model.encode(
                chunk["content"]
            ).tolist()

            self._collection.add(
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

    @property
    def collection(self):
        """
        Return the Chroma collection.
        """
        return self._collection

    @property
    def embedding_model(self):
        """
        Return the embedding model.
        """
        return self._model