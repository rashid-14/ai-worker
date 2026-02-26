import os
import time

os.environ["HOME"] = "/app"
os.environ["OPENCLAW_HOME"] = "/app"
os.environ["OPENCLAW_WORKSPACE"] = "/app/workspace"

from workspace.runner import main

print("Worker started...")

while True:
    main()
    time.sleep(10)
