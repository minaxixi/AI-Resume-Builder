# AI Resume Builder

An intelligent resume tailoring application that uses GPT-4 to optimize resumes for specific job descriptions. The application automatically extracts job descriptions from URLs and provides a side-by-side comparison of the original and tailored resumes.

## Features

- Upload PDF resumes
- Automatic job description extraction from URLs
- GPT-4 powered resume tailoring
- Side-by-side comparison with diff highlighting
- Modern, responsive UI using Chakra UI

## Tech Stack

### Backend
- Python
- Flask
- OpenAI GPT-4
- PyPDF2 for PDF processing
- BeautifulSoup4 for web scraping

### Frontend
- React
- TypeScript
- Chakra UI
- Axios

## Setup

1. Clone the repository
```bash
git clone [your-repo-url]
cd AIResumeBuilder
```

2. Set up the backend
```bash
cd backend
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables
```bash
# Create a .env file in the backend directory
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

4. Set up the frontend
```bash
cd frontend
npm install
```

5. Run the application
```bash
# Terminal 1 (Backend)
cd backend
flask run --port=5001

# Terminal 2 (Frontend)
cd frontend
npm start
```

The application will be available at `http://localhost:3000`

## Usage

1. Upload your resume (PDF format)
2. Paste the job posting URL
3. Click "Tailor Resume"
4. View the original and tailored versions side by side
5. Toggle diff highlighting to see the changes

## License

MIT
