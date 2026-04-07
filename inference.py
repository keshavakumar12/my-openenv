
import os
import sys
import re
import random
import argparse
import requests
from openai import OpenAI


API_BASE_URL = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME   = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN     = os.environ.get("HF_TOKEN", "")

DEFAULT_ENV_URL = "http://localhost:7860"
ENV_NAME = "sql_fixer"

SCHEMAS_TO_PICK = 3

DIFFICULTIES = ["easy", "medium", "hard", "expert"]

MAX_STEPS = 3


SYSTEM_PROMPT = """You are an expert SQL debugging assistant. Your job is to fix broken SQL queries.

You will be given:
1. A description of what the query SHOULD do
2. The broken SQL query that needs fixing
3. A hint about what is wrong
4. The database schema

Your task: Return ONLY the corrected SQL query. Do not include any explanation,
markdown formatting, or code fences. Just output the raw SQL query that fixes the issue.

Rules:
- Fix syntax errors (typos, missing keywords, bad punctuation)
- Fix logic errors (wrong JOINs, bad WHERE clauses, wrong aggregations)
- Optimize inefficient queries (remove unnecessary subqueries, use JOINs instead)
- The output must be a valid SQL query that can execute on SQLite
- Do NOT wrap your answer in ```sql``` or any other markdown — return ONLY the SQL"""


def extract_sql(response_text: str) -> str:
    text = response_text.strip()
    match = re.search(r"```(?:sql)?\s*\n?(.*?)\n?```", text, re.DOTALL | re.IGNORECASE)
    if match:
        text = match.group(1).strip()
    text = text.strip("`").strip()

    sql_lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("--") or stripped.startswith("#"):
            continue
        sql_lines.append(line)

    result = " ".join(sql_lines).strip().rstrip(";").strip()
    return result if result else response_text.strip()


def call_llm(client: OpenAI, prompt: str, attempt: int = 1) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=512,
            temperature=0.1 * attempt,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"  [LLM ERROR] {e}", file=sys.stderr)
        return ""


def build_prompt(obs: dict, feedback: str = "", attempt: int = 1) -> str:
    prompt = f"""Fix the following broken SQL query.

**Description:** {obs.get('description', '')}

**Broken Query:**
{obs.get('broken_query', '')}

**Hint:** {obs.get('hint', '')}

**Database Schema:**
{obs.get('schema_info', '')}"""

    if feedback and attempt > 1:
        prompt += f"""

**Previous attempt feedback:** {feedback}
Please try a different approach to fix this query."""

    prompt += "\n\nReturn ONLY the corrected SQL query, nothing else:"
    return prompt


