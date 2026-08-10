import os

from dotenv import load_dotenv
from google import genai


from schemas import (
    CareerProfile,
    CertificationData,
    ProjectData,
    DocumentClassification,
    JobDescription
)
def analyze_job_description(text):

    prompt = f"""
    Analyze the following job description.

    Extract:

    1. Job title
    2. Company name
    3. Required technical and professional skills
    4. Preferred or nice-to-have skills
    5. Main responsibilities
    6. Qualifications and experience requirements

    Rules:

    - Extract only information supported by the job description.
    - Do not invent skills.
    - Keep individual skills separate.
    - Normalize obvious variations where appropriate.
      Example:
      "Python programming" → "Python"
      "CI/CD pipelines" → "CI/CD"
    - Do not treat every responsibility as a skill.
    - If the company name is unavailable, return an empty string.

    JOB DESCRIPTION:

    {text}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": JobDescription.model_json_schema()
        }
    )

    return JobDescription.model_validate_json(response.text)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. Check your .env file."
    )

client = genai.Client(api_key=api_key)


def ask_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text

def classify_document(text):
    prompt = f"""
    Classify the following career-related document.

    Choose exactly ONE document type from:

    - resume
    - certification
    - project
    - education
    - achievement
    - other

    Rules:
    - Choose "resume" for a resume or CV.
    - Choose "certification" for a certificate or credential.
    - Choose "project" for a project description/report.
    - Choose "education" for academic records or educational documents.
    - Choose "achievement" for awards, competitions, recognitions, etc.
    - Choose "other" if none of these apply.
    - Do not guess based only on filenames.
    - Base the classification on the document content.

    DOCUMENT:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": DocumentClassification.model_json_schema()
        }
    )

    return DocumentClassification.model_validate_json(response.text)

def extract_career_profile(text):
    prompt = f"""
    Analyze the following career document.

    Extract only information explicitly present in the document.
    Do not invent or assume information.

    Identify:
    - person's name
    - professional title
    - technical/professional skills
    - projects
    - certifications
    - education
    - achievements

    Important classification rules:

- Employment responsibilities belong under experience.
- Only include something under projects if the document explicitly identifies it as a project, academic project, personal project, or similar.
- Do not invent project names.
- Do not convert individual work responsibilities into projects.
- Only include certifications explicitly identified as certifications, courses, or credentials.
- Do not invent certification issuers.
- If information is unavailable, use an empty string rather than guessing.

    DOCUMENT
    {text}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": CareerProfile.model_json_schema()
        }
    )

    return CareerProfile.model_validate_json(response.text)
def extract_certification(text):
    prompt = f"""
    Extract information from this certification document.

    Extract:
    - certification name
    - issuing organization
    - issue date
    - skills or topics demonstrated

    Rules:
    - Only extract information explicitly present.
    - Do not invent an issuer.
    - Do not infer an issue date.
    - If information is unavailable, return an empty string.
    - Only include skills supported by the document.

    DOCUMENT:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": CertificationData.model_json_schema()
        }
    )

    return CertificationData.model_validate_json(response.text)
def extract_project(text):
    prompt = f"""
    Extract information from this project document.

    Extract:
    - project name
    - project description
    - technologies used
    - skills demonstrated

    Rules:
    - Only extract information explicitly present.
    - Do not invent technologies.
    - Do not infer skills that are not supported.
    - If information is unavailable, return an empty string or empty list.

    DOCUMENT:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": ProjectData.model_json_schema()
        }
    )

    return ProjectData.model_validate_json(response.text)
