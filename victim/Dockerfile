FROM ubuntu:18.04
ADD victim.sh /root/
RUN apt-get update && apt-get install -y iputils-ping net-tools iproute2 bash \
	dnsutils openssl wget

CMD ["/bin/bash"]
