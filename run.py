import os
import time

os.environ["HOME"] = "/app"
os.environ["OPENCLAW_HOME"] = "/app"
os.environ["OPENCLAW_WORKSPACE"] = "/app/workspace"

from workspace.runner import main

while True:
    try:
        main()
    except Exception as e:
        print("Worker crashed:", e)
    time.sleep(5)
