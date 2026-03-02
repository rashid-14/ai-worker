import json
import psycopg2
import os

def get_db():
    DB_URL = os.getenv("DATABASE_PUBLIC_URL") or os.getenv("DATABASE_URL")
    return psycopg2.connect(DB_URL)

def get_new_opportunity(cursor):
    cursor.execute("""
        SELECT id, payload
        FROM tasks
        WHERE task_type='opportunity' AND status='new'
        LIMIT 1;
    """)
    return cursor.fetchone()

def save_solution(conn, cursor, task_id, solution):
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

    print("🏗 Building solution (cloud-safe)...")

    # ensure payload is dict
    if isinstance(opportunity, str):
        try:
            opportunity = json.loads(opportunity)
        except:
            opportunity = {"text": opportunity}

    solution = {
        "solution_name": "Smart Workflow System",
        "target_industry": opportunity.get("industry", "General Business"),
        "problem_summary": opportunity.get("text", "Manual workflow inefficiency"),
        "proposed_solution": "Automation software to streamline operations",
        "core_modules": [
            "Dashboard",
            "Client Management",
            "Workflow Automation",
            "Reporting"
        ],
        "packages": [
            {"name": "Starter", "features": ["Basic CRM", "Dashboard"]},
            {"name": "Growth", "features": ["CRM", "Automation", "Reports"]},
            {"name": "Enterprise", "features": ["Full Suite", "Analytics"]}
        ],
        "landing_copy": "Transform your operations with intelligent automation.",
        "delivery_scope": "End-to-end development & deployment",
        "fit_for": ["SMEs", "Agencies", "Service Businesses"]
    }

    return solution

def run_builder():
    try:
        conn = get_db()
        cursor = conn.cursor()

        task = get_new_opportunity(cursor)
        if task:
            task_id, payload = task
            solution = build_solution(payload)
            save_solution(conn, cursor, task_id, solution)
            print("Built solution for task:", task_id)

        cursor.close()
        conn.close()

    except Exception as e:
        print("Builder error:", e)
