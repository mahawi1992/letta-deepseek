from typing import Dict, Any
from letta import create_client
from letta.schemas.memory import ChatMemory
from letta.schemas.llm_config import LLMConfig
from .deepseek_wrapper import DeepSeekWrapper

class CodingAgent:
    def __init__(self):
        self.llm = DeepSeekWrapper()
        self.client = create_client()
        self.setup_agent()

    def setup_agent(self):
        """Initialize the Letta agent with coding-specific memory"""
        self.agent_state = self.client.create_agent(
            name="deepseek_coding_agent",
            memory=ChatMemory(
                human="",
                persona=self._get_coding_persona()
            ),
            llm_config=self._get_custom_llm_config()
        )

    def _get_coding_persona(self) -> str:
        return """You are an expert programming assistant powered by DeepSeek-Coder.
Your expertise includes:
- Writing clean, efficient, and well-documented code
- Debugging and problem-solving
- Best practices and design patterns
- Multiple programming languages with a focus on Python
Always explain your code and include comments for clarity."""

    def _get_custom_llm_config(self) -> LLMConfig:
        """Create custom LLM configuration for DeepSeek"""
        return LLMConfig(
            model_provider="custom",
            model_name="deepseek-coder-v2.5",
            generate_fn=self.llm.generate
        )

    async def process_message(self, message: str) -> Dict[str, Any]:
        """Process incoming messages and return responses"""
        response = self.client.send_message(
            agent_id=self.agent_state.id,
            message=message,
            role="user"
        )
        return {
            "response": response.messages[-1].content,
            "agent_id": self.agent_state.id
        }

    def get_memory(self) -> Dict[str, Any]:
        """Retrieve agent's memory state"""
        return self.client.get_core_memory(self.agent_state.id)