# Vector Database CRUD in Python

This repository provides a sample Python project that demonstrates how to perform CRUD (Create, Read, Update, Delete) operations on text documents stored in a vector database. It uses [Chroma](https://github.com/chroma-core/chroma) as the backend and [SentenceTransformer](https://www.sbert.net/) for generating embeddings.

## Features

- Create a new collection (or index) for vector data.
- Insert text documents into the collection (with embeddings).
- Update documents by replacing their text content.
- Delete documents by their ID.
- Retrieve the top N most relevant documents given a query text.
- **RESTful API** with FastAPI for all operations.
- Project competencies:
  - python programming
  - vector Database interactions
  - API Design via RESTful web services
  - Testing (TDD) feating`pytest` and test driven development
  - Version Control (Git)
  - Documentation (README)


## Project Structure
```
vector_db_operations
│
├── sample_text.txt      # Sample text file for demonstration
├── requirements.txt     # Dependencies
├── README.md
|── .gitignore           # to ignore venv, etc.
├── src/
│   ├── db.py        # Vector database interaction
|   |── sample.py    # sample code demonstration use of db.py
│   └── api.py      # FastAPI application
└── tests/
    └── test_db.py   # Tests for db.py
```

## Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/mikejmckinney/vector_db_operations.git
   cd vector_db_operations
   ```

2. **Create and activate a virtual environment (optional but recommended)**  
    - `python -m venv venv`
    - `source venv/bin/activate`    # Linux/Mac
    - `venv\Scripts\activate`       # Windows

3. **Install dependencies**  
    - `pip install -r requirements.txt`

## Usage

The `src/vector_db.py` file contains the `VectorDB` class. Refer to `src/sample.py` below for an example showing how to use it:
    ```python
        from vector_db import VectorDB

        db = VectorDB()
        db.delete_collection("example_collection")
        db.create_collection("example_collection")
        db.insert_document("example_collection", "doc1", "Hello world, this is a test.")
        db.insert_document("example_collection", "doc2", "Another piece of text data.")
        results = db.retrieve_similar_documents("example_collection", "test", top_n=2)
        print("Search Results:", results)
        

## Function Explanations
- create_collection(): Creates a new collection in the ChromaDB database.
- insert_document(text): Vectorizes the input text and adds it to the collection.
- update_document(document_id, new_text): Updates the document with the given document_id using the provided new_text.
- delete_document(document_id): Deletes the document with the given document_id.
- retrieve_documents(query_text, n): Searches the collection for the top n documents most similar to the query_text.

## Running Tests
To execute the unit tests, use the following command.
```
pytest tests/
```

## RESTful API with FAstAPI
- The api.py file includes a basic FastAPI application exposing REST endpoints for each operation.
- To start the server:
`uvicorn api:app --reload`
- Then open your browser at http://127.0.0.1:8000/docs for an auto-generated interactive API documentation.
- if you're using github codespaces, you can start the server using [Uvicorn](https://www.uvicorn.org/):
    1. set the host to 0.0.0.0 so that it listens on all network interfaces (this is necessary for Codespaces to forward the port):
    `python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000`
        - --reload flag lets the server restart automatically when you change your code.
        - --host 0.0.0.0 setting ensures that the server is accessible from outside the container.
        - Port 8000 is the default, but you can choose another port if you like.
    2. Open the forwarded port (8000) in your browser via the Codespaces interface.
    3. Access the API documentation at http://<codespace-url>:8000/docs to interact with your endpoints.  for example:
    `https://randomworkspaceurl8000.app.github.dev/docs`
- Example Interactions using curl:
  1. create a Document:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"text": "This is a new document via API."}' http://127.0.0.1:8000/documents/
    ```
  2. Retrieve a Document:
    ```bash
    curl -X GET "http://127.0.0.1:8000/documents/?query_text=API&n=2"
    ```
  3. Update a Document (in this example the id of the document is 1):
    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{"new_text": "Updated text content via API."}' http://127.0.0.1:8000/documents/1
    ```
  4. Delete Document id 1
    ```bash
    curl -X DELETE http://127.0.0.1:8000/documents/1
    ```
  * -X: Specifies http method (POST, GET, PUT, DELETE).
  * -H: sets a header, in this case specifies content type.
  * -d: sends data with the request.

