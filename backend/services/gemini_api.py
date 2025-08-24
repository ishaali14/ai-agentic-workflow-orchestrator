"""
Gemini API Service Module
Handles all interactions with Google's Gemini API for the AI agents.
"""

import os
import asyncio
import logging
from typing import Dict, Any, List, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

class GeminiAPIService:
    """
    Service class for handling Gemini API interactions.
    Provides async methods for generating responses with proper error handling.
    """
    
    def __init__(self):
        """Initialize the Gemini API service with configuration."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        try:
            # Try the newer model name first
            try:
                self.model = genai.GenerativeModel('gemini-1.5-pro')
                logger.info("Gemini API service initialized with gemini-1.5-pro")
            except:
                # Fallback to the older model name
                self.model = genai.GenerativeModel('gemini-pro')
                logger.info("Gemini API service initialized with gemini-pro")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini API: {e}")
            raise
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """
        Generate a response from Gemini API asynchronously.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt for context
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated response text
            
        Raises:
            Exception: If API call fails
        """
        try:
            # Combine system prompt and user prompt
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            
            # Run the API call in a thread pool to make it async
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(
                    full_prompt,
                    generation_config=generation_config
                )
            )
            
            if response.text:
                logger.info(f"Generated response successfully ({len(response.text)} characters)")
                return response.text
            else:
                raise Exception("Empty response from Gemini API")
                
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            raise Exception(f"Failed to generate response: {str(e)}")
    
    async def generate_structured_response(
        self, 
        prompt: str, 
        system_prompt: str = "",
        expected_format: str = "JSON",
        temperature: float = 0.3
    ) -> Dict[str, Any]:
        """
        Generate a structured response (JSON) from Gemini API.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt for context
            expected_format: Expected response format (default: JSON)
            temperature: Controls randomness (0.0 to 1.0)
            
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
        Validate that the Gemini API is accessible and working.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # First, try to list available models
            try:
                models = genai.list_models()
                logger.info(f"Available models: {[model.name for model in models]}")
            except Exception as e:
                logger.warning(f"Could not list models: {e}")
            
            test_response = await self.generate_response(
                "Hello, please respond with 'API is working' if you can see this message.",
                temperature=0.1
            )
            return "API is working" in test_response or len(test_response) > 0
        except Exception as e:
            logger.error(f"API validation failed: {e}")
            return False

# Global instance for reuse across agents
gemini_service = None

def get_gemini_service() -> GeminiAPIService:
    """
    Get or create a global Gemini API service instance.
    
    Returns:
        GeminiAPIService instance
    """
    global gemini_service
    if gemini_service is None:
        gemini_service = GeminiAPIService()
    return gemini_service
