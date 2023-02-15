#!/bin/bash

if [ "${REDIS_CLOUD_API_ACCOUNT_KEY}X" == "X" ]; then
	exec python3 /cloud-api-exporter/app.py -e ${REDIS_CLOUD_PRIVATE_ENDPOINT}
else
	exec python3 /cloud-api-exporter/app.py -a ${REDIS_CLOUD_API_ACCOUNT_KEY} -u ${REDIS_CLOUD_API_SECRET} -e ${REDIS_CLOUD_PRIVATE_ENDPOINT}
fi
