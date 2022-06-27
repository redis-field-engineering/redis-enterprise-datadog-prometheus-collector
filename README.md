# Dockerized Build of Redis Cloud Prometheus Collector

## Prerequisites

1) Datadog API key
```
   Can be obtained from your Datadog account
```

2) Cloud Internal Endpoint
```
   Note: remove the redis-### from the beginning
         it should look like https://internal.blah.us-central1-mz.gcp.cloud.rlrcp.com:8070/metrics
```

## Running the Container

```
docker run --rm -e DATADOG_API_KEY=<DATADOG-API-KEY> -e DATADOG_SITE=datadoghq.com \
	-e REDIS_CLOUD_ENDPOINT_URL=<FQDN:https://internal.blah.us-central1-mz.gcp.cloud.rlrcp.com:8070/metrics> \
	maguec/redisenterprise-dd-prometheus
```

## Running the Container with TLS CA Cert

### Download the CA Cert

```
echo -n "" | openssl s_client -showcerts -servername server -connect internal.blah.us-central1-mz.gcp.cloud.rlrcp.com:8070 > cacert.pem

# Edit the file to only keep what starts with -----BEGIN CERTIFICATE----- and ends with -----END CERTIFICATE-----
```

### Run the container with the cert env var set

```
CA_CERT=$(cat cacert.pem)
docker run --rm -e DATADOG_API_KEY=<DATADOG-API-KEY> -e DATADOG_SITE=datadoghq.com \
	-e REDIS_CLOUD_ENDPOINT_URL=https://mague.demo-azure.redislabs.com:8070/metrics \
	-e REDIS_CLOUD_CA_CERT="${CA_CERT}" \
 	maguec/redisenterprise-dd-prometheus
```

## Building the Container

edit the Makefile and change maguec to your docker prefix

```
make
```

## Support 

Good faith effort support is available to Redis Enterprise licensed customers from field.engineers@redis.com. 
In addition, Community support is available through Github

