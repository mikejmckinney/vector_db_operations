from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.db import VectorDB  # Import the VectorDB class

# --- Pydantic Models ---
class Document(BaseModel):
    text: str

class UpdateDocument(BaseModel):
    new_text: str

# --- FastAPI Setup ---
app = FastAPI()
db = VectorDB()  # Create a VectorDB instance
db.create_collection() # Create collection if it doesn't exist on startup.

# --- API Endpoints ---
@app.post("/documents/")
async def create_document(document: Document):
    doc_id = db.insert_document(document.text)
    return {"document_id": doc_id}

@app.get("/documents/")
async def read_documents(query_text: str, n: int = 5):
    results = db.retrieve_documents(query_text, n)
    return {"results": results}

@app.put("/documents/{document_id}")
async def update_existing_document(document_id: str, update_doc: UpdateDocument):
    try:
        db.update_document(document_id, update_doc.new_text)
        return {"message": f"Document {document_id} updated."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/documents/{document_id}")
async def delete_existing_document(document_id: str):
    try:
        db.delete_document(document_id)
        return {"message": f"Document {document_id} deleted."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))