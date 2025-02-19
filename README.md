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
```
vector_db_operations
│
├── vector_db.py         # Python class encapsulating the vector DB logic 
├── api.py               # FastAPI server exposing CRUD endpoints (bonus)
├── test_vector_db.py    # pytest test suite
|── sample.py            # sample code demonstration use of vector_db.py
├── sample_text.txt      # Sample text file for demonstration
├── requirements.txt     # Dependencies
├── README.md
└── .gitignore           # to ignore venv, etc.
```

## Getting Started

1. **Clone the repository**  
   ```
   bash
   git clone https://github.com/mikejmckinney/vector_db_operations.git
   cd vector_db_operations
   ```

2. **Create and activate a virtual environment (optional but recommended)**  
    - `python -m venv venv`
    - `source venv/bin/activate`    # Linux/Mac
    # or
    - `venv\Scripts\activate`       # Windows

3. **Install dependencies**  
    - `pip install -r requirements.txt`

4. **Run the sample code** 
    - You can directly run vector_db.py in a Python shell or integrate it into your own project.  For example:
    ```python
        from vector_db import VectorDB

        db = VectorDB()
        db.delete_collection("example_collection")
        db.create_collection("example_collection")
        db.insert_document("example_collection", "doc1", "Hello world, this is a test.")
        db.insert_document("example_collection", "doc2", "Another piece of text data.")
        results = db.retrieve_similar_documents("example_collection", "test", top_n=2)
        print("Search Results:", results)
    ```

5. **Run tests** 
    - `pytest`

    - This will run the test cases in test_vector_db.py.

6. **RESTful API with FAstAPI**
    - The api.py file includes a basic FastAPI application exposing REST endpoints for each operation.
    - To start the server:
    `uvicorn api:app --reload`
    - Then open your browser at http://127.0.0.1:8000/docs for an auto-generated interactive API documentation.
    - if you're using github codespaces, you can start the server using [Uvicorn](https://www.uvicorn.org/):
        1. set the host to 0.0.0.0 so that it listens on all network interfaces (this is necessary for Codespaces to forward the port):
        `uvicorn api:app --reload --host 0.0.0.0 --port 8000`
            - --reload flag lets the server restart automatically when you change your code.
            - --host 0.0.0.0 setting ensures that the server is accessible from outside the container.
            - Port 8000 is the default, but you can choose another port if you like.
        2. Open the forwarded port (8000) in your browser via the Codespaces interface.
        3. Access the API documentation at http://<codespace-url>:8000/docs to interact with your endpoints.  for example:
        `https://randomworkspaceurl8000.app.github.dev/docs`

## Additional Notes
    - Persisting Data: Chroma is configured to store data in ./chroma_db by default. You can adjust the persist_directory parameter in VectorDB.__init__.
    - Embedding Model: Using the "all-MiniLM-L6-v2" model for SentenceTransformer. You can choose any other model from [Hugging Face Hub](https://huggingface.co/models).
    - Scalability: For larger scale deployments, you may consider a distributed or hosted vector database (e.g., Weaviate, Milvus) and adapt the code accordingly.
