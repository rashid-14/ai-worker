import time
from agents.scout import run_scout
from agents.strategist import run_strategist
from agents.builder import run_builder
from agents.proposal import run_proposal
from agents.delivery import run_delivery

while True:
    print("Running Workflow Cycle...")

    run_scout()
    run_strategist()
    run_builder()
    run_proposal()
    run_delivery()

    print("Cycle complete. Sleeping...")
    time.sleep(3600)
