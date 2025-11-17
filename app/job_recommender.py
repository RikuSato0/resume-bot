from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import json

load_dotenv()

class JobRecommendation(BaseModel):
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    description: str = Field(description="Job description")
    required_skills: List[str] = Field(description="Required skills for the position")
    match_score: float = Field(description="Match score between candidate and job (0-100)")
    source_url: str = Field(description="URL of the job posting")

class JobRecommender:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,  # Low temperature for reduced randomness
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.parser = PydanticOutputParser(pydantic_object=JobRecommendation)
        
        self.recommendation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a precise job recommender. Your task is to analyze job postings and match them with candidate profiles.
            Follow these guidelines:
            1. Only recommend jobs that match the candidate's skills and experience
            2. Calculate match score based on explicit skill matches
            3. Do not make assumptions about candidate's preferences
            4. Provide detailed reasoning for each recommendation
            5. Include only verified job postings
            
            {format_instructions}"""),
            ("user", """Candidate Profile:
            {candidate_profile}
            
            Job Posting:
            {job_posting}
            
            Please analyze the match and provide a recommendation.""")
        ])

    def search_jobs(self, skills: List[str], location: str = "remote") -> List[Dict]:
        """Search for jobs using various job boards APIs."""
        # This is a placeholder for actual job board API integration
        # In a real implementation, you would integrate with LinkedIn, Indeed, or other job boards
        jobs = []
        
        # Example job board API call (replace with actual API)
        search_query = f"{' '.join(skills)} {location}"
        # jobs = self._call_job_board_api(search_query)
        
        return jobs

    def analyze_job_match(self, candidate_profile: Dict, job_posting: Dict) -> JobRecommendation:
        """Analyze match between candidate and job posting."""
        formatted_prompt = self.recommendation_prompt.format_messages(
            candidate_profile=json.dumps(candidate_profile, indent=2),
            job_posting=json.dumps(job_posting, indent=2),
            format_instructions=self.parser.get_format_instructions()
        )
        
        response = self.llm.invoke(formatted_prompt)
        recommendation = self.parser.parse(response.content)
        return recommendation

    def get_recommendations(self, candidate_profile: Dict, max_recommendations: int = 5) -> List[JobRecommendation]:
        """Get job recommendations for a candidate."""
        # Extract skills from candidate profile
        skills = candidate_profile.get("skills", [])
        
        # Search for jobs
        jobs = self.search_jobs(skills)
        
        # Analyze each job posting
        recommendations = []
        for job in jobs[:max_recommendations]:
            recommendation = self.analyze_job_match(candidate_profile, job)
            recommendations.append(recommendation)
        
        # Sort by match score
        recommendations.sort(key=lambda x: x.match_score, reverse=True)
        return recommendations 