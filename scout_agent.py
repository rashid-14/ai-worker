import json
from datetime import datetime
from database import save_task
from ai import generate_ai_opportunity


def run_scout():
    print("🚀 Running Scout...")

    try:
        ai_result = generate_ai_opportunity()

        if not ai_result:
            raise Exception("AI returned empty")

        payload = {
            "text": ai_result,
            "source": "ai",
            "created_at": datetime.utcnow().isoformat()
        }

        save_task(
            task_type="opportunity",
            assigned_to=None,
            status="new",
            payload=payload,
            result=None
        )

        print("✅ Opportunity saved from AI")

    except Exception as e:
        print(f"❌ Scout error: {e}")

        fallback_text = """Create CRM for interior design companies.
Skills: Python, UI/UX, Database
Difficulty: Medium"""

        payload = {
            "text": fallback_text,
            "source": "fallback",
            "created_at": datetime.utcnow().isoformat()
        }

        save_task(
            task_type="opportunity",
            assigned_to=None,
            status="new",
            payload=payload,
            result=None
        )

        print("⚠️ Saved fallback opportunity")
