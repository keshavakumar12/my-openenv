import sqlite3
import random
import re
from typing import Any

from tasks import TASKS, SCHEMAS


def create_database(schema_name: str = "hr") -> sqlite3.Connection:
    """Create a fresh in-memory SQLite database with seed data for the given schema."""
    schema = SCHEMAS.get(schema_name)
    if not schema:
        raise ValueError(f"Unknown schema: {schema_name}. Available: {list(SCHEMAS.keys())}")

    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(schema["create_sql"])
    conn.executescript(schema["seed_sql"])
    return conn


def normalize_query(query: str) -> str:
    """Normalize a SQL query for comparison: lowercase, collapse whitespace, strip."""
    query = query.strip().rstrip(";").strip()
    query = re.sub(r"\s+", " ", query)
    return query.lower()


def execute_query(conn: sqlite3.Connection, query: str) -> dict:
    """
    Safely execute a SQL query and return results + metadata.
    Returns dict with 'success', 'rows', 'columns', 'error', 'row_count'.
    """
    try:
        cursor = conn.execute(query)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        return {
            "success": True,
            "rows": rows,
            "columns": columns,
            "row_count": len(rows),
            "error": None,
        }
    except Exception as e:
        return {
            "success": False,
            "rows": [],
            "columns": [],
            "row_count": 0,
            "error": str(e),
        }


def grade_syntax_fix(conn: sqlite3.Connection, agent_query: str, correct_query: str) -> dict:
    """
    Grade a syntax fix task.

    Scoring:
      - 0.0  : agent query doesn't execute at all
      - 0.3  : agent query executes but returns wrong results
      - 0.7  : agent query returns correct results but different structure
      - 1.0  : agent query returns identical results to the correct query
    """
    agent_result = execute_query(conn, agent_query)
    correct_result = execute_query(conn, correct_query)

    if not agent_result["success"]:
        return {"score": 0.0, "reason": f"Query failed to execute: {agent_result['error']}"}

    if not correct_result["success"]:
        return {"score": 0.0, "reason": "Internal error: correct query failed."}

    if set(map(tuple, agent_result["rows"])) == set(map(tuple, correct_result["rows"])):
        if agent_result["columns"] == correct_result["columns"]:
            return {"score": 1.0, "reason": "Perfect — results and column names match exactly."}
        else:
            return {"score": 0.7, "reason": "Results match but column names differ."}

    return {"score": 0.3, "reason": f"Query runs but returns wrong results. Expected {correct_result['row_count']} rows, got {agent_result['row_count']}."}


def grade_logic_fix(conn: sqlite3.Connection, agent_query: str, correct_query: str, difficulty: str = "medium") -> dict:
    """
    Grade a logic fix task with difficulty-aware partial credit.

    Scoring brackets shift by difficulty — harder tiers give less partial credit:

                      easy   medium   hard   expert
    Fails to execute: 0.0    0.0      0.0    0.0
    Completely wrong:  0.3    0.2      0.1    0.05
    ~50% overlap:      0.6    0.5      0.3    0.2
    Near correct:      0.8    0.8      0.6    0.5
    Exact match:       1.0    1.0      1.0    1.0
    """
    agent_result = execute_query(conn, agent_query)
    correct_result = execute_query(conn, correct_query)

    if not agent_result["success"]:
        return {"score": 0.0, "reason": f"Query failed to execute: {agent_result['error']}"}

    if not correct_result["success"]:
        return {"score": 0.0, "reason": "Internal error: correct query failed."}

    
    brackets = {
        "easy":   {"wrong": 0.3,  "base": 0.4, "scale": 0.4, "near": 0.8},
        "medium": {"wrong": 0.2,  "base": 0.3, "scale": 0.5, "near": 0.8},
        "hard":   {"wrong": 0.1,  "base": 0.15, "scale": 0.45, "near": 0.6},
        "expert": {"wrong": 0.05, "base": 0.1, "scale": 0.4, "near": 0.5},
    }
    b = brackets.get(difficulty, brackets["medium"])

    correct_rows = set(map(tuple, correct_result["rows"]))
    agent_rows = set(map(tuple, agent_result["rows"]))

    if agent_rows == correct_rows:
        return {"score": 1.0, "reason": "Perfect — logic is correct, all rows match."}

    if len(correct_rows) > 0:
        overlap = agent_rows & correct_rows
        overlap_ratio = len(overlap) / len(correct_rows)

        if overlap_ratio == 0:
            return {"score": b["wrong"], "reason": "Query runs but returns completely wrong results."}

        
        extra = len(agent_rows) - len(correct_rows)
        if extra > 0:
            extra_penalty = min(0.2, (extra / len(correct_rows)) * 0.2)
            score = round(b["base"] + (overlap_ratio * b["scale"]) - extra_penalty, 2)
            score = max(b["wrong"], min(score, b["near"]))
            return {"score": score, "reason": f"Partial match: {len(overlap)}/{len(correct_rows)} correct rows, {extra} extra rows."}

        score = round(b["base"] + (overlap_ratio * b["scale"]), 2)
        score = min(score, b["near"])
        return {"score": score, "reason": f"Partial match: {len(overlap)}/{len(correct_rows)} correct rows."}

    return {"score": b["wrong"], "reason": "Could not determine correctness."}


