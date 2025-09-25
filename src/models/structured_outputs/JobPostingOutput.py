from pydantic import BaseModel
from typing import List, Optional

class JobPostingResponse(BaseModel):
    title: str
    company: str
    skills : List[str]
    recruiter_email : Optional[str] = None
