import os
import json
from google import genai
from models.task import Task
from database import SessionLocal


def run_scout():

    session = SessionLocal()

    prompt = """
Generate one real freelance opportunity idea.

Return in this format:

Project:
Skills:
Difficulty:
"""

    try:
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

        response = client.models.generate_content(
            model=os.getenv("MODEL"),
            contents=prompt
        )

        ai_text = getattr(response, "text", None)

        if not ai_text:
            raise Exception("Empty AI response")

        payload = {
            "text": ai_text.strip(),
            "source": "ai"
        }

    except Exception as e:
        print("⚠️ AI Failed — using fallback")

        payload = {
            "text": """Build CRM for interior design companies.
Skills: Python, UI/UX, Database
Difficulty: Medium""",
            "source": "fallback"
        }

    try:
        task = Task(
            task_type="opportunity",
            status="new",
            payload=json.dumps(payload)   # ✅ ALWAYS JSON
        )

        session.add(task)
        session.commit()

        print("✅ Opportunity saved")

    except Exception as db_error:
        print("❌ DB Save error:", db_error)

    finally:
        session.close()
