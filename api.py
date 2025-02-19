# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from vector_db import VectorDB

app = FastAPI()
# Initialize the VectorDB class
db = VectorDB()

class DocumentRequest(BaseModel):
    collection_name: str
    doc_id: str
    text: str

class QueryRequest(BaseModel):
    collection_name: str
    query_text: str
    top_n: int = 3

@app.post("/create_collection")
def create_collection(collection_name: str):
    db.create_collection(collection_name)
    return {"message": f"Collection '{collection_name}' created."}

@app.post("/insert_document")
def insert_document(data: DocumentRequest):
    db.insert_document(data.collection_name, data.doc_id, data.text)
    return {"message": f"Document '{data.doc_id}' inserted."}

@app.post("/update_document")
def update_document(data: DocumentRequest):
    db.update_document(data.collection_name, data.doc_id, data.text)
    return {"message": f"Document '{data.doc_id}' updated."}

@app.delete("/delete_document")
def delete_document(collection_name: str, doc_id: str):
    db.delete_document(collection_name, doc_id)
    return {"message": f"Document '{doc_id}' deleted from '{collection_name}'."}

@app.post("/retrieve")
def retrieve_documents(data: QueryRequest):
    results = db.retrieve_similar_documents(data.collection_name, data.query_text, data.top_n)
    return {"results": results}
