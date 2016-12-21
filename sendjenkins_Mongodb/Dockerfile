# This dockerfile uses the centos 7 image
# Tomcat 7.0.59 Dockerfile
# Version 1.0
# Author: Leon xie

# Pull base images.
FROM template-centos7

# Define author info.
MAINTAINER jsjyw-yunjiayuan xie.di@jyall.com


#Add repo
ADD mongodb-org-3.2.repo /etc/yum.repos.d/mongodb-org-3.2.repo
RUN yum -y update; yum clean all
RUN yum -y install epel-release; yum clean all
RUN yum -y install mongodb-org mongodb-org-server
RUN yum -y install shellinabox openssl
RUN mkdir -p /data/db
RUN easy_install argon python-consul

#ADD config

ADD ./supervisord.conf /etc/supervisord.conf
ADD uploading_config.py /root/uploading_config.py
ADD cluster_mongo.py /root/cluster_mongo.py
ADD container-entrypoint /container-entrypoint
RUN chmod +x /root/uploading_config.py
RUN chmod +x /root/cluster_mongo.py
RUN chmod +x /container-entrypoint

RUN rm -f /etc/sysconfig/shellinaboxd
COPY package/white-on-black.css /usr/share/shellinabox/white-on-black.css
COPY package/shellinaboxd /etc/sysconfig/shellinaboxd
RUN useradd test &&  echo "test:test"|chpasswd


#Env
ENV LANG zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8


# Define ports.
EXPOSE 27017 22 4200

# Define default command.
CMD ["/container-entrypoint"]

