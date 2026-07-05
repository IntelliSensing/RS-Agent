"""Configuration loading for RS-Agent."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent


def _deep_update(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_update(base[key], value)
        else:
            base[key] = value
    return base


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """Load YAML config and apply environment variable overrides."""
    load_dotenv(PROJECT_ROOT / ".env")

    config_file = Path(config_path) if config_path else PROJECT_ROOT / "configs" / "default.yaml"
    with open(config_file, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    config["embedding"]["model"] = os.getenv("EMBEDDING_MODEL", config["embedding"]["model"])
    config["embedding"]["device"] = os.getenv("EMBEDDING_DEVICE", config["embedding"]["device"])

    if os.getenv("OPENAI_API_KEY"):
        config.setdefault("llm", {})["api_key"] = os.getenv("OPENAI_API_KEY")
    if os.getenv("OPENAI_API_BASE"):
        config.setdefault("llm", {})["api_base"] = os.getenv("OPENAI_API_BASE")

    return config


def resolve_path(path: str | Path) -> Path:
    """Resolve a path relative to the project root."""
    path = Path(path)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path
