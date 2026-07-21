from aikubagent.models.webhook import AlertmanagerWebhook
from aikubagent.models.incident import Incident


class AlertParser:

    @staticmethod
    def parse(webhook: AlertmanagerWebhook) -> list[Incident]:

        incidents = []

        for alert in webhook.alerts:

            incident = Incident(
                alert_name=alert.labels.get("alertname", "Unknown"),
                severity=alert.labels.get("severity", "unknown"),
                status=alert.status,
                service=alert.labels.get("job"),
                summary=alert.annotations.get("summary"),
                description=alert.annotations.get("description"),
                starts_at=alert.startsAt,
                fingerprint=alert.fingerprint,
            )

            incidents.append(incident)

        return incidents