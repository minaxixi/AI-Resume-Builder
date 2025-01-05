import os
import openai
import logging
import sys
from typing import Dict, Any
from . import prompts
from .llm_agent import LLMAgent

# Configure module logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Create console handler
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# Add handler to logger
logger.addHandler(handler)

class ResumeTailor(LLMAgent):
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            logger.error("OpenAI API key not found")
            raise ValueError("OpenAI API key not found in environment variables")
        logger.debug("ResumeTailor initialized with API key")

    def get_user_prompt(self, resume_text: str, job_description: str) -> str:
        """
        Load and format the resume tailoring prompt.
        
        Args:
            resume_text (str): The original resume text
            job_description (str): The target job description
            
        Returns:
            str: The formatted prompt
        """
        logger.debug("Creating tailoring prompt")
        return prompts.get_resume_tailor_user_prompt(resume_text, job_description)

    def get_system_prompt(self) -> str:
        """
        Get the system prompt for resume tailoring.
        
        Returns:
            str: The system prompt
        """
        return prompts.get_resume_tailor_system_prompt()

    def process_response(self, response: Any, resume_text: str, *args, **kwargs) -> Dict[str, Any]:
        """
        Process the LLM response into the desired format.
        
        Args:
            response: The raw response from the LLM
            resume_text (str): The original resume text
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            Dict[str, Any]: The processed result containing original and enhanced text
        """
        enhanced_text = response.choices[0].message['content'].strip()
        logger.debug("Extracted enhanced text from response")
        
        if not enhanced_text:
            logger.error("Empty response from OpenAI API")
            raise ValueError("Empty response from OpenAI API")

        return {
            "original_text": resume_text,
            "enhanced_text": enhanced_text
        }

    def tailor_resume(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Tailor a resume to match a job description.
        
        Args:
            resume_text (str): The original resume text
            job_description (str): The target job description
            
        Returns:
            Dict[str, Any]: Dictionary containing the original and enhanced resume text
        """
        logger.debug("Starting resume tailoring process")
        
        if not resume_text.strip():
            logger.error("Empty resume text provided")
            raise ValueError("Empty resume text provided")

        if not job_description.strip():
            logger.error("Empty job description provided")
            raise ValueError("Empty job description provided")

        return self.run(resume_text, job_description)
