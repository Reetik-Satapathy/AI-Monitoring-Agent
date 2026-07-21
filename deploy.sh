docker build -t ai-agent:latest ./ai-agent
kind load docker-image ai-agent:latest --name ai-platform
kubectl rollout restart deployment/ai-agent -n ai-platform
kubectl rollout status deployment/ai-agent -n ai-platform
kubectl logs -f deployment/ai-agent -n ai-platform