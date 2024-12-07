import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from letta.schemas.block import Block
from letta.schemas.memory import ChatMemory
from .agents import ResearchAgent, CodingAgent
from .documentation import EnhancedDocumentation
from .memory_manager import MemoryOptimizer

class EnhancedOrchestratorAgent:
    """Advanced orchestrator with sophisticated agent coordination"""
    def __init__(self):
        self.client = create_client()
        
        # Create organization block
        self.org_block = Block(
            name="organization",
            value=json.dumps({
                "name": "LettaOS Technical Organization",
                "purpose": "Advanced technical research and implementation",
                "core_capabilities": [
                    "Research and Development",
                    "Code Implementation",
                    "Documentation Management",
                    "Knowledge Optimization"
                ]
            })
        )
        
        # Initialize shared memory with organization context
        self.memory = ChatMemory(
            human="",
            persona=self._get_orchestrator_persona()
        )
        
        # Initialize agents with shared context
        self.research_agent = self._create_research_agent()
        self.coding_agent = self._create_coding_agent()
        
        # Initialize memory optimization
        self.memory_optimizer = MemoryOptimizer(self.client, self.org_block.id)
        self.documentation = EnhancedDocumentation(self.client, self.org_block.id)

    def _get_orchestrator_persona(self) -> str:
        return """You are an advanced orchestrator agent responsible for:
1. Coordinating between research and coding agents
2. Managing shared knowledge and memory optimization
3. Ensuring efficient information flow between agents
4. Maintaining system-wide best practices
5. Optimizing agent interactions and resource usage"""

    def _create_research_agent(self) -> ResearchAgent:
        """Create research agent with enhanced capabilities"""
        return ResearchAgent(
            self.client,
            self.org_block,
            enhanced_features={
                "memory_optimization": True,
                "documentation_storage": True,
                "rag_enabled": True
            }
        )

    def _create_coding_agent(self) -> CodingAgent:
        """Create coding agent with shared context"""
        return CodingAgent(
            self.client,
            self.org_block,
            model_config=self._get_deepseek_config()
        )

    def _get_deepseek_config(self) -> Dict[str, Any]:
        """Get optimized DeepSeek configuration"""
        return {
            "model_provider": "openai",
            "model_name": "deepseek-v2.5",
            "api_key": os.getenv("DEEPSEEK_API_KEY"),
            "api_base": "https://api.deepseek.com/v1",
            "model_kwargs": {
                "temperature": 0.7,
                "top_p": 0.95,
                "max_tokens": 4096,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1
            }
        }

    async def process_request(self, request: str) -> Dict[str, Any]:
        """Process user request with enhanced orchestration"""
        # Check documentation first
        existing_docs = await self.documentation.search_documentation(
            query=request,
            filters={"complexity": self._assess_request_complexity(request)}
        )

        if existing_docs:
            print("Found existing documentation")
            return self._prepare_documented_response(existing_docs[0])

        # If no documentation exists, proceed with research and implementation
        workflow = await self._create_workflow(request)
        response = await self._execute_workflow(workflow)
        
        # Store new documentation
        await self._store_workflow_results(workflow, response)
        
        # Optimize memory periodically
        if self.should_optimize():
            await self._optimize_system()
            
        return response

    def should_optimize(self) -> bool:
        """Determine if system optimization should run"""
        # Check last optimization time from org block
        context = json.loads(self.org_block.value)
        last_optimization = context.get("system_context", {}).get("last_optimization")
        
        if not last_optimization:
            return True
            
        # Optimize if more than 24 hours have passed
        last_opt_time = datetime.fromisoformat(last_optimization)
        return (datetime.now() - last_opt_time).days >= 1

    async def _optimize_system(self) -> None:
        """Perform system-wide optimization"""
        # Update context with optimization time
        context = json.loads(self.org_block.value)
        context["system_context"]["last_optimization"] = str(datetime.now())
        self.org_block.value = json.dumps(context)
        
        # Run memory optimization
        self.memory_optimizer.consolidate_memory()
        await self._cleanup_old_workflows()
        await self._update_metrics()

    def _assess_request_complexity(self, request: str) -> str:
        """Assess the complexity of the request"""
        request_lower = request.lower()
        complexity_indicators = {
            'high': ['complex', 'advanced', 'optimize', 'scale'],
            'medium': ['implement', 'create', 'develop'],
            'low': ['explain', 'describe', 'what is']
        }
        
        for level, indicators in complexity_indicators.items():
            if any(indicator in request_lower for indicator in indicators):
                return level
        return 'medium'

    def _prepare_documented_response(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare response from existing documentation"""
        return {
            "explanation": doc["content"].get("explanation", ""),
            "code": doc["content"].get("code", ""),
            "research_summary": doc["content"].get("research_summary", ""),
            "source": "documentation",
            "doc_id": doc.get("id")
        }

    async def _create_workflow(self, request: str) -> Dict[str, Any]:
        """Create execution workflow"""
        return {
            "id": str(uuid.uuid4()),
            "request": request,
            "timestamp": str(datetime.now()),
            "steps": [
                {
                    "type": "research",
                    "status": "pending",
                    "agent": "research_agent"
                },
                {
                    "type": "implementation",
                    "status": "pending",
                    "agent": "coding_agent"
                }
            ],
            "metadata": {
                "complexity": self._assess_request_complexity(request),
                "priority": "normal"
            }
        }

    async def _execute_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow steps"""
        results = {}
        
        # Execute research
        workflow["steps"][0]["status"] = "in_progress"
        research_results = await self.research_agent.research(workflow["request"])
        results["research"] = research_results
        workflow["steps"][0]["status"] = "completed"
        
        # Execute implementation
        if research_results:
            workflow["steps"][1]["status"] = "in_progress"
            implementation = await self.coding_agent.implement(
                research_results,
                workflow["request"]
            )
            results["implementation"] = implementation
            workflow["steps"][1]["status"] = "completed"
        
        return self._prepare_response(results, workflow)

    def _prepare_response(self, results: Dict[str, Any], workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare final response"""
        return {
            "explanation": results.get("implementation", {}).get("explanation", ""),
            "code": results.get("implementation", {}).get("code", ""),
            "research_summary": results.get("research", {}).get("summary", ""),
            "workflow_id": workflow["id"]
        }