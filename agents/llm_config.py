import os
import logging
from dotenv import load_dotenv

# Bulletproof multi-version import for LangChain
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    try:
        from langchain_community.chat_models import ChatOpenAI
    except ImportError:
        from langchain.chat_models import ChatOpenAI

load_dotenv(dotenv_path="../.env")
logger = logging.getLogger("SwarmBrain")

class SwarmBrain:
    """
    The Intelligence Controller for Swarm Enterprise.
    Enforces the Sovereignty Protocol by ensuring all Action tasks
    stay local while Strategy tasks use High-Speed Groq.
    """

    @staticmethod
    def initialize_isolation():
        """SOP-07 Enforcement: Nukes telemetry and ensures isolation."""
        os.environ["CREWAI_SKIP_TELEMETRY"] = "true"
        os.environ["OTEL_SDK_DISABLED"] = "true"

    @staticmethod
    def get_manager_brain():
        """
        Tier 1 (Managers) & Tier 2 (Supervisors).
        Uses Groq (Llama-3.3-70b-versatile) for high-scale planning.
        """
        return ChatOpenAI(
            api_key=os.getenv("GROQ_API_KEY", "NO_KEY_PROVIDED"),
            base_url="https://api.groq.com/openai/v1",
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            request_timeout=300,
            max_retries=3
        )

    @staticmethod
    def get_worker_brain():
        """
        Tier 3 (Workers).
        Uses Local Ollama (Llama-3.2-3b) for private action.
        Extended timeout (900s) ensures no choking on large file writes.
        """
        ollama_base = os.getenv("OLLAMA_URL", "http://172.22.96.1:11434")
        return ChatOpenAI(
            api_key="NA",
            base_url=f"{ollama_base}/v1",
            model="llama3.2:3b",
            temperature=0.1,
            request_timeout=900,
            max_retries=3
        )

    @staticmethod
    def get_embedder_config():
        """SOP-06: Local Vector Memory standards."""
        return {
            "provider": "ollama",
            "config": {
                "model": "nomic-embed-text:latest",
                "base_url": os.getenv("OLLAMA_URL", "http://172.22.96.1:11434")
            }
        }

# --- GLOBAL INITIALIZATION ---
SwarmBrain.initialize_isolation()

# Global instances for use throughout the fractal hierarchy
MANAGER_BRAIN = SwarmBrain.get_manager_brain()
WORKER_BRAIN = SwarmBrain.get_worker_brain()
EMBEDDER_CONFIG = SwarmBrain.get_embedder_config()