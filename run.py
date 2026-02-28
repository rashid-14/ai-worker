import time
import os
from database import engine, Base
from models import Task
from agents.scout_agent import run_scout
import threading
import logging
from fastapi import FastAPI
import uvicorn

# NEW imports for Stage 4
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

def init_db():
    import time
    from sqlalchemy.exc import OperationalError

    for i in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            print("DB connected and table created")
            return
        except OperationalError:
            print("Waiting for DB...")
            time.sleep(3)

init_db()

@app.get("/")
def health():
    return {"status": "ok"}


# ---------------- WORKFLOW ENGINE ---------------- #

def run_workflow_cycle(iteration):
    try:
        logger.info(f"Workflow iteration {iteration} started")

        print("🚀 Running Scout...")
        run_scout()
        print("✅ Scout Completed")

        print("🧠 Running Strategist...")
        run_strategist()
        print("✅ Strategist Completed")

        print("🏗 Running Builder...")
        run_builder()
        print("✅ Builder Completed")

        print("📦 Running Proposal...")
        run_proposal()
        print("✅ Proposal Completed")

        print("🚚 Running Delivery...")
        run_delivery()
        print("✅ Delivery Completed")

        logger.info(f"Workflow iteration {iteration} completed")

    except Exception as e:
        logger.error(f"Workflow crashed: {e}")


def run_worker():
    logger.info("Worker thread started")

    iteration = 0

    while True:
        iteration += 1
        run_workflow_cycle(iteration)

        # Sleep 10 mins to stay safe with Railway quota
        time.sleep(600)


threading.Thread(target=run_worker, daemon=True).start()

# ---------------- FASTAPI ---------------- #

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting FastAPI on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
