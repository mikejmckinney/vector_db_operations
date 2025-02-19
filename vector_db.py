# vector_db.py
import os
#os.environ["CHROMA_INDEX_IMPL"] = "flat" # must be done before chroma client is created to avoid HNSW error
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

class VectorDB:
    """
    A Python class to perform CRUD operations on a text-based vector database.
    Uses Chroma for storage and SentenceTransformer for embedding.
    """

    def __init__(self, persist_directory: str = "./chroma_db", embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize the vector database client and the embedding model.
        The model all-MiniLM-L6-v2 was used because its a popular and lightweight SentenceTransformer that is
        sufficient for most small to medium-scale similarity search tasks.
        
        :param persist_directory: Path to directory where Chroma will store data.
        :param embedding_model: Model name for SentenceTransformer embeddings.
        """
        # Configure Chroma to persist data locally
        self.client = chromadb.Client(
            Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_directory)
        )
        # Load the embedding model
        self.model = SentenceTransformer(embedding_model)

    def _embed_text(self, text: str):
        """
        Convert text into a vector embedding using the SentenceTransformer model.
        """
        return self.model.encode([text])[0].tolist()

    def create_collection(self, name: str):
        """
        Create a new collection (index) in the vector database.
        
        :param name: Name of the collection to create.
        """
        return self.client.create_collection(name, get_or_create = True)

    def insert_document(self, collection_name: str, doc_id: str, text: str):
        """
        Insert a new text document into the collection.
        
        :param collection_name: Name of the collection to insert the document into.
        :param doc_id: An identifier for the document.
        :param text: The text content to be vectorized and stored.
        """
        collection = self.client.get_or_create_collection(collection_name)
        embedding = self._embed_text(text)
        collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            metadatas=[{"text": text}]
        )

    def update_document(self, collection_name: str, doc_id: str, new_text: str):
        """
        Update/Replace an existing text document in the database.
        
        :param collection_name: Name of the collection containing the document.
        :param doc_id: The identifier of the document to update.
        :param new_text: The new text content to replace the old content.
        """
        collection = self.client.get_collection(collection_name)
        # Delete old entry first
        collection.delete(ids=[doc_id])
        # Insert updated entry
        self.insert_document(collection_name, doc_id, new_text)

    def delete_document(self, collection_name: str, doc_id: str):
        """
        Delete a text document from the database.
        
        :param collection_name: Name of the collection containing the document.
        :param doc_id: The identifier of the document to delete.
        """
        collection = self.client.get_collection(collection_name)
        collection.delete(ids=[doc_id])

    def retrieve_similar_documents(self, collection_name: str, query_text: str, top_n: int = 3):
        """
        Retrieve the top N most relevant documents in the collection, given the query text.
        
        :param collection_name: Name of the collection to search in.
        :param query_text: The query text to match against stored documents.
        :param top_n: Number of documents to retrieve.
        :return: List of (doc_id, text, score) tuples for the most relevant documents.
        """
        collection = self.client.get_collection(collection_name)
        query_embedding = self._embed_text(query_text)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_n
        )
        # The results object typically looks like:
        # {
        #    'ids': [['doc1', 'doc2']],
        #    'metadatas': [[{'text': 'Sample text1'}, {'text': 'Sample text2'}]],
        #    'embeddings': [[[...] ... ]],
        #    'distances': [[distance1, distance2]]
        # }
        output = []
        for i, doc_id in enumerate(results['ids'][0]):
            text_content = results['metadatas'][0][i]['text']
            distance = results['distances'][0][i]
            similarity_score = 1.0 - distance  # simple conversion if needed
            output.append((doc_id, text_content, similarity_score))
        return output
    
    def delete_collection(self, name: str):
        """
        Delete an entire collection from the database if it exists.
        """
        # Fetch all existing collections
        all_collections = self.client.list_collections()
        # Convert them to a simple list of collection names
        existing_names = [c.name for c in all_collections]
        
        # Check if `name` is in the list of existing collection names
        if name in existing_names:
            self.client.delete_collection(name)
            print(f"Collection '{name}' deleted.")
        else:
            print(f"Collection '{name}' does not exist; skipping delete.")




    def persist(self):
        """
        Eusre that the collection is created and fully persisted before any other tests or methods that depend on it are ran
        """
        self.client.persist() 