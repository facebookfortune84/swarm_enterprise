import uvicorn
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

# Modular Imports - These align with our Stage 1 Blueprint
from backend.api.routes import router as swarm_router
from backend.api.webhooks import router as webhook_router
from backend.api.auth_routes import router as auth_router
from backend.db.linear_engine import swarm_db
from agents.llm_config import SwarmBrain

# --- 1. LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("/app/output/swarm_system.log")]
)
logger = logging.getLogger("SwarmOS")

# --- 2. LIFESPAN ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("SYSTEM_BOOT: Initializing Fractal Infrastructure...")
    # Initialize Sovereignty
    SwarmBrain.initialize_isolation()
    # Initialize SQLite Linear Engine
    try:
        os.makedirs("/app/output/src", exist_ok=True)
        logger.info("DB_SYNC: Linear Engine is ONLINE.")
    except Exception as e:
        logger.error(f"DB_CRITICAL: {e}")
    yield
    swarm_db.close()

# --- 3. APP INSTANCE ---
app = FastAPI(title="Swarm Enterprise OS", lifespan=lifespan)

# --- 4. CORS & SECURITY ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # We use '*' temporarily to ensure the 1033/CORS stops
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 5. STATIC VIEWER ---
app.mount("/view", StaticFiles(directory="/app/output"), name="view")

# --- 6. ROUTE REGISTRATION ---
app.include_router(swarm_router)
app.include_router(webhook_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=4)