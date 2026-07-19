from prometheus_client import Counter, Histogram, Gauge

# =====================================================
# Business Metrics
# =====================================================

homepage_visits = Counter(
    "homepage_visits_total",
    "Total number of homepage visits"
)

contact_submissions = Counter(
    "contact_form_submissions_total",
    "Total successful contact form submissions"
)

invalid_contact_submissions = Counter(
    "invalid_contact_submissions_total",
    "Total invalid contact form submissions"
)

# =====================================================
# HTTP Metrics
# =====================================================

http_requests = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

request_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"]
)

active_requests = Gauge(
    "http_requests_in_progress",
    "Number of active HTTP requests"
)

# =====================================================
# Database Metrics
# =====================================================

database_inserts = Counter(
    "database_inserts_total",
    "Total successful database inserts"
)

database_insert_failures = Counter(
    "database_insert_failures_total",
    "Total failed database inserts"
)

database_insert_duration = Histogram(
    "database_insert_duration_seconds",
    "Time spent inserting into the database"
)