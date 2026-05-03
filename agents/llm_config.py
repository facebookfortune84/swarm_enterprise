import os
import logging
from crewai import LLM
from dotenv import load_dotenv

# Load enterprise-grade environment configurations
load_dotenv(dotenv_path="../.env")

logger = logging.getLogger("SwarmBrain")

class SwarmBrain:
    """
    The Central Intelligence Controller for Swarm Enterprise.
    Implements hybrid-cloud-local routing to ensure zero marginal cost 
    while maintaining elite-level reasoning.
    """

    @staticmethod
    def initialize_isolation():
        """
        Enforces SOP-07 (Networking) and SOP-01 (Governance).
        Nukes all telemetry and redirects OpenAI hooks to the local gateway.
        """
        # Disable all phone-home tracking
        os.environ["CREWAI_SKIP_TELEMETRY"] = "true"
        os.environ["OTEL_SDK_DISABLED"] = "true"
        
        # Security: Force OpenAI libraries to point to the Laptop Bridge
        # This prevents 'Connection Refused' errors to api.openai.com
        ollama_url = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")
        os.environ["OPENAI_API_KEY"] = "NA"
        os.environ["OPENAI_API_BASE"] = f"{ollama_url}/v1"
        
        logger.info("BRAIN_ISOLATION: Sovereignty Protocol Active. Telemetry NUKED.")

    @staticmethod
    def get_manager_brain():
        """
        Level 1 Board & Level 2 Supervisors.
        Uses Groq (Llama-3.3-70B) for 10x faster strategic decomposition.
        Required for complex architectural planning and ticket generation.
        """
        groq_key = os.getenv("GROQ_API_KEY")
        
        # Fallback to worker brain if Groq is unavailable
        if not groq_key or groq_key == "NA":
            logger.warning("BRAIN_FAILOVER: Groq key missing. Falling back to local brain.")
            return SwarmBrain.get_worker_brain(strict=False)
            
        return LLM(
            model="groq/llama-3.3-70b-versatile",
            api_key=groq_key,
            temperature=0.3,  # Low temperature for reliable ticket formatting
            timeout=300,      # 5 minute strategic window
            max_tokens=8192   # High context for the 30-ticket Strategic Masterplan
        )

    @staticmethod
    def get_worker_brain(strict=True):
        """
        Level 3 Worker Pairs (Executor + Critic).
        Uses Local Ollama (Llama-3.2-3B) for private, zero-cost execution.
        Optimized for CPU/RAM inference on the Windows 11 Laptop.
        """
        ollama_url = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")
        
        return LLM(
            model="ollama/llama3.2:3b",
            base_url=ollama_url,
            temperature=0.1 if strict else 0.5, # Strict mode for physical file writes
            timeout=900,  # 15 minute window for heavy coding on CPU
            max_tokens=4096
        )

    @staticmethod
    def get_embedder_config():
        """
        The RAG Memory configuration (SOP-06).
        Ensures all vector math stays local and private.
        """
        return {
            "provider": "ollama",
            "config": {
                "model": "nomic-embed-text:latest",
                "base_url": os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")
            }
        }

# Execute global isolation on module load
SwarmBrain.initialize_isolation()

# Global Instances for internal Swarm access
MANAGER_BRAIN = SwarmBrain.get_manager_brain()
WORKER_BRAIN = SwarmBrain.get_worker_brain()
EMBEDDER_CONFIG = SwarmBrain.get_embedder_config()