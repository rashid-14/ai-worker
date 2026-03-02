from database import SessionLocal
from models.proposal import Proposal
from models.solution import Solution

def run_proposal():

    session = SessionLocal()

    try:
        # find solutions without proposal
        solutions = session.query(Solution).all()

        for sol in solutions:
            existing = session.query(Proposal).filter_by(solution_id=sol.id).first()

            if not existing:
                # Instead of generating proposal
                # mark as pending
                proposal = Proposal(
                    solution_id=sol.id,
                    status="pending",
                    payload={"note": "Waiting for local AI"}
                )

                session.add(proposal)
                session.commit()

                print(f"Proposal marked pending for solution {sol.id}")

    except Exception as e:
        print("Proposal worker error:", e)

    finally:
        session.close()
