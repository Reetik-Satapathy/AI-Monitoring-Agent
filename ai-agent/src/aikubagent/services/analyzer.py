from unittest import result

from aikubagent.crew import Aikubagent
from aikubagent.models.incident import Incident
import json
from aikubagent.models.analysis import IncidentAnalysis
from aikubagent.models.enriched_incident import EnrichedIncident

class IncidentAnalyzer:

    @staticmethod
    def analyze(incident: EnrichedIncident) -> str:

        inputs = {
            "alert_name": incident.alert_name,
            "severity": incident.severity,
            "service": incident.service,
            "summary": incident.summary,
            "description": incident.description,

            "request_rate": incident.request_rate,
            "avg_request_duration": incident.avg_request_duration,
            "active_requests": incident.active_requests,
            "homepage_visits": incident.homepage_visits,
            "contact_submissions": incident.contact_submissions,
        }

        result = Aikubagent().crew().kickoff(inputs=inputs)


        return result.pydantic