# Test sync with GitHub
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uuid
from pinecone import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

# Initialize FastAPI
app = FastAPI()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "MegaBridge API is running!"}

# Request model for storing memory
class MemoryRequest(BaseModel):
    text: str

@app.post("/store_memory")
def store_memory(request: MemoryRequest):
    """Store a new memory in Pinecone."""
    try:
        # Generate a unique ID for the memory
        memory_id = str(uuid.uuid4())

        # Convert text to vector using OpenAI Embeddings
        vector = embeddings.embed_query(request.text)  # FIXED: Use embed_query() instead of embed_documents()

        # Store vector in Pinecone
        index.upsert(
            vectors=[{"id": memory_id, "values": vector, "metadata": {"content": request.text}}]
        )

        return {"message": "Memory stored successfully!", "id": memory_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing memory: {str(e)}")

# Request model for retrieving memory
class QueryRequest(BaseModel):
    query: str

@app.post("/retrieve_memory")
def retrieve_memory(request: QueryRequest):
    """Retrieve the most relevant stored memory from Pinecone."""
    try:
        # Convert query to vector
        query_vector = embeddings.embed_query(request.query)  # FIXED: Use embed_query() instead of embed_documents()

        # Query Pinecone for similar vectors
        results = index.query(vector=query_vector, top_k=1, include_metadata=True)

        # Return the best match
        if results.get("matches"):
            return {"retrieved_memory": results["matches"][0]["metadata"]["content"]}
        else:
            return {"message": "No relevant memory found."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving memory: {str(e)}")
