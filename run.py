import os
import time

os.environ["OPENCLAW_HOME"] = "/app"
os.environ["OPENCLAW_WORKSPACE"] = "/app/workspace"

from workspace.runner import main

if __name__ == "__main__":
    print("OpenClaw Worker Started...")
    while True:
        try:
            main()
        except Exception as e:
            print("Worker error:", e)
        time.sleep(5)
