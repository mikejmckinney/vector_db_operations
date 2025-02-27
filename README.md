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
        `python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000`
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

# FAQ

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

## How did you handle dependencies?  What is the purpose of requirements.txt
- requirements.txt specifies all the Python packages needed for the project, including ChromaDB, Sentence Transformers, pytest, FastAPI, and Uvicorn. This allows anyone to easily recreate the project's environment using pip install -r requirements.txt. It ensures that everyone is using the same versions of the libraries, avoiding compatibility issues.

## Why is a virtual environment recommended?
- Using a virtual environment isolates the project's dependencies from the global Python installation and from other projects. This prevents conflicts if different projects require different versions of the same library. It keeps your global environment clean and makes your project more portable

## Describe your approach to testing. Why did you use pytest?
- I followed a test-driven development approach, writing unit tests using pytest before implementing the corresponding functionality in the VectorDB class. This helped ensure that the code meets the requirements and is robust. pytest is a widely used testing framework that provides features like fixtures (like the vector_db fixture I used) to set up a consistent testing environment for each test case, making the tests more organized and easier to write

