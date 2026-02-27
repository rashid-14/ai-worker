import os
import time
from google import genai
from models.task import Task
from database import SessionLocal

# Cooldown to avoid hitting quota repeatedly
AI_COOLDOWN_SECONDS = 3600   # 1 hour
last_ai_failure_time = 0


def run_scout():
    global last_ai_failure_time

    session = SessionLocal()

    try:
        now = time.time()

        # 🚫 Skip AI if recently failed
        if now - last_ai_failure_time < AI_COOLDOWN_SECONDS:
            print("⏳ AI cooldown active — using fallback opportunity")
            raise Exception("AI Cooldown Active")

        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

        prompt = """
Generate one real freelance opportunity idea for a developer.

Return in this format:

Project:
Skills:
Difficulty:
"""

        response = client.models.generate_content(
            model=os.getenv("MODEL"),
            contents=prompt
        )

        opportunity_text = getattr(response, "text", None)

        if not opportunity_text:
            raise Exception("Empty AI response")

        print("🧠 AI Opportunity Generated")

        payload_data = {
            "text": opportunity_text.strip()
        }

        task = Task(
            task_type="opportunity",
            assigned_to=None,
            status="new",
            payload=payload_data
        )

        session.add(task)
        session.commit()

        print("✅ Opportunity saved from AI")

    except Exception as e:
        print("⚠️ AI unavailable:", e)

        # mark failure time
        last_ai_failure_time = time.time()

        fallback_text = """
Create CRM system for interior design companies
Skills: Python, React, PostgreSQL
Difficulty: Medium
"""

        payload_data = {
            "text": fallback_text.strip()
        }

        task = Task(
            task_type="opportunity",
            assigned_to=None,
            status="new",
            payload=payload_data
        )

        session.add(task)
        session.commit()

        print("🟡 Fallback opportunity saved")

    finally:
        session.close()
