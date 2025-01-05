"""
This module contains prompt templates used for various AI operations.
"""

def get_resume_tailor_system_prompt() -> str:
    """
    Get the system prompt for the resume tailoring assistant.
    
    Returns:
        str: The system prompt
    """
    return """You are an expert resume tailoring assistant with years of experience in HR and recruitment. Your task is to enhance resumes while maintaining absolute truthfulness and professionalism.

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

Please provide the tailored resume in a clear, professional format. Maintain any existing sections but optimize their content for this specific role.
    """

def get_resume_tailor_user_prompt(resume_text: str, job_description: str) -> str:
    """
    Get the user prompt for tailoring a resume to a specific job description.
    
    Args:
        resume_text (str): The original resume text
        job_description (str): The target job description
    
    Returns:
        str: The formatted prompt
    """
    return f"""
Job Description:
{job_description}

Original Resume:
{resume_text}
"""
