from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TaskType(str, Enum):
    """The three task categories."""
    SYNTAX_FIX = "syntax_fix"
    LOGIC_FIX = "logic_fix"
    OPTIMIZATION = "optimization"


class Difficulty(str, Enum):
    """Difficulty tiers — logic_fix spans all four, syntax_fix is easy,
    optimization is hard/expert."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class SQLFixAction(BaseModel):
    """
    The agent's submission for the current task.

    The only required field is `fixed_query` — the SQL string the agent
    believes is the corrected / optimized version of the broken query.
    """

    fixed_query: str = Field(
        ...,
        description="The agent's corrected SQL query.",
        min_length=1,
        examples=["SELECT name, salary FROM employees WHERE department = 'Engineering'"],
    )


class SQLFixObservation(BaseModel):
    """
    Everything the agent needs to see after calling reset() or step().

    After **reset()**  → task_type, difficulty, description, broken_query,
                         hint, schema_info, and max_steps are populated;
                         score / feedback / done reflect the initial state.

    After **step()**   → score, feedback, and done are updated with grading
                         results; the task fields remain the same so the agent
                         can retry if not done.
    """

    task_type: TaskType = Field(
        ...,
        description="Which category this task belongs to.",
    )
    difficulty: Difficulty = Field(
        ...,
        description="Difficulty tier for this task.",
    )
    description: str = Field(
        ...,
        description="Natural-language explanation of what the query SHOULD do.",
    )
    broken_query: str = Field(
        ...,
        description="The SQL query the agent must fix.",
    )
    hint: str = Field(
        default="",
        description="Optional hint about what is wrong with the broken query.",
    )
    schema_info: str = Field(
        default="",
        description="Summary of the database schema (tables and columns).",
    )
    schema_name: str = Field(
        default="hr",
        description="Which database schema is active for this task.",
    )
    max_steps: int = Field(
        default=3,
        description="Maximum number of attempts the agent has for this task.",
    )

    score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Reward for the most recent submission (0.0 – 1.0).",
    )
    feedback: str = Field(
        default="",
        description="Human-readable grading explanation.",
    )
    done: bool = Field(
        default=False,
        description="True when the episode is over (perfect score or max steps reached).",
    )
    steps_taken: int = Field(
        default=0,
        ge=0,
        description="How many submissions the agent has made so far.",
    )


class SQLFixState(BaseModel):
    """
    Internal bookkeeping the server maintains across requests.

    This is NOT sent to the agent — it lives on the server so it can
    reconstruct the environment between HTTP calls.
    """

    task_type: Optional[TaskType] = Field(
        default=None,
        description="The task type for the current episode (None if idle).",
    )
    task_index: Optional[int] = Field(
        default=None,
        description="Index into the TASKS list for the current task.",
    )
    schema_name: str = Field(
        default="hr",
        description="Which database schema is active.",
    )
    steps_taken: int = Field(
        default=0,
        ge=0,
        description="Number of submissions so far in this episode.",
    )
    max_steps: int = Field(
        default=3,
        gt=0,
        description="Step budget for the episode.",
    )
    is_active: bool = Field(
        default=False,
        description="Whether an episode is currently in progress.",
    )
    last_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Score from the most recent step() call.",
    )
