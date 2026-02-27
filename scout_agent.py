import os
import json
from google import genai
from models.task import Task
from database import SessionLocal


def run_scout():

    session = SessionLocal()

    prompt = """
Generate one real freelance opportunity.

Return in format:

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

    except Exception:
        print("⚠️ AI failed → using fallback")

        payload = {
            "text": "Create CRM for interior design companies. Skills: Python, UI/UX, Database. Difficulty: Medium",
            "source": "fallback"
        }

    try:
        task = Task(
            task_type="opportunity",
            status="new",
            payload=payload   # 🚀 IMPORTANT: DO NOT json.dumps
        )

        session.add(task)
        session.commit()

        print("✅ Task saved")

    except Exception as e:
        print("❌ DB Save error:", e)

    finally:
        session.close()
