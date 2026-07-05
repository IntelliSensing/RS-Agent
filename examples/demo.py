#!/usr/bin/env python3
"""Minimal demo: run RS-Agent on a single query."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from rs_agent.config import load_config, resolve_path
from rs_agent.controller.agent import RSAgent


def main() -> None:
    parser = argparse.ArgumentParser(description="RS-Agent single-query demo")
    parser.add_argument("--question", type=str, required=True)
    parser.add_argument("--image", type=str, default=None)
    parser.add_argument("--config", type=str, default=None)
    parser.add_argument("--mode", type=str, default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    if args.mode:
        config.setdefault("agent", {})["mode"] = args.mode

    agent = RSAgent.from_config(config)
    image_path = args.image or str(resolve_path(config["paths"]["default_image"]))

    result = agent.run(question=args.question, image_path=image_path)

    print("Predicted task type:", result.get("predicted_task_type"))
    print("Guidance:", result.get("guidance"))
    print("Output:", result.get("output"))
    if result.get("intermediate_steps"):
        print("Tools invoked:", [s[0].tool for s in result["intermediate_steps"]])


if __name__ == "__main__":
    main()
