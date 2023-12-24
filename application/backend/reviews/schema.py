from typing import List
from datetime import datetime
from pydantic import BaseModel, constr, EmailStr


class Rewiews(BaseModel):

    id: int
    text: str
    problem: str
    problem_short: str
    solution: str
    tags: str
    date: datetime
