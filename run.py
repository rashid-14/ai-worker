import os
import time
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

@app.get("/")
def health():
    return {"status": "ok"}

def run_worker():
    logger.info("Worker thread started")
    iteration = 0
    while True:
        iteration += 1
        try:
            logger.info(f"Worker iteration {iteration} started")
            main()
            logger.info(f"Worker iteration {iteration} completed")
        except Exception as e:
            logger.error(f"Worker crashed: {e}")
        time.sleep(5)

threading.Thread(target=run_worker, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting FastAPI on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
