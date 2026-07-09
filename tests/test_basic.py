"""Basic unit tests for RS-Agent (no LLM required)."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from benchmarks.planning.score import (
    extract_first_tool,
    normalize_task_type,
    score_single_tool_prediction,
)
from rs_agent.config import load_config, resolve_path
from rs_agent.toolkit.registry import TASK_TO_TOOL, get_stub_tools


class FakeAction:
    def __init__(self, tool: str):
        self.tool = tool


def test_normalize_task_type():
    assert normalize_task_type('["Scene_Classification"]') == "Scene_Classification"
    assert normalize_task_type("Scene_Classification") == "Scene_Classification"
    assert normalize_task_type("Object Counting") == "Object_Counting"


def test_extract_first_tool():
    steps = [(FakeAction("scene"), "result")]
    assert extract_first_tool(steps) == "scene"


def test_score_single_tool():
    steps = [(FakeAction("denoising"), "ok")]
    assert score_single_tool_prediction("Denoising", steps, TASK_TO_TOOL) is True
    assert score_single_tool_prediction("Captioning", steps, TASK_TO_TOOL) is False


def test_config_loads():
    config = load_config()
    assert "llm" in config
    assert "solution_space" in config
    assert resolve_path("data/solutions/guidance.txt").exists()


def test_solution_data_exists():
    assert (PROJECT_ROOT / "data/solutions/guidance.txt").exists()
    assert (PROJECT_ROOT / "data/indices/solution_db/index.faiss").exists()
    assert (PROJECT_ROOT / "examples/sample.png").exists()


def test_stub_tools():
    assert len(get_stub_tools("rsagent")) > 0
    assert len(get_stub_tools("rschatgpt")) == 7
