import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions
from chromadb.config import Settings
import uuid


class VectorDB:
    def __init__(self, collection_name="my_collection", persist_directory="db"):
        """
        Initializes the VectorDB class.

        Args:
            collection_name (str): The name of the collection.
            persist_directory (str): Directory to persist ChromaDB data.
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

    def create_collection(self):
        """Creates a new collection or gets existing."""
        try:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"},
            )
            print(f"Collection '{self.collection_name}' created.")
        except chromadb.db.base.UniqueConstraintError:
            self.collection = self.client.get_collection(
                name=self.collection_name, embedding_function=self.embedding_function
            )
            print(f"Collection '{self.collection_name}' exists. Using existing.")

    def insert_document(self, text):
        """Inserts a document."""
        document_id = str(uuid.uuid4())  # Use UUIDs for unique IDs
        self.collection.add(documents=[text], ids=[document_id])
        print(f"Document with id {document_id} added.")
        return document_id

    def update_document(self, document_id, new_text):
        """Updates a document."""
        if not self.collection.get(ids=[document_id])["ids"]:
            raise ValueError(f"Document with id '{document_id}' not found.")
        self.collection.update(ids=[document_id], documents=[new_text])
        print(f"Document '{document_id}' updated.")

    def delete_document(self, document_id):
        """Deletes a document."""
        if not self.collection.get(ids=[document_id])["ids"]:
            raise ValueError(f"Document with id '{document_id}' not found.")
        self.collection.delete(ids=[document_id])
        print(f"Document '{document_id}' deleted.")

    def retrieve_documents(self, query_text, n=5):
        """Retrieves relevant documents."""
        results = self.collection.query(query_texts=[query_text], n_results=n)
        return results["documents"][0]