import os
import time
from google import genai
from models.task import Task
from database import SessionLocal

LAST_API_CALL = 0
COOLDOWN = 3600   # 1 hour cooldown if quota hit

def run_scout():
    global LAST_API_CALL

    session = SessionLocal()

    try:
        now = time.time()

        # ⛔ Avoid API spam if quota hit
        if now - LAST_API_CALL < COOLDOWN:
            print("⏳ Skipping AI call (Cooldown active)")
            return

        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

        prompt = """
Generate ONE real freelance opportunity idea.

Return plain text only.
Include:
Project
Skills
Difficulty
"""

        response = client.models.generate_content(
            model=os.getenv("MODEL"),
            contents=prompt
        )

        opportunity_text = getattr(response, "text", None)

        if not opportunity_text:
            raise Exception("Empty AI response")

        print("🧠 AI RESPONSE:", opportunity_text)

        task = Task(
            task_type="opportunity",
            status="new",
            payload={"text": opportunity_text}
        )

        session.add(task)
        session.commit()

        LAST_API_CALL = time.time()

        print("✅ Scout saved new opportunity")

    except Exception as e:
        print("❌ Scout error:", e)

        LAST_API_CALL = time.time()   # Activate cooldown

        fallback = """
Build a simple CRM for interior designers.
Skills: Python, React, PostgreSQL
Difficulty: Medium
"""

        task = Task(
            task_type="opportunity",
            status="new",
            payload={"text": fallback}
        )

        session.add(task)
        session.commit()

        print("⚠️ Saved fallback task")

    finally:
        session.close()
