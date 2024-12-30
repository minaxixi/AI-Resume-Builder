import os
import openai
import logging
import sys
from typing import Dict, Any

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

class ResumeTailor:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            logger.error("OpenAI API key not found")
            raise ValueError("OpenAI API key not found in environment variables")
        logger.debug("ResumeTailor initialized with API key")
        
    def _create_tailoring_prompt(self, resume_text: str, job_description: str) -> str:
        logger.debug("Creating tailoring prompt")
        prompt = f"""You are an expert resume tailoring assistant. Your task is to modify the given resume to better match the job description while maintaining honesty and authenticity.

INSTRUCTIONS:
1. Analyze the job description for key requirements, skills, and preferences
2. Review the resume content
3. Modify the resume to:
   - Highlight relevant experiences and skills that match the job requirements
   - Use industry-specific keywords from the job description
   - Quantify achievements where possible
   - Maintain truthfulness (don't invent experiences)
   - Keep the same basic structure but reorganize if needed
   - Maintain professional tone and format

Job Description:
{job_description}

Original Resume:
{resume_text}

Please provide the tailored resume in a clear, professional format. Maintain any existing sections but optimize their content for this specific role."""
        logger.debug("Created prompt successfully")
        return prompt

    def tailor_resume(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        logger.debug("Starting resume tailoring process")
        
        if not resume_text.strip():
            logger.error("Empty resume text provided")
            raise ValueError("Empty resume text provided")

        if not job_description.strip():
            logger.error("Empty job description provided")
            raise ValueError("Empty job description provided")

        try:
            # Create the tailoring prompt
            prompt = self._create_tailoring_prompt(resume_text, job_description)
            logger.debug("Created tailoring prompt")
            
            # Call OpenAI API
            try:
                logger.debug("Calling OpenAI API")
                response = openai.ChatCompletion.create(
                    model="gpt-4",  # Using GPT-4 for better understanding and output
                    messages=[
                        {"role": "system", "content": "You are an expert resume tailoring assistant with years of experience in HR and recruitment. Your task is to enhance resumes while maintaining absolute truthfulness and professionalism."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,  # More focused on consistency
                    max_tokens=4000,  # Allow for longer responses
                    top_p=0.9,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                logger.debug("Received response from OpenAI API")
            except Exception as e:
                logger.error(f"OpenAI API Error: {str(e)}")
                raise ValueError(f"Failed to generate response from OpenAI API: {str(e)}")
            
            # Extract the tailored resume from the response
            enhanced_text = response.choices[0].message['content'].strip()
            logger.debug("Extracted enhanced text from response")
            
            if not enhanced_text:
                logger.error("Empty response from OpenAI API")
                raise ValueError("Empty response from OpenAI API")

            result = {
                "original_text": resume_text,
                "enhanced_text": enhanced_text
            }
            logger.debug("Successfully created result dictionary")
            return result
            
        except openai.error.AuthenticationError as e:
            logger.error(f"OpenAI Authentication Error: {str(e)}")
            raise ValueError("Invalid OpenAI API key. Please check your configuration.")
        except openai.error.RateLimitError as e:
            logger.error(f"OpenAI Rate Limit Error: {str(e)}")
            raise ValueError("OpenAI API rate limit exceeded. Please try again later.")
        except Exception as e:
            logger.error(f"Unexpected error in resume tailoring: {str(e)}")
            raise ValueError(f"Error in resume tailoring: {str(e)}")
