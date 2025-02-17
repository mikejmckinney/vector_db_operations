# Vector Database CRUD in Python

This repository provides a sample Python project that demonstrates how to perform CRUD (Create, Read, Update, Delete) operations on text documents stored in a vector database. It uses [Chroma](https://github.com/chroma-core/chroma) as the backend and [SentenceTransformer](https://www.sbert.net/) for generating embeddings.

## Features

- Create a new collection (or index) for vector data.
- Insert text documents into the collection (with embeddings).
- Update documents by replacing their text content.
- Delete documents by their ID.
- Retrieve the top N most relevant documents given a query text.
- (Bonus) **RESTful API** with FastAPI for all operations.

## Project Structure

vector_db_operations
│
├── vector_db.py         # Python class encapsulating the vector DB logic 
├── api.py               # FastAPI server exposing CRUD endpoints (bonus)
├── test_vector_db.py    # pytest test suite
├── sample_text.txt      # Sample text file for demonstration
├── requirements.txt     # Dependencies
├── README.md
└── .gitignore           # to ignore venv, etc.
