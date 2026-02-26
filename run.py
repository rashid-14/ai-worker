import os
import pathlib

# Force OpenClaw home inside Railway container
os.environ["HOME"] = "/app"
os.environ["OPENCLAW_HOME"] = "/app/.openclaw"
os.environ["OPENCLAW_WORKSPACE"] = "/app/workspace"

# Create required folders if not exists
pathlib.Path("/app/.openclaw/workspace").mkdir(parents=True, exist_ok=True)
pathlib.Path("/app/workspace").mkdir(parents=True, exist_ok=True)

from workspace.runner import main

if __name__ == "__main__":
    main()
