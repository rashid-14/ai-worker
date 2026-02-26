import os
import time
import threading
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

os.environ["OPENCLAW_HOME"] = "/home/rashi/.openclaw"
os.environ["OPENCLAW_WORKSPACE"] = "/home/rashi/.openclaw/workspace"

from workspace.runner import main

def health_server():
    port = int(os.environ.get("PORT", 8080))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

        def log_message(self, format, *args):
            pass

    try:
        server = HTTPServer(("0.0.0.0", port), Handler)
        logger.info(f"Health server running on port {port}")
        server.serve_forever()
    except OSError as e:
        logger.error(f"Failed to start health server on port {port}: {e}")
        sys.exit(1)

# Start health server
threading.Thread(target=health_server, daemon=True).start()
time.sleep(1)

logger.info("OpenClaw Worker Started")

while True:
    try:
        main()
    except Exception as e:
        logger.error(f"Agent crashed: {e}", exc_info=True)

    time.sleep(5)
