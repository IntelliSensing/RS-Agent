"""Build FAISS index for the Solution Database."""

from __future__ import annotations

from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def build_solution_index(
    source_file: str | Path,
    output_dir: str | Path,
    embedding_model: str = "moka-ai/m3e-base",
    device: str = "cpu",
) -> int:
    """Build and save a FAISS index from solution documents."""
    source_file = Path(source_file)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    loader = TextLoader(str(source_file), encoding="utf-8")
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n"],
        chunk_size=300,
        chunk_overlap=0,
    )
    docs = splitter.split_documents(pages)

    embed_model = HuggingFaceEmbeddings(
        model_name=embedding_model,
        model_kwargs={"device": device},
    )
    store = FAISS.from_documents(docs, embed_model)
    store.save_local(str(output_dir))
    return len(docs)
