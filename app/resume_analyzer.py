from typing import Dict, List
import PyPDF2
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

class ResumeAnalysis(BaseModel):
    name: str = Field(description="Full name of the candidate")
    email: str = Field(description="Email address if found")
    phone: str = Field(description="Phone number if found")
    skills: List[str] = Field(description="List of technical and soft skills")
    experience: List[Dict] = Field(description="List of work experiences with company, role, and duration")
    education: List[Dict] = Field(description="List of educational qualifications")
    summary: str = Field(description="Professional summary or objective statement")

class ResumeAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,  # Low temperature for reduced randomness
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.parser = PydanticOutputParser(pydantic_object=ResumeAnalysis)
        
        self.analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a precise resume analyzer. Your task is to extract information from resumes with high accuracy.
            Follow these guidelines:
            1. Only extract information that is explicitly stated in the resume
            2. Do not make assumptions or inferences
            3. If information is not found, leave it blank
            4. Format dates consistently
            5. Extract skills that are explicitly mentioned
            6. Maintain the original order of experiences and education
            
            {format_instructions}"""),
            ("user", "Please analyze this resume text and extract the relevant information:\n\n{resume_text}")
        ])

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file."""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    def analyze_resume(self, pdf_path: str) -> ResumeAnalysis:
        """Analyze resume and return structured data."""
        resume_text = self.extract_text_from_pdf(pdf_path)
        
        # Format the prompt with the parser's instructions
        formatted_prompt = self.analysis_prompt.format_messages(
            resume_text=resume_text,
            format_instructions=self.parser.get_format_instructions()
        )
        
        # Get response from LLM
        response = self.llm.invoke(formatted_prompt)
        
        # Parse the response into structured data
        analysis = self.parser.parse(response.content)
        return analysis 