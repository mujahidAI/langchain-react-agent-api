import logging
import os
import time
from typing import Any, Union
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("agent_api")
logger.setLevel(logging.INFO)

# console handler — prints to terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# file handler — writes to logs/agent.log
file_handler = logging.FileHandler("logs/agent.log")
file_handler.setLevel(logging.INFO)

# format
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


class LoggingCallbackHandler(BaseCallbackHandler):
    """Logs all LangChain events — LLM calls, tool calls, chain events."""

    def __init__(self):
        self._llm_start_time: dict[str, float] = {}

    # Chain events
    def on_chain_start(
        self,
        serialized: dict,
        inputs: dict,
        run_id: UUID,
        **kwargs,
    ) -> None:
        chain_name = serialized.get("name", "Unknown Chain")
        logger.info(f"CHAIN START | {chain_name} | input keys: {list(inputs.keys())}")

    def on_chain_end(self, outputs: dict, run_id: UUID, **kwargs) -> None:
        logger.info(f"CHAIN END | output keys: {list(outputs.keys())}")

    def on_chain_error(
        self, error: Union[Exception, KeyboardInterrupt], run_id: UUID, **kwargs
    ) -> None:
        logger.error(f"CHAIN ERROR | {type(error).__name__}: {str(error)}")

    # LLM events
    def on_llm_start(
        self, serialized: dict, prompts: list[str], run_id: UUID, **kwargs
    ) -> None:
        self._llm_start_time[str(run_id)] = time.time()
        model = serialized.get("kwargs", {}).get("model", "unknown")
        logger.info(
            f"LLM START | model: {model} | prompt length: {len(prompts[0])} chars"
        )

    def on_llm_end(self, response: LLMResult, run_id: UUID, **kwargs) -> None:
        elapsed = time.time() - self._llm_start_time.pop(str(run_id), time.time())

        # extract token usage if available
        usage = {}
        if response.llm_output:
            usage = response.llm_output.get("token_usage", {})

        output_text = response.generations[0][0].text if response.generations else ""

        logger.info(
            f"LLM END | time: {elapsed:.2f}s | "
            f"tokens: {usage} | "
            f"response length: {len(output_text)} chars"
        )

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], run_id: UUID, **kwargs
    ) -> None:
        logger.error(f"LLM ERROR | {type(error).__name__}: {str(error)}")

    #  Tool events

    def on_tool_start(
        self, serialized: dict, input_str: str, run_id: UUID, **kwargs
    ) -> None:
        tool_name = serialized.get("name", "unknown")
        logger.info(f"TOOL START | tool: {tool_name} | input: {input_str[:200]}")

    def on_tool_end(self, output: str, run_id: UUID, **kwargs) -> None:
        logger.info(
            f"TOOL END | output length: {len(output)} chars | preview: {output[:100]}"
        )

    def on_tool_error(
        self, error: Union[Exception, KeyboardInterrupt], run_id: UUID, **kwargs
    ) -> None:
        logger.error(f"TOOL ERROR | {type(error).__name__}: {str(error)}")

    #  Agent events

    def on_agent_action(self, action: Any, run_id: UUID, **kwargs) -> None:
        logger.info(
            f"AGENT ACTION | tool: {action.tool} | "
            f"input: {str(action.tool_input)[:200]}"
        )

    def on_agent_finish(self, finish: Any, run_id: UUID, **kwargs) -> None:
        logger.info(
            f"AGENT FINISH | output: {str(finish.return_values.get('output', ''))[:200]}"
        )
