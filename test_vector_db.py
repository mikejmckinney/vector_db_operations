# test_vector_db.py
import pytest
import os
#os.environ["CHROMA_INDEX_IMPL"] = "flat"  # must be done before creating Chroma client

from vector_db import VectorDB

@pytest.fixture(scope="function")
def db():
    # ephemeral DB => None means no data persists between tests
    test_db = VectorDB(persist_directory="./test_chroma_db")
    yield test_db

def test_create_collection(db):
    collection = db.create_collection("test_collection")
    assert collection.name == "test_collection"
    db.persist() #ensure collection is persisted

def test_insert_and_retrieve(db):
    db.insert_document("test_collection", "doc1", "This is some test text")
    results = db.retrieve_similar_documents("test_collection", "test text", top_n=1)
    assert len(results) == 1
    doc_id, text_content, score = results[0]
    assert doc_id == "doc1"
    assert "test text" in text_content

def test_update_document(db):
    db.update_document("test_collection", "doc1", "This is updated text")
    results = db.retrieve_similar_documents("test_collection", "updated text", top_n=1)
    assert len(results) == 1
    doc_id, text_content, score = results[0]
    assert doc_id == "doc1"
    assert "updated" in text_content

def test_delete_document(db):
    db.delete_document("test_collection", "doc1")
    results = db.retrieve_similar_documents("test_collection", "test text", top_n=1)
    # Should not return any doc
    assert len(results) == 0
