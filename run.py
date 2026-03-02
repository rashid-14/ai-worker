import time
import os
import threading
import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from database import engine, Base
from agents.scout_agent import run_scout
from strategist import run_strategist
from builder_worker import run_builder
from proposal_worker import run_proposal
from delivery_worker import run_delivery

# ---------------- LOGGING ---------------- #

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ---------------- DB INIT ---------------- #

def init_db():
    from sqlalchemy.exc import OperationalError
    for _ in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("DB connected")
            return
        except OperationalError:
            logger.info("Waiting for DB...")
            time.sleep(3)

# ---------------- MODE ---------------- #

RUN_MODE = os.getenv("RUN_MODE", "LOCAL")

# ---------------- WORKFLOW ---------------- #

def run_workflow_cycle():
    try:
        logger.info("🚀 Scout...")
        run_scout()

        logger.info("🧠 Strategist...")
        run_strategist()

        logger.info("🏗 Builder...")
        run_builder()

        if RUN_MODE == "LOCAL":
            logger.info("📦 Proposal...")
            run_proposal()

            logger.info("🚚 Delivery...")
            run_delivery()
        else:
            logger.info("☁️ Cloud mode — skipping Proposal & Delivery")

    except Exception as e:
        logger.error(f"Workflow crashed: {e}")

def worker_loop():
    logger.info("🔁 Continuous workflow started")

    while True:
        run_workflow_cycle()
        time.sleep(600)

# ---------------- LIFESPAN ---------------- #

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Startup triggered")

    init_db()

    def delayed_worker():
        logger.info("⏳ Waiting before starting workflow...")
        time.sleep(20)
        worker_loop()

    threading.Thread(target=delayed_worker, daemon=True).start()

    yield

    logger.info("🛑 App shutdown")

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
