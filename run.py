import os
import time
import threading
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ["OPENCLAW_HOME"] = "/home/rashi/.openclaw"
os.environ["OPENCLAW_WORKSPACE"] = "/home/rashi/.openclaw/workspace"

from workspace.runner import main


# Worker runs in background
def worker_loop():
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


# Health server runs as MAIN process
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))

    # Start worker in background
    threading.Thread(target=worker_loop, daemon=True).start()
    logger.info("Worker thread started")

    # Start HTTP server as MAIN process
    server = HTTPServer(("0.0.0.0", port), Handler)
    logger.info(f"Health server running on port {port}")
    server.serve_forever()
