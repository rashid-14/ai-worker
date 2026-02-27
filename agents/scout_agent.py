import os
from google import genai
from models.task import Task
from database import SessionLocal


def run_scout():
    prompt = "Generate one real freelance opportunity idea for a developer. Include project type, required skills and difficulty."

    session = SessionLocal()

    try:
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

        response = client.models.generate_content(
            model=os.getenv("MODEL"),
            contents=prompt
        )

        opportunity_text = getattr(response, "text", None)

        if not opportunity_text:
            raise Exception("Empty AI response")

        print("AI RESPONSE:", opportunity_text)

    except Exception as e:
        print("Scout error:", e)

        opportunity_text = """
Create CRM for interior design companies.
Skills: Python, UI/UX, Database
Difficulty: Medium
"""

    # ✅ SAVE AS STRING (NOT DICT)
    try:
        task = Task(
            task_type="opportunity",
            status="new",
            payload=opportunity_text.strip()   # <-- IMPORTANT FIX
        )

        session.add(task)
        session.commit()

        print("Opportunity saved")

    except Exception as db_error:
        print("DB Save error:", db_error)

    finally:
        session.close()
