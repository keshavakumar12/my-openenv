---
title: SQL Query Fixer
emoji: 📊
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
tags:
  - openenv
---
# SQL Query Fixer — OpenEnv Environment

An AI training environment where agents practice diagnosing and fixing broken SQL queries. Built for the **Meta PyTorch + Hugging Face OpenEnv Hackathon**.

---

## Why SQL Fixing?

SQL debugging is one of the most common real-world developer tasks, yet it's rarely used as an AI training benchmark. This environment is a good fit because:

- **Deterministic grading** — a query either returns the correct rows or it doesn't. No subjective evaluation needed.
- **Natural difficulty progression** — from simple typos (easy) to query restructuring (hard).
- **Partial credit** — queries that run but return wrong results still earn some reward, giving the agent a useful learning signal.
- **Real execution** — every submission is run against a live in-memory SQLite database with realistic seed data (employees, departments, projects, assignments).

---

## Action Space

The agent sends a single JSON field:

```json
{ "fixed_query": "SELECT name, salary FROM employees WHERE department = 'Engineering'" }
```

`fixed_query` is a plain SQL string. The environment executes it against the database and compares the output to the gold-standard answer.

---

## Observation Space

After calling `/reset` or `/step`, the environment returns:

| Field          | Type   | Description                                              |
|----------------|--------|----------------------------------------------------------|
| `task_type`    | string | `syntax_fix`, `logic_fix`, or `optimization`             |
| `difficulty`   | string | `easy`, `medium`, or `hard`                              |
| `description`  | string | What the query is supposed to do (natural language)      |
| `broken_query` | string | The SQL query the agent must fix                         |
| `hint`         | string | A clue about what is wrong                               |
| `schema_info`  | string | Table and column listing for the database                |
| `max_steps`    | int    | Maximum attempts allowed (default 3)                     |
| `score`        | float  | Reward from 0.0 to 1.0 for the latest submission        |
| `feedback`     | string | Human-readable grading explanation                       |
| `done`         | bool   | `true` when the episode is over                          |
| `steps_taken`  | int    | Number of submissions so far                             |

---

## Tasks

The environment contains **18 tasks** across three difficulty tiers.

### Task 1 — `syntax_fix` (Easy) · 6 tasks

Fix SQL syntax errors: misspelled keywords (`SELCT`, `WERE`, `ORDERY`, `FORM`), missing commas, missing spaces (`GROUPBY`), and trailing punctuation.

**Scoring:** 0.0 (won't execute) → 0.3 (runs, wrong results) → 0.7 (right results, wrong column names) → 1.0 (exact match).

### Task 2 — `logic_fix` (Medium) · 6 tasks

Fix logical errors: wrong JOIN conditions, `INNER JOIN` vs `LEFT JOIN`, `WHERE` vs `HAVING` misplacement, wrong aggregation functions (`MIN` instead of `MAX`), and subqueries comparing against the wrong scope.

**Scoring:** 0.0 (won't execute) → 0.2 (completely wrong) → 0.5 (partial row overlap) → 0.8 (correct rows but extra/missing) → 1.0 (exact match).

### Task 3 — `optimization` (Hard) · 6 tasks

Rewrite correct-but-slow queries: eliminate unnecessary subqueries, replace correlated subqueries with JOINs, remove redundant `EXISTS` nesting, and simplify overall structure.

**Scoring:** 0.0 (won't execute) → 0.2 (wrong results) → 0.4 (correct but not simplified) → 0.7 (somewhat simpler) → 1.0 (matches ideal optimized form).

---

## Database Schema

The environment creates a fresh in-memory SQLite database each episode with four tables:

- **employees** — `id, name, department, salary, hire_date, manager_id, is_active` (12 rows)
- **departments** — `id, name, budget, location` (5 rows)
- **projects** — `id, name, department_id, start_date, end_date, status` (6 rows)
- **assignments** — `id, employee_id, project_id, role, hours_per_week` (12 rows)

---

## How to Run Locally

### 1. Clone and build

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/sql-query-fixer
cd sql-query-fixer
docker build -t sql-fixer .
docker run -p 7860:7860 sql-fixer
```

### 2. Test the endpoints

```bash
# Start a new episode
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task_type": "syntax_fix"}'

# Submit a fix
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{"fixed_query": "SELECT name, salary FROM employees WHERE department = '\''Engineering'\''"}'

# Check state
curl http://localhost:7860/state
```

### 3. Run the inference agent

```bash
export HF_TOKEN="your_huggingface_token"
export API_BASE_URL="https://api-inference.huggingface.co/v1"
export MODEL_NAME="mistralai/Mistral-7B-Instruct-v0.3"

python inference.py --url http://localhost:7860 --episodes 2
```

---

## Baseline Scores

| Agent Strategy         | syntax_fix | logic_fix | optimization | Overall Avg |
|------------------------|-----------|-----------|--------------|-------------|
| **Random / no-op**     | 0.0       | 0.0       | 0.2 – 0.4   | ~0.1        |
| **Echo broken query**  | 0.0       | 0.0 – 0.3 | 0.4          | ~0.15       |
| **Small LLM (7B)**     | 0.7 – 1.0 | 0.5 – 0.8 | 0.4 – 0.7   | ~0.65       |
| **Strong LLM (70B+)**  | 1.0       | 0.8 – 1.0 | 0.7 – 1.0   | ~0.90       |

- A **random agent** that submits garbage SQL scores near zero — syntax and logic tasks fail to execute, and optimization tasks return 0.4 at best (since the broken query already produces correct results).
- **Echoing the broken query** back earns nothing on syntax tasks (they don't execute) and 0.4 on optimization tasks (correct output, no simplification).
- A **7B instruction-tuned model** reliably fixes syntax errors but struggles with nuanced logic fixes and rarely produces ideal optimizations.
- A **strong 70B+ model** achieves near-perfect scores across the board.

---

## Project Structure

```
├── app.py              # FastAPI server with /reset, /step, /state endpoints
├── environment.py       # Core environment: tasks, grading, SQLite database
├── models.py            # Pydantic models (action, observation, state)
├── inference.py         # Agent script — calls LLM and submits fixes
├── openenv.yaml         # Environment metadata for OpenEnv
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container config for Hugging Face Spaces
└── README.md            # This file
```

---

## License

MIT
