"""
Research Agent Module
Expands user input into comprehensive sub-questions and research areas.
"""

import logging
from typing import Dict, Any, List
from ..services.openai_api import get_openai_service

logger = logging.getLogger(__name__)

class ResearchAgent:
    """
    Research Agent responsible for expanding user tasks into research questions.
    
    This agent analyzes the user's input and generates comprehensive sub-questions
    that need to be addressed to fully understand and solve the given task.
    """
    
    def __init__(self):
        """Initialize the Research Agent."""
        self.openai_service = get_openai_service()
        
        # System prompt for the research agent
        self.system_prompt = """
You are a Research Agent in an AI Agentic Workflow Orchestrator. Your role is to:

1. ANALYZE the user's task or problem statement
2. EXPAND it into comprehensive sub-questions and research areas
3. IDENTIFY key aspects that need investigation
4. STRUCTURE the research approach systematically

Your output should be a JSON object with the following structure:
{
    "task_analysis": {
        "main_objective": "Clear statement of the primary goal",
        "key_domains": ["List of main areas to research"],
        "complexity_level": "low/medium/high",
        "estimated_scope": "Brief description of scope"
    },
    "research_questions": [
        {
            "question": "Specific research question",
            "category": "Domain/area this belongs to",
            "priority": "high/medium/low",
            "rationale": "Why this question is important"
        }
    ],
    "research_areas": [
        {
            "area": "Research area name",
            "description": "What this area covers",
            "key_topics": ["List of specific topics to explore"],
            "dependencies": ["Other areas this depends on"]
        }
    ],
    "success_criteria": [
        "List of criteria that define successful research completion"
    ]
}

Be thorough but focused. Generate 5-10 research questions and 3-5 research areas.
Focus on actionable, specific questions that will lead to concrete insights.
"""
    
    async def process(self, task: str, context: str = "") -> Dict[str, Any]:
        """
        Process the user task and generate comprehensive research plan.
        
        Args:
            task: The main task or problem statement from the user
            context: Additional context or background information
            
        Returns:
            Dictionary containing the research analysis and questions
        """
        try:
            logger.info(f"Research Agent processing task: {task}")
            
            # Construct the prompt
            prompt = f"""
TASK: {task}

{f"CONTEXT: {context}" if context else ""}

Please analyze this task and generate a comprehensive research plan following the structure specified in the system prompt.

Focus on:
- Breaking down complex tasks into manageable research questions
- Identifying all relevant domains and areas of investigation
- Prioritizing questions based on importance and dependencies
- Ensuring comprehensive coverage of the problem space
"""
            
            # Generate structured response
            research_results = await self.openai_service.generate_structured_response(
                prompt=prompt,
                system_prompt=self.system_prompt,
                temperature=0.3
            )
            
            # Add metadata
            research_results["metadata"] = {
                "agent": "Research Agent",
                "task": task,
                "context": context,
                "timestamp": self._get_timestamp()
            }
            
            logger.info("Research Agent completed successfully")
            return research_results
            
        except Exception as e:
            logger.error(f"Research Agent failed: {e}")
            raise Exception(f"Research Agent processing failed: {str(e)}")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for metadata."""
        import datetime
        return datetime.datetime.now().isoformat()
    
    async def validate_agent(self) -> bool:
        """
        Validate that the Research Agent can function properly.
        
        Returns:
            True if validation passes, False otherwise
        """
        try:
            test_task = "Create a simple to-do list application"
            result = await self.process(test_task)
            
            # Check if result has expected structure
            required_keys = ["task_analysis", "research_questions", "research_areas"]
            return all(key in result for key in required_keys)
            
        except Exception as e:
            logger.error(f"Research Agent validation failed: {e}")
            return False
