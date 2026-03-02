from dotenv import load_dotenv
load_dotenv()

import json
from database import SessionLocal
from models.task import Task
from sqlalchemy import update

def run_local_proposal():
    session = SessionLocal()

    try:
        tasks = session.query(Task).filter(Task.status=="built").limit(1).all()

        if not tasks:
            print("No built tasks found")
            return

        for task in tasks:
            print("Creating proposal for:", task.payload)

            proposal_text = f"""
Offer:

Product: CRM for Interior Designers

Pricing:
Basic - $999
Pro - $2499
Enterprise - $4999

Target:
Interior design firms managing projects & quotations

Outcome:
Centralized client & project workflow
"""

            session.execute(
                update(Task)
                .where(Task.id == task.id)
                .values(
                    status="proposed",
                    result=json.dumps({"text": proposal_text})
                )
            )

            session.commit()

            print("Proposal created")

    except Exception as e:
        print("Proposal error:", e)

    finally:
        session.close()

if __name__ == "__main__":
    run_local_proposal()
