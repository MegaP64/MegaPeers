"""Context Manager module for handling stored context and retrieval."""

import logging
from datetime import datetime
from typing import Dict, List

from memory_processor import MemoryProcessor

class ContextManager:
    """Manages conversation context storage and retrieval."""

    def __init__(self):
        self.processor = MemoryProcessor()
        self.current_context: Dict[str, Dict] = {}

    def add_context(self, category: str, content: str) -> None:
        """Store and track new context."""
        try:
            timestamp = datetime.now().isoformat()
            metadata = {
                'category': category,
                'timestamp': timestamp,
                'content': content
            }

            self.processor.store_conversation(text=content, metadata=metadata)

            self.current_context[category] = {
                'content': content,
                'timestamp': timestamp
            }
        except Exception as e:
            logging.error(f"Error adding context: {e}")

    def get_relevant_context(self, query: str) -> List[Dict]:
        """Retrieve relevant stored context."""
        results = self.processor.retrieve_context(query)
        return results if results else []

    def get_current_context(self) -> Dict[str, Dict]:
        """Retrieve the most recent stored context."""
        return self.current_context
