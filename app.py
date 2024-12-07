import os
import gradio as gr
from lightning.app import LightningFlow, LightningApp
from letta import create_client
from letta.schemas.memory import ChatMemory
from letta.schemas.llm_config import LLMConfig
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LettaCodingApp(LightningFlow):
    def __init__(self):
        super().__init__()
        self.client = create_client()
        self.setup_agent()

    def setup_agent(self):
        """Initialize the Letta agent with DeepSeek V2.5"""
        llm_config = LLMConfig(
            model_provider="openai",  # DeepSeek is OpenAI API compatible
            model_name="deepseek-v2.5",  # Latest combined model
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            api_base="https://api.deepseek.com/v1",
            model_kwargs={
                "temperature": 0.7,
                "top_p": 0.95,
                "max_tokens": 4096,  # V2.5 supports longer outputs
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1
            }
        )

        persona = """You are an expert AI assistant powered by DeepSeek V2.5, combining advanced coding capabilities with general intelligence. 
Your expertise includes:

Programming:
- Writing clean, efficient, and well-documented code
- Advanced software architecture and design patterns
- Debugging complex issues
- Best practices in multiple programming languages
- Modern development workflows and tools

General Capabilities:
- Technical documentation and explanation
- Problem-solving and algorithmic thinking
- System design and optimization
- Code review and improvement suggestions

When writing code:
1. Always include comprehensive comments
2. Follow best practices and modern conventions
3. Consider performance implications
4. Include error handling where appropriate
5. Break down complex solutions into manageable parts

For complex requests:
1. First clarify the requirements if needed
2. Explain your approach before implementing
3. Provide examples and explanations with the code
4. Suggest potential improvements or alternatives"""

        self.agent_state = self.client.create_agent(
            name="deepseek_v25_agent",
            memory=ChatMemory(
                human="",
                persona=persona
            ),
            llm_config=llm_config
        )

    async def process_message(self, message: str):
        """Handle incoming messages to the agent"""
        response = self.client.send_message(
            agent_id=self.agent_state.id,
            message=message,
            role="user"
        )
        
        # Extract code blocks from response
        content = response.messages[-1].content
        code = ""
        explanation = content
        
        if "```" in content:
            parts = content.split("```")
            # Store non-code parts as explanation
            explanation = parts[0]
            for i in range(2, len(parts), 2):
                explanation += parts[i]
            
            # Extract code parts
            for i in range(1, len(parts), 2):
                lang_hint = parts[i].split('\n')[0].lower()
                code_part = parts[i]
                if lang_hint in ['python', 'py']:
                    code_part = '\n'.join(parts[i].split('\n')[1:])
                code += code_part.strip() + '\n\n'

        return {
            "explanation": explanation.strip(),
            "code": code.strip() if code else None
        }

    def setup_interface(self):
        """Create Gradio interface"""
        interface = gr.Interface(
            fn=self.process_message,
            inputs=[
                gr.Textbox(
                    label="Question/Request",
                    placeholder="Ask me about coding, technical concepts, or general programming questions...",
                    lines=3
                )
            ],
            outputs=[
                gr.Textbox(label="Explanation", lines=5),
                gr.Code(label="Code Output", language="python", lines=10)
            ],
            title="DeepSeek V2.5 Coding Assistant",
            description="""Powered by Letta AI and DeepSeek V2.5 - Combining advanced coding capabilities with general intelligence.
            Ask about code implementation, software design, debugging, or any technical concepts.""",
            examples=[
                ["Write a Python class for a REST API client with async support"],
                ["Explain and implement the Observer design pattern"],
                ["Create a data processing pipeline using Python generators"],
                ["How would you optimize a slow database query? Show examples."],
                ["Implement a React component that fetches and displays data with error handling"]
            ]
        )
        return interface

app = LightningApp(LettaCodingApp().setup_interface())