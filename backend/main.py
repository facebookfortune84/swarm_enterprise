import uvicorn
import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

# Internal Modular Imports
from backend.api.routes import router as swarm_router
from backend.api.webhooks import router as webhook_router
from backend.api.auth_routes import router as auth_router
from backend.db.linear_engine import swarm_db
from agents.llm_config import SwarmBrain

# --- 1. PRODUCTION LOGGING CONFIGURATION ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("/app/output/swarm_system.log")
    ]
)
logger = logging.getLogger("SwarmOS")

# --- 2. LIFESPAN MANAGEMENT ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("SYSTEM_BOOT: Initializing Fractal Infrastructure...")
    SwarmBrain.initialize_isolation()
    try:
        # Initialize SQLite and ensure output directories are ready
        os.makedirs("/app/output/src", exist_ok=True)
        logger.info("DB_SYNC: Linear Ticketing Engine is ONLINE.")
    except Exception as e:
        logger.error(f"DB_CRITICAL: Initialization failed: {e}")
    yield
    logger.info("SYSTEM_SHUTDOWN: Cleaning up workforce handles...")
    swarm_db.close()

# --- 3. THE APP INSTANCE ---
app = FastAPI(
    title="Swarm Enterprise OS",
    description="The world's first self-replicating autonomous digital factory.",
    version="1.0.0",
    lifespan=lifespan
)

# --- 4. ENTERPRISE SECURITY & CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://realms2riches.com",
        "https://www.realms2riches.com",
        "https://corp.realms2riches.com",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Trace-ID", "X-Process-Time"]
)

# --- 5. STATIC ASSET EXPOSURE ---
app.mount("/view", StaticFiles(directory="/app/output"), name="view")

# --- 6. ROUTE REGISTRATION ---
app.include_router(swarm_router)
app.include_router(webhook_router)
app.include_router(auth_router)

# --- 7. PRODUCTION ENTRY ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False, workers=4)