"""
AI Agentic Workflow Orchestrator - FastAPI Backend
Main application entry point with API routes for workflow orchestration.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any, List
import asyncio
import logging
import os
import subprocess
import sys
from pathlib import Path

from .agents.research_agent import ResearchAgent
from .agents.planning_agent import PlanningAgent
from .agents.execution_agent import ExecutionAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Agentic Workflow Orchestrator",
    description="Multi-agent AI workflow orchestration powered by Gemini API",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class WorkflowRequest(BaseModel):
    task: str
    context: str = ""

class WorkflowResponse(BaseModel):
    status: str
    research_results: Dict[str, Any]
    planning_results: Dict[str, Any]
    execution_results: Dict[str, Any]
    total_duration: float

class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: str

# Initialize agents
research_agent = ResearchAgent()
planning_agent = PlanningAgent()
execution_agent = ExecutionAgent()

# Streamlit integration
STREAMLIT_PORT = 8501
streamlit_process = None

def start_streamlit():
    """Start Streamlit process in background."""
    global streamlit_process
    try:
        frontend_path = Path(__file__).parent.parent / "frontend"
        streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", 
            str(frontend_path / "app.py"),
            "--server.port", str(STREAMLIT_PORT),
            "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"Streamlit started on port {STREAMLIT_PORT}")
        return True
    except Exception as e:
        logger.error(f"Failed to start Streamlit: {e}")
        return False

def stop_streamlit():
    """Stop Streamlit process."""
    global streamlit_process
    if streamlit_process:
        streamlit_process.terminate()
        streamlit_process.wait()
        logger.info("Streamlit stopped")

@app.on_event("startup")
async def startup_event():
    """Start Streamlit on app startup."""
    start_streamlit()

@app.on_event("shutdown")
async def shutdown_event():
    """Stop Streamlit on app shutdown."""
    stop_streamlit()

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Root endpoint that redirects to the Streamlit frontend.
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Agentic Workflow Orchestrator</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 40px 20px;
            }
            h1 {
                font-size: 2.5rem;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .subtitle {
                font-size: 1.2rem;
                margin-bottom: 40px;
                opacity: 0.9;
            }
            .buttons {
                display: flex;
                gap: 20px;
                justify-content: center;
                flex-wrap: wrap;
            }
            .btn {
                display: inline-block;
                padding: 15px 30px;
                background: rgba(255,255,255,0.2);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                border: 2px solid rgba(255,255,255,0.3);
                transition: all 0.3s ease;
                font-size: 1.1rem;
                font-weight: bold;
            }
            .btn:hover {
                background: rgba(255,255,255,0.3);
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .btn-primary {
                background: rgba(255,255,255,0.3);
                border-color: rgba(255,255,255,0.5);
            }
            .status {
                margin-top: 40px;
                padding: 20px;
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                border: 1px solid rgba(255,255,255,0.2);
            }
            .status-item {
                margin: 10px 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .status-label {
                font-weight: bold;
            }
            .status-value {
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9rem;
            }
            .status-ok {
                background: rgba(76, 175, 80, 0.3);
                border: 1px solid rgba(76, 175, 80, 0.5);
            }
            .status-error {
                background: rgba(244, 67, 54, 0.3);
                border: 1px solid rgba(244, 67, 54, 0.5);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI Agentic Workflow Orchestrator</h1>
            <p class="subtitle">Multi-agent AI workflow orchestration powered by Gemini API</p>
            
            <div class="buttons">
                <a href="/app" class="btn btn-primary">🚀 Launch Application</a>
                <a href="http://localhost:8501" class="btn">📱 Direct Frontend</a>
                <a href="/docs" class="btn">📚 API Documentation</a>
                <a href="/health" class="btn">🔧 Health Check</a>
            </div>
            
            <div class="status">
                <h3>System Status</h3>
                <div class="status-item">
                    <span class="status-label">Backend API:</span>
                    <span class="status-value status-ok">Running</span>
                </div>
                <div class="status-item">
                    <span class="status-label">Frontend:</span>
                    <span class="status-value status-ok">Available</span>
                </div>
                <div class="status-item">
                    <span class="status-label">Gemini API:</span>
                    <span class="status-value status-ok">Connected</span>
                </div>
            </div>
        </div>
        
        <script>
            // Check if Streamlit is available
            fetch('/app')
                .then(response => {
                    if (!response.ok) {
                        document.querySelector('.status-item:nth-child(2) .status-value').className = 'status-value status-error';
                        document.querySelector('.status-item:nth-child(2) .status-value').textContent = 'Not Available';
                    }
                })
                .catch(() => {
                    document.querySelector('.status-item:nth-child(2) .status-value').className = 'status-value status-error';
                    document.querySelector('.status-item:nth-child(2) .status-value').textContent = 'Not Available';
                });
        </script>
    </body>
    </html>
    """

@app.get("/app")
async def streamlit_app():
    """
    Redirect to Streamlit frontend.
    """
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"http://localhost:{STREAMLIT_PORT}")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify API status.
    """
    import datetime
    
    # Check Streamlit status
    streamlit_status = "healthy"
    try:
        import requests
        response = requests.get(f"http://localhost:{STREAMLIT_PORT}", timeout=2)
        if response.status_code != 200:
            streamlit_status = "error"
    except:
        streamlit_status = "unavailable"
    
    return HealthResponse(
        status="healthy",
        message=f"AI Agentic Workflow Orchestrator is running. Frontend: {streamlit_status}",
        timestamp=datetime.datetime.now().isoformat()
    )

@app.post("/workflow", response_model=WorkflowResponse)
async def orchestrate_workflow(request: WorkflowRequest):
    """
    Main workflow orchestration endpoint that coordinates all three agents.
    
    Flow: Research → Planning → Execution
    """
    import time
    start_time = time.time()
    
    try:
        logger.info(f"Starting workflow for task: {request.task}")
        
        # Phase 1: Research Agent
        logger.info("Phase 1: Research Agent")
        research_results = await research_agent.process(request.task, request.context)
        
        # Phase 2: Planning Agent
        logger.info("Phase 2: Planning Agent")
        planning_results = await planning_agent.process(
            request.task, 
            research_results
        )
        
        # Phase 3: Execution Agent
        logger.info("Phase 3: Execution Agent")
        execution_results = await execution_agent.process(
            request.task,
            research_results,
            planning_results
        )
        
        total_duration = time.time() - start_time
        logger.info(f"Workflow completed in {total_duration:.2f} seconds")
        
        return WorkflowResponse(
            status="completed",
            research_results=research_results,
            planning_results=planning_results,
            execution_results=execution_results,
            total_duration=total_duration
        )
        
    except Exception as e:
        logger.error(f"Workflow failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
