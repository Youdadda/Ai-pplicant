from pydantic import BaseModel
from typing import Optional

class ProcessingRequest(BaseModel):
    file_id : str 
    posting : bool ## Temporary solution