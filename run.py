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


def worker_loop():
    logger.info("Worker loop started")
    while True:
        try:
            main()
        except Exception as e:
            logger.error(f"Worker crashed: {e}", exc_info=True)
        time.sleep(5)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))

    # Start worker in background thread
    thread = threading.Thread(target=worker_loop)
    thread.start()

    # Start health server in main thread (important)
    server = HTTPServer(("0.0.0.0", port), Handler)
    logger.info(f"Health server running on port {port}")
    server.serve_forever()
