import time
import os
import threading
import logging
from fastapi import FastAPI
import uvicorn

from database import engine, Base
from models import Task
from agents.scout_agent import run_scout
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

# ---------------- HEALTH CHECK ---------------- #

@app.get("/")
def health():
    return {"status": "alive"}

# ---------------- DB INIT ---------------- #

def init_db():
    from sqlalchemy.exc import OperationalError

    for _ in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("DB Ready")
            return
        except OperationalError:
            logger.info("Waiting for DB...")
            time.sleep(2)

# ---------------- WORKFLOW ---------------- #

def run_workflow_loop():
    logger.info("Workflow engine started")

    iteration = 0

    while True:
        iteration += 1
        try:
            logger.info(f"Workflow iteration {iteration}")

            run_scout()
            run_strategist()
            run_builder()
            run_proposal()
            run_delivery()

        except Exception as e:
            logger.error(f"Workflow crashed: {e}")

        time.sleep(600)

# ---------------- STARTUP ---------------- #

@app.on_event("startup")
def startup_event():
    logger.info("Starting app...")

    # Start workflow AFTER small delay
    def delayed_start():
        time.sleep(5)
        init_db()
        run_workflow_loop()

    threading.Thread(target=delayed_start, daemon=True).start()

# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Booting FastAPI on {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
