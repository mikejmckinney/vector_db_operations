import pytest
from src.db import VectorDB  # Import from db.py

# Fixture to create a new VectorDB instance for each test
@pytest.fixture
def vector_db():
    db = VectorDB(collection_name="test_collection", persist_directory="test_db")
    db.create_collection()  # Ensure the collection exists
    return db

def test_insert_and_retrieve(vector_db):
    vector_db.insert_document("This is a test document.")
    results = vector_db.retrieve_documents("test document", n=1)
    assert len(results) == 1
    assert "test document" in results[0]

def test_update_document(vector_db):
    doc_id = vector_db.insert_document("Original text.")
    vector_db.update_document(doc_id, "Updated text.")
    results = vector_db.retrieve_documents("Updated text", n=1)
    assert len(results) == 1
    assert "Updated text" in results[0]
    with pytest.raises(ValueError):
        vector_db.update_document("nonexistent_id", "This should fail.")

def test_delete_document(vector_db):
    doc_id = vector_db.insert_document("Text to be deleted.")
    vector_db.delete_document(doc_id)
    results = vector_db.retrieve_documents("to be deleted", n=1)
    assert len(results) == 0  # Should be empty after deletion
    with pytest.raises(ValueError):
        vector_db.delete_document("nonexistent_id")



def test_create_collection_already_exists(vector_db):
  #create it a second time.  should get existing
  vector_db.create_collection()