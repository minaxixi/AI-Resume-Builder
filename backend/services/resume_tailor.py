import os
import openai
from typing import Dict, Any

class ResumeTailor:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
    def _create_tailoring_prompt(self, resume_text: str, job_description: str) -> str:
        return f"""You are an expert resume tailoring assistant. Your task is to modify the given resume to better match the job description while maintaining honesty and authenticity.

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

    def tailor_resume(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        
        if not resume_text.strip():
            raise ValueError("Empty resume text provided")

        if not job_description.strip():
            raise ValueError("Empty job description provided")

        try:
            # Create the tailoring prompt
            prompt = self._create_tailoring_prompt(resume_text, job_description)
            
            # Call OpenAI API
            try:
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
            except:
                raise ValueError("Failed to generate response from OpenAI API")
            
            # Extract the tailored resume from the response
            tailored_resume = response.choices[0].message['content'].strip()
            
            if not tailored_resume:
                raise ValueError("Empty response from OpenAI API")

            return {
                "original_resume": resume_text,
                "tailored_resume": tailored_resume
            }
            
        except openai.error.AuthenticationError as e:
            print(f"OpenAI Authentication Error: {str(e)}")
            raise ValueError("Invalid OpenAI API key. Please check your configuration.")
        except openai.error.RateLimitError as e:
            print(f"OpenAI Rate Limit Error: {str(e)}")
            raise ValueError("OpenAI API rate limit exceeded. Please try again later.")
        except Exception as e:
            print(f"Unexpected error in resume tailoring: {str(e)}")
            raise ValueError(f"Error in resume tailoring: {str(e)}")
