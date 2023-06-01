import os
import re
from jinja2 import Template
from jinja2 import Environment

def get_cluster_fqdn(databse_endpoint):
    # Remove the port section if present
    str = re.sub(":\d+", "", databse_endpoint)
    # Remove the "redis-12345" section if present
    str = re.sub("redis-\d+\.", "", str)
    # Remove the "internal." section if present
    str = re.sub("internal\.", "", str)
    return str

if __name__ == "__main__":

  cluster_fqdn = get_cluster_fqdn(os.getenv("REDIS_CLOUD_PRIVATE_ENDPOINT"))

  redis_ca_cert = os.getenv("REDIS_CLOUD_CA_CERT")
  ca_cert_present = redis_ca_cert != None
  if ca_cert_present:
    f = open("/etc/datadog-agent/conf.d/prometheus.d/ca.pem", "w")
    f.write(redis_ca_cert)
    f.close()

  template = """init_config:
instances:
  - prometheus_url: https://internal.{{ cluster_fqdn }}:8070/metric
{% if ca_cert_present %}
    ssl_ca_cert: /etc/datadog-agent/conf.d/prometheus.d/ca.pem
{% else %}
    ssl_ca_cert: false
{% endif %}
    namespace: redise
    max_returned_metrics: 2000
    metrics:
      - "*"

  - prometheus_url: http://localhost:8000/
    ssl_ca_cert: false
    namespace: redise
    max_returned_metrics: 2000
    metrics:
      - bdb_estimated_max_throughput
      - bdb_data_persistence
  """

  data = {
      "cluster_fqdn": cluster_fqdn,
      "ca_cert_present": ca_cert_present
  }

  env = Environment(trim_blocks=True, lstrip_blocks=True)

  template = env.from_string(template)

  f = open("/etc/datadog-agent/conf.d/prometheus.d/conf.yaml", "w")
  f.write(template.render(data))
  f.close()
