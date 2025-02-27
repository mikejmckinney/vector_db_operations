# test_vector_db.py

import pytest
import os
# If you want to switch to a 'flat' index rather than HNSW, uncomment the line below
# os.environ["CHROMA_INDEX_IMPL"] = "flat"

from vector_db import VectorDB

@pytest.fixture(scope="function")
def db():
    """
    A pytest fixture that provides a fresh VectorDB instance for each test.

    Scope "function" means every test function in this file will call this fixture 
    to create a brand-new database instance. Here, we point to a local folder 
    './test_chroma_db' for data persistence. If you want truly isolated 
    ephemeral tests, consider using a unique or temporary directory 
    (e.g., via tmp_path fixture).
    """
    test_db = VectorDB(persist_directory="./test_chroma_db")
    # The 'yield' keyword allows us to return the fixture value and then 
    # run any teardown code after the test if needed.
    yield test_db

def test_create_collection(db):
    """
    Test creating a new collection named 'test_collection'.
    
    Steps:
    1. Call db.create_collection() to create the collection.
    2. Verify the collection's name is 'test_collection'.
    3. Persist data to ensure the newly created collection is flushed to disk.
    """
    collection = db.create_collection("test_collection")
    assert collection.name == "test_collection"
    # Call persist() to explicitly flush the collection metadata to disk
    db.persist()

def test_insert_and_retrieve(db):
    """
    Test inserting a document into 'test_collection' and retrieving it.

    Steps:
    1. Insert a document with ID "doc1" and text "This is some test text".
    2. Retrieve top 1 most similar document to "test text".
    3. Confirm that the retrieved document has ID "doc1" and contains "test text" 
       in its stored content.
    """
    db.insert_document("test_collection", "doc1", "This is some test text")
    results = db.retrieve_similar_documents("test_collection", "test text", top_n=1)
    assert len(results) == 1

    doc_id, text_content, score = results[0]
    assert doc_id == "doc1"
    assert "test text" in text_content

def test_update_document(db):
    """
    Test updating the existing document 'doc1' in 'test_collection'.

    Steps:
    1. Update the text of "doc1" to "This is updated text".
    2. Retrieve top 1 document similar to "updated text".
    3. Confirm the retrieved doc has ID "doc1" and the new text content 
       includes "updated".
    """
    db.update_document("test_collection", "doc1", "This is updated text")
    results = db.retrieve_similar_documents("test_collection", "updated text", top_n=1)
    assert len(results) == 1

    doc_id, text_content, score = results[0]
    assert doc_id == "doc1"
    assert "updated" in text_content

def test_delete_document(db):
    """
    Test deleting the document 'doc1' in 'test_collection'.

    Steps:
    1. Delete the document with ID "doc1".
    2. Attempt to retrieve the top 1 result for "test text".
    3. Confirm the result set is empty, indicating the document is gone.
    """
    db.delete_document("test_collection", "doc1")
    results = db.retrieve_similar_documents("test_collection", "test text", top_n=1)
    # Ensure no documents were found
    assert len(results) == 0
