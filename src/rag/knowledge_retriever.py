from rag.retriever import Retriever
from rag.vector_store import VectorStore


class KnowledgeRetriever:
    """
    Retrieve relevant knowledge base documents for downstream
    recommendation generation.
    """

    def __init__(
        self,
        chroma_db_path: str,
        collection_name: str,
    ) -> None:

        self._vector_store = VectorStore(
            db_path=chroma_db_path,
            collection_name=collection_name,
        )

        self._retriever = Retriever(
            self._vector_store
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Retrieve the most relevant knowledge base chunks.
        """

        return self._retriever.retrieve(
            query=query,
            top_k=top_k,
        )