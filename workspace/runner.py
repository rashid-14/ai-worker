import time
import threading
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

def start_health_server():
    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Health server running on port {port}")
    server.serve_forever()

def main():
    print("Runner started")

    # Start health server in background
    threading.Thread(target=start_health_server, daemon=True).start()

    while True:
        print("Loop running...")
        time.sleep(5)
