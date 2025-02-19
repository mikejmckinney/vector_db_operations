# sample.py
from vector_db import VectorDB

db = VectorDB()
db.delete_collection("example_collection")
db.create_collection("example_collection")
db.insert_document("example_collection", "doc1", "Hello world, this is a test.")
db.insert_document("example_collection", "doc2", "Another piece of text data.")
results = db.retrieve_similar_documents("example_collection", "test", top_n=2)
print("Search Results:", results)