def fetch_schemas(env_url: str) -> dict:
    """Call GET /schemas to discover available schemas and their task counts."""
    try:
        resp = requests.get(f"{env_url}/schemas", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[WARN] Could not fetch /schemas: {e}. Using fallback.", file=sys.stderr)
        return {
            "hr": {"difficulties": {"easy": 9, "medium": 16, "hard": 26, "expert": 13}},
            "hospital": {"difficulties": {"easy": 3, "medium": 4, "hard": 4, "expert": 3}},
            "university": {"difficulties": {"easy": 3, "medium": 4, "hard": 4, "expert": 3}},
            "ecommerce": {"difficulties": {"easy": 3, "medium": 4, "hard": 4, "expert": 3}},
            "library": {"difficulties": {"easy": 3, "medium": 4, "hard": 4, "expert": 3}},
        }


def run_episode(env_url: str, client: OpenAI, schema_name: str, difficulty: str) -> float:
    """Run a single episode for a given schema + difficulty. Returns final score."""

    # Reset with schema + difficulty filters
    try:
        reset_resp = requests.post(
            f"{env_url}/reset",
            json={"schema_name": schema_name, "difficulty": difficulty},
            timeout=30,
        )
        reset_resp.raise_for_status()
        obs = reset_resp.json()
    except Exception as e:
        print(f"[ERROR] Failed to reset ({schema_name}/{difficulty}): {e}", file=sys.stderr)
        return 0.0

    task_type = obs.get("task_type", "unknown")
    print(f"[START] task={task_type} env={ENV_NAME} model={MODEL_NAME} schema={schema_name} difficulty={difficulty}")
    sys.stdout.flush()

    feedback = ""
    episode_score = 0.0
    done = False
    step_rewards = []

    for step_num in range(1, MAX_STEPS + 1):
        if done:
            break

        prompt = build_prompt(obs, feedback, step_num)
        raw_response = call_llm(client, prompt, step_num)
        fixed_query = extract_sql(raw_response)

        if not fixed_query:
            fixed_query = obs.get("broken_query", "SELECT 1")

        error_msg = "null"
        try:
            step_resp = requests.post(
                f"{env_url}/step",
                json={"fixed_query": fixed_query},
                timeout=30,
            )
            step_resp.raise_for_status()
            result = step_resp.json()
        except Exception as e:
            error_msg = str(e)
            print(f"[STEP] step={step_num} action={fixed_query} reward=0.00 done=false error={error_msg}")
            sys.stdout.flush()
            step_rewards.append(0.0)
            break

        score = result.get("score", 0.0)
        feedback = result.get("feedback", "")
        done = result.get("done", False)
        episode_score = score
        step_rewards.append(score)

        print(f"[STEP] step={step_num} action={fixed_query} reward={score:.2f} done={str(done).lower()} error={error_msg}")
        sys.stdout.flush()

        if score >= 1.0:
            done = True
            break

    success = episode_score >= 1.0
    rewards_str = ",".join(f"{r:.2f}" for r in step_rewards)

    print(f"[END] success={str(success).lower()} steps={len(step_rewards)} score={episode_score:.3f} rewards={rewards_str} schema={schema_name} difficulty={difficulty}")
    sys.stdout.flush()

    return episode_score


def run_inference(env_url: str):
    """
    Main loop:
      1. Fetch available schemas from the server
      2. Randomly pick SCHEMAS_TO_PICK schemas
      3. For each schema, run 1 task per difficulty (easy/medium/hard/expert)
      4. Aggregate and report scores
    """
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN if HF_TOKEN else "dummy-key",
    )


    all_schemas = fetch_schemas(env_url)
    schema_names = list(all_schemas.keys())

    n_pick = min(SCHEMAS_TO_PICK, len(schema_names))
    chosen_schemas = random.sample(schema_names, n_pick)

    total_episodes = n_pick * len(DIFFICULTIES)

    print(f"\n{'=' * 60}")
    print(f"Available schemas : {schema_names}")
    print(f"Chosen schemas    : {chosen_schemas}")
    print(f"Difficulties      : {DIFFICULTIES}")
    print(f"Total episodes    : {n_pick} schemas x {len(DIFFICULTIES)} difficulties = {total_episodes}")
    print(f"{'=' * 60}\n")
    sys.stdout.flush()

  
    all_scores = []
    scores_by_schema = {}
    scores_by_difficulty = {d: [] for d in DIFFICULTIES}

    for schema_name in chosen_schemas:
        schema_scores = []
        for difficulty in DIFFICULTIES:
            score = run_episode(env_url, client, schema_name, difficulty)
            all_scores.append(score)
            schema_scores.append(score)
            scores_by_difficulty[difficulty].append(score)
            print()  

        scores_by_schema[schema_name] = schema_scores


    print(f"{'=' * 60}")
    print(f"AGGREGATED RESULTS")
    print(f"{'=' * 60}")

    if all_scores:
        overall_avg = sum(all_scores) / len(all_scores)

        print(f"\n  Per Schema:")
        for schema, scores in scores_by_schema.items():
            avg = sum(scores) / len(scores) if scores else 0
            detail = " | ".join(f"{d}={s:.2f}" for d, s in zip(DIFFICULTIES, scores))
            print(f"    {schema:12s} : avg={avg:.3f}  ({detail})")

        print(f"\n  Per Difficulty:")
        for diff in DIFFICULTIES:
            scores = scores_by_difficulty[diff]
            avg = sum(scores) / len(scores) if scores else 0
            detail = ", ".join(f"{s:.2f}" for s in scores)
            print(f"    {diff:8s} : avg={avg:.3f}  ({detail})")

        print(f"\n  Overall: {overall_avg:.4f} ({len(all_scores)} episodes)")
        print(f"  Scores : {all_scores}")
    else:
        print("  No episodes completed.")

    print(f"{'=' * 60}")
    sys.stdout.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SQL Fixer Inference Agent")
    parser.add_argument("--url", type=str, default=DEFAULT_ENV_URL,
                        help="Base URL of the SQL Fixer environment server")
    parser.add_argument("--schemas", type=int, default=SCHEMAS_TO_PICK,
                        help="Number of schemas to randomly pick (default 3)")
    args = parser.parse_args()

    SCHEMAS_TO_PICK = args.schemas

    print("=" * 60)
    print("SQL Fixer — Inference Agent")
    print("=" * 60)
    print(f"  Environment URL : {args.url}")
    print(f"  LLM API Base    : {API_BASE_URL}")
    print(f"  Model           : {MODEL_NAME}")
    print(f"  Schemas to pick : {SCHEMAS_TO_PICK}")
    print(f"  Difficulties    : {DIFFICULTIES}")
    print("=" * 60)
    sys.stdout.flush()

    run_inference(args.url)