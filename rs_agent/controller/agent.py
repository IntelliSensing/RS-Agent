"""Central Controller for RS-Agent."""

from __future__ import annotations

from typing import Any, Literal

from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.tools import Tool
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

from rs_agent.controller.prompts import TASK_TYPE_PROMPT, TASK_TYPE_PROMPT_RSCHATGPT
from rs_agent.solution_space.retriever import SolutionRetriever

AgentMode = Literal["full", "baseline", "task_inference_only", "solution_retrieval_only"]
ToolkitType = Literal["rsagent", "rschatgpt"]


class RSAgent:
    """LLM-based central controller with Task-Aware Retrieval."""

    def __init__(
        self,
        llm: BaseChatModel,
        tools: list[Tool],
        solution_retriever: SolutionRetriever | None = None,
        mode: AgentMode = "full",
        toolkit: ToolkitType = "rsagent",
        verbose: bool = False,
    ) -> None:
        self.llm = llm
        self.tools = tools
        self.solution_retriever = solution_retriever
        self.mode = mode
        self.toolkit = toolkit
        self.verbose = verbose
        self.task_type_prompt = (
            TASK_TYPE_PROMPT if toolkit == "rsagent" else TASK_TYPE_PROMPT_RSCHATGPT
        )

    @classmethod
    def from_config(
        cls,
        config: dict[str, Any],
        tools: list[Tool] | None = None,
        toolkit: ToolkitType = "rsagent",
    ) -> "RSAgent":
        """Create an agent from a configuration dictionary."""
        from rs_agent.config import resolve_path
        from rs_agent.toolkit.registry import get_stub_tools

        llm_cfg = config["llm"]
        agent_cfg = config.get("agent", {})
        mode: AgentMode = agent_cfg.get("mode", "full")

        llm_kwargs: dict[str, Any] = {
            "model": llm_cfg["model"],
            "temperature": llm_cfg.get("temperature", 0),
        }
        if llm_cfg.get("api_key"):
            llm_kwargs["api_key"] = llm_cfg["api_key"]
        if llm_cfg.get("api_base"):
            llm_kwargs["base_url"] = llm_cfg["api_base"]

        if not llm_kwargs.get("api_key"):
            raise ValueError(
                "OPENAI_API_KEY is not set. Copy .env.example to .env and configure your API key."
            )

        llm = ChatOpenAI(**llm_kwargs)

        solution_retriever = None
        if mode in ("full", "solution_retrieval_only"):
            sol_cfg = config["solution_space"]
            if toolkit == "rschatgpt":
                index_dir = resolve_path("data/indices/solution_db_rschatgpt")
            else:
                index_dir = resolve_path(sol_cfg["index_dir"])
            solution_retriever = SolutionRetriever(
                index_dir=index_dir,
                embedding_model=config["embedding"]["model"],
                device=config["embedding"]["device"],
                top_k=sol_cfg.get("top_k", 10),
            )

        return cls(
            llm=llm,
            tools=tools or get_stub_tools(toolkit),
            solution_retriever=solution_retriever,
            mode=mode,
            toolkit=toolkit,
            verbose=agent_cfg.get("verbose", False),
        )

    def infer_task_type(self, question: str) -> str:
        """Stage 1: Task Inference."""
        prompt = self.task_type_prompt.format(question=question)
        response = self.llm.invoke(prompt)
        return response.content.strip()

    def retrieve_guidance(self, question: str, predicted_task_type: str | None) -> str | None:
        """Stage 1b: Solution Retrieval via Task-Aware Retrieval."""
        if self.solution_retriever is None:
            return None

        if self.mode == "solution_retrieval_only":
            return self.solution_retriever.retrieve_by_query(question)
        if self.mode == "full" and predicted_task_type:
            return self.solution_retriever.retrieve(predicted_task_type)
        return None

    def build_input(
        self,
        question: str,
        image_path: str,
        guidance: str | None,
        predicted_task_type: str | None,
    ) -> str:
        """Construct the agent input based on ablation mode."""
        base = f"{question} The image path is {image_path}."

        if self.mode == "baseline":
            return base
        if self.mode == "task_inference_only" and predicted_task_type:
            return f"{base} The task type for this problem is most likely:{predicted_task_type}"
        if guidance:
            return f"{base} The following content can offer you guidance to solve the question:{guidance}"
        return base

    def run(self, question: str, image_path: str) -> dict[str, Any]:
        """Execute the full RS-Agent workflow for a single query."""
        predicted_task_type = None
        guidance = None

        if self.mode in ("full", "task_inference_only", "solution_retrieval_only"):
            if self.mode != "solution_retrieval_only":
                predicted_task_type = self.infer_task_type(question)

        if self.mode in ("full", "solution_retrieval_only"):
            guidance = self.retrieve_guidance(question, predicted_task_type)

        agent_input = self.build_input(question, image_path, guidance, predicted_task_type)

        prompt = hub.pull("hwchase17/structured-chat-agent")
        agent = create_structured_chat_agent(self.llm, self.tools, prompt)
        executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=self.verbose,
            return_intermediate_steps=True,
        )
        output = executor.invoke({"input": agent_input})

        return {
            "predicted_task_type": predicted_task_type,
            "guidance": guidance,
            "output": output.get("output"),
            "intermediate_steps": output.get("intermediate_steps", []),
        }
