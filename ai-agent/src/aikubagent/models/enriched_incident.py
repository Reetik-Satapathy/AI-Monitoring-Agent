from typing import Optional

from aikubagent.models.incident import Incident


class EnrichedIncident(Incident):

    # -------------------------
    # Prometheus Metrics
    # -------------------------
    request_rate: Optional[float] = None

    avg_request_duration: Optional[float] = None

    active_requests: Optional[int] = None

    homepage_visits: Optional[int] = None

    contact_submissions: Optional[int] = None

    # -------------------------
    # Kubernetes Context
    # -------------------------
    pod_name: Optional[str] = None

    pod_phase: Optional[str] = None

    pod_ready: Optional[bool] = None

    pod_restart_count: Optional[int] = None

    pod_node: Optional[str] = None

    pod_ip: Optional[str] = None

    cpu_request: Optional[str] = None

    memory_request: Optional[str] = None

    cpu_limit: Optional[str] = None

    memory_limit: Optional[str] = None

    current_state: Optional[str] = None

    last_termination_reason: Optional[str] = None

    deployment_name: Optional[str] = None

    desired_replicas: Optional[int] = None

    ready_replicas: Optional[int] = None

    available_replicas: Optional[int] = None

    updated_replicas: Optional[int] = None

    unavailable_replicas: Optional[int] = None