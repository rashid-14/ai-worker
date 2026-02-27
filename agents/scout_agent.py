from models.task import Task
from database import engine
from sqlalchemy.orm import sessionmaker
import google.generativeai as genai
import os

Session = sessionmaker(bind=engine)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(os.getenv("MODEL"))

def run_scout():

    session = Session()

    print("Scout scanning market...")

    prompt = """
    Find one high-demand freelance opportunity that is:
    - trending
    - underserved
    - beginner-executable

    Output in this format:

    TITLE:
    NICHE:
    DEMAND_REASON:
    POSSIBLE_SERVICE:
    """

    response = model.generate_content(prompt)

    opportunity = response.text

    task = Task(
        type="opportunity",
        status="new",
        content=opportunity
    )

    session.add(task)
    session.commit()
    session.close()

    print("Scout stored new opportunity")
