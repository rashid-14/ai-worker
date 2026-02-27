import time
import os
from database import engine, Base
from agents.scout_agent import run_scout
from models.task import Task
import threading
import logging
from fastapi import FastAPI
import uvicorn

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


last_scout_run = 0

def run_worker():
    global last_scout_run
    logger.info("Worker thread started")

    iteration = 0

    while True:
        iteration += 1
        try:
            logger.info(f"Worker iteration {iteration} started")

            current_time = time.time()

            # Run scout only every 30 minutes
            if current_time - last_scout_run > 1800:
                print("🚀 RUNNING SCOUT (Cooldown Passed)")
                run_scout()
                last_scout_run = current_time
                print("✅ SCOUT DONE")
            else:
                print("⏳ Cooldown active... waiting")

            logger.info(f"Worker iteration {iteration} completed")

        except Exception as e:
            logger.error(f"Worker crashed: {e}")

        # Check every 60 seconds
        time.sleep(60)

threading.Thread(target=run_worker, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting FastAPI on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

