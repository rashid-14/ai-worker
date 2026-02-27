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

        # ---------- AI FAILED ----------
        if not opportunity_text:
            print("⚠️ No AI response — using fallback")

            opportunity_text = """
Build a simple inventory dashboard for furniture manufacturers.
Skills: React, FastAPI, PostgreSQL
Difficulty: Medium
"""

        print("🧠 AI RESPONSE:", opportunity_text)

        # ✅ SAVE AS JSON (IMPORTANT)
        payload_json = {
            "text": opportunity_text.strip()
        }

        task = Task(
            task_type="opportunity",
            assigned_to=None,
            status="new",
            payload=payload_json,
            result=None
        )

        session.add(task)
        session.commit()

        print("✅ Scout saved new opportunity")

    except Exception as e:
        print("❌ Scout error:", e)

        fallback = {
            "text": "Create CRM for interior design companies. Skills: Python, UI/UX, Database. Difficulty: Medium"
        }

        task = Task(
            task_type="opportunity",
            assigned_to=None,
            status="new",
            payload=fallback,
            result=None
        )

        session.add(task)
        session.commit()

        print("⚠️ Saved fallback task")

    finally:
        session.close()
