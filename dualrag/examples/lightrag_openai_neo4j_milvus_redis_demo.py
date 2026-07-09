import os
import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_embed, openai_complete_if_cache
from lightrag.utils import EmbeddingFunc
from lightrag.kg.shared_storage import initialize_pipeline_status

# WorkingDir
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKING_DIR = os.path.join(ROOT_DIR, "myKG")
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)
print(f"WorkingDir: {WORKING_DIR}")

# redis
os.environ["REDIS_URI"] = "redis://localhost:6379"

# neo4j / milvus / redis — configure via environment variables before running
os.environ.setdefault("NEO4J_URI", "bolt://localhost:7687")
os.environ.setdefault("NEO4J_USERNAME", "neo4j")
os.environ.setdefault("NEO4J_PASSWORD", "your-neo4j-password")

os.environ.setdefault("MILVUS_URI", "http://localhost:19530")
os.environ.setdefault("MILVUS_USER", "root")
os.environ.setdefault("MILVUS_PASSWORD", "your-milvus-password")
os.environ.setdefault("MILVUS_DB_NAME", "lightrag")

ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
openai_api_key = os.environ.get("OPENAI_API_KEY", "")
openai_api_base = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
llm_model = os.environ.get("LLM_MODEL", "gpt-4o-mini")


async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs
) -> str:
    return await openai_complete_if_cache(
        llm_model,
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key=openai_api_key,
        base_url=openai_api_base,
        **kwargs,
    )


embedding_func = EmbeddingFunc(
    embedding_dim=768,
    max_token_size=512,
    func=lambda texts: ollama_embed(
        texts, embed_model="shaw/dmeta-embedding-zh", host=ollama_host
    ),
)


async def initialize_rag():
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=llm_model_func,
        llm_model_max_token_size=32768,
        embedding_func=embedding_func,
        chunk_token_size=512,
        chunk_overlap_token_size=256,
        kv_storage="RedisKVStorage",
        graph_storage="Neo4JStorage",
        vector_storage="MilvusVectorDBStorage",
        doc_status_storage="RedisKVStorage",
    )

    await rag.initialize_storages()
    await initialize_pipeline_status()

    return rag


def main():
    # Initialize RAG instance
    rag = asyncio.run(initialize_rag())

    with open("./book.txt", "r", encoding="utf-8") as f:
        rag.insert(f.read())

    # Perform naive search
    print(
        rag.query(
            "What are the top themes in this story?", param=QueryParam(mode="naive")
        )
    )

    # Perform local search
    print(
        rag.query(
            "What are the top themes in this story?", param=QueryParam(mode="local")
        )
    )

    # Perform global search
    print(
        rag.query(
            "What are the top themes in this story?", param=QueryParam(mode="global")
        )
    )

    # Perform hybrid search
    print(
        rag.query(
            "What are the top themes in this story?", param=QueryParam(mode="hybrid")
        )
    )


if __name__ == "__main__":
    main()
