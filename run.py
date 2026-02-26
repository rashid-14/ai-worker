import os
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

os.environ["OPENCLAW_HOME"] = "/home/rashi/.openclaw"
os.environ["OPENCLAW_WORKSPACE"] = "/home/rashi/.openclaw/workspace"

from workspace.runner import main


# ---- Dummy Health Server ----
def health_server():
    port = int(os.environ.get("PORT", 8080))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Health server running on port {port}")
    server.serve_forever()


# Run health server in background
threading.Thread(target=health_server, daemon=True).start()


print("OpenClaw Worker Started")

while True:
    try:
        main()
    except Exception as e:
        print("Agent crashed:", e)

    time.sleep(5)
