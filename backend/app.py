import os
import logging
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from services.pdf_parser import PDFParser
from services.resume_tailor import ResumeTailor
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import traceback

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Get environment-specific settings
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
FRONTEND_URL = os.getenv('FRONTEND_URL', '')

# Configure CORS
allowed_origins = [
    'http://localhost:3000',     # Local React development
    'http://localhost:5001',     # Local Flask development
    'http://localhost:8080',     # Production port
    'https://localhost:8080',    # Production port with HTTPS
    FRONTEND_URL                 # Production frontend URL from env
]

logger.info(f"Allowed CORS origins: {allowed_origins}")
logger.info(f"Environment: {ENVIRONMENT}")
logger.info(f"Frontend URL: {FRONTEND_URL}")

CORS(app, resources={
    r"/*": {
        "origins": allowed_origins,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": False
    }
})

@app.before_request
def log_request_info():
    logger.debug('Headers: %s', dict(request.headers))
    logger.debug('Body: %s', request.get_data())

pdf_parser = PDFParser()
resume_tailor = ResumeTailor()

def extract_text_from_url(url):
    try:
        # Add User-Agent header to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text and clean it up
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        logger.error(f"Error extracting text from URL: {str(e)}", exc_info=True)
        return None

@app.route('/health', methods=['GET'])
def health_check():
    logger.debug("Received request to /health")
    return jsonify({"status": "healthy"}), 200

@app.route('/tailor-resume', methods=['POST'])
def tailor_resume():
    try:
        logger.debug("Received request to /tailor-resume")
        logger.debug(f"Form data: {request.form}")
        logger.debug(f"Files: {request.files}")
        
        if 'resume' not in request.files:
            logger.error("No resume file in request")
            return jsonify({"error": "No resume file provided"}), 400
            
        if 'job_url' not in request.form:
            logger.error("No job URL provided")
            return jsonify({"error": "No job URL provided"}), 400

        resume_file = request.files['resume']
        job_url = request.form['job_url']
        
        logger.debug(f"Processing resume file: {resume_file.filename}")
        logger.debug(f"Job URL: {job_url}")
        
        if resume_file.filename == '':
            logger.error("No selected file")
            return jsonify({"error": "No selected file"}), 400
            
        if not resume_file.filename.lower().endswith('.pdf'):
            logger.error("File must be a PDF")
            return jsonify({"error": "File must be a PDF"}), 400

        # Extract text from PDF
        resume_text = pdf_parser.extract_text_from_pdf(resume_file)
        logger.debug("Successfully extracted text from PDF")
        if not resume_text:
            logger.error("Could not extract text from PDF")
            return jsonify({"error": "Could not extract text from PDF"}), 400

        # Fetch and extract text from job description URL
        job_description = extract_text_from_url(job_url)
        logger.debug("Successfully extracted job description")
        if not job_description:
            logger.error("Could not fetch job description from URL")
            return jsonify({"error": "Could not fetch job description from URL"}), 400

        logger.debug(f"Extracted job description: {job_description[:200]}...")

        # Tailor the resume
        logger.debug("Starting resume tailoring process...")
        result = resume_tailor.tailor_resume(resume_text, job_description)
        logger.debug("Successfully tailored resume")
        
        return jsonify({
            'original_text': resume_text,
            'enhanced_text': result['enhanced_text']
        }), 200

    except Exception as e:
        logger.error(f"Error in tailor_resume: {str(e)}", exc_info=True)
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
