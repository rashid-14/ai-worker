import os
import google.generativeai as genai
from models.task import Task
from database import SessionLocal

def run_scout():
    try:
        # Configure Gemini
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel(os.getenv("MODEL"))

        prompt = "Generate one freelance software project opportunity idea."

        response = model.generate_content(prompt)
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
