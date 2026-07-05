#!/usr/bin/env python3
"""Build the Solution Space FAISS index."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from rs_agent.config import load_config, resolve_path
from rs_agent.solution_space.builder import build_solution_index


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Solution Space FAISS index")
    parser.add_argument("--config", type=str, default=None)
    parser.add_argument("--source", type=str, default=None, help="Override source file")
    parser.add_argument("--output", type=str, default=None, help="Override output directory")
    args = parser.parse_args()

    config = load_config(args.config)
    source = resolve_path(args.source or config["solution_space"]["source_file"])
    output = resolve_path(args.output or config["solution_space"]["index_dir"])

    count = build_solution_index(
        source_file=source,
        output_dir=output,
        embedding_model=config["embedding"]["model"],
        device=config["embedding"]["device"],
    )
    print(f"Built index with {count} documents at {output}")


if __name__ == "__main__":
    main()
