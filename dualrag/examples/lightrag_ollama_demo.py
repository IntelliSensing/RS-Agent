import asyncio
import nest_asyncio

nest_asyncio.apply()
import os
import inspect
import logging
from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc
from lightrag.kg.shared_storage import initialize_pipeline_status

WORKING_DIR = "./remote_data"

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


async def initialize_rag():
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
    await rag.initialize_storages()
    await initialize_pipeline_status()

    return rag


async def print_stream(stream):
    async for chunk in stream:
        print(chunk, end="", flush=True)


def main():
    # Initialize RAG instance
    rag = asyncio.run(initialize_rag())
    
    
    # from pypdf import PdfReader
    # file_path = '/home/yzj/data2/code2024/GPT/gptAPI_demo/langchain/RS_agent/LightRAG/remote_sensing.pdf'
    # reader = PdfReader(file_path)
    # text_content = ""
    # for page in reader.pages:
    #     text_content += page.extract_text()
    # rag.insert(text_content)


    # # Insert example text
    # with open("./santi.txt", "r", encoding="utf-8") as f:
    #     rag.insert(f.read())

    # # Test different query modes
    # print("\nNaive Search:")
    # print(
    #     rag.query(
    #         "Give a detailed description about the whole database", param=QueryParam(only_need_context=True, mode="naive")
    #         # "What is Remote Sensing?", param=QueryParam(mode="naive")
    #     )
    # )

    # print("\nLocal Search:")
    # print(
    #     rag.query(
    #         "What are the top themes in this book?", param=QueryParam(mode="local")
    #     )
    # )

    # print("\nGlobal Search:")
    # print(
    #     rag.query(
    #         "What are the top themes in this book?", param=QueryParam(only_need_context=True,mode="global")
    #     )
    # )

    print("\nHybrid Search:")
    print(
        rag.query(
            "What are the key performance and operational differences between the Su-35 and C-130 models?", param=QueryParam(top_k=10, mode="hybrid")
        )
    )

    # # stream response
    # print("\nHybrid Search:")
    # resp = rag.query(
    #     "What is Remote Sensing?",
    #     # param=QueryParam(mode="hybrid", only_need_context=True, stream=True),
    #     param=QueryParam(mode="hybrid", stream=True),
    # )

    # if inspect.isasyncgen(resp):
    #     asyncio.run(print_stream(resp))
    # else:
    #     print(resp)


if __name__ == "__main__":
    main()
