from pydantic import BaseModel, Field
from typing import Optional, Dict

class CommandRequest(BaseModel):
    command: str = Field(..., example="deploy")
    params: Optional[Dict[str, str]] = Field(
        None, example={"model_type": "text-generation", "model_name": "TinyLlama/TinyLlama-1.1B-Chat-v1.0"}
    )

class CommandResponse(BaseModel):
    status: str
    detail: Optional[str] = None
    data: Optional[dict] = None
