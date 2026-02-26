import os
import time

os.environ["OPENCLAW_HOME"] = "/home/rashi/.openclaw"
os.environ["OPENCLAW_WORKSPACE"] = "/home/rashi/.openclaw/workspace"

from workspace.runner import main

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print("Runner crashed:", e)

        time.sleep(5)