def grade_optimization(conn: sqlite3.Connection, agent_query: str, correct_query: str, broken_query: str) -> dict:
    """
    Grade an optimization task.

    Scoring:
      - 0.0  : agent query doesn't execute
      - 0.2  : executes but wrong results
      - 0.4  : correct results but no simpler than the original
      - 0.7  : correct results and somewhat simpler
      - 1.0  : correct results and significantly simpler/optimized
    """
    agent_result = execute_query(conn, agent_query)
    correct_result = execute_query(conn, correct_query)

    if not agent_result["success"]:
        return {"score": 0.0, "reason": f"Query failed to execute: {agent_result['error']}"}

    if not correct_result["success"]:
        return {"score": 0.0, "reason": "Internal error: correct query failed."}

    correct_rows = set(map(tuple, correct_result["rows"]))
    agent_rows = set(map(tuple, agent_result["rows"]))

    if agent_rows != correct_rows:
        return {"score": 0.2, "reason": "Optimized query returns different results than expected."}

    
    agent_norm = normalize_query(agent_query)
    broken_norm = normalize_query(broken_query)
    correct_norm = normalize_query(correct_query)

    
    agent_subqueries = agent_norm.count("select") - 1
    broken_subqueries = broken_norm.count("select") - 1
    agent_len = len(agent_norm)
    broken_len = len(broken_norm)

    
    if agent_norm == broken_norm:
        return {"score": 0.4, "reason": "Results are correct but the query was not optimized — it's the same as the original."}

    
    if agent_norm == correct_norm:
        return {"score": 1.0, "reason": "Perfect — query is optimized and matches the ideal solution."}

    
    improved = False
    score = 0.5

    if agent_subqueries < broken_subqueries:
        score += 0.2
        improved = True

    if agent_len < broken_len * 0.85:
        score += 0.15
        improved = True

    if "exists" not in agent_norm and "exists" in broken_norm:
        score += 0.1
        improved = True

    if agent_subqueries == 0 and broken_subqueries > 0:
        score += 0.1
        improved = True

    score = round(min(score, 0.95), 2)

    if improved:
        return {"score": score, "reason": f"Good optimization — query is simpler (from {broken_subqueries + 1} to {agent_subqueries + 1} SELECT statements, length reduced by {round((1 - agent_len / broken_len) * 100)}%)."}

    return {"score": 0.5, "reason": "Results correct but optimization is minimal."}




class SQLFixerEnvironment:
    """
    The main environment class.

    Usage:
        env = SQLFixerEnvironment()
        observation = env.reset(task_type="syntax_fix")
        result = env.step(agent_fixed_query)
    """

    def __init__(self):
        self.db: sqlite3.Connection = create_database("hr")
        self.current_task: dict | None = None
        self.task_started: bool = False
        self.steps_taken: int = 0
        self.max_steps: int = 3
        self.schema_name: str = "hr"

    def get_task_types(self) -> list[str]:
        """Return available task types."""
        return ["syntax_fix", "logic_fix", "optimization"]

    def reset(self, task_type: str | None = None, difficulty: str | None = None, schema_name: str | None = None) -> dict:
        """
        Start a new episode. Pick a random task matching the given filters.

        Args:
            task_type: one of "syntax_fix", "logic_fix", "optimization", or None for random.
            difficulty: one of "easy", "medium", "hard", "expert", or None for any.
            schema_name: one of the schema keys, or None for any.

        Returns:
            Observation dict with the broken query and description.
        """
        self.steps_taken = 0
        self.task_started = True

        
        available = TASKS
        if task_type:
            available = [t for t in available if t["task_type"] == task_type]
        if difficulty:
            available = [t for t in available if t["difficulty"] == difficulty]
        if schema_name:
            available = [t for t in available if t.get("schema_name") == schema_name]

        if not available:
            raise ValueError(f"No tasks available for type={task_type}, difficulty={difficulty}, schema={schema_name}")

        self.current_task = random.choice(available)

        
        self.schema_name = self.current_task.get("schema_name", "hr")
        self.db = create_database(self.schema_name)

        
        schema_info = SCHEMAS[self.schema_name]["schema_info"]

        return {
            "task_type": self.current_task["task_type"],
            "difficulty": self.current_task["difficulty"],
            "description": self.current_task["description"],
            "broken_query": self.current_task["broken_query"],
            "hint": self.current_task["hint"],
            "schema_info": schema_info,
            "schema_name": self.schema_name,
            "max_steps": self.max_steps,
        }

    def step(self, action: str) -> dict:
        """
        Agent submits a fixed query. Environment grades it.

        Args:
            action: the agent's fixed SQL query string.

        Returns:
            Dict with score, feedback, and done flag.
        """
        if not self.task_started or self.current_task is None:
            return {
                "score": 0.0,
                "feedback": "No active task. Call reset() first.",
                "done": True,
                "steps_taken": self.steps_taken,
                "max_steps": self.max_steps,
            }

        self.steps_taken += 1
        task = self.current_task
        task_type = task["task_type"]
        difficulty = task["difficulty"]
        correct_query = task["correct_query"]

        
        if task_type == "syntax_fix":
            result = grade_syntax_fix(self.db, action, correct_query)
        elif task_type == "logic_fix":
            result = grade_logic_fix(self.db, action, correct_query, difficulty)
        elif task_type == "optimization":
            result = grade_optimization(self.db, action, correct_query, task["broken_query"])
        else:
            result = {"score": 0.0, "reason": f"Unknown task type: {task_type}"}

        
        done = (result["score"] >= 1.0) or (self.steps_taken >= self.max_steps)

        if done:
            self.task_started = False

        return {
            "score": result["score"],
            "feedback": result["reason"],
            "done": done,
            "steps_taken": self.steps_taken,
            "max_steps": self.max_steps,
        }


