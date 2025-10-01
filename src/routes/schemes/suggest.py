from pydantic import BaseModel
from typing import Optional

class SuggestRequest(BaseModel):
    posting_id : int