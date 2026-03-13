from pydantic import BaseModel
from typing import List


class RunRequest(BaseModel):
    instruction: str


class ShortIdea(BaseModel):
    title: str
    hook: str
    visual_prompt: str
    description: str


class RunResult(BaseModel):
    instruction: str
    created: int
    uploaded: int
    items: List[dict]
