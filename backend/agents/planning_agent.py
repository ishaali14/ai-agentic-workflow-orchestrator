"""
Planning Agent Module
Generates step-by-step execution plans based on research findings.
"""

import logging
from typing import Dict, Any, List
from ..services.openai_api import get_openai_service

logger = logging.getLogger(__name__)

class PlanningAgent:
    """
    Planning Agent responsible for creating detailed execution plans.
    
    This agent takes the research results and converts them into actionable,
    step-by-step plans that can be executed by the Execution Agent.
    """
    
    def __init__(self):
        """Initialize the Planning Agent."""
        self.openai_service = get_openai_service()
        
        # System prompt for the planning agent
        self.system_prompt = """
You are a Planning Agent in an AI Agentic Workflow Orchestrator. Your role is to:

1. ANALYZE research findings and requirements
2. CREATE detailed, actionable execution plans
3. BREAK DOWN complex tasks into sequential steps
4. IDENTIFY dependencies and resource requirements
5. ESTIMATE effort and timeline for each step

Your output should be a JSON object with the following structure:
{
    "execution_plan": {
        "overview": "High-level summary of the plan",
        "total_estimated_effort": "low/medium/high",
        "estimated_timeline": "Brief timeline estimate",
        "key_milestones": ["List of major milestones"]
    },
    "phases": [
        {
            "phase_number": 1,
            "phase_name": "Descriptive name",
            "description": "What this phase accomplishes",
            "objectives": ["List of specific objectives"],
            "estimated_duration": "Time estimate",
            "dependencies": ["What must be completed before this phase"]
        }
    ],
    "detailed_steps": [
        {
            "step_number": 1,
            "phase": "Which phase this step belongs to",
            "title": "Clear, actionable step title",
            "description": "Detailed description of what to do",
            "inputs_required": ["What information/materials are needed"],
            "outputs_expected": ["What should be produced"],
            "effort_estimate": "low/medium/high",
            "dependencies": ["Steps that must be completed first"],
            "success_criteria": ["How to know this step is complete"]
        }
    ],
    "risk_assessment": [
        {
            "risk": "Description of potential risk",
            "probability": "low/medium/high",
            "impact": "low/medium/high",
            "mitigation": "How to address this risk"
        }
    ],
    "resource_requirements": {
        "tools": ["List of tools/technologies needed"],
        "skills": ["Required skills or expertise"],
        "materials": ["Any materials or data needed"]
    }
}

Create 3-5 phases with 5-15 detailed steps total. Be specific and actionable.
Focus on practical, implementable steps that lead to concrete deliverables.
"""
    
    async def process(self, task: str, research_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process research results and generate detailed execution plan.
        
        Args:
            task: The original task from the user
            research_results: Output from the Research Agent
            
        Returns:
            Dictionary containing the detailed execution plan
        """
        try:
            logger.info(f"Planning Agent processing task: {task}")
            
            # Extract key information from research results
            research_summary = self._extract_research_summary(research_results)
            
            # Construct the prompt
            prompt = f"""
ORIGINAL TASK: {task}

RESEARCH FINDINGS:
{research_summary}

Based on the research findings above, create a detailed, actionable execution plan.

Requirements:
- Convert research insights into concrete, implementable steps
- Consider dependencies and logical sequence
- Include risk assessment and mitigation strategies
- Provide clear success criteria for each step
- Ensure the plan is comprehensive yet practical

Focus on creating a plan that:
1. Addresses all identified research areas
2. Follows logical progression from research to implementation
3. Includes quality checks and validation steps
4. Provides clear deliverables for each phase
"""
            
            # Generate structured response
            planning_results = await self.openai_service.generate_structured_response(
                prompt=prompt,
                system_prompt=self.system_prompt,
                temperature=0.4
            )
            
            # Add metadata
            planning_results["metadata"] = {
                "agent": "Planning Agent",
                "task": task,
                "research_summary": research_summary,
                "timestamp": self._get_timestamp()
            }
            
            logger.info("Planning Agent completed successfully")
            return planning_results
            
        except Exception as e:
            logger.error(f"Planning Agent failed: {e}")
            raise Exception(f"Planning Agent processing failed: {str(e)}")
    
    def _extract_research_summary(self, research_results: Dict[str, Any]) -> str:
        """
        Extract and format key information from research results.
        
        Args:
            research_results: Output from Research Agent
            
        Returns:
            Formatted summary string
        """
        try:
            summary_parts = []
            
            # Extract task analysis
            if "task_analysis" in research_results:
                analysis = research_results["task_analysis"]
                summary_parts.append(f"Main Objective: {analysis.get('main_objective', 'N/A')}")
                summary_parts.append(f"Key Domains: {', '.join(analysis.get('key_domains', []))}")
                summary_parts.append(f"Complexity: {analysis.get('complexity_level', 'N/A')}")
            
            # Extract research questions
            if "research_questions" in research_results:
                questions = research_results["research_questions"]
                summary_parts.append(f"\nResearch Questions ({len(questions)} total):")
                for i, q in enumerate(questions[:5], 1):  # Show first 5
                    summary_parts.append(f"{i}. {q.get('question', 'N/A')} ({q.get('priority', 'N/A')} priority)")
            
            # Extract research areas
            if "research_areas" in research_results:
                areas = research_results["research_areas"]
                summary_parts.append(f"\nResearch Areas ({len(areas)} total):")
                for area in areas:
                    summary_parts.append(f"- {area.get('area', 'N/A')}: {area.get('description', 'N/A')}")
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            logger.warning(f"Failed to extract research summary: {e}")
            return "Research results available but summary extraction failed"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for metadata."""
        import datetime
        return datetime.datetime.now().isoformat()
    
    async def validate_agent(self) -> bool:
        """
        Validate that the Planning Agent can function properly.
        
        Returns:
            True if validation passes, False otherwise
        """
        try:
            # Create mock research results for testing
            mock_research = {
                "task_analysis": {
                    "main_objective": "Create a simple web application",
                    "key_domains": ["Frontend", "Backend", "Database"],
                    "complexity_level": "medium"
                },
                "research_questions": [
                    {"question": "What framework to use?", "priority": "high"},
                    {"question": "How to structure the database?", "priority": "medium"}
                ],
                "research_areas": [
                    {"area": "Technology Stack", "description": "Choose appropriate technologies"}
                ]
            }
            
            result = await self.process("Create a web app", mock_research)
            
            # Check if result has expected structure
            required_keys = ["execution_plan", "phases", "detailed_steps"]
            return all(key in result for key in required_keys)
            
        except Exception as e:
            logger.error(f"Planning Agent validation failed: {e}")
            return False
