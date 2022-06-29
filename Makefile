#################################################
default:	docker

docker:
	docker build -t redislabs/redisenterprise-rs-hostedcloud .
