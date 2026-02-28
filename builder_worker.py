import time
import json
import psycopg2
import os
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

# 🚀 Cloud-safe builder (no localhost AI)

def build_solution(opportunity):

    print("🏗 Building solution (cloud mode)...")

    solution = {
        "solution_name": "Smart Business System",
        "target_industry": opportunity.get("industry", "General Business"),
        "problem_summary": opportunity.get("problem", "Manual workflow inefficiency"),
        "proposed_solution": "Custom software system to automate workflows",
        "core_modules": [
            "Dashboard",
            "Client Management",
            "Workflow Automation",
            "Reporting"
        ],
        "packages": [
            {"name": "Starter", "features": ["Basic CRM", "Dashboard"]},
            {"name": "Growth", "features": ["CRM", "Automation", "Reports"]},
            {"name": "Enterprise", "features": ["Full Suite", "Analytics", "Custom Logic"]}
        ],
        "landing_copy": "Transform your business with automation and smart systems.",
        "delivery_scope": "End-to-end development and deployment",
        "fit_for": ["SMEs", "Service Businesses"]
    }

    return solution

def run_builder():
    task = get_new_opportunity()
    if task:
        task_id, payload = task
        solution = build_solution(payload)
        save_solution(task_id, solution)
        print("Built solution for task:", task_id)

# Worker loop
while True:
    run_builder()
    time.sleep(60)
