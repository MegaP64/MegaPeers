import uuid
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional
from pinecone import Pinecone
from openai import OpenAIEmbeddings

class MemoryConfig:
    vector_dimension = 1536
    index_name = "megapeers-memory"
    namespace = "project-context"
    
    storage_config = {
        "conversations": "chat-history",
        "code_snippets": "code-base",
        "decisions": "decision-log"
    }
    
    retrieval_config = {
        "top_k": 5,
        "threshold": 0.7
    }

class VectorStore:
    def __init__(self, config: MemoryConfig):
        self.config = config
        self.pc = Pinecone()
        self.index = self._initialize_index()
        
    def _initialize_index(self):
        if self.config.index_name not in self.pc.list_indexes():
            self.pc.create_index(
                name=self.config.index_name,
                dimension=self.config.vector_dimension,
                spec={'serverless': {'cloud': 'aws', 'region': 'us-west-2'}}
            )
        return self.pc.Index(self.config.index_name)
    
    def store_vectors(self, vectors: List[float], metadata: Dict) -> str:
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
            logging.error(f"Error storing vectors: {e}")
            raise
    
    def query_vectors(self, vector: List[float]) -> List[Dict]:
        try:
            results = self.index.query(
                vector=vector,
                top_k=self.config.retrieval_config["top_k"],
                namespace=self.config.namespace
            )
            return [match for match in results.matches 
                   if match.score >= self.config.retrieval_config["threshold"]]
        except Exception as e:
            logging.error(f"Error querying vectors: {e}")
            raise

class MemoryProcessor:
    def __init__(self):
        self.config = MemoryConfig()
        self.vector_store = VectorStore(self.config)
        self.embeddings = OpenAIEmbeddings()
    
    def store_conversation(self, text: str, metadata: Dict) -> str:
        try:
            vector = self.embeddings.embed_text(text)
            if not metadata.get('content'):
                metadata['content'] = text
            return self.vector_store.store_vectors(vector, metadata)
        except Exception as e:
            logging.error(f"Error storing conversation: {e}")
            raise
    
    def retrieve_context(self, query: str) -> List[Dict]:
        try:
            query_vector = self.embeddings.embed_text(query)
            results = self.vector_store.query_vectors(query_vector)
            return self._process_results(results)
        except Exception as e:
            logging.error(f"Error retrieving context: {e}")
            raise
    
    def _process_results(self, results: List[Dict]) -> List[Dict]:
        processed = []
        for match in results:
            if 'content' not in match.metadata:
                logging.warning(f"Missing content in metadata for match {match.id}")
                continue
            processed.append({
                'content': match.metadata['content'],
                'score': match.score
            })
        return processed

class ContextManager:
    def __init__(self):
        self.processor = MemoryProcessor()
        self.current_context: Dict = {}
    
    def add_context(self, category: str, content: str) -> None:
        try:
            timestamp = datetime.now().isoformat()
            metadata = {
                'category': category,
                'timestamp': timestamp,
                'content': content
            }
            
            self.processor.store_conversation(content, metadata)
            self.current_context[category] = {
                'content': content,
                'timestamp': timestamp
            }
        except Exception as e:
            logging.error(f"Error adding context: {e}")
            raise
    
    def get_relevant_context(self, query: str) -> List[Dict]:
        return self.processor.retrieve_context(query)
    
    def get_current_context(self) -> Dict:
        return self.current_context

__all__ = ['MemoryConfig', 'VectorStore', 'MemoryProcessor', 'ContextManager']
