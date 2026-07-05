# DualRAG: Weighted Dual-Path Retrieval-Augmented Generation

This directory contains a modified fork of [LightRAG](https://github.com/HKUDS/LightRAG) implementing the **DualRAG** method proposed in RS-Agent.

## Key Modifications

Compared to the original LightRAG baseline (`LightRAG_old` in the research workspace), DualRAG modifies:

| File | Change |
|------|--------|
| `lightrag/prompt.py` | Keyword extraction now assigns per-keyword **importance** scores (0–10) |
| `lightrag/operate.py` | **Dual-path retrieval**: global concatenated query + per-keyword weighted allocation |

## Installation

```bash
cd dualrag
pip install -e .
```

## Evaluation Pipeline

```bash
# 1. Prepare unique contexts from corpus
python reproduce/Step_0.py

# 2. Index documents into knowledge graph
python reproduce/Step_1.py

# 3. Generate evaluation questions (requires OPENAI_API_KEY)
python reproduce/Step_2.py

# 4. Run queries (local / global / hybrid modes)
python reproduce/Step_3.py
python reproduce/Step_3_local.py
python reproduce/Step_3_global.py

# 5. Compare DualRAG vs LightRAG baseline
python datasets/eval.py
```

## Environment Variables

Set in the project root `.env` or export directly:

```bash
export OPENAI_API_KEY=your-key
export OPENAI_API_BASE=https://api.openai.com/v1
```

## Note on Baseline

The original LightRAG baseline used for ablation in the paper is kept separately in the research workspace (`LightRAG_old/`). It is not included here to avoid duplication. For pairwise comparison, install both forks in separate virtual environments.
