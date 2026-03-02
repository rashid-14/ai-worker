from dotenv import load_dotenv
load_dotenv()

import json
from database import SessionLocal
from models.task import Task

def run_local_delivery():

    session = SessionLocal()

    try:
        # Only pick tasks that are proposed but NOT delivered
        tasks = session.query(Task).filter(Task.status=="proposed").all()

        if not tasks:
            print("No proposed tasks found")
            return

        for task in tasks:

            # Skip if already delivered
            if task.status == "delivered":
                continue

            # Skip if execution already exists
            if task.result and "Execution Plan" in str(task.result):
                continue

            print("Creating delivery plan for:", task.payload)

            delivery_text = """
Execution Plan:

Phase 1:
Client onboarding & requirement setup

Phase 2:
CRM modules setup:
- Client Management
- Project Tracking
- Quotation System

Phase 3:
Dashboard & Reporting

Phase 4:
Deployment & Handover

Outcome:
Interior design firm gets complete client & project management system ready for use.
"""

            task.status = "delivered"
            task.result = json.dumps({"text": delivery_text})

            session.commit()

            print("Delivery plan created")

    except Exception as e:
        print("Delivery error:", e)

    finally:
        session.close()


if __name__ == "__main__":
    run_local_delivery()
