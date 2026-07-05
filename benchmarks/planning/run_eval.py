#!/usr/bin/env python3
"""Run task planning accuracy evaluation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from rs_agent.config import load_config, resolve_path
from rs_agent.controller.agent import RSAgent
from rs_agent.toolkit.registry import TASK_TO_TOOL, TASK_TO_TOOL_RSCHATGPT
from benchmarks.planning.score import score_single_tool_prediction


def run_eval(
    input_file: Path,
    output_file: Path,
    config_path: str | None = None,
    toolkit: str = "rsagent",
    image_path: str | None = None,
    limit: int | None = None,
) -> None:
    config = load_config(config_path)
    agent = RSAgent.from_config(config, toolkit=toolkit)  # type: ignore[arg-type]

    task_to_tool = TASK_TO_TOOL if toolkit == "rsagent" else TASK_TO_TOOL_RSCHATGPT
    default_image = image_path or str(resolve_path(config["paths"]["default_image"]))

    questions = []
    with open(input_file, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                questions.append(json.loads(line))

    if limit:
        questions = questions[:limit]

    output_file.parent.mkdir(parents=True, exist_ok=True)
    if output_file.exists():
        output_file.unlink()

    correct = 0
    total = 0

    for item in tqdm(questions, desc="Evaluating task planning"):
        question_id = item["question_id"]
        task_type = item["task_type"]
        question = item["question"]

        try:
            result = agent.run(question=question, image_path=default_image)
            steps = result["intermediate_steps"]
            is_correct = score_single_tool_prediction(task_type, steps, task_to_tool)
            correct += int(is_correct)
            total += 1

            record = {
                "question_id": question_id,
                "task_type": task_type,
                "predicted_task_type": result.get("predicted_task_type"),
                "first_tool": steps[0][0].tool if steps else None,
                "correct": is_correct,
                "intermediate_steps": [repr(s) for s in steps],
            }
        except Exception as exc:
            record = {
                "question_id": question_id,
                "task_type": task_type,
                "error": str(exc),
                "correct": False,
            }
            total += 1

        with open(output_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    accuracy = correct / total if total else 0.0
    print(f"Task planning accuracy: {correct}/{total} = {accuracy:.2%}")


def main() -> None:
    parser = argparse.ArgumentParser(description="RS-Agent task planning evaluation")
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Input JSONL file (defaults to config paths.eval_questions)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "outputs/planning_results.jsonl",
    )
    parser.add_argument("--config", type=str, default=None)
    parser.add_argument("--toolkit", choices=["rsagent", "rschatgpt"], default="rsagent")
    parser.add_argument("--image", type=str, default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--mode",
        choices=["full", "baseline", "task_inference_only", "solution_retrieval_only"],
        default=None,
    )
    args = parser.parse_args()

    config = load_config(args.config)
    input_file = args.input or resolve_path(config["paths"]["eval_questions"])

    if args.mode:
        import yaml

        config.setdefault("agent", {})["mode"] = args.mode
        tmp_config = PROJECT_ROOT / "outputs" / "_tmp_config.yaml"
        tmp_config.parent.mkdir(parents=True, exist_ok=True)
        with open(tmp_config, "w", encoding="utf-8") as f:
            yaml.dump(config, f)
        run_eval(input_file, args.output, str(tmp_config), args.toolkit, args.image, args.limit)
    else:
        run_eval(input_file, args.output, args.config, args.toolkit, args.image, args.limit)


if __name__ == "__main__":
    main()
