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
    ssl_ca_cert: /etc/datadog-agent/conf.d/prometheus.d/ca.pem"
{% else %}
    ssl_ca_cert: false
{% endif %}
    namespace: redise
    max_returned_metrics: 2000
    metrics:
      - bdb_avg_latency
      - bdb_avg_latency_max
      - bdb_avg_other_latency
      - bdb_avg_read_latency
      - bdb_avg_write_latency
      - bdb_conns
      - bdb_egress_bytes
      - bdb_evicted_objects
      - bdb_expired_objects
      - bdb_fork_cpu_system
      - bdb_ingress_bytes
      - bdb_main_thread_cpu_system
      - bdb_main_thread_cpu_system_max
      - bdb_memory_limit
      - bdb_no_of_keys
      - bdb_other_req
      - bdb_read_req
      - bdb_shard_cpu_system
      - bdb_shard_cpu_system_max
      - bdb_total_req
      - bdb_total_req_max
      - bdb_used_memory
      - bdb_write_req
      - listener_acc_latency
      - listener_conns
      - listener_total_req
      - bdb_crdt_syncer_egress_bytes
      - bdb_crdt_syncer_egress_bytes_decompressed
      - bdb_crdt_syncer_ingress_bytes
      - bdb_crdt_syncer_ingress_bytes_decompressed
      - bdb_crdt_syncer_local_ingress_lag_time
      - bdb_crdt_syncer_pending_local_writes_max
      - bdb_crdt_syncer_pending_local_writes_min
      - bdb_crdt_syncer_status
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
