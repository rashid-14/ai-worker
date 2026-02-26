import os
import time

# Force Linux home
os.environ["HOME"] = "/app"

# Force OpenClaw paths
os.environ["OPENCLAW_HOME"] = "/app"
os.environ["OPENCLAW_WORKSPACE"] = "/app/workspace"

from workspace.runner import main

if __name__ == "__main__":
    while True:
        main()
        time.sleep(5)
