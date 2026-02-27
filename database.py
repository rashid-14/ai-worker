import json
from sqlalchemy import text
from db import engine


def save_task(task_type, assigned_to, status, payload, result):

    payload_json = json.dumps(payload)

    query = text("""
        INSERT INTO tasks (task_type, assigned_to, status, payload, result, updated_at)
        VALUES (:task_type, :assigned_to, :status, :payload, :result, NOW())
    """)

    with engine.begin() as conn:
        conn.execute(query, {
            "task_type": task_type,
            "assigned_to": assigned_to,
            "status": status,
            "payload": payload_json,
            "result": result
        })
