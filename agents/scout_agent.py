import os
import json
from google import genai
from models.task import Task
from database import SessionLocal


def run_scout():

    prompt = """
Generate one real freelance opportunity idea for a developer.
Include:

Project Title
Required Skills
Difficulty (Easy / Medium / Hard)
Short Description
"""

    session = SessionLocal()

    try:
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

        response = client.models.generate_content(
            model=os.getenv("MODEL"),
            contents=prompt
        )

        opportunity_text = getattr(response, "text", None)

        # 🛟 SAFETY FALLBACK if AI fails
        if not opportunity_text:
            print("⚠️ No AI response — using fallback")

            opportunity_text = """
Build Inventory Dashboard for Furniture Manufacturers

Skills: React, FastAPI, PostgreSQL  
Difficulty: Medium  
Description: Create a simple dashboard to track stock, production and sales.
"""

        print("🧠 AI RESPONSE:", opportunity_text)

        # ✅ SAVE PROPER JSON (FIXED)
        task = Task(
            task_type="opportunity",
            assigned_to=None,
            status="new",
            payload=json.dumps({
                "text": opportunity_text
            }),
            result=None
        )

        session.add(task)
        session.commit()

        print("✅ Scout saved new opportunity")

    except Exception as e:
        print("❌ Scout error:", e)

        fallback = """
Create CRM for interior design companies

Skills: Python, UI/UX, Database  
Difficulty: Medium  
Description: Manage clients, projects and quotations.
"""

        # ✅ SAVE FALLBACK JSON (FIXED)
        task = Task(
            task_type="opportunity",
            assigned_to=None,
            status="new",
            payload=json.dumps({
                "text": fallback
            }),
            result=None
        )

        session.add(task)
        session.commit()

        print("⚠️ Saved fallback task due to AI failure")

    finally:
        session.close()
