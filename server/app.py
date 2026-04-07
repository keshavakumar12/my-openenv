
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from environment import SQLFixerEnvironment
from models import SQLFixAction, SQLFixObservation, SQLFixState
from tasks import SCHEMAS, TASKS


app = FastAPI(
    title="SQL Fixer Environment",
    description="OpenEnv hackathon – fix broken SQL queries and get graded.",
    version="2.0.0",
)

env = SQLFixerEnvironment()


class ResetRequest(BaseModel):
    task_type: Optional[str] = None
    difficulty: Optional[str] = None
    schema_name: Optional[str] = None


@app.post("/reset", response_model=SQLFixObservation)
def reset(body: ResetRequest = ResetRequest()):
    """Start a new episode. Optionally filter by task_type, difficulty, and/or schema_name."""
    try:
        obs = env.reset(task_type=body.task_type, difficulty=body.difficulty, schema_name=body.schema_name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return SQLFixObservation(
        task_type=obs["task_type"],
        difficulty=obs["difficulty"],
        description=obs["description"],
        broken_query=obs["broken_query"],
        hint=obs["hint"],
        schema_info=obs["schema_info"],
        schema_name=obs.get("schema_name", "hr"),
        max_steps=obs["max_steps"],
        score=0.0,
        feedback="",
        done=False,
        steps_taken=0,
    )


@app.post("/step", response_model=SQLFixObservation)
def step(action: SQLFixAction):
    """Submit a fixed SQL query. Returns score, feedback, and done flag."""
    if not env.task_started or env.current_task is None:
        raise HTTPException(status_code=400, detail="No active task. Call POST /reset first.")

    result = env.step(action.fixed_query)

    schema_info = SCHEMAS[env.schema_name]["schema_info"]

    task = env.current_task
    return SQLFixObservation(
        task_type=task["task_type"],
        difficulty=task["difficulty"],
        description=task["description"],
        broken_query=task["broken_query"],
        hint=task["hint"],
        schema_info=schema_info,
        schema_name=env.schema_name,
        max_steps=result["max_steps"],
        score=result["score"],
        feedback=result["feedback"],
        done=result["done"],
        steps_taken=result["steps_taken"],
    )


@app.get("/state", response_model=SQLFixState)
def state():
    """Return internal metadata about the current episode."""
    return SQLFixState(
        task_type=env.current_task["task_type"] if env.current_task else None,
        task_index=None,
        schema_name=env.schema_name,
        steps_taken=env.steps_taken,
        max_steps=env.max_steps,
        is_active=env.task_started,
        last_score=0.0,
    )


@app.get("/schemas")
def schemas():
    """Return available schemas with task counts per difficulty level."""
    from collections import Counter
    combo = Counter((t["schema_name"], t["difficulty"]) for t in TASKS)
    result = {}
    for schema_name in SCHEMAS:
        result[schema_name] = {
            "difficulties": {
                diff: combo.get((schema_name, diff), 0)
                for diff in ["easy", "medium", "hard", "expert"]
            }
        }
    return result
