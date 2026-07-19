from typing import List, Dict

from pydantic import BaseModel

from .alert import Alert


class AlertmanagerWebhook(BaseModel):
    receiver: str

    status: str

    alerts: List[Alert]

    groupLabels: Dict[str, str]

    commonLabels: Dict[str, str]

    commonAnnotations: Dict[str, str]

    externalURL: str

    version: str

    groupKey: str

    truncatedAlerts: int