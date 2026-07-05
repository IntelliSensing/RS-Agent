"""Utilities for scoring task planning accuracy."""

from __future__ import annotations

import ast
import re
from typing import Any


def extract_first_tool(intermediate_steps: list[Any]) -> str | None:
    """Extract the name of the first invoked tool from agent intermediate steps."""
    if not intermediate_steps:
        return None

    first_step = intermediate_steps[0]
    if isinstance(first_step, tuple) and len(first_step) >= 1:
        action = first_step[0]
        if hasattr(action, "tool"):
            return action.tool
        if isinstance(action, dict) and "tool" in action:
            return action["tool"]

    step_repr = repr(first_step)
    match = re.search(r"tool='([^']+)'", step_repr)
    if match:
        return match.group(1)
    match = re.search(r'"tool":\s*"([^"]+)"', step_repr)
    if match:
        return match.group(1)
    return None


def extract_all_tools(intermediate_steps: list[Any]) -> list[str]:
    """Extract all invoked tool names in order."""
    tools: list[str] = []
    for step in intermediate_steps:
        if isinstance(step, tuple) and len(step) >= 1:
            action = step[0]
            if hasattr(action, "tool"):
                tools.append(action.tool)
            elif isinstance(action, dict) and "tool" in action:
                tools.append(action["tool"])
    return tools


def normalize_task_type(task_type: str) -> str:
    """Normalize task type labels from JSON or LLM output."""
    match = re.search(r"\[([^\]]+)\]", task_type)
    if match:
        return match.group(1).strip().strip("'\"")
    return task_type.strip().strip("'\"")


def score_single_tool_prediction(
    task_type: str,
    intermediate_steps: list[Any],
    task_to_tool: dict[str, str],
) -> bool:
    """Check whether the first invoked tool matches the expected tool."""
    expected = task_to_tool.get(normalize_task_type(task_type))
    if not expected:
        return False
    predicted = extract_first_tool(intermediate_steps)
    return predicted == expected


def parse_intermediate_steps(raw_steps: Any) -> list[Any]:
    """Parse intermediate steps from saved JSONL results."""
    if isinstance(raw_steps, list):
        return raw_steps
    if isinstance(raw_steps, str):
        try:
            return ast.literal_eval(raw_steps)
        except (SyntaxError, ValueError):
            return []
    return []
