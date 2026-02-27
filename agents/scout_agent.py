import os
import google.generativeai as genai
from models.task import Task
from database import SessionLocal

def run_scout():
    prompt = "Generate one real freelance opportunity idea for a developer. Include project type, required skills and difficulty."

    session = SessionLocal()


try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel(os.getenv("MODEL"))
    response = model.generate_content(prompt)

    opportunity_text = response.text

    if not opportunity_text:
        return

    task = Task(
        status="new",
        content=opportunity_text
    )

    session.add(task)
    session.commit()

except Exception as e:
    print("Scout error:", e)

    except Exception as e:
        print("Scout error:", e)

    finally:
        session.close()