## Important Considerations and Improvements:

- Error Handling (More Robust): The provided code includes basic error handling. For a production-ready API, you would want to implement more comprehensive error handling, including:
  - Handling different types of exceptions (e.g., database connection errors).
  - Returning more specific error codes and messages.
  - Logging errors for debugging.
- Input Validation: Pydantic models provide basic input validation. You might need to add more specific validation rules (e.g., minimum/maximum length of text, allowed characters).
- Authentication and Authorization: For a real-world application, you would need to implement authentication (verifying user identity) and authorization (controlling access to resources) to protect your API. FastAPI has excellent support for this using tools like OAuth2 and JWT (JSON Web Tokens).
- Asynchronous Operations: For very large documents or high traffic, you might want to make your database operations asynchronous to avoid blocking the event loop. ChromaDB supports asynchronous operations, and FastAPI makes it easy to work with async code.
- Database Connection Pooling: For improved performance, consider using a connection pool for your database. This allows you to reuse existing database connections instead of creating a new connection for each request.
- Scaling Consider horizontal scaling by deploying multiple instances of the api service, and running a message queue in front of the vector database.
- Id Generation: Instead of incrementing the collection.count(), use UUIDs to generate ids.
- More complex Retrieval:  Instead of just returning the top N documents, you could explore:
  - Filtering: Allow filtering results based on metadata (if you add metadata to your documents).
  - Relevance Threshold: Only return results above a certain similarity score.
  - Hybrid Search: Combine vector search with keyword-based filtering.
- Deploy the API to a cloud platform

