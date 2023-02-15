#################################################
default:	docker

docker:
	docker build . -t fieldengineering/redis-cloud-datadog

push:
	docker buildx build \
		--platform linux/amd64 \
		--push \
		-t fieldengineering/redis-cloud-datadog:latest .

