from aikubagent.services.kubernetes_service import KubernetesService

service = KubernetesService()

print(
    service.get_deployment_context(
        namespace="ai-platform",
        deployment_name="demo-app",
    )
)