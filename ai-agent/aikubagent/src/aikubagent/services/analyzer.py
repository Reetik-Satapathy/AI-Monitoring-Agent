from aikubagent.crew import Aikubagent
from aikubagent.models.incident import Incident


class IncidentAnalyzer:

    @staticmethod
    def analyze(incident: Incident) -> str:

        inputs = {
            "alert_name": incident.alert_name,
            "severity": incident.severity,
            "service": incident.service,
            "summary": incident.summary,
            "description": incident.description,
        }

        result = Aikubagent().crew().kickoff(inputs=inputs)

        return str(result)