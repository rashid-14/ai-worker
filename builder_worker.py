import time
import json
import psycopg2
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Connect DB
DB_URL = os.getenv("DATABASE_PUBLIC_URL") or os.getenv("DATABASE_URL")
conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()

def get_new_opportunity():
    cursor.execute("""
        SELECT id, payload
        FROM tasks
        WHERE task_type='opportunity' AND status='new'
        LIMIT 1;
    """)
    return cursor.fetchone()

def save_solution(task_id, solution):
    cursor.execute("""
        INSERT INTO solutions (
            task_id,
            solution_name,
            target_industry,
            problem_summary,
            proposed_solution,
            core_modules,
            packages,
            landing_copy,
            delivery_scope,
            fit_for
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
    """, (
        task_id,
        solution["solution_name"],
        solution["target_industry"],
        solution["problem_summary"],
        solution["proposed_solution"],
        json.dumps(solution["core_modules"]),
        json.dumps(solution["packages"]),
        solution["landing_copy"],
        solution["delivery_scope"],
        json.dumps(solution["fit_for"])
    ))

    cursor.execute("UPDATE tasks SET status='built' WHERE id=%s;", (task_id,))
    conn.commit()

def build_solution(opportunity):

    prompt = f"""
You are a Solution Architect AI.

Convert this opportunity into a sellable software solution.

Opportunity:
{opportunity}

Return ONLY JSON:

{{
  "solution_name": "",
  "target_industry": "",
  "problem_summary": "",
  "proposed_solution": "",
  "core_modules": [],
  "packages": [],
  "landing_copy": "",
  "delivery_scope": "",
  "fit_for": []
}}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    text = result["response"]

    return json.loads(text)

while True:
    task = get_new_opportunity()
    if task:
        task_id, payload = task
        solution = build_solution(payload)
        save_solution(task_id, solution)
        print("Built solution for task:", task_id)
    time.sleep(60)
