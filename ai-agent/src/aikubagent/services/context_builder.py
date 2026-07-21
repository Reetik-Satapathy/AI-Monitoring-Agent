from aikubagent.models.enriched_incident import EnrichedIncident
from aikubagent.models.incident import Incident
from aikubagent.services.prometheus_service import PrometheusService


class ContextBuilder:

    @staticmethod
    def build(incident: Incident) -> EnrichedIncident:

        service = PrometheusService()

        return EnrichedIncident(
            **incident.model_dump(),

            request_rate=service.get_request_rate(),

            avg_request_duration=service.get_average_request_duration(),

            active_requests=service.get_active_requests(),

            homepage_visits=service.get_homepage_visits(),

            contact_submissions=service.get_contact_submissions(),
        )