## Additional Notes
    - Persisting Data: Chroma is configured to store data in ./chroma_db by default. You can adjust the persist_directory parameter in VectorDB.__init__.
    - Embedding Model: Using the "all-MiniLM-L6-v2" model for SentenceTransformer. You can choose any other model from [Hugging Face Hub](https://huggingface.co/models).
    - Scalability: For larger scale deployments, you may consider a distributed or hosted vector database (e.g., Weaviate, Milvus) and adapt the code accordingly.

# FAQ

This section addresses common questions about the project's design, implementation, and usage.

## What Are Embedding Models?

An embedding model is a way of converting text (or other data) into numerical vectors so that semantically similar items are close together in vector space. Below is a quick overview of popular embedding model families and how to choose among them.

### 1. SentenceTransformer Models

These models are widely used for semantic search, clustering, and other similarity tasks. They’re available via the [SentenceTransformers](https://www.sbert.net/) library and are built on top of transformer architectures.

- **all-MiniLM-L6-v2**  
  - **Description**: A lightweight model offering a good balance between speed and accuracy.  
  - **Pros**: Fast, efficient, and low resource usage.  
  - **Cons**: Lower accuracy than larger models.  
  - **Use When**: Real-time applications, limited compute resources, and moderate accuracy needs.

- **all-MiniLM-L12-v2**  
  - **Description**: A slightly larger variant than L6.  
  - **Pros**: Better accuracy than L6.  
  - **Cons**: Higher computational cost.  
  - **Use When**: You can handle a bit more compute overhead for better performance.

- **paraphrase-MiniLM-L6-v2**  
  - **Description**: Fine-tuned on paraphrase tasks, good for detecting semantically equivalent sentences.  
  - **Pros**: Efficient and fast for paraphrase detection.  
  - **Cons**: May be less optimal for other tasks.  
  - **Use When**: Tasks where recognizing paraphrases or near-duplicate text is key.

- **paraphrase-mpnet-base-v2**  
  - **Description**: Built on MPNet, known for producing high-quality embeddings.  
  - **Pros**: Very good accuracy and nuanced representations.  
  - **Cons**: Larger and slower than the MiniLM variants.  
  - **Use When**: You need higher accuracy and can afford more compute cost.

- **all-distilroberta-v1**  
  - **Description**: A distilled RoBERTa model for sentence embeddings.  
  - **Pros**: Solid balance between performance and efficiency.  
  - **Cons**: More resource-intensive than MiniLM.  
  - **Use When**: You want robust language understanding with moderate computational requirements.

### 2. BERT-Based Models

- **bert-base-nli-mean-tokens**  
  - **Description**: Early model using average pooling on BERT outputs for sentence embeddings.  
  - **Pros**: Familiar, well-studied baseline.  
  - **Cons**: Slower and less accurate than newer models.  
  - **Use When**: Legacy or baseline comparisons.

### 3. Domain-Specific & Multilingual Models

- **LaBSE (Language-agnostic BERT Sentence Embedding)**  
  - **Description**: Focused on multilingual sentence embeddings.  
  - **Pros**: Great for cross-lingual semantic search, supporting over 100 languages.  
  - **Cons**: Larger and more compute-intensive.  
  - **Use When**: Cross-lingual tasks or multilingual applications.

- **SciBERT, BioBERT, etc.**  
  - **Description**: Specialized for scientific or biomedical text.  
  - **Pros**: Domain-specific terminology handling.  
  - **Cons**: Less effective on general domains.  
  - **Use When**: Your data is mostly scientific papers, medical documents, or other specialized content.

### When to Use Which

- **Speed & Low Resource**: Use MiniLM-based models (e.g., `all-MiniLM-L6-v2`) where quick inference is key.  
- **Higher Accuracy**: Larger models like `paraphrase-mpnet-base-v2` if you have the resources.  
- **Multilingual or Domain-Specific**: Models like LaBSE or SciBERT for specialized use cases.  
- **Baseline/Legacy**: Older BERT-based models for comparisons or systems requiring them.

The best model depends on your project’s requirements (accuracy, speed, resource limits, domain coverage). Experiment with a few models on your dataset to see which works best. 


## Why Use ChromaDB for This Project?

[ChromaDB](https://github.com/chroma-core/chroma) was chose for its simplicity and ease of integration. It offers:
- **Local Persistence**: You can store data in a local folder (using DuckDB under the hood) without complex setup.
- **In-Memory Options**: For smaller or ephemeral projects, Chroma can run entirely in memory.
- **Quick Start**: Minimal code changes to get CRUD operations on vector embeddings up and running.
- **Active Community & Development**: Frequent updates and helpful documentation for new features.

## Alternative Vector Databases

There are many other vector databases, each with its own strengths. Here are a few notable ones:

1. **[Pinecone](https://www.pinecone.io/)**
   - **Description**: Fully managed SaaS vector database.
   - **Pros**: Easy to scale, high availability, and robust performance SLAs.
   - **Cons**: Commercial pricing for larger usage; data is hosted offsite.

2. **[Weaviate](https://www.weaviate.io/)**
   - **Description**: Open-source vector search engine with built-in modules (e.g., text2vec) and cloud hosting options.
   - **Pros**: Rich features like hybrid search, schema-based data modeling, and pre-built transformers.
   - **Cons**: Managing self-hosted Weaviate can be more involved; advanced features might require extra configuration.

3. **[Milvus](https://milvus.io/)**
   - **Description**: High-performance open-source vector database for large-scale similarity search.
   - **Pros**: Optimized for high-throughput, large data volumes; strong community.
   - **Cons**: Some learning curve for setup, plus additional dependencies like etcd for clustering.

4. **[FAISS](https://github.com/facebookresearch/faiss)**
   - **Description**: A library by Facebook AI for efficient similarity search.
   - **Pros**: Very fast, widely used in research and production for approximate nearest neighbor search.
   - **Cons**: Not a full database—more of an indexing library. Requires you to handle persistence and scaling layers yourself.

### When to Use Which

- **ChromaDB**: Great for local development, prototypes, or smaller-scale deployments where ease of setup is key.
- **Pinecone**: Good for fully managed, production-ready services where you don’t want to manage infrastructure.
- **Weaviate**: Handy if you want an all-in-one open-source solution with advanced features like hybrid search, knowledge graphs, etc.
- **Milvus**: Ideal for large-scale, high-throughput vector similarity searches, especially in distributed environments.
- **FAISS**: Useful if you only need a powerful indexing library and can handle storage or clustering on your own.

**Q: What is the overall structure of this project, and why is it organized this way?**

A: The project is structured to promote modularity and separation of concerns. The main components are:

*   **`src/`**: Contains the source code.
    *   **`db.py`**:  Handles all interactions with the vector database (ChromaDB).  This is the data access layer.
    *   **`main.py`**: Contains the FastAPI application, defining the API endpoints and using `db.py` for database operations.
*   **`tests/`**: Contains unit tests for the `db.py` module, written using `pytest`.
*   **`requirements.txt`**: Lists all necessary Python packages and their versions for easy installation.
*   **`README.md`**: Provides project documentation, setup instructions, usage examples, and this FAQ.
*   **`.gitignore`**: Specifies files and directories that should be ignored by Git (e.g., virtual environments, cache files).
*   **`sample_text.txt`**: A sample text file that can be used for testing.

This structure makes the code easier to understand, maintain, and test. The separation of the database logic from the API logic allows for independent modification and potential scaling.

**Q: Why was ChromaDB chosen as the vector database?**

A: ChromaDB was selected for its ease of setup, in-memory capabilities (ideal for development and testing), and simple Python API. It provides a good balance of features and simplicity for this project's scope. While other options like FAISS, Weaviate, Qdrant, or Milvus were considered, ChromaDB's integrated embedding functions and straightforward persistent storage made it a suitable choice. For larger-scale, production deployments, a more specialized vector database might be preferred.

**Q: Which embedding model is used, and why?**

A: The project uses the `all-MiniLM-L6-v2` model from Sentence Transformers. This model provides a good balance between speed and accuracy for generating sentence embeddings. It maps text to a 384-dimensional vector space, capturing semantic meaning efficiently. It's relatively small and fast, making it suitable for this project, while still providing high-quality embeddings.

**Q: How are dependencies managed?**

A: Dependencies are managed using `requirements.txt`.  This file lists all required Python packages (ChromaDB, Sentence Transformers, pytest, FastAPI, Uvicorn) with their specific versions. This ensures consistent environments and avoids compatibility issues. Users can install the dependencies using `pip install -r requirements.txt`.

**Q: Why is using a virtual environment recommended?**

A: A virtual environment isolates the project's dependencies from the global Python installation and other projects. This prevents conflicts that can arise when different projects require different versions of the same package. It keeps your global environment clean and makes the project more portable.

**Q: How is testing handled in this project?**

A: The project uses `pytest` for unit testing, following a test-driven development (TDD) approach. Tests are located in the `tests/` directory and cover the core functionality of the `VectorDB` class. Fixtures are used to create a consistent testing environment.

**Q: What happens if no matches are found during a search?**

A:  If no documents match the search query, the `retrieve_documents` method returns an empty list.  This is a natural consequence of how ChromaDB's `query` method works.

**Q: What is the purpose of the `.gitignore` file?**

A: The `.gitignore` file tells Git which files and directories to exclude from version control.  This typically includes files that are generated during development or are specific to a user's environment, such as virtual environments (`venv/`), pytest cache directories (`.pytest_cache/`), and compiled Python files (`__pycache__/`).  Keeping these files out of the repository keeps it cleaner and smaller.

### Database (`db.py`) Questions

**Q: How does `create_collection` handle existing collections?**

A: The `create_collection` method uses a `try...except` block to handle the case where a collection with the given name already exists. It first attempts to create the collection. If a `UniqueConstraintError` is raised (meaning the collection already exists), it catches the error and retrieves the existing collection.  This ensures the code works correctly in both scenarios.

**Q: How are document IDs generated?  Why use UUIDs?**

A: Document IDs are generated using `uuid.uuid4()`, which creates universally unique identifiers (UUIDs).  UUIDs are used to avoid collisions, even in distributed systems or when documents are inserted from multiple sources concurrently.  This is a more robust approach than simply incrementing a counter.

**Q: Why is error handling important in `update_document` and `delete_document`?**

A: These methods check if a document with the given ID exists *before* attempting to update or delete it. If the ID is not found, a `ValueError` is raised with a descriptive message. This prevents unexpected errors and provides informative feedback to the user, making the application more robust and user-friendly.

**Q: What does `retrieve_documents` return?**

A: `retrieve_documents` takes a query string and the number of results (`n`) as input.  It uses ChromaDB's `query` method to find the `n` documents in the collection most similar to the query text, based on cosine similarity. It returns a *list* containing the *text* of the most relevant documents.

**Q: What is the role of the `embedding_function`?**

A: The `embedding_function` (provided by `sentence-transformers`) is responsible for converting text into numerical vectors (embeddings). These embeddings capture the semantic meaning of the text, allowing ChromaDB to compare documents and queries based on their meaning, not just keyword matches.

### API (`main.py`) Questions

**Q: Why was FastAPI chosen for the API?**

A: FastAPI is a modern, high-performance web framework for building APIs. Its key advantages include:

*   **Speed:** It's very fast, built on Starlette and Uvicorn.
*   **Automatic Data Validation:** Uses Pydantic for data validation, ensuring data integrity.
*   **Automatic Documentation:** Generates interactive API documentation (Swagger UI and ReDoc) automatically.
*   **Ease of Use:**  It's relatively easy to learn and use.

**Q: What is the purpose of the Pydantic models?**

A: The Pydantic models (`Document` and `UpdateDocument`) define the expected structure and data types of the request bodies for the API endpoints. They provide automatic data validation and conversion, making the API more robust and preventing errors caused by invalid input data.

**Q: How does the API interact with the database logic?**

A: The API endpoints in `main.py` create an instance of the `VectorDB` class (from `db.py`) and call its methods (`insert_document`, `retrieve_documents`, etc.) to perform the database operations. This keeps the API logic separate from the database interaction logic.

**Q: How is error handling implemented in the API?**

A: `HTTPException` from FastAPI is used to return standard HTTP error responses.  For example, if a document is not found during an update or delete operation, the API catches the `ValueError` raised by `db.py` and raises an `HTTPException` with a 404 status code (Not Found).

**Q: How can I test the API endpoints?**

A: You can test the API using:

*   **FastAPI's Automatic Documentation:** Access the Swagger UI at `http://127.0.0.1:8000/docs` (when the server is running) to interact with the API and see the request/response formats.
*   **`curl`:** Use `curl` commands in the terminal (examples are provided in the Usage section above).
*   **Postman:** Use a tool like Postman to send HTTP requests and inspect the responses.
* **TestClient** Write unit tests in pytest that uses TestClient provided by FastAPI.

### Vector Database & Embedding Concepts

**Q: What is a vector database, and how does it differ from a relational database?**

A: A vector database stores data as high-dimensional vectors (embeddings) and allows for similarity search based on distance metrics (like cosine similarity). Relational databases, on the other hand, store data in tables and use SQL for querying based on exact matches or relationships. Vector databases excel at finding items that are *semantically similar*, while relational databases are better for structured data and exact matches.

**Q: What are embeddings, and why are they useful?**

A: Embeddings are numerical representations of data (text, images, etc.) that capture semantic meaning. Items with similar meanings have embeddings that are close together in the vector space. This allows for efficient similarity searches and other tasks like clustering and recommendation.

**Q: What is cosine similarity?**

A: Cosine similarity measures the cosine of the angle between two vectors. It ranges from -1 to 1, where:

*   1: Vectors point in the same direction (perfectly similar).
*   0: Vectors are orthogonal (no similarity).
*   -1: Vectors point in opposite directions (completely dissimilar).

It's a common metric for vector similarity because it focuses on the *direction* of the vectors, not their magnitude, which is often more important for representing semantic similarity.

### Potential Improvements

**Q: How could performance be improved for a very large number of documents?**

A: Several approaches could be taken:

*   **Database Choice:** Consider a database optimized for large-scale vector search (e.g., Weaviate, Qdrant, Milvus, or a cloud-based solution).
*   **Asynchronous Operations:** Use asynchronous database operations and `async/await` in FastAPI.
*   **Batching:** Process documents in batches.
*   **Connection Pooling:** Use a database connection pool.
*   **Hardware:** Use more powerful hardware.
*   **Indexing (Advanced):** Explore different indexing techniques (e.g., HNSW, IVF) within the chosen database.
* **Scaling (Advanced):** Deploy multiple API instances and database instances, and utilize a message queue.

**Q: How could authentication and authorization be added?**

A: FastAPI has built-in support for security features using OAuth2 and JSON Web Tokens (JWTs). The general process would involve:

1.  **Authentication:** Verifying user identity (e.g., username/password, API key).
2.  **Authorization:** Determining what resources the authenticated user has access to.

FastAPI's documentation provides detailed guidance on implementing these security measures.