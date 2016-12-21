# This dockerfile uses the centos 7 image
# Tomcat 7.0.59 Dockerfile
# Version 1.0
# Author: Leon xie

# Pull base images.
FROM registry.cloud.jyall.com/centos7:1.0 

# Define author info.
MAINTAINER jsjyw-yunjiayuan xie.di@jyall.com

#ADD
ADD  package/redis-3.0.3.tar.gz /usr/local/src
WORKDIR /usr/local/src/redis-3.0.3 
RUN mkdir /redis /redis/data /redis/logs /redis/conf
RUN  yum -y install gcc automake autoconf libtool make 
RUN  \ 
	 cd /usr/local/src/redis-3.0.3 && \
	 make   && \
	 make  install 

#RUN 
RUN \
	cp /usr/local/src/redis-3.0.3/redis.conf /redis/conf && \
	cp /usr/local/src/redis-3.0.3/src/redis-cli /redis  && \
	cp /usr/local/src/redis-3.0.3/src/redis-server /redis  && \
	cp /usr/local/src/redis-3.0.3/src/redis-sentinel /redis  && \
	cp /usr/local/src/redis-3.0.3/src/redis-benchmark /redis  && \
	cp /usr/local/src/redis-3.0.3/src/redis-check-aof /redis  && \
	cp /usr/local/src/redis-3.0.3/src/redis-check-dump /redis 

#ADD config
RUN yum -y install shellinabox openssl
RUN useradd test &&  echo "test:test"|chpasswd
ADD ./supervisord.conf /etc/supervisord.conf
ADD container-entrypoint /container-entrypoint
ADD uploading_config.py /root/uploading_config.py
ADD cluster_redis.py /root/cluster_redis.py
RUN chmod +x /root/uploading_config.py
RUN chmod +x /root/cluster_redis.py
RUN chmod +x /container-entrypoint
RUN easy_install argon
RUN easy_install python-consul

RUN rm -f /etc/sysconfig/shellinaboxd
COPY package/cfg.json /root/cfg.json
COPY package/control /root/control
COPY package/white-on-black.css /usr/share/shellinabox/white-on-black.css
COPY package/shellinaboxd /etc/sysconfig/shellinaboxd

#give +x
RUN chmod +x /root/control

#Env
ENV LANG zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8

# Expose ports.
EXPOSE 6379 22 4200

# Define default command.
CMD ["/container-entrypoint"]
ENTRYPOINT [ "sh","-c" ]
