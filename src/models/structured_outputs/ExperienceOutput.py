from pydantic import BaseModel
from typing import Optional, List


class Experience(BaseModel):
    job_title: str
    company: str
    description: str
    experience_type: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    skills: List[str]

class ExperienceResponse(BaseModel):
    experiences: List[Experience]
