from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
