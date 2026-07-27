from aikubagent.models.enriched_incident import EnrichedIncident
from aikubagent.models.incident import Incident

from aikubagent.services.prometheus_service import PrometheusService
from aikubagent.services.kubernetes_service import KubernetesService


class ContextBuilder:

    @staticmethod
    def build(incident: Incident) -> EnrichedIncident:

        prometheus = PrometheusService()
        kubernetes = KubernetesService()

        deployment = kubernetes.get_deployment_context(
            namespace="ai-platform",
            deployment_name=incident.service,
        )

        pod = None

        if deployment and deployment["desired_replicas"] > 0:

            pod = kubernetes.get_pod_context(
                namespace="ai-platform",
                app_label=incident.service,
            )

        return EnrichedIncident(
            **incident.model_dump(),

            # -------------------------
            # Prometheus Metrics
            # -------------------------
            request_rate=prometheus.get_request_rate(),
            avg_request_duration=prometheus.get_average_request_duration(),
            active_requests=prometheus.get_active_requests(),
            homepage_visits=prometheus.get_homepage_visits(),
            contact_submissions=prometheus.get_contact_submissions(),

            # -------------------------
            # Kubernetes Context
            # -------------------------
            pod_name=pod["pod_name"] if pod else None,
            pod_phase=pod["phase"] if pod else None,
            pod_ready=pod["ready"] if pod else None,
            pod_restart_count=pod["restart_count"] if pod else None,
            pod_node=pod["node"] if pod else None,
            pod_ip=pod["pod_ip"] if pod else None,
            current_state=pod["current_state"] if pod else None,

            last_termination_reason=pod["last_termination_reason"] if pod else None,

            cpu_request=pod["cpu_request"] if pod else None,
            memory_request=pod["memory_request"] if pod else None,

            cpu_limit=pod["cpu_limit"] if pod else None,
            memory_limit=pod["memory_limit"] if pod else None,
            deployment_name=deployment["deployment_name"] if deployment else None,

            desired_replicas=deployment["desired_replicas"] if deployment else None,

            ready_replicas=deployment["ready_replicas"] if deployment else None,

            available_replicas=deployment["available_replicas"] if deployment else None,

            updated_replicas=deployment["updated_replicas"] if deployment else None,

            unavailable_replicas=deployment["unavailable_replicas"] if deployment else None,
        )