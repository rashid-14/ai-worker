import os
from google import genai
from models.task import Task
from database import SessionLocal

def run_scout():
    try:
        # Configure Gemini
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

response = client.models.generate_content(
    model=os.getenv("MODEL"),
    contents=prompt
)

opportunity_text = response.text
        if not opportunity_text:
            return None

        session = SessionLocal()

        try:
            task = Task(
                status="new",
                content=opportunity_text
            )
            session.add(task)
            session.commit()
            return task
        finally:
            session.close()

    except Exception as e:
        print("Scout skipped:", e)
        return None
