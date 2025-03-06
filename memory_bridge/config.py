class MemoryConfig:
    def __init__(self):
        self.vector_dimension = 1536
        self.index_name = "megapeers-memory"
        self.namespace = "project-context"
        
        # Storage configuration
        self.storage_config = {
            "conversations": "conversations",
            "code_snippets": "code",
            "decisions": "decisions",
            "integrations": "integrations"
        }
        
        # Retrieval settings
        self.retrieval_config = {
            "top_k": 5,
            "threshold": 0.7
        }
        from pinecone import Pinecone, ServerlessSpec
from config import MemoryConfig

class VectorStore:
    def __init__(self):
        self.config = MemoryConfig()
        self.pc = Pinecone()
        self.index = self._initialize_index()
    
    def _initialize_index(self):
        if self.config.index_name not in self.pc.list_indexes():
            self.pc.create_index(
                name=self.config.index_name,
                dimension=self.config.vector_dimension,
                spec=ServerlessSpec()
            )
        return self.pc.Index(self.config.index_name)
    
    def store_vectors(self, vectors, metadata):
        return self.index.upsert(vectors=vectors, namespace=self.config.namespace)
    
    def query_vectors(self, query_vector):
        return self.index.query(
            vector=query_vector,
            top_k=self.config.retrieval_config["top_k"],
            namespace=self.config.namespace
        )
    from langchain.embeddings import OpenAIEmbeddings
from vector_store import VectorStore
from config import MemoryConfig

class MemoryProcessor:
    def __init__(self):
        self.config = MemoryConfig()
        self.vector_store = VectorStore()
        self.embeddings = OpenAIEmbeddings()
    
    def store_conversation(self, text, metadata=None):
        vectors = self.embeddings.embed_text(text)
        return self.vector_store.store_vectors(
            vectors=vectors,
            metadata=metadata or {}
        )
    
    def retrieve_context(self, query):
        query_vector = self.embeddings.embed_text(query)
        results = self.vector_store.query_vectors(query_vector)
        return self._process_results(results)
    
    def _process_results(self, results):
        return [
            {
                'content': match.metadata.get('content', ''),
                'score': match.score
            }
            for match in results.matches
        ]
    from memory_processor import MemoryProcessor
from datetime import datetime

class ContextManager:
    def __init__(self):
        self.processor = MemoryProcessor()
        self.current_context = {}
    
    def add_context(self, category, content):
        timestamp = datetime.now().isoformat()
        metadata = {
            'category': category,
            'timestamp': timestamp,
            'content': content
        }
        
        self.processor.store_conversation(
            text=content,
            metadata=metadata
        )
        
        self.current_context[category] = {
            'content': content,
            'timestamp': timestamp
        }
    
    def get_relevant_context(self, query):
        return self.processor.retrieve_context(query)
    
    def get_current_context(self):
        return self.current_context
    from .config import MemoryConfig
from .vector_store import VectorStore
from .memory_processor import MemoryProcessor
from .context_manager import ContextManager

__all__ = [
    'MemoryConfig',
    'VectorStore',
    'MemoryProcessor',
    'ContextManager'
]

