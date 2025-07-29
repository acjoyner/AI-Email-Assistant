# models.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Email(BaseModel):
    id: str
    thread_id: str
    subject: Optional[str] = None
    sender: str
    recipients: List[str]
    date: datetime
    body: str = Field(..., description="The main content of the email")