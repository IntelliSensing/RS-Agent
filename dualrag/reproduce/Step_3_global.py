import re
import json
from pathlib import Path

from lightrag import LightRAG, QueryParam
from lightrag.utils import always_get_an_event_loop
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc

def extract_queries(file_path):
    with open(file_path, "r") as f:
        data = f.read()

    data = data.replace("**", "")

    queries = re.findall(r"- Question \d+: (.+)", data)

    return queries


async def process_query(query_text, rag_instance, query_param):
    try:
        result = await rag_instance.aquery(query_text, param=query_param)
        return {"query": query_text, "result": result}, None
    except Exception as e:
        return None, {"query": query_text, "error": str(e)}


def run_queries_and_save_to_json(
    queries, rag_instance, query_param, output_file, error_file
):
    loop = always_get_an_event_loop()

    with open(output_file, "a", encoding="utf-8") as result_file, open(
        error_file, "a", encoding="utf-8"
    ) as err_file:
        result_file.write("[\n")
        first_entry = True

        for query_text in queries:
            result, error = loop.run_until_complete(
                process_query(query_text, rag_instance, query_param)
            )

            if result:
                if not first_entry:
                    result_file.write(",\n")
                json.dump(result, result_file, ensure_ascii=False, indent=4)
                first_entry = False
            elif error:
                json.dump(error, err_file, ensure_ascii=False, indent=4)
                err_file.write("\n")

        result_file.write("\n]")


if __name__ == "__main__":
    dualrag_root = Path(__file__).resolve().parents[1]
    datasets_dir = dualrag_root / "datasets"

    cls = "mix"
    mode = "global"
    WORKING_DIR = f"./{cls}"

    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=ollama_model_complete,
        llm_model_name="qwen2.5:14b-instruct",
        llm_model_max_async=4,
        llm_model_max_token_size=32768,
        llm_model_kwargs={
            "host": "http://localhost:11434",
            "options": {"num_ctx": 32768},
        },
        embedding_func=EmbeddingFunc(
            embedding_dim=1024, #768,
            max_token_size=8192, #8192,
            func=lambda texts: ollama_embed(
                texts, embed_model="bge-m3:latest", host="http://localhost:11434"
            ),
        ),
    )
    query_param = QueryParam(mode=mode)

    query_file = datasets_dir / "questions" / f"{cls}_questions.txt"
    queries = extract_queries(str(query_file))
    run_queries_and_save_to_json(
        queries, rag, query_param, f"{cls}_global_result.json", f"{cls}_global_errors.json"
    )
