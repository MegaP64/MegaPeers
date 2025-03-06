"""Memory Bridge test module for validating context management functionality."""

from context_manager import ContextManager
from dotenv import load_dotenv

def run_tests():
    """Execute Memory Bridge functionality tests including context storage and retrieval."""
    # Load environment variables
    try:
        load_dotenv()
    except FileNotFoundError as env_error:
        print(f"Error loading environment variables: {env_error}")
        return

    # Initialize our Memory Bridge
    try:
        context_manager = ContextManager()
    except ImportError as manager_error:
        print(f"Error initializing ContextManager: {manager_error}")
        return

    # Test storing context
    test_content = ("MegaPeers is designed as a peer-driven economic paradigm that shifts "
                   "from traditional corporate-driven capitalism to a participatory model.")

    try:
        context_manager.add_context("project_vision", test_content)
        print("Successfully added context.")
    except ImportError as context_error:
        print(f"Error adding context: {context_error}")
        return

    # Test retrieving context
    try:
        results = context_manager.get_relevant_context("What is MegaPeers about?")
        print("Retrieved Context:")
        if not results:
            print("No relevant context found.")
        else:
            for result in results:
                print(f"Content: {result['content']}")
                print(f"Relevance Score: {result['score']}")
    except ImportError as retrieve_error:
        print(f"Error retrieving context: {retrieve_error}")

if __name__ == "__main__":
    run_tests()
    