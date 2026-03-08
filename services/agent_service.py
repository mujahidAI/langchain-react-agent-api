import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from callbacks import LoggingCallbackHandler
from services.tools import all_tools

BASE_DIR = Path(__file__).resolve().parents[1]
PROMPT_FILE = BASE_DIR / "services" / "react_prompt.txt"


def _load_react_prompt_template() -> PromptTemplate:
    if not PROMPT_FILE.exists():
        raise FileNotFoundError(f"Prompt file not found: {PROMPT_FILE}")

    content = PROMPT_FILE.read_text(encoding="utf-8").strip()
    if not content:
        raise ValueError(f"Prompt file is empty: {PROMPT_FILE}")

    return PromptTemplate.from_template(content)


class AgentService:
    def __init__(self, model_name: str, temperature: float, max_iterations: int):
        load_dotenv(BASE_DIR / ".env")

        self.model_name = model_name
        self.max_iterations = max_iterations
        self.prompt_template = _load_react_prompt_template()
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model=self.model_name,
            temperature=temperature,
        )
        self.callback_handler = LoggingCallbackHandler()

    def run(self, query: str) -> dict:
        agent = create_react_agent(
            llm=self.llm,
            tools=all_tools,
            prompt=self.prompt_template,
        )
        executor = AgentExecutor(
            agent=agent,
            tools=all_tools,
            max_iterations=self.max_iterations,
            handle_parsing_errors=True,
            verbose=False,
            callbacks=[self.callback_handler],
            return_intermediate_steps=True,
        )
        result = executor.invoke({"input": query})

        steps = []
        for action, observation in result.get("intermediate_steps", []):
            steps.append(
                f"Tool: {getattr(action, 'tool', '')} | "
                f"Input: {getattr(action, 'tool_input', '')} | "
                f"Result: {observation}"
            )

        return {
            "result": result.get("output", ""),
            "steps": steps,
        }
