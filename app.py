"""
AI Agentic Workflow Orchestrator - Streamlit Application
Complete application with multi-agent AI workflow orchestration powered by Gemini API.
"""

import streamlit as st
import asyncio
import json
import time
import os
from datetime import datetime
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Agentic Workflow Orchestrator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .status-research {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .status-planning {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .status-execution {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
    }
    .status-complete {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    .code-block {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'workflow_history' not in st.session_state:
    st.session_state.workflow_history = []
if 'current_workflow' not in st.session_state:
    st.session_state.current_workflow = None
if 'gemini_service' not in st.session_state:
    st.session_state.gemini_service = None

# Import AI agents
from backend.agents.research_agent import ResearchAgent
from backend.agents.planning_agent import PlanningAgent
from backend.agents.execution_agent import ExecutionAgent

# Initialize agents
@st.cache_resource
def get_agents():
    """Get or create AI agents."""
    try:
        research_agent = ResearchAgent()
        planning_agent = PlanningAgent()
        execution_agent = ExecutionAgent()
        return research_agent, planning_agent, execution_agent
    except Exception as e:
        st.error(f"Failed to initialize agents: {e}")
        return None, None, None

def check_openai_api():
    """Check if OpenAI API is properly configured."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        return False, "OPENAI_API_KEY not configured"
    return True, "API key configured"

async def run_workflow(task: str, context: str = "") -> Dict[str, Any]:
    """
    Run the complete AI workflow: Research → Planning → Execution
    """
    start_time = time.time()
    
    try:
        # Get agents
        research_agent, planning_agent, execution_agent = get_agents()
        if not all([research_agent, planning_agent, execution_agent]):
            raise Exception("Failed to initialize agents")
        
        # Phase 1: Research Agent
        with st.spinner("🔍 Research Agent: Analyzing task and generating research questions..."):
            research_results = await research_agent.process(task, context)
        
        # Phase 2: Planning Agent
        with st.spinner("📋 Planning Agent: Creating detailed execution plan..."):
            planning_results = await planning_agent.process(task, research_results)
        
        # Phase 3: Execution Agent
        with st.spinner("⚡ Execution Agent: Generating final deliverables..."):
            execution_results = await execution_agent.process(task, research_results, planning_results)
        
        total_duration = time.time() - start_time
        
        return {
            "status": "completed",
            "research_results": research_results,
            "planning_results": planning_results,
            "execution_results": execution_results,
            "total_duration": total_duration
        }
        
    except Exception as e:
        st.error(f"Workflow failed: {str(e)}")
        return None

def display_workflow_progress(workflow_data: Dict[str, Any]):
    """Display workflow progress and results."""
    
    # Progress indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="status-box status-research">
            <h4>🔍 Research Phase</h4>
            <p>✓ Completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="status-box status-planning">
            <h4>📋 Planning Phase</h4>
            <p>✓ Completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="status-box status-execution">
            <h4>⚡ Execution Phase</h4>
            <p>✓ Completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="status-box status-complete">
            <h4>🎯 Complete</h4>
            <p>✓ Workflow Finished</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        duration = workflow_data.get('total_duration', 0)
        st.metric("Total Duration", f"{duration:.2f}s")
    
    with col2:
        research_questions = len(workflow_data.get('research_results', {}).get('research_questions', []))
        st.metric("Research Questions", research_questions)
    
    with col3:
        execution_steps = len(workflow_data.get('planning_results', {}).get('detailed_steps', []))
        st.metric("Execution Steps", execution_steps)

def display_research_results(research_data: Dict[str, Any]):
    """Display research phase results."""
    st.subheader("🔍 Research Results")
    
    if 'task_analysis' in research_data:
        analysis = research_data['task_analysis']
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Main Objective:**")
            st.info(analysis.get('main_objective', 'N/A'))
        
        with col2:
            st.write("**Complexity Level:**")
            complexity = analysis.get('complexity_level', 'N/A')
            if complexity == 'high':
                st.error(f"🔴 {complexity.title()}")
            elif complexity == 'medium':
                st.warning(f"🟡 {complexity.title()}")
            else:
                st.success(f"🟢 {complexity.title()}")
    
    if 'research_questions' in research_data:
        st.write("**Research Questions:**")
        questions = research_data['research_questions']
        for i, q in enumerate(questions, 1):
            priority_color = {
                'high': '🔴',
                'medium': '🟡', 
                'low': '🟢'
            }.get(q.get('priority', 'medium'), '⚪')
            
            st.write(f"{i}. {priority_color} **{q.get('question', 'N/A')}**")
            st.write(f"   Category: {q.get('category', 'N/A')} | Priority: {q.get('priority', 'N/A')}")
            st.write(f"   Rationale: {q.get('rationale', 'N/A')}")
            st.divider()

def display_planning_results(planning_data: Dict[str, Any]):
    """Display planning phase results."""
    st.subheader("📋 Planning Results")
    
    if 'execution_plan' in planning_data:
        plan = planning_data['execution_plan']
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Plan Overview:**")
            st.info(plan.get('overview', 'N/A'))
        
        with col2:
            st.write("**Estimated Effort:**")
            effort = plan.get('total_estimated_effort', 'N/A')
            if effort == 'high':
                st.error(f"🔴 {effort.title()}")
            elif effort == 'medium':
                st.warning(f"🟡 {effort.title()}")
            else:
                st.success(f"🟢 {effort.title()}")
    
    if 'phases' in planning_data:
        st.write("**Execution Phases:**")
        phases = planning_data['phases']
        for phase in phases:
            st.write(f"**Phase {phase.get('phase_number', 'N/A')}: {phase.get('phase_name', 'N/A')}**")
            st.write(f"Description: {phase.get('description', 'N/A')}")
            st.write(f"Duration: {phase.get('estimated_duration', 'N/A')}")
            st.divider()
    
    if 'detailed_steps' in planning_data:
        with st.expander("📝 Detailed Steps", expanded=False):
            steps = planning_data['detailed_steps']
            for step in steps:
                st.write(f"**Step {step.get('step_number', 'N/A')}: {step.get('title', 'N/A')}**")
                st.write(f"Phase: {step.get('phase', 'N/A')}")
                st.write(f"Description: {step.get('description', 'N/A')}")
                st.write(f"Effort: {step.get('effort_estimate', 'N/A')}")
                st.divider()

def display_execution_results(execution_data: Dict[str, Any]):
    """Display execution phase results."""
    st.subheader("⚡ Execution Results")
    
    if 'executive_summary' in execution_data:
        summary = execution_data['executive_summary']
        
        st.write("**Problem Statement:**")
        st.info(summary.get('problem_statement', 'N/A'))
        
        st.write("**Solution Overview:**")
        st.success(summary.get('solution_overview', 'N/A'))
        
        if 'key_insights' in summary:
            st.write("**Key Insights:**")
            for insight in summary['key_insights']:
                st.write(f"• {insight}")
    
    if 'deliverables' in execution_data:
        st.write("**Deliverables:**")
        deliverables = execution_data['deliverables']
        for deliverable in deliverables:
            priority_color = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(deliverable.get('priority', 'medium'), '⚪')
            
            st.write(f"{priority_color} **{deliverable.get('title', 'N/A')}**")
            st.write(f"Type: {deliverable.get('type', 'N/A')}")
            st.write(f"Description: {deliverable.get('description', 'N/A')}")
            
            if deliverable.get('format') == 'code':
                st.code(deliverable.get('content', ''), language='python')
            else:
                st.text_area(f"Content ({deliverable.get('format', 'text')})", 
                           deliverable.get('content', ''), height=200, disabled=True)
            st.divider()
    
    if 'code_templates' in execution_data:
        with st.expander("💻 Code Templates", expanded=False):
            templates = execution_data['code_templates']
            for template in templates:
                st.write(f"**{template.get('purpose', 'N/A')}**")
                st.write(f"Language: {template.get('language', 'N/A')}")
                st.write(f"Filename: {template.get('filename', 'N/A')}")
                st.code(template.get('code', ''), language=template.get('language', 'text'))
                st.divider()
    
    if 'next_steps' in execution_data:
        st.write("**Next Steps:**")
        next_steps = execution_data['next_steps']
        for i, step in enumerate(next_steps, 1):
            st.write(f"{i}. **{step.get('action', 'N/A')}**")
            st.write(f"   Timeline: {step.get('timeline', 'N/A')}")
            st.write(f"   Owner: {step.get('owner', 'N/A')}")

def show_workflow_page():
    """Display the main workflow page."""
    
    # Check API configuration
    api_ok, api_message = check_openai_api()
    if not api_ok:
        st.error(f"⚠️ {api_message}")
        st.info("Please configure your OPENAI_API_KEY in the .env file")
        return
    
    # Workflow input
    st.header("🚀 Start New Workflow")
    
    task = st.text_area(
        "Enter your task or problem statement:",
        placeholder="Describe what you want to accomplish...",
        height=100
    )
    
    context = st.text_area(
        "Additional context (optional):",
        placeholder="Provide any additional context, constraints, or requirements...",
        height=80
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🚀 Execute Workflow", type="primary", use_container_width=True):
            if not task.strip():
                st.error("Please enter a task to execute.")
                return
            
            # Execute workflow
            workflow_result = asyncio.run(run_workflow(task, context))
            
            if workflow_result:
                # Store in history
                workflow_entry = {
                    "id": len(st.session_state.workflow_history) + 1,
                    "task": task,
                    "context": context,
                    "timestamp": datetime.now().isoformat(),
                    "result": workflow_result
                }
                st.session_state.workflow_history.append(workflow_entry)
                st.session_state.current_workflow = workflow_entry
                
                st.success("✅ Workflow completed successfully!")
                st.rerun()
    
    # Display current workflow results
    if st.session_state.current_workflow:
        st.header("📊 Current Workflow Results")
        
        workflow_data = st.session_state.current_workflow['result']
        
        # Display progress
        display_workflow_progress(workflow_data)
        
        # Display results by phase
        if 'research_results' in workflow_data:
            display_research_results(workflow_data['research_results'])
        
        if 'planning_results' in workflow_data:
            display_planning_results(workflow_data['planning_results'])
        
        if 'execution_results' in workflow_data:
            display_execution_results(workflow_data['execution_results'])

def show_history_page():
    """Display the workflow history page."""
    
    st.header("📚 Workflow History")
    
    if not st.session_state.workflow_history:
        st.info("No workflows in history yet. Execute a workflow to see results here.")
        return
    
    # Display history
    for i, workflow in enumerate(reversed(st.session_state.workflow_history)):
        with st.expander(f"Workflow #{workflow['id']} - {workflow['task'][:50]}...", expanded=False):
            st.write(f"**Task:** {workflow['task']}")
            if workflow['context']:
                st.write(f"**Context:** {workflow['context']}")
            st.write(f"**Timestamp:** {workflow['timestamp']}")
            
            # Quick metrics
            result = workflow['result']
            col1, col2, col3 = st.columns(3)
            
            with col1:
                duration = result.get('total_duration', 0)
                st.metric("Duration", f"{duration:.2f}s")
            
            with col2:
                research_questions = len(result.get('research_results', {}).get('research_questions', []))
                st.metric("Research Qs", research_questions)
            
            with col3:
                execution_steps = len(result.get('planning_results', {}).get('detailed_steps', []))
                st.metric("Steps", execution_steps)
            
            # View full results button
            if st.button(f"View Full Results", key=f"view_{i}"):
                st.session_state.current_workflow = workflow
                st.rerun()

def show_about_page():
    """Display the about page."""
    
    st.header("🤖 About AI Agentic Workflow Orchestrator")
    
    st.markdown("""
    ## Overview
    
    The AI Agentic Workflow Orchestrator is a sophisticated multi-agent AI system that processes complex tasks through three specialized AI agents:
    
    1. **🔍 Research Agent** - Expands user input into comprehensive research questions and areas
    2. **📋 Planning Agent** - Generates detailed, actionable execution plans
    3. **⚡ Execution Agent** - Delivers structured final output with actionable deliverables
    
    ## Features
    
    - **Multi-Agent Architecture**: Three specialized AI agents working in sequence
    - **OpenAI API Integration**: Powered by OpenAI's latest AI technology
    - **Stateless Design**: No database required, session-based storage
    - **Professional UI**: Beautiful Streamlit interface with real-time progress tracking
    - **Comprehensive Output**: Research analysis, planning, and actionable deliverables
    
    ## How It Works
    
    1. **Research Phase**: Analyzes the task and generates comprehensive research questions
    2. **Planning Phase**: Creates detailed, step-by-step execution plans
    3. **Execution Phase**: Delivers structured final output with code templates and next steps
    
    ## Technology Stack
    
    - **Frontend**: Streamlit
    - **AI**: OpenAI API
    - **Language**: Python 3.8+
    - **Architecture**: Multi-agent orchestration
    
    ## Getting Started
    
    1. Configure your `OPENAI_API_KEY` in the `.env` file
    2. Enter a task or problem statement
    3. Watch the AI agents work through the three phases
    4. Review the comprehensive results and deliverables
    """)

# Main application
def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Agentic Workflow Orchestrator</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Multi-agent AI workflow orchestration powered by OpenAI API</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Status Check
        api_ok, api_message = check_openai_api()
        status_color = "🟢" if api_ok else "🔴"
        st.write(f"{status_color} API Status: {api_message}")
        
        # Navigation
        st.header("📱 Navigation")
        page = st.selectbox(
            "Choose a page:",
            ["Workflow", "History", "About"],
            index=0
        )
        
        # Session Info
        st.header("📊 Session Info")
        st.write(f"Workflows in History: {len(st.session_state.workflow_history)}")
        
        if st.button("🗑️ Clear History"):
            st.session_state.workflow_history = []
            st.session_state.current_workflow = None
            st.rerun()
    
    # Page routing
    if page == "Workflow":
        show_workflow_page()
    elif page == "History":
        show_history_page()
    elif page == "About":
        show_about_page()

if __name__ == "__main__":
    main()
