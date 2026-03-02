import time
import os
import threading
import logging
from fastapi import FastAPI

from database import engine, Base
from agents.scout_agent import run_scout

# Stage 4 Agents
from strategist import run_strategist
from builder_worker import run_builder
from proposal_worker import run_proposal
from delivery_worker import run_delivery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ["OPENCLAW_HOME"] = "/home/rashi/.openclaw"
os.environ["OPENCLAW_WORKSPACE"] = "/home/rashi/.openclaw/workspace"

from workspace.runner import main

app = FastAPI()

# ---------------- DB INIT ---------------- #

def init_db():
    from sqlalchemy.exc import OperationalError

    for i in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("DB connected and table created")
            return
        except OperationalError:
            logger.info("Waiting for DB...")
            time.sleep(3)

# ---------------- HEALTH ---------------- #

@app.get("/")
def health():
    return {"status": "ok"}

# ---------------- WORKFLOW ---------------- #

def run_workflow_cycle(iteration):
    try:
        logger.info(f"Workflow iteration {iteration} started")

        logger.info("🚀 Running Scout...")
        run_scout()

        logger.info("🧠 Running Strategist...")
        run_strategist()

        logger.info("🏗 Running Builder...")
        run_builder()

        logger.info("📦 Running Proposal...")
        run_proposal()

        logger.info("🚚 Running Delivery...")
        run_delivery()

        logger.info(f"Workflow iteration {iteration} completed")

    except Exception as e:
        logger.error(f"Workflow crashed: {e}")

def run_worker():
    logger.info("Worker thread started")

    iteration = 0

    while True:
        iteration += 1
        run_workflow_cycle(iteration)

        # Sleep 10 minutes (Railway safe)
        time.sleep(600)

# ---------------- STARTUP EVENT ---------------- #

@app.on_event("startup")
def startup_event():
    logger.info("🚀 Starting background workflow engine...")
    init_db()
    threading.Thread(target=run_worker, daemon=True).start()
