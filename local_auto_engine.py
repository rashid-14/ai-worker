from agents.scout_agent import run_scout
from builder_worker import run_builder
from local_proposal_worker import run_local_proposal
from local_delivery_worker import run_local_delivery
import time

def run_full_workflow():

    print("\n==============================")
    print("🚀 AI WORKFLOW STARTED")
    print("==============================\n")

    try:
        print("🔎 Running Scout...")
        run_scout()
    except Exception as e:
        print("Scout failed:", e)

    try:
        print("🏗 Running Builder...")
        run_builder()
    except Exception as e:
        print("Builder failed:", e)

    try:
        print("📦 Running Proposal...")
        run_local_proposal()
    except Exception as e:
        print("Proposal failed:", e)

    try:
        print("🚚 Running Delivery...")
        run_local_delivery()
    except Exception as e:
        print("Delivery failed:", e)

    print("\n✅ WORKFLOW COMPLETED\n")

def run_continuous_engine():

    print("🟢 AI Business Engine Running Continuously...\n")

    cycle = 1

    while True:
        print(f"\n🔁 Cycle {cycle} started...\n")

        run_full_workflow()

        print("⏳ Waiting 5 minutes before next cycle...\n")
        time.sleep(300)   # 5 minutes

        cycle += 1

if __name__ == "__main__":
    run_continuous_engine()
