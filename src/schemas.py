from pydantic import BaseModel
from typing import List


class Experience(BaseModel):
    company: str
    role: str
    responsibilities: List[str]
    achievements: List[str]


class Project(BaseModel):
    name: str
    description: str
    technologies: List[str]


class Certification(BaseModel):
    name: str
    issuer: str


class CareerProfile(BaseModel):
    name: str
    title: str
    skills: List[str]
    experience: List[Experience]
    projects: List[Project]
    certifications: List[Certification]
    education: List[str]
    achievements: List[str]
class DocumentClassification(BaseModel):
    document_type: str
    confidence: float
class CertificationData(BaseModel):
    name: str
    issuer: str
    issue_date: str
    skills: List[str]


class ProjectData(BaseModel):
    name: str
    description: str
    technologies: List[str]
    skills: List[str]
class JobDescription(BaseModel):
    job_title: str
    company: str
    required_skills: List[str]
    preferred_skills: List[str]
    responsibilities: List[str]
    qualifications: List[str]