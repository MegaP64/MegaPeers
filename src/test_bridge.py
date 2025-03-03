from memory_bridge import ContextManager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize our Memory Bridge
context_manager = ContextManager()

# Test storing context
test_content = "MegaPeers is designed as a peer-driven economic paradigm that shifts from traditional corporate-driven capitalism to a participatory model."
context_manager.add_context("project_vision", test_content)

# Test retrieving context
results = context_manager.get_relevant_context("What is MegaPeers about?")

print("Retrieved Context:")
for result in results:
    print(f"Content: {result['content']}")
    print(f"Relevance Score: {result['score']}\n")