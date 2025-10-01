from pydantic import BaseModel
from typing import List

class SuggestOutput(BaseModel):
    missing_skills : List[str]
    preparation_advice: str