import os
from typing import Dict, Any, Optional
from datetime import datetime
import json
from langchain_community.tools import TavilySearchResults
from letta.schemas.memory import ChatMemory
from letta.schemas.llm_config import LLMConfig
from .documentation import EnhancedDocumentation

class ResearchAgent:
    def __init__(self, client, shared_block, enhanced_features: Optional[Dict[str, bool]] = None):
        self.client = client
        self.shared_block = shared_block
        self.search_tool = TavilySearchResults(
            api_key=os.getenv("TAVILY_API_KEY"),
            search_depth="advanced",
            include_domains=[
                "github.com",
                "stackoverflow.com",
                "python.org",
                "docs.python.org",
                "developer.mozilla.org"
            ]
        )
        
        # Initialize agent with shared memory
        self.agent_state = self.client.create_agent(
            name="research_agent",
            memory=ChatMemory(
                human="",
                persona=self._get_research_persona()
            ),
            tools=[self.search_tool.name]
        )
        
        # Initialize documentation manager if enabled
        if enhanced_features and enhanced_features.get("documentation_storage"):
            self.docs = EnhancedDocumentation(client, self.agent_state.id)

    def _get_research_persona(self) -> str:
        return """You are an advanced research agent specialized in technical research and documentation.
        Your responsibilities:
        1. Search and analyze programming topics
        2. Maintain comprehensive documentation
        3. Store and retrieve best practices
        4. Build knowledge base
        5. Track technology trends
        6. Share findings through shared memory
        7. Validate and update stored information"""

    async def research(self, query: str) -> Dict[str, Any]:
        # Check existing documentation first
        if hasattr(self, 'docs'):
            existing_docs = await self.docs.search_documentation(query)
            if existing_docs:
                recent_docs = [doc for doc in existing_docs 
                             if (datetime.now() - datetime.fromisoformat(doc['metadata']['timestamp'])).days < 30]
                if recent_docs:
                    return self._prepare_documented_response(recent_docs[0])

        # Perform research using Tavily
        search_results = self.search_tool.run(
            query,
            search_parameters={
                "max_results": 10,
                "sort_by": "relevance"
            }
        )

        # Process and analyze findings
        analysis_prompt = f"""Analyze these search results and provide:
        1. Key technical insights
        2. Best practices identified
        3. Common patterns or approaches
        4. Potential pitfalls to avoid

        Search results:
        {json.dumps(search_results, indent=2)}"""

        response = self.client.send_message(
            agent_id=self.agent_state.id,
            message=analysis_prompt,
            role="user"
        )

        findings = {
            "query": query,
            "timestamp": str(datetime.now()),
            "results": search_results,
            "summary": response.messages[-1].content,
            "categories": self._extract_categories(response.messages[-1].content),
            "best_practices": self._extract_best_practices(response.messages[-1].content)
        }

        # Store findings if documentation is enabled
        if hasattr(self, 'docs'):
            await self.docs.store_documentation(
                doc_type="research_findings",
                content=findings,
                metadata={
                    "query": query,
                    "timestamp": str(datetime.now()),
                    "source": "tavily"
                }
            )

        return findings

    def _extract_categories(self, text: str) -> List[str]:
        categories = set()
        category_indicators = {
            'algorithm': ['algorithm', 'complexity', 'optimization'],
            'design_pattern': ['pattern', 'design', 'architecture'],
            'security': ['security', 'authentication', 'encryption'],
            'performance': ['performance', 'optimization', 'scaling'],
            'best_practice': ['practice', 'convention', 'standard']
        }

        for category, indicators in category_indicators.items():
            if any(indicator in text.lower() for indicator in indicators):
                categories.add(category)

        return list(categories)

    def _extract_best_practices(self, text: str) -> List[str]:
        practices = []
        lines = text.split('\n')
        for line in lines:
            if any(indicator in line.lower() for indicator in 
                   ['best practice', 'recommended', 'should', 'must', 'important']):
                practices.append(line.strip())
        return practices

    def _prepare_documented_response(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "query": doc["metadata"]["query"],
            "timestamp": doc["metadata"]["timestamp"],
            "results": doc["content"]["results"],
            "summary": doc["content"]["summary"],
            "source": "documentation",
            "categories": doc["content"].get("categories", []),
            "best_practices": doc["content"].get("best_practices", [])
        }

class CodingAgent:
    def __init__(self, client, shared_block, model_config: Optional[LLMConfig] = None):
        self.client = client
        self.shared_block = shared_block
        
        self.agent_state = self.client.create_agent(
            name="coding_agent",
            memory=ChatMemory(
                human="",
                persona=self._get_coding_persona()
            ),
            llm_config=model_config or self._get_default_config()
        )

    def _get_coding_persona(self) -> str:
        return """You are an expert programming assistant with access to research insights.
        Your responsibilities:
        1. Implement solutions based on research findings
        2. Write clean, efficient, and well-documented code
        3. Follow best practices and patterns
        4. Consider security and performance implications
        5. Learn from shared experiences
        6. Provide comprehensive documentation
        7. Include error handling and edge cases"""

    def _get_default_config(self) -> LLMConfig:
        return LLMConfig(
            model_provider="openai",
            model_name="deepseek-v2.5",
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            api_base="https://api.deepseek.com/v1",
            model_kwargs={
                "temperature": 0.7,
                "top_p": 0.95,
                "max_tokens": 4096,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1
            }
        )

    async def implement(self, research_findings: Dict[str, Any], request: str) -> Dict[str, Any]:
        # Create implementation prompt
        implementation_prompt = f"""Based on the following research and request, implement a solution:

        Research Findings:
        {research_findings['summary']}

        Best Practices to Follow:
        {json.dumps(research_findings.get('best_practices', []), indent=2)}

        Request:
        {request}

        Please provide:
        1. Implementation explanation
        2. Code solution
        3. Usage examples
        4. Error handling
        5. Performance considerations
        6. Security notes (if applicable)
        7. Testing suggestions"""

        response = self.client.send_message(
            agent_id=self.agent_state.id,
            message=implementation_prompt,
            role="user"
        )

        content = response.messages[-1].content
        explanation = content
        code = ""

        # Extract code blocks
        if "```" in content:
            parts = content.split("```")
            explanation = parts[0]
            
            for i in range(1, len(parts), 2):
                if parts[i].startswith('python'):
                    code += parts[i][6:].strip() + "\n\n"
                else:
                    code += parts[i].strip() + "\n\n"

        return {
            "explanation": explanation.strip(),
            "code": code.strip() if code else None,
            "research_findings": research_findings,
            "timestamp": str(datetime.now())
        }
