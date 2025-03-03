"""Memory Processor module for handling vector embeddings and context management."""

import logging
import os  
from typing import Dict, List

from openai import OpenAIEmbeddings
from vector_store import VectorStore
from config import MemoryConfig


class MemoryProcessor:
    """Processes and manages memory operations including storing and retrieving context."""

    def __init__(self):
        self.config = MemoryConfig()
        self.vector_store = VectorStore(self.config)
        self.embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

    def store_conversation(self, text: str, metadata: Dict) -> str:
        """Store conversation text with metadata and return vector ID."""
        try:
            vector = self.embeddings.embed_documents([text])[0]
            if not metadata.get("content"):
                metadata["content"] = text
            return self.vector_store.store_vectors(vector, metadata)
        except Exception as e:
            logging.error("Error storing conversation: %s", e)
            raise

    def retrieve_context(self, query: str) -> List[Dict]:
        """Retrieve relevant context based on query string."""
        try:
            query_vector = self.embeddings.embed_query(query)
            results = self.vector_store.query_vectors(query_vector)
            return self._process_results(results)
        except Exception as e:
            logging.error("Error retrieving context: %s", e)
            raise

    def _process_results(self, results: List[Dict]) -> List[Dict]:
        """Process and format query results safely."""
        processed = []
        if not results:
            logging.warning("No relevant matches found.")
            return []
        for match in results:
            if "content" not in match.metadata:
                logging.warning("Missing content in metadata for match %s", match.get("id", "Unknown"))
                continue
            processed.append({"content": match.metadata["content"], "score": match.score})
        return processed

    def _process_results_simple(self, results: List[Dict]) -> List[Dict]:
        """Basic result processing without extra validation."""
        processed = []
        for match in results:
            if "content" not in match.metadata:
                logging.warning("Missing content in metadata for match %s", match.id)
                continue
            processed.append(
                {"content": match.metadata["content"], "score": match.score}
            )
        return processed
