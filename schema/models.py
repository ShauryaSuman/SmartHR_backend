from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TemplateBase(BaseModel):
    job_title: str
    department: str
    location: str
    experience_level: str
    employment_type: str
    salary_range: str
    required_skills: str
    preferred_skills: str
    responsibilities: str
    qualifications: str
    benefits: str

class TemplateCreate(TemplateBase):
    pass

class TemplateUpdate(TemplateBase):
    pass

class Template(TemplateBase):
    template_id: str
    created_at: datetime
    modified_time: datetime

    class Config:
        from_attributes = True