FROM	ubuntu:18.04

# Setup the repo and key
RUN 	apt-get update -y && \
	apt-get install -y gnupg2 apt-transport-https software-properties-common && \
	apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 33EE313BAD9589B7 &&\
	add-apt-repository 'deb https://apt.datadoghq.com/ stable 7' &&\
	apt-get update -y && apt-get install -y datadog-agent

COPY 	startup.sh /startup.sh

WORKDIR         /
ENTRYPOINT      [ "/startup.sh" ]

