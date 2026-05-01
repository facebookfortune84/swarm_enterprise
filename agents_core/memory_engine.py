import os
import chromadb
from langchain_community.embeddings import OllamaEmbeddings

class SwarmMemory:
    def __init__(self):
        # Point to your Laptop (Windows 11) for embeddings
        self.embedding_fn = OllamaEmbeddings(
            model="nomic-embed-text", 
            base_url=os.getenv("OLLAMA_URL")
        )
        # Persistent storage on the Windows Server VM
        self.client = chromadb.PersistentClient(path="./memory/chroma_db")
        self.collection = self.client.get_or_create_collection(name="swarm_brain")

    def remember(self, key, content, metadata=None):
        """Saves a code snippet or logic pattern."""
        self.collection.add(
            documents=[content],
            metadatas=[metadata or {"type": "general"}],
            ids=[key]
        )

    def recall(self, query, n=3):
        """Retrieves the most relevant past experiences."""
        return self.collection.query(query_texts=[query], n_results=n)

memory = SwarmMemory()