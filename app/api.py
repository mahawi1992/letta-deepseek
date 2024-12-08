from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
import traceback

from .health_check import HealthMonitor
from components.orchestrator import EnhancedOrchestratorAgent

app = FastAPI(
    title="Letta DeepSeek API",
    description="Advanced multi-agent system with memory optimization",
    version="1.0.0"
)

# Initialize components
health_monitor = HealthMonitor()
orchestrator = EnhancedOrchestratorAgent()

class ProcessRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    status: str
    details: Dict[str, Any]

@app.post("/process", response_model=Dict[str, Any])
async def process_request(request: ProcessRequest):
    """Process a request through the agent system"""
    start_time = datetime.now()
    try:
        response = await orchestrator.process_request(request.query)
        
        # Record successful request
        processing_time = (datetime.now() - start_time).total_seconds()
        health_monitor.record_request(processing_time)
        
        return response
    except Exception as e:
        # Record failed request
        processing_time = (datetime.now() - start_time).total_seconds()
        health_monitor.record_request(
            processing_time, 
            error=True,
            error_details=str(e)
        )
        
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Get system health status"""
    health_status = await health_monitor.check_health()
    return {
        "status": health_status["status"],
        "details": health_status
    }

@app.post("/optimize")
async def optimize_memory():
    """Trigger memory optimization"""
    try:
        await orchestrator._optimize_system()
        health_monitor.record_memory_optimization()
        return {"status": "success", "message": "Memory optimization completed"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Memory optimization failed: {str(e)}"
        )

@app.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    return {
        "request_count": health_monitor.metrics["request_count"],
        "average_latency": sum(health_monitor.metrics["api_latency"][-100:]) / len(health_monitor.metrics["api_latency"][-100:]) if health_monitor.metrics["api_latency"] else 0,
        "error_rate": health_monitor._calculate_error_rate(),
        "memory_status": (await health_monitor.check_health())["memory"]
    }