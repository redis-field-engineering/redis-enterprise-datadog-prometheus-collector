echo "api_key: ${DATADOG_API_KEY}" > /etc/datadog-agent/datadog.yaml
echo "site: ${DATADOG_SITE}" >> /etc/datadog-agent/datadog.yaml
echo "${REDIS_CLOUD_CA_CERT}" > /etc/datadog-agent/conf.d/prometheus.d/ca.pem

python3 datadog_config.py

chown dd-agent:dd-agent /etc/datadog-agent/datadog.yaml
chown dd-agent:dd-agent /etc/datadog-agent/conf.d/prometheus.d/conf.yaml

usermod --shell /bin/bash dd-agent
exec su - dd-agent -c "/opt/datadog-agent/bin/agent/agent run -p /opt/datadog-agent/run/agent.pid"
