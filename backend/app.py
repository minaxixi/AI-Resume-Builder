import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from services.pdf_parser import PDFParser
from services.resume_tailor import ResumeTailor
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import re

load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes and origins
CORS(app, resources={r"/*": {"origins": "*"}})

pdf_parser = PDFParser()
resume_tailor = ResumeTailor()

def extract_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text and clean it
        text = soup.get_text()
        # Remove extra whitespace and normalize newlines
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except Exception as e:
        print(f"Error fetching job description: {str(e)}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Server is running"}), 200

@app.route('/tailor-resume', methods=['POST'])
def tailor_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({"error": "No resume file provided"}), 400
            
        if 'job_description' not in request.form:
            return jsonify({"error": "No job description URL provided"}), 400

        resume_file = request.files['resume']
        job_url = request.form['job_description']
        
        print(f"Received job URL: {job_url}")
        
        if resume_file.filename == '':
            return jsonify({"error": "No selected file"}), 400
            
        if not resume_file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "File must be a PDF"}), 400

        # Extract text from PDF
        resume_text = pdf_parser.extract_text_from_pdf(resume_file)
        if not resume_text:
            return jsonify({"error": "Could not extract text from PDF"}), 400

        # Fetch and extract text from job description URL
        job_description = extract_text_from_url(job_url)
        if not job_description:
            return jsonify({"error": "Could not fetch job description from URL"}), 400

        print(f"Extracted job description: {job_description[:200]}...")

        # Tailor the resume
        result = resume_tailor.tailor_resume(resume_text, job_description)
        
        return jsonify(result), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request", "details": str(e)}), 500

if __name__ == '__main__':
    # Enable debug mode and allow all hosts
    app.run(debug=True, host='0.0.0.0', port=5001)
