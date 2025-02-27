# api.py

from fastapi import FastAPI
from pydantic import BaseModel
from vector_db import VectorDB

# Create a FastAPI instance
app = FastAPI()

# Initialize a global VectorDB instance
# This allows all endpoints to use the same database connection/instance.
db = VectorDB()

class DocumentRequest(BaseModel):
    """
    Represents the JSON payload for inserting or updating a document.

    Attributes:
    - collection_name (str): The name of the collection where the document belongs.
    - doc_id (str): A unique identifier for the document.
    - text (str): The text content of the document to be stored or updated.
    """
    collection_name: str
    doc_id: str
    text: str

class QueryRequest(BaseModel):
    """
    Represents the JSON payload for retrieving similar documents.

    Attributes:
    - collection_name (str): The name of the collection to query.
    - query_text (str): The text query for which similar documents are sought.
    - top_n (int): The maximum number of results to return (default=3).
    """
    collection_name: str
    query_text: str
    top_n: int = 3

@app.post("/create_collection")
def create_collection(collection_name: str):
    """
    Create a new collection in the vector database.

    Args:
        collection_name (str): Name of the new collection to be created.

    Returns:
        dict: A simple message confirming collection creation.
    """
    db.create_collection(collection_name)
    return {"message": f"Collection '{collection_name}' created."}

@app.post("/insert_document")
def insert_document(data: DocumentRequest):
    """
    Insert a new document into the specified collection.

    Args:
        data (DocumentRequest): 
            - collection_name: The target collection for the document.
            - doc_id: A unique identifier for the document.
            - text: The text content to be vectorized and stored.

    Returns:
        dict: A message confirming successful insertion.
    """
    db.insert_document(data.collection_name, data.doc_id, data.text)
    return {"message": f"Document '{data.doc_id}' inserted."}

@app.post("/update_document")
def update_document(data: DocumentRequest):
    """
    Update an existing document in the specified collection.

    This replaces the content of a document with new text,
    identified by doc_id within the given collection.

    Args:
        data (DocumentRequest):
            - collection_name: The target collection containing the document.
            - doc_id: The identifier of the document to update.
            - text: The new text content to replace the old one.

    Returns:
        dict: A message confirming successful update.
    """
    db.update_document(data.collection_name, data.doc_id, data.text)
    return {"message": f"Document '{data.doc_id}' updated."}

@app.delete("/delete_document")
def delete_document(collection_name: str, doc_id: str):
    """
    Delete an existing document from the specified collection.

    Args:
        collection_name (str): Name of the collection containing the document.
        doc_id (str): The identifier of the document to delete.

    Returns:
        dict: A message confirming successful deletion.
    """
    db.delete_document(collection_name, doc_id)
    return {"message": f"Document '{doc_id}' deleted from '{collection_name}'."}

@app.post("/retrieve")
def retrieve_documents(data: QueryRequest):
    """
    Retrieve documents most similar to the given query text.

    Args:
        data (QueryRequest):
            - collection_name: The target collection to query.
            - query_text: The text to match for similarity.
            - top_n: Number of top results to retrieve.

    Returns:
        dict: A JSON object containing a "results" list. Each element is a tuple
              of (doc_id, text_content, similarity_score).
    """
    results = db.retrieve_similar_documents(data.collection_name, data.query_text, data.top_n)
    return {"results": results}
