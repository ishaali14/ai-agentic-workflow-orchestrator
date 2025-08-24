"""
OpenAI API Service Module
Handles all interactions with OpenAI's API for the AI agents.
"""

import os
import asyncio
import logging
from typing import Dict, Any, List, Optional
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

class OpenAIAPIService:
    """
    Service class for handling OpenAI API interactions.
    Provides async methods for generating responses with proper error handling.
    """
    
    def __init__(self):
        """Initialize the OpenAI API service with configuration."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Configure OpenAI API
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # Default model
        self.model = "gpt-4o-mini"  # You can change this to gpt-4o, gpt-4-turbo, etc.
        
        logger.info("OpenAI API service initialized successfully")
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """
        Generate a response from OpenAI API asynchronously.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt for context
            temperature: Controls randomness (0.0 to 2.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated response text
            
        Raises:
            Exception: If API call fails
        """
        try:
            # Prepare messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            # Run the API call in a thread pool to make it async
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            )
            
            if response.choices and response.choices[0].message.content:
                content = response.choices[0].message.content
                logger.info(f"Generated response successfully ({len(content)} characters)")
                return content
            else:
                raise Exception("Empty response from OpenAI API")
                
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise Exception(f"Failed to generate response: {str(e)}")
    
    async def generate_structured_response(
        self, 
        prompt: str, 
        system_prompt: str = "",
        expected_format: str = "JSON",
        temperature: float = 0.3
    ) -> Dict[str, Any]:
        """
        Generate a structured response (JSON) from OpenAI API.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt for context
            expected_format: Expected response format (default: JSON)
            temperature: Controls randomness (0.0 to 2.0)
            
        Returns:
            Parsed structured response
        """
        try:
            # Add format instructions to the prompt
            format_prompt = f"{prompt}\n\nPlease respond in {expected_format} format."
            
            response_text = await self.generate_response(
                format_prompt, 
                system_prompt, 
                temperature
            )
            
            # Try to parse as JSON if that's the expected format
            if expected_format.upper() == "JSON":
                import json
                try:
                    # Clean the response to extract JSON
                    response_text = response_text.strip()
                    if response_text.startswith("```json"):
                        response_text = response_text[7:]
                    if response_text.endswith("```"):
                        response_text = response_text[:-3]
                    
                    return json.loads(response_text)
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse JSON response: {e}")
                    # Return as text if JSON parsing fails
                    return {"response": response_text}
            
            return {"response": response_text}
            
        except Exception as e:
            logger.error(f"Structured response generation failed: {e}")
            raise
    
    async def validate_api_connection(self) -> bool:
        """
        Validate that the OpenAI API is accessible and working.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            test_response = await self.generate_response(
                "Hello, please respond with 'API is working' if you can see this message.",
                temperature=0.1
            )
            return "API is working" in test_response or len(test_response) > 0
        except Exception as e:
            logger.error(f"API validation failed: {e}")
            return False

# Global instance for reuse across agents
openai_service = None

def get_openai_service() -> OpenAIAPIService:
    """
    Get or create a global OpenAI API service instance.
    
    Returns:
        OpenAIAPIService instance
    """
    global openai_service
    if openai_service is None:
        openai_service = OpenAIAPIService()
    return openai_service
