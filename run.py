import os

# Force Railway workspace path
os.environ["OPENCLAW_HOME"] = "/app"
os.environ["OPENCLAW_WORKSPACE"] = "/app/workspace"

from workspace.runner import main

main()
