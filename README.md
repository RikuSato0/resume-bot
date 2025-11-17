# Resume Bot

An intelligent resume analysis and job recommendation system that processes PDF resumes and provides personalized job recommendations based on skills and experience.

## Features
- PDF Resume Processing
- Skills and Experience Extraction
- Job Recommendations with Internet Search Integration
- Well-formatted Resume Analysis
- Low Hallucination Rate through Optimized Prompting

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
OPENAI_API_KEY=your_openai_api_key
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints
- POST `/analyze-resume`: Upload and analyze a PDF resume
- GET `/recommendations/{resume_id}`: Get job recommendations for a specific resume 