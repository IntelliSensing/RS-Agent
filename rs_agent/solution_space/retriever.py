"""Task-Aware Retrieval for the Solution Space."""

from __future__ import annotations

import re
from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def _clean_content(content: str) -> str:
    return content.strip().replace("\n", " ").replace("\r", "").replace("  ", " ")


class SolutionRetriever:
    """Retrieve expert solution guidance using Task-Aware Retrieval."""

    def __init__(
        self,
        index_dir: str | Path,
        embedding_model: str = "moka-ai/m3e-base",
        device: str = "cpu",
        top_k: int = 10,
    ) -> None:
        self.top_k = top_k
        self.embed_model = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={"device": device},
        )
        self.store = FAISS.load_local(
            str(index_dir),
            self.embed_model,
            allow_dangerous_deserialization=True,
        )

    def retrieve(self, task_type: str) -> str | None:
        """Retrieve solution guidance conditioned on inferred task type."""
        query = self._normalize_task_type(task_type)
        results = self.store.similarity_search_with_score(query, k=self.top_k)

        filtered = [
            (doc, score)
            for doc, score in results
            if query.lower() in doc.page_content.lower()
        ]

        if filtered:
            filtered.sort(key=lambda item: item[1], reverse=True)
            return _clean_content(filtered[0][0].page_content)

        return _clean_content(results[0][0].page_content) if results else None

    def retrieve_by_query(self, query: str) -> str | None:
        """Retrieve solution guidance using the raw user query (ablation mode)."""
        results = self.store.similarity_search_with_score(query, k=self.top_k)

        filtered = [
            (doc, score)
            for doc, score in results
            if query.lower() in doc.page_content.lower()
        ]

        if filtered:
            filtered.sort(key=lambda item: item[1], reverse=True)
            return _clean_content(filtered[0][0].page_content)

        return _clean_content(results[0][0].page_content) if results else None

    @staticmethod
    def _normalize_task_type(task_type: str) -> str:
        """Extract task type label from LLM output like '["Scene_Classification"]'."""
        match = re.search(r"\[([^\]]+)\]", task_type)
        if match:
            return match.group(1).strip().strip("'\"")
        return task_type.strip().strip("'\"")
