# Dockerized Build of Redis Cloud Prometheus Collector

## Building the Container

edit the Makefile and change maguec to your docker prefix

```
make
```

## Prerequisites

1) Datadog API key
   Can be obtained from your Datadog account

2) Cloud Internal Endpoint
   Note: remove the redis-### from the beginning
         it should look like https://internal.blah.us-central1-mz.gcp.cloud.rlrcp.com:8070/metrics

## Running the Container

```
docker run --rm -e DATADOG_API_KEY=<DATADOG-API-KEY> -e DATADOG_SITE=datadoghq.com \
	-e REDIS_CLOUD_ENDPOINT_URL=<FQDN:https://internal.blah.us-central1-mz.gcp.cloud.rlrcp.com:8070/metrics> \
	maguec/redisenterprise-dd-prometheus
```

## Support 

Please contact your friendly Solutions Architect for support