import time
import json
import psycopg2
import os
import requests
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_PUBLIC_URL") or os.getenv("DATABASE_URL")
conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()

def get_new_solution():
    cursor.execute("""
        SELECT id, solution_name, target_industry, proposed_solution
        FROM solutions
        WHERE id NOT IN (SELECT solution_id FROM proposals)
        LIMIT 1;
    """)
    return cursor.fetchone()

def save_proposal(solution_id, proposal):
    cursor.execute("""
        INSERT INTO proposals (
            solution_id,
            offer_title,
            positioning,
            pricing_tiers,
            delivery_scope,
            target_customer,
            use_cases
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s);
    """, (
        solution_id,
        proposal["offer_title"],
        proposal["positioning"],
        json.dumps(proposal["pricing_tiers"]),
        proposal["delivery_scope"],
        proposal["target_customer"],
        json.dumps(proposal["use_cases"])
    ))
    conn.commit()

def generate_proposal(solution):

    prompt = f"""
You are a Business Strategy AI.

Convert this solution into a service offer.

Solution:
Name: {solution[1]}
Industry: {solution[2]}
Description: {solution[3]}

Return ONLY JSON:

{{
  "offer_title": "",
  "positioning": "",
  "pricing_tiers": [],
  "delivery_scope": "",
  "target_customer": "",
  "use_cases": []
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
    solution = get_new_solution()
    if solution:
        proposal = generate_proposal(solution)
        save_proposal(solution[0], proposal)
        print("Proposal created for solution:", solution[0])
    time.sleep(60)
