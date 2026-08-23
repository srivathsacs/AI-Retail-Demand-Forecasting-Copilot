from rag.chunker import chunk_documents
from rag.document_loader import load_documents
from rag.vector_store import VectorStore


class KnowledgeBaseIndexer:
    """
    Build and update the vector database from the knowledge base.
    """

    def __init__(
        self,
        knowledge_base_path: str,
        chroma_db_path: str,
        collection_name: str,
    ) -> None:
        self._knowledge_base_path = knowledge_base_path

        self._vector_store = VectorStore(
            db_path=chroma_db_path,
            collection_name=collection_name,
        )

    def build(self) -> None:
        """
        Build the vector database.
        """

        documents = load_documents(
            self._knowledge_base_path
        )

        chunks = chunk_documents(
            documents
        )

        self._vector_store.index_documents(
            chunks
        )