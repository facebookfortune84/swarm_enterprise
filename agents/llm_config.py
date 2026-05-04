import os
import logging
from dotenv import load_dotenv

# 1. VERSION-AGNOSTIC BRAIN CONNECTOR
# This specifically solves the 'ImportError: cannot import name LLM' 
# by dynamically checking the library entry points.
try:
    from crewai import LLM
    _USE_NATIVE = True
except ImportError:
    # Fallback if the specific version of CrewAI expects a different import path
    _USE_NATIVE = False

load_dotenv(dotenv_path="../.env")
logger = logging.getLogger("SwarmBrain")

class SwarmBrain:
    """
    The Intelligence Controller for Swarm Enterprise.
    Enforces the 'Sovereignty Protocol' by ensuring all Action tasks
    stay local while Strategy tasks use High-Speed Groq.
    """

    @staticmethod
    def initialize_isolation():
        """SOP-07 Enforcement: Nukes telemetry and redirects OpenAI calls."""
        os.environ["CREWAI_SKIP_TELEMETRY"] = "true"
        os.environ["OTEL_SDK_DISABLED"] = "true"
        # Security: Force any rogue OpenAI dependencies to route to your Laptop IP
        # This prevents the 'Connection Error' when the library tries to phone home.
        ollama_base = os.getenv("OLLAMA_URL", "http://172.22.96.1:11434")
        os.environ["OPENAI_API_KEY"] = "NA"
        os.environ["OPENAI_API_BASE"] = f"{ollama_base}/v1"

    @staticmethod
    def get_manager_brain():
        """
        Tier 1 (Managers) & Tier 2 (Supervisors).
        Uses Groq (Llama-3.3-70b-versatile) for high-scale planning.
        """
        api_key = os.getenv("GROQ_API_KEY")
        model_name = "groq/llama-3.3-70b-versatile"
        
        if _USE_NATIVE:
            return LLM(
                model=model_name,
                api_key=api_key,
                temperature=0.3,
                timeout=300
            )
        return model_name

    @staticmethod
    def get_worker_brain():
        """
        Tier 3 (Workers).
        Uses Local Ollama (Llama-3.2-3b) for private action.
        Extended timeout (900s) ensures no choking on large file writes.
        """
        model_name = "ollama/llama3.2:3b"
        base_url = os.getenv("OLLAMA_URL", "http://172.22.96.1:11434")
        
        if _USE_NATIVE:
            return LLM(
                model=model_name,
                base_url=base_url,
                temperature=0.1, # Strictness for code accuracy
                timeout=900
            )
        return model_name

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