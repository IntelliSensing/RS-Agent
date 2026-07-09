# RS-ChatGPT Baseline

Upstream repository: [HaonanGuo/Remote-Sensing-ChatGPT](https://github.com/HaonanGuo/Remote-Sensing-ChatGPT)

RS-Agent supports RS-ChatGPT as a comparison baseline via `--toolkit rschatgpt` in `benchmarks/planning/run_eval.py`.

Solution templates: `data/solutions/guidance_rschatgpt.txt`  
FAISS index: `data/indices/solution_db_rschatgpt/`

Evaluation questions are **not** included in this repository. Prepare a local JSONL file (fields: `question_id`, `task_type`, `question`) and pass it explicitly:

```bash
python benchmarks/planning/run_eval.py \
  --toolkit rschatgpt \
  --input /path/to/your/question_rschatgpt.jsonl
```
