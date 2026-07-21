from typing import Optional

from aikubagent.models.incident import Incident


class EnrichedIncident(Incident):
    request_rate: Optional[float] = None

    avg_request_duration: Optional[float] = None

    active_requests: Optional[int] = None

    homepage_visits: Optional[int] = None

    contact_submissions: Optional[int] = None