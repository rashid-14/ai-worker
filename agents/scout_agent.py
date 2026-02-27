import os
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

        opportunity_text = response.text

        if not opportunity_text:
            return

        # ✅ Save using correct DB columns
        task = Task(
            task_type="opportunity",
            status="new",
            payload=opportunity_text
        )

        session.add(task)
        session.commit()

        print("Scout saved new opportunity")

    except Exception as e:
        print("Scout error:", e)

    finally:
        session.close()
