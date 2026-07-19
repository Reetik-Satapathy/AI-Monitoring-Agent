from pydantic import BaseModel
from typing import Optional


class Incident(BaseModel):
    alert_name: str

    severity: str

    status: str

    service: Optional[str] = None

    summary: Optional[str] = None

    description: Optional[str] = None

    starts_at: str

    fingerprint: Optional[str] = None