"""Vector Store module for managing vector embeddings and Pinecone operations."""

import uuid
import logging
import os  # Added for environment variables
from typing import Dict, List

from pinecone import Pinecone
from config import MemoryConfig

class VectorStore:
    """Manages vector storage and retrieval operations using Pinecone."""
    
    def __init__(self, config: MemoryConfig):
        self.config = config
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))  # Ensures API authentication
        self.index = self._initialize_index()
    
    def _initialize_index(self):
        """Initialize or connect to existing Pinecone index."""
        existing_indexes = [index["name"] for index in self.pc.list_indexes()]
        
        if self.config.index_name not in existing_indexes:
            self.pc.create_index(
                name=self.config.index_name,
                dimension=self.config.vector_dimension,
                metric="cosine",  # Added metric for proper indexing
                spec={'serverless': {'cloud': 'aws', 'region': 'us-west-2'}}
            )
        return self.pc.Index(self.config.index_name)
    
    def store_vectors(self, vectors: List[float], metadata: Dict) -> str:
        """Store vectors with metadata in Pinecone index."""
        try:
            vector_id = str(uuid.uuid4())
            vector_data = [{
                'id': vector_id,
                'values': vectors,
                'metadata': metadata
            }]
            self.index.upsert(vectors=vector_data, namespace=self.config.namespace)
            return vector_id
        except Exception as e:
            logging.error("Error storing vectors: %s", e)
            raise
    
    def query_vectors(self, vector: List[float]) -> List[Dict]:
        """Query vectors from Pinecone index."""
        try:
            results = self.index.query(
                vector=vector,
                top_k=self.config.retrieval_config["top_k"],
                namespace=self.config.namespace
            )
            if not results or not hasattr(results, "matches"):
                logging.warning("No matches found.")
                return []
            
            return [match for match in results.matches 
                    if match.score >= self.config.retrieval_config["threshold"]]
        except Exception as e:
            logging.error("Error querying vectors: %s", e)
            return []
