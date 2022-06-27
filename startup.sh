#!/bin/bash

echo "api_key: ${DATADOG_API_KEY}" > /etc/datadog-agent/datadog.yaml
echo "ste: ${DATADOG_SITE}" >> /etc/datadog-agent/datadog.yaml

echo "init_config:" > /etc/datadog-agent/conf.d/prometheus.d/conf.yaml
echo "instances:" >> /etc/datadog-agent/conf.d/prometheus.d/conf.yaml
echo "  - prometheus_url: ${REDIS_CLOUD_ENDPOINT_URL}" >> /etc/datadog-agent/conf.d/prometheus.d/conf.yaml
if [ "${REDIS_CLOUD_CA_CERT}X" == "X" ]; then
	echo "    ssl_ca_cert: false" >> /etc/datadog-agent/conf.d/prometheus.d/conf.yaml
else	
	echo "${REDIS_CLOUD_CA_CERT}" > /etc/datadog-agent/conf.d/prometheus.d/ca.pem
	echo "    ssl_ca_cert: /etc/datadog-agent/conf.d/prometheus.d/ca.pem" >> /etc/datadog-agent/conf.d/prometheus.d/conf.yaml
fi
echo "    namespace: redise" >> /etc/datadog-agent/conf.d/prometheus.d/conf.yaml
echo "    max_returned_metrics: 2000" >> /etc/datadog-agent/conf.d/prometheus.d/conf.yaml
echo "    metrics:" >> /etc/datadog-agent/conf.d/prometheus.d/conf.yaml

for i in bdb_avg_latency bdb_avg_latency_max bdb_avg_other_latency bdb_avg_read_latency bdb_avg_write_latency bdb_conns bdb_egress_bytes bdb_evicted_objects bdb_expired_objects bdb_fork_cpu_system bdb_ingress_bytes bdb_main_thread_cpu_system bdb_main_thread_cpu_system_max bdb_memory_limit bdb_no_of_keys bdb_other_req bdb_read_req bdb_shard_cpu_system bdb_shard_cpu_system_max bdb_total_req bdb_total_req_max bdb_used_memory bdb_write_req listener_acc_latency listener_conns listener_total_req bdb_crdt_syncer_egress_bytes bdb_crdt_syncer_egress_bytes_decompressed bdb_crdt_syncer_ingress_bytes bdb_crdt_syncer_ingress_bytes_decompressed bdb_crdt_syncer_local_ingress_lag_time bdb_crdt_syncer_pending_local_writes_max bdb_crdt_syncer_pending_local_writes_min bdb_crdt_syncer_status; do
  echo "      - ${i}" >> /etc/datadog-agent/conf.d/prometheus.d/conf.yaml
done

chown dd-agent:dd-agent /etc/datadog-agent/datadog.yaml
chown dd-agent:dd-agent /etc/datadog-agent/conf.d/prometheus.d/conf.yaml

usermod --shell /bin/bash dd-agent
su - dd-agent -c "/opt/datadog-agent/bin/agent/agent run -p /opt/datadog-agent/run/agent.pid"

