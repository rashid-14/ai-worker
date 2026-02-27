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

        # If AI fails → use fallback
        if not opportunity_text:
            print("⚠️ No AI response — using fallback")

            opportunity_text = """
Fallback Opportunity:
Build CRM for furniture manufacturers.
Skills: React, FastAPI, PostgreSQL
Difficulty: Medium
"""

        print("🧠 AI RESPONSE:", opportunity_text)

    except Exception as e:
        print("❌ Scout error:", e)

        opportunity_text = """
Fallback Opportunity:
Create CRM for interior design companies.
Skills: Python, UI/UX, Database
Difficulty: Medium
"""

    # ✅ ALWAYS SAVE (AI or fallback)

    try:
        task = Task(
            task_type="opportunity",
            status="new",
            payload=opportunity_text   # TEXT not dict
        )

        session.add(task)
        session.commit()

        print("✅ Opportunity saved")

    except Exception as db_error:
        print("❌ DB Save error:", db_error)

    finally:
        session.close()
