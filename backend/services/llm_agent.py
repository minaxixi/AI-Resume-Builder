"""
Base class for LLM-based agents.
"""

import os
import openai
import logging
import sys
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

# Configure module logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class LLMAgent(ABC):
    def __init__(self):
        """Initialize the LLM agent with OpenAI API key."""
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            logger.error("OpenAI API key not found")
            raise ValueError("OpenAI API key not found in environment variables")
        logger.debug(f"{self.__class__.__name__} initialized with API key")

    @abstractmethod
    def get_user_prompt(self, *args, **kwargs) -> str:
        """
        Load and format the prompt template with given parameters.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            str: The formatted prompt
        """
        pass

    def run(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Run the LLM agent with the given inputs.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            Dict[str, Any]: The result of the LLM operation
        """
        try:
            # Get the prompts
            user_prompt = self.get_user_prompt(*args, **kwargs)
            system_prompt = self.get_system_prompt()
            logger.debug("Created prompt")
            
            # Call OpenAI API
            try:
                logger.debug("Calling OpenAI API")
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.5,
                    max_tokens=4000,
                    top_p=0.9,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                logger.debug("Received response from OpenAI API")
            except Exception as e:
                logger.error(f"OpenAI API Error: {str(e)}")
                raise ValueError(f"Failed to generate response from OpenAI API: {str(e)}")
            
            # Process the response
            result = self.process_response(response, *args, **kwargs)
            logger.debug("Successfully processed response")
            return result
            
        except openai.error.AuthenticationError as e:
            logger.error(f"OpenAI Authentication Error: {str(e)}")
            raise ValueError("Invalid OpenAI API key. Please check your configuration.")
        except openai.error.RateLimitError as e:
            logger.error(f"OpenAI Rate Limit Error: {str(e)}")
            raise ValueError("OpenAI API rate limit exceeded. Please try again later.")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise ValueError(f"Error in LLM operation: {str(e)}")

    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Get the system prompt for the agent.
        
        Returns:
            str: The system prompt
        """
        pass

    @abstractmethod
    def process_response(self, response: Any, *args, **kwargs) -> Dict[str, Any]:
        """
        Process the LLM response into the desired format.
        
        Args:
            response: The raw response from the LLM
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            Dict[str, Any]: The processed result
        """
        pass
