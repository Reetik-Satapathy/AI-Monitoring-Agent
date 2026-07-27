from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException


class KubernetesService:

    def __init__(self):
        try:
            config.load_incluster_config()
            print("Using in-cluster Kubernetes config")
        except ConfigException:
            config.load_kube_config()
            print("Using local kubeconfig")

        self.core = client.CoreV1Api()
        self.apps = client.AppsV1Api()

    def get_pod(self, namespace: str, app_label: str):

        pods = self.core.list_namespaced_pod(
            namespace=namespace,
            label_selector=f"app={app_label}"
        )

        if not pods.items:
            return None

        # Return the newest pod
        pods.items.sort(
            key=lambda pod: pod.metadata.creation_timestamp,
            reverse=True
        )

        return pods.items[0]

    def get_deployment(self, namespace: str, deployment_name: str):

        try:
            return self.apps.read_namespaced_deployment(
                name=deployment_name,
                namespace=namespace,
            )

        except client.exceptions.ApiException as e:

            if e.status == 404:
                return None

            raise

    def get_pod_context(self, namespace: str, app_label: str):

        pod = self.get_pod(namespace, app_label)

        if pod is None:
            return None

        container = None

        if pod.status.container_statuses:
            container = pod.status.container_statuses[0]

        resources = pod.spec.containers[0].resources

        requests = resources.requests or {}
        limits = resources.limits or {}

        last_state = None

        if container and container.last_state and container.last_state.terminated:
            last_state = container.last_state.terminated.reason

        current_state = None

        if container:
            if container.state.running:
                current_state = "Running"
            elif container.state.waiting:
                current_state = container.state.waiting.reason
            elif container.state.terminated:
                current_state = container.state.terminated.reason

        return {

            # -------------------------
            # Pod Details
            # -------------------------
            "pod_name": pod.metadata.name,
            "phase": pod.status.phase,
            "node": pod.spec.node_name,
            "pod_ip": pod.status.pod_ip,
            "host_ip": pod.status.host_ip,
            "start_time": pod.status.start_time,

            # -------------------------
            # Container Status
            # -------------------------
            "ready": container.ready if container else None,
            "restart_count": container.restart_count if container else 0,
            "current_state": current_state,
            "last_termination_reason": last_state,

            # -------------------------
            # Resource Requests
            # -------------------------
            "cpu_request": requests.get("cpu"),
            "memory_request": requests.get("memory"),

            # -------------------------
            # Resource Limits
            # -------------------------
            "cpu_limit": limits.get("cpu"),
            "memory_limit": limits.get("memory"),
        }
    def get_deployment_context(self, namespace: str, deployment_name: str):

        deployment = self.get_deployment(
            namespace,
            deployment_name,
        )

        if deployment is None:
            return None

        status = deployment.status

        return {

            "deployment_name": deployment.metadata.name,

            "desired_replicas": status.replicas or 0,

            "ready_replicas": status.ready_replicas or 0,

            "available_replicas": status.available_replicas or 0,

            "updated_replicas": status.updated_replicas or 0,

            "unavailable_replicas": status.unavailable_replicas or 0,
        }