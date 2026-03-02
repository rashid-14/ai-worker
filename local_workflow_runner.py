from agents.scout_agent import run_scout
from builder_worker import run_builder
from local_proposal_worker import run_local_proposal
from local_delivery_worker import run_local_delivery
import time

def run_full_workflow():

    print("\n--- WORKFLOW STARTED ---\n")

    print("Running Scout...")
    run_scout()

    print("Running Builder...")
    run_builder()

    print("Running Proposal...")
    run_local_proposal()

    print("Running Delivery...")
    run_local_delivery()

    print("\n--- WORKFLOW COMPLETED ---\n")

if __name__ == "__main__":
    run_full_workflow()
