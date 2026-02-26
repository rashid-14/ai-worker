import os
import time

os.environ["OPENCLAW_HOME"] = "/home/rashi/.openclaw"
os.environ["OPENCLAW_WORKSPACE"] = "/home/rashi/.openclaw/workspace"

from workspace.runner import main

if __name__ == "__main__":
    while True:
        try:
            print("Running OpenClaw loop...")
            main()
        except Exception as e:
            print("Error:", e)
        
        print("Restarting runner in 5 sec...")
        time.sleep(5)
