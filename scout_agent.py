import json
import time
from sqlalchemy import text
from db import engine
from ai import generate_opportunity


def save_task(task_type, payload_text):
    try:
        # ✅ Always convert payload to JSON
        payload_json = json.dumps({
            "text": payload_text
        })

        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO tasks (task_type, assigned_to, status, payload, result, updated_at)
                VALUES (:task_type, NULL, 'new', :payload, NULL, NULL)
            """), {
                "task_type": task_type,
                "payload": payload_json
            })

        print("✅ Opportunity saved")

    except Exception as e:
        print(f"❌ DB Save error: {e}")


def run_scout():
    print("🚀 Running Scout...")

    try:
        opportunity = generate_opportunity()

        if opportunity:
            save_task("opportunity", opportunity)
            print("✅ Scout Completed")
        else:
            raise Exception("AI returned empty")

    except Exception as e:
        print(f"❌ Scout error: {e}")

        # 🔁 Fallback Opportunity (ALWAYS SAFE JSON)
        fallback_text = """
Create CRM for interior design companies.

Skills: Python, UI/UX, Database
Difficulty: Medium
"""
        save_task("opportunity", fallback_text)
        print("⚠️ Saved fallback task due to AI failure")


if __name__ == "__main__":
    while True:
        run_scout()
        time.sleep(30)
