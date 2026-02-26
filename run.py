import os
from workspace.runner import main

print("OpenClaw Worker Started")

while True:
    try:
        main()
    except Exception as e:
        print("Agent crashed:", e)
