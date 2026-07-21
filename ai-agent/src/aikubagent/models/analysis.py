from pydantic import BaseModel
from typing import List


class IncidentAnalysis(BaseModel):
    summary: str
    severity: str
    impact: str

    probable_root_cause: str

    possible_causes: list[str]

    first_troubleshooting_step: str

    confidence: float