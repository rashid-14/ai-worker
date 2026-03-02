import time
import os
import threading
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from database import init_db
from database import engine, Base
from agents.scout_agent import run_scout
from strategist import run_strategist
from builder_worker import run_builder
from proposal_worker import run_proposal
from delivery_worker import run_delivery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- DB INIT ---------------- #

def init_db():
    from sqlalchemy.exc import OperationalError
    for i in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("DB connected")
            return
        except OperationalError:
            logger.info("Waiting for DB...")
            time.sleep(3)

# ---------------- WORKFLOW ---------------- #

def run_workflow_cycle():
    try:
        logger.info("🚀 Scout...")
        run_scout()

        logger.info("🧠 Strategist...")
        run_strategist()

        logger.info("🏗 Builder...")
        run_builder()

        logger.info("📦 Proposal...")
        run_proposal()

        logger.info("🚚 Delivery...")
        run_delivery()

    except Exception as e:
        logger.error(f"Workflow crashed: {e}")

def run_worker_loop():
    logger.info("Worker loop started")
    while True:
        run_workflow_cycle()
        time.sleep(600)

# ---------------- LIFESPAN ---------------- #

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App startup")

    init_db()

    def delayed_worker_start():
        logger.info("Waiting for network warmup...")
        time.sleep(20)
        run_worker_loop()

    # start worker AFTER API is alive
    threading.Thread(target=delayed_worker_start, daemon=True).start()

    yield

    logger.info("App shutdown")

# ---------------- FASTAPI ---------------- #

app = FastAPI(lifespan=lifespan)

@app.get("/")
def health():
    return {"status": "alive"}

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting server on {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
