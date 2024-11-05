from prometheus_client import Counter, Gauge

# Define the Prometheus counter metric
connections_counter = Counter('total_connections', 'Total number of connections')
