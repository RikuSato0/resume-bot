from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import uuid
from .resume_analyzer import ResumeAnalyzer, ResumeAnalysis
from .job_recommender import JobRecommender, JobRecommendation
from .config import *

app = FastAPI(title=APP_NAME)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
resume_analyzer = ResumeAnalyzer()
job_recommender = JobRecommender()

# In-memory cache (Note: This will be cleared on serverless function cold starts)
resume_cache = {}

@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    """Upload and analyze a PDF resume."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Check file size (Vercel has a 50MB limit)
    content = await file.read()
    if len(content) > 50 * 1024 * 1024:  # 50MB
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 50MB")
    
    # Create a temporary file in /tmp (Vercel's writable directory)
    temp_path = f"/tmp/temp_{uuid.uuid4()}.pdf"
    try:
        with open(temp_path, "wb") as buffer:
            buffer.write(content)
        
        # Analyze resume
        analysis = resume_analyzer.analyze_resume(temp_path)
        
        # Store in cache
        resume_id = str(uuid.uuid4())
        resume_cache[resume_id] = analysis.dict()
        
        return JSONResponse({
            "resume_id": resume_id,
            "analysis": analysis.dict()
        })
    
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/recommendations/{resume_id}")
async def get_recommendations(resume_id: str, max_recommendations: int = 5):
    """Get job recommendations for a specific resume."""
    if resume_id not in resume_cache:
        raise HTTPException(status_code=404, detail="Resume analysis not found")
    
    candidate_profile = resume_cache[resume_id]
    recommendations = job_recommender.get_recommendations(
        candidate_profile,
        max_recommendations=max_recommendations
    )
    
    return JSONResponse({
        "recommendations": [rec.dict() for rec in recommendations]
    })

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT) 