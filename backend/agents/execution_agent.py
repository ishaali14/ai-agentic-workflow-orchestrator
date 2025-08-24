"""
Execution Agent Module
Delivers structured final output and actionable deliverables based on the execution plan.
"""

import logging
from typing import Dict, Any, List
from ..services.openai_api import get_openai_service

logger = logging.getLogger(__name__)

class ExecutionAgent:
    """
    Execution Agent responsible for delivering final structured output.
    
    This agent takes the research findings and execution plan to produce
    comprehensive, actionable deliverables that can be immediately used.
    """
    
    def __init__(self):
        """Initialize the Execution Agent."""
        self.openai_service = get_openai_service()
        
        # System prompt for the execution agent
        self.system_prompt = """
You are an Execution Agent in an AI Agentic Workflow Orchestrator. Your role is to:

1. SYNTHESIZE research findings and execution plans
2. DELIVER comprehensive, actionable final output
3. PROVIDE concrete deliverables and next steps
4. CREATE implementation-ready solutions
5. OFFER strategic recommendations and insights

Your output should be a JSON object with the following structure:
{
    "executive_summary": {
        "problem_statement": "Clear definition of the original problem",
        "solution_overview": "High-level solution approach",
        "key_insights": ["Most important findings from research"],
        "recommendations": ["Strategic recommendations"]
    },
    "deliverables": [
        {
            "type": "documentation/code/strategy/analysis",
            "title": "Descriptive title",
            "description": "What this deliverable contains",
            "content": "Detailed content or implementation",
            "format": "markdown/code/json/text",
            "priority": "high/medium/low"
        }
    ],
    "implementation_guide": {
        "prerequisites": ["What needs to be in place before starting"],
        "step_by_step_instructions": [
            {
                "step": 1,
                "action": "Clear action to take",
                "details": "Detailed explanation",
                "expected_outcome": "What should happen",
                "validation": "How to verify success"
            }
        ],
        "timeline": "Estimated implementation timeline",
        "resource_allocation": "How to allocate resources"
    },
    "code_templates": [
        {
            "language": "python/javascript/html/etc",
            "purpose": "What this code accomplishes",
            "filename": "suggested_filename.ext",
            "code": "Complete, runnable code",
            "dependencies": ["Required libraries/frameworks"],
            "usage_instructions": "How to use this code"
        }
    ],
    "quality_assurance": {
        "testing_strategy": "How to test the solution",
        "validation_criteria": ["Criteria for success"],
        "risk_mitigation": ["How to address potential issues"]
    },
    "next_steps": [
        {
            "action": "Immediate next action",
            "timeline": "When to do this",
            "owner": "Who should do this",
            "dependencies": ["What must be completed first"]
        }
    ]
}

Focus on providing:
- Actionable, implementable solutions
- Clear, detailed deliverables
- Practical code templates where applicable
- Comprehensive implementation guidance
- Quality assurance measures
- Clear next steps for continued progress
"""
    
    async def process(
        self, 
        task: str, 
        research_results: Dict[str, Any], 
        planning_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process research and planning results to deliver final structured output.
        
        Args:
            task: The original task from the user
            research_results: Output from the Research Agent
            planning_results: Output from the Planning Agent
            
        Returns:
            Dictionary containing comprehensive deliverables and implementation guide
        """
        try:
            logger.info(f"Execution Agent processing task: {task}")
            
            # Extract key information from previous agents
            research_summary = self._extract_research_summary(research_results)
            planning_summary = self._extract_planning_summary(planning_results)
            
            # Construct the prompt
            prompt = f"""
ORIGINAL TASK: {task}

RESEARCH FINDINGS:
{research_summary}

EXECUTION PLAN:
{planning_summary}

Based on the research findings and execution plan above, deliver comprehensive, actionable final output.

Requirements:
- Synthesize all findings into coherent, implementable solutions
- Provide concrete deliverables that can be immediately used
- Include code templates and implementation guides where applicable
- Offer strategic recommendations and next steps
- Ensure all outputs are practical and actionable

Focus on creating deliverables that:
1. Address the original task comprehensively
2. Build upon research insights and planning
3. Provide immediate value and actionable next steps
4. Include quality assurance and validation measures
5. Offer clear implementation guidance
"""
            
            # Generate structured response
            execution_results = await self.openai_service.generate_structured_response(
                prompt=prompt,
                system_prompt=self.system_prompt,
                temperature=0.5
            )
            
            # Add metadata
            execution_results["metadata"] = {
                "agent": "Execution Agent",
                "task": task,
                "research_summary": research_summary,
                "planning_summary": planning_summary,
                "timestamp": self._get_timestamp()
            }
            
            logger.info("Execution Agent completed successfully")
            return execution_results
            
        except Exception as e:
            logger.error(f"Execution Agent failed: {e}")
            raise Exception(f"Execution Agent processing failed: {str(e)}")
    
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
            
            if "task_analysis" in research_results:
                analysis = research_results["task_analysis"]
                summary_parts.append(f"Main Objective: {analysis.get('main_objective', 'N/A')}")
                summary_parts.append(f"Key Domains: {', '.join(analysis.get('key_domains', []))}")
            
            if "research_questions" in research_results:
                questions = research_results["research_questions"]
                summary_parts.append(f"\nKey Research Questions ({len(questions)} total):")
                for i, q in enumerate(questions[:3], 1):  # Show first 3
                    summary_parts.append(f"{i}. {q.get('question', 'N/A')}")
            
            if "research_areas" in research_results:
                areas = research_results["research_areas"]
                summary_parts.append(f"\nResearch Areas ({len(areas)} total):")
                for area in areas:
                    summary_parts.append(f"- {area.get('area', 'N/A')}")
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            logger.warning(f"Failed to extract research summary: {e}")
            return "Research results available but summary extraction failed"
    
    def _extract_planning_summary(self, planning_results: Dict[str, Any]) -> str:
        """
        Extract and format key information from planning results.
        
        Args:
            planning_results: Output from Planning Agent
            
        Returns:
            Formatted summary string
        """
        try:
            summary_parts = []
            
            if "execution_plan" in planning_results:
                plan = planning_results["execution_plan"]
                summary_parts.append(f"Plan Overview: {plan.get('overview', 'N/A')}")
                summary_parts.append(f"Estimated Effort: {plan.get('total_estimated_effort', 'N/A')}")
                summary_parts.append(f"Timeline: {plan.get('estimated_timeline', 'N/A')}")
            
            if "phases" in planning_results:
                phases = planning_results["phases"]
                summary_parts.append(f"\nExecution Phases ({len(phases)} total):")
                for phase in phases:
                    summary_parts.append(f"- Phase {phase.get('phase_number', 'N/A')}: {phase.get('phase_name', 'N/A')}")
            
            if "detailed_steps" in planning_results:
                steps = planning_results["detailed_steps"]
                summary_parts.append(f"\nDetailed Steps ({len(steps)} total):")
                for i, step in enumerate(steps[:5], 1):  # Show first 5
                    summary_parts.append(f"{i}. {step.get('title', 'N/A')}")
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            logger.warning(f"Failed to extract planning summary: {e}")
            return "Planning results available but summary extraction failed"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for metadata."""
        import datetime
        return datetime.datetime.now().isoformat()
    
    async def validate_agent(self) -> bool:
        """
        Validate that the Execution Agent can function properly.
        
        Returns:
            True if validation passes, False otherwise
        """
        try:
            # Create mock inputs for testing
            mock_research = {
                "task_analysis": {
                    "main_objective": "Create a simple web application",
                    "key_domains": ["Frontend", "Backend"]
                },
                "research_questions": [
                    {"question": "What framework to use?", "priority": "high"}
                ],
                "research_areas": [
                    {"area": "Technology Stack", "description": "Choose appropriate technologies"}
                ]
            }
            
            mock_planning = {
                "execution_plan": {
                    "overview": "Build a simple web app using modern frameworks",
                    "total_estimated_effort": "medium"
                },
                "phases": [
                    {"phase_number": 1, "phase_name": "Setup and Planning"}
                ],
                "detailed_steps": [
                    {"title": "Choose technology stack", "description": "Select appropriate frameworks"}
                ]
            }
            
            result = await self.process("Create a web app", mock_research, mock_planning)
            
            # Check if result has expected structure
            required_keys = ["executive_summary", "deliverables", "implementation_guide"]
            return all(key in result for key in required_keys)
            
        except Exception as e:
            logger.error(f"Execution Agent validation failed: {e}")
            return False
