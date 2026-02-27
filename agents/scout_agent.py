import os
import google.generativeai as genai
from models.task import Task
from database import SessionLocal

def run_scout():
    """Generate a freelance opportunity using Gemini API and save to Task table."""
    # Configure Gemini API with environment variable
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # Initialize the model from environment variable
    model = genai.GenerativeModel(os.getenv("MODEL"))
    
    # Generate freelance opportunity
    prompt = "Generate a single specific freelance opportunity idea that a developer could pursue. Include the project type, skills required, and estimated difficulty level. Keep it concise."
    
try:
    response = model.generate_content(prompt)
    opportunity_text = response.text
except Exception as e:
    print("Gemini quota hit or error:", e)
    return None

# Stop if nothing generated
if not opportunity_text:
    return None

task = Task(
    status="new",
    content=opportunity_text
)        
        # Add to session and commit
        session.add(task)
        session.commit()
        
        return task
    finally:
        session.close()
