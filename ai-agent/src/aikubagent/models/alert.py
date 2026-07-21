from pydantic import BaseModel
from typing import Dict, Optional


class Alert(BaseModel):
    status: str

    labels: Dict[str, str]

    annotations: Dict[str, str]

    startsAt: str

    endsAt: Optional[str] = None

    generatorURL: Optional[str] = None

    fingerprint: Optional[str] = None