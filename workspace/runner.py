import time
import subprocess
import os

TASK_FILE = "/home/rashi/.openclaw/workspace/TASK.md"

while True:
    try:
        with open(TASK_FILE, "r") as f:
            task = f.read().strip()

        if task == "RUN_BROWSER":
            print("Opening Fiverr...")
            subprocess.run(["python3", "/home/rashi/.openclaw/workspace/browser_agent.py"])
            open(TASK_FILE, "w").write("DONE")

        elif task == "CREATE_GIG":
            print("Creating Fiverr Gig...")
            subprocess.run(["python3", "/home/rashi/.openclaw/workspace/gig_creator.py"])
            open(TASK_FILE, "w").write("DONE")

    except Exception as e:
        print("Error:", e)

    time.sleep(5)
