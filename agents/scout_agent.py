import os
import json
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
            print("⚠️ No AI response received — using fallback")

            opportunity_text = """
Build CRM for interior design companies.
Skills: Python, UI/UX, Database
Difficulty: Medium
"""

        print("🧠 AI RESPONSE:", opportunity_text)

        task = Task(
            task_type="opportunity",
            status="new",
            payload={
                "text": opportunity_text.strip()
            }
        )

        session.add(task)
        session.commit()

        print("✅ Scout saved new opportunity")

    except Exception as e:
        print("❌ Scout error:", e)

        fallback = """
Build inventory dashboard for furniture manufacturers.
Skills: React, FastAPI, PostgreSQL
Difficulty: Medium
"""

        task = Task(
            task_type="opportunity",
            status="new",
            payload={
                "text": fallback.strip()
            }
        )

        session.add(task)
        session.commit()

        print("⚠️ Saved fallback task due to AI failure")

    finally:
        session.close()