if __name__ == "__main__":
    print("=" * 60)
    print("SQL Fixer Environment — Local Test")
    print("=" * 60)

    env = SQLFixerEnvironment()

 
    for task_type in env.get_task_types():
        print(f"\n--- Testing task type: {task_type} ---")
        obs = env.reset(task_type=task_type)
        print(f"  Difficulty  : {obs['difficulty']}")
        print(f"  Description : {obs['description']}")
        print(f"  Broken query: {obs['broken_query']}")
        print(f"  Hint        : {obs['hint']}")

        correct = env.current_task["correct_query"]
        result = env.step(correct)
        print(f"  Agent answer: {correct}")
        print(f"  Score       : {result['score']}")
        print(f"  Feedback    : {result['feedback']}")
        print(f"  Done        : {result['done']}")

   
    print(f"\n--- Testing wrong answer ---")
    obs = env.reset(task_type="syntax_fix")
    print(f"  Broken: {obs['broken_query']}")
    result = env.step("SELECT * FROM nonexistent_table")
    print(f"  Score : {result['score']}")
    print(f"  Feedback: {result['feedback']}")


    print(f"\n--- Testing partially correct answer ---")
    obs = env.reset(task_type="logic_fix")
    print(f"  Broken: {obs['broken_query']}")
    result = env.step("SELECT name FROM employees")
    print(f"  Score : {result['score']}")
    print(f"  Feedback: {result['feedback']}")


    print(f"\n{'=' * 60}")
    print("Validating ALL tasks (correct_query must score 1.0)...")
    print(f"{'=' * 60}")
    failures = []
    for i, task in enumerate(TASKS):
        schema_name = task.get("schema_name", "hr")
        db = create_database(schema_name)
        correct = task["correct_query"]
        task_type = task["task_type"]
        difficulty = task["difficulty"]

        if task_type == "syntax_fix":
            result = grade_syntax_fix(db, correct, correct)
        elif task_type == "logic_fix":
            result = grade_logic_fix(db, correct, correct, difficulty)
        elif task_type == "optimization":
            result = grade_optimization(db, correct, correct, task["broken_query"])
        else:
            result = {"score": 0.0, "reason": "unknown type"}

        if result["score"] < 1.0:
            failures.append((i, task["description"][:60], result["score"], result["reason"]))

    if failures:
        print(f"\n  FAILURES ({len(failures)}):")
        for idx, desc, score, reason in failures:
            print(f"    Task {idx}: {desc}... → score={score} ({reason})")
    else:
        print(f"\n  All {len(TASKS)} tasks validated successfully!")

    print(f"\n{'=' * 60}")
    print("Verifying broken queries don't score 1.0...")
    print(f"{'=' * 60}")
    false_positives = []
    for i, task in enumerate(TASKS):
        schema_name = task.get("schema_name", "hr")
        db = create_database(schema_name)
        broken = task["broken_query"]
        correct = task["correct_query"]
        task_type = task["task_type"]
        difficulty = task["difficulty"]

        if task_type == "syntax_fix":
            result = grade_syntax_fix(db, broken, correct)
        elif task_type == "logic_fix":
            result = grade_logic_fix(db, broken, correct, difficulty)
        elif task_type == "optimization":
            result = grade_optimization(db, broken, correct, broken)
        else:
            result = {"score": 0.0, "reason": "unknown type"}

        if result["score"] >= 1.0:
            false_positives.append((i, task["description"][:60], result["score"]))

    if false_positives:
        print(f"\n  FALSE POSITIVES ({len(false_positives)}) — broken query scored 1.0:")
        for idx, desc, score in false_positives:
            print(f"    Task {idx}: {desc}...")
    else:
        print(f"\n  All {len(TASKS)} broken queries correctly score < 1.0!")

    print(f"\n{'=' * 60}")
    print(f"Total tasks: {len(TASKS)}")
    print("All tests passed! Environment is working.")
    print(f"{'=' * 60}")
