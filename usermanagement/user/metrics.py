# myapp/metrics.py

from prometheus_client import Counter, Gauge

# Define the Prometheus counter metric
user_created_counter = Counter('my_usermanagement_users_created_total', 'Total number of users created successfully')
user_logged_in_counter = Gauge('my_usermanagement_users_logged_in_total', 'Total number of users logged in')
