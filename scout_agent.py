import os
import json
from google import genai
from models.task import Task
from database import SessionLocal


def run_scout():

    prompt = """
Generate one real freelance opportunity idea.

Return ONLY in this format:

Title:
Skills:
Difficulty:
"""

    session = SessionLocal()

    try:
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

        response = client.models.generate_content(
            model=os.getenv("MODEL"),
            contents=prompt
        )

        opportunity_text = getattr(response, "text", None)

        # ---------- SAFE FALLBACK ----------
        if not opportunity_text:
            print("⚠️ AI empty — using fallback")

            opportunity_text = """
Title: Inventory Dashboard for Furniture Manufacturer
Skills: React, FastAPI, PostgreSQL
Difficulty: Medium
"""

        print("🧠 AI RESPONSE:", opportunity_text)

        # ---------- FIX: CONVERT TO JSON ----------
        payload_json = {
            "text": opportunity_text.strip()
        }

        task = Task(
            task_type="opportunity",
            status="new",
            payload=json.dumps(payload_json)   # 🔥 THIS FIXES YOUR ERROR
        )

        session.add(task)
        session.commit()

        print("✅ Opportunity saved")

    except Exception as e:
        print("❌ Scout error:", e)

        fallback = {
            "text": """Title: CRM for Interior Designers
Skills: Python, UI/UX, Database
Difficulty: Medium"""
        }

        task = Task(
            task_type="opportunity",
            status="new",
            payload=json.dumps(fallback)   # 🔥 ALSO JSON
        )

        session.add(task)
        session.commit()

        print("⚠️ Saved fallback task")

    finally:
        session.close()
