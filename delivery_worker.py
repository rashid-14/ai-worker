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

def get_new_proposal():
    cursor.execute("""
        SELECT id, offer_title, positioning, delivery_scope
        FROM proposals
        WHERE id NOT IN (SELECT proposal_id FROM deliveries)
        LIMIT 1;
    """)
    return cursor.fetchone()

def save_delivery(proposal_id, delivery):
    cursor.execute("""
        INSERT INTO deliveries (
            proposal_id,
            implementation_summary,
            execution_steps,
            modules_included,
            delivery_checklist,
            client_handover
        )
        VALUES (%s,%s,%s,%s,%s,%s);
    """, (
        proposal_id,
        delivery["implementation_summary"],
        json.dumps(delivery["execution_steps"]),
        json.dumps(delivery["modules_included"]),
        json.dumps(delivery["delivery_checklist"]),
        delivery["client_handover"]
    ))
    conn.commit()

def generate_delivery(proposal):

    prompt = f"""
You are a Technical Delivery AI.

Convert this proposal into an execution-ready delivery plan.

Proposal:
Title: {proposal[1]}
Positioning: {proposal[2]}
Scope: {proposal[3]}

Return ONLY JSON:

{{
  "implementation_summary": "",
  "execution_steps": [],
  "modules_included": [],
  "delivery_checklist": [],
  "client_handover": ""
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
    proposal = get_new_proposal()
    if proposal:
        delivery = generate_delivery(proposal)
        save_delivery(proposal[0], delivery)
        print("Delivery created for proposal:", proposal[0])
    time.sleep(60)
