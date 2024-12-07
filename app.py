import os
import gradio as gr
from lightning.app import LightningFlow, LightningApp
from components.orchestrator import EnhancedOrchestratorAgent

class WebInterface(LightningFlow):
    def __init__(self):
        super().__init__()
        self.orchestrator = EnhancedOrchestratorAgent()

    def setup_interface(self):
        interface = gr.Interface(
            fn=self.orchestrator.process_request,
            inputs=[
                gr.Textbox(
                    label="Request",
                    placeholder="Describe what you want to implement...",
                    lines=3
                )
            ],
            outputs=[
                gr.Textbox(label="Explanation", lines=5),
                gr.Code(label="Code Solution", language="python", lines=10),
                gr.Json(label="Research Findings")
            ],
            title="Research-Driven Coding Assistant",
            description="""An intelligent coding assistant that:
            1. Researches your request using Tavily
            2. Analyzes findings and best practices
            3. Implements a solution using DeepSeek
            4. Provides comprehensive documentation""",
            examples=[
                ["Implement a secure JWT authentication system in Python"],
                ["Create a Redis caching layer for a REST API"],
                ["Implement a rate limiting middleware for Express.js"],
                ["Build a connection pool for PostgreSQL with proper error handling"]
            ]
        )
        return interface

def create_app():
    app = LightningApp(WebInterface().setup_interface())
    return app