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

        # fallback if AI fails
        if not opportunity_text:
            print("⚠️ No AI response received — using fallback")

            opportunity_text = """
Build a simple inventory dashboard for a small furniture manufacturer.
Skills: React, FastAPI, PostgreSQL
Difficulty: Medium
"""

        print("🧠 AI RESPONSE:", opportunity_text)

        # ✅ SAVE USING CORRECT COLUMNS
        task = Task(
            task_type="opportunity",
            status="new",
            payload=opportunity_text
        )

        session.add(task)
        session.commit()

        print("✅ Scout saved new opportunity")

    except Exception as e:
        print("❌ Scout error:", e)

        fallback = """
Create CRM for interior design companies.
Skills: Python, UI/UX, Database
Difficulty: Medium
"""

        task = Task(
            task_type="opportunity",
            status="new",
            payload=fallback
        )

        session.add(task)
        session.commit()

        print("⚠️ Saved fallback task")

    finally:
        session.close()
