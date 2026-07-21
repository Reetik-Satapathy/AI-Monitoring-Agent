import os
import requests


class PrometheusService:

    def __init__(self):
        self.base_url = os.getenv(
            "PROMETHEUS_URL",
            "http://prometheus:9090"
        )

    def query(self, promql: str):
        response = requests.get(
            f"{self.base_url}/api/v1/query",
            params={"query": promql},
            timeout=5,
        )

        response.raise_for_status()

        data = response.json()

        if data["status"] != "success":
            return None

        result = data["data"]["result"]

        if not result:
            return None

        return float(result[0]["value"][1])

    def get_request_rate(self):
        return self.query(
            "sum(rate(http_requests_total[1m]))"
        )

    def get_average_request_duration(self):
        return self.query(
            "rate(http_request_duration_seconds_sum[1m]) / rate(http_request_duration_seconds_count[1m])"
        )

    def get_active_requests(self):
        return self.query(
            "http_requests_in_progress"
        )

    def get_homepage_visits(self):
        return self.query(
            "homepage_visits_total"
        )

    def get_contact_submissions(self):
        return self.query(
            "contact_form_submissions_total"
        )