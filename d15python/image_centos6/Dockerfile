# This dockerfile uses the centos 7 image
# Python 2.7 Dockerfile for mount
# Version 1.0
# Author: Leon xie

# Pull base images.
FROM registry50.jyall.com/jsjyw/init/centos:6.6 

# Define author info.
MAINTAINER jsjyw-yunjiayuan xie.di@jyall.com


#ADD
ADD container-entrypoint /container-entrypoint
ADD uploading_config.py /uploading_config.py
RUN chmod +x  /container-entrypoint
RUN chmod +x  /uploading_config.py

RUN \
        yum -y install  wget vim tree lsof net-tools openssh-server  openssh-clients passwd unzip  && \
        \cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN yum -y install wget
RUN mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak && \
        wget -O /etc/yum.repos.d/CentOS-Base.repo  http://mirrors.aliyun.com/repo/Centos-6.repo && \
        wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-6.repo && \

        yum -y install supervisor shellinabox openssl
#ADD
ADD ./supervisord.conf /etc/supervisord.conf

RUN 	echo "root:root123"|chpasswd 


#yum pakege
RUN yum -y install vim tree lsof net-tools passwd unzip git

# Define default port.
EXPOSE 22 4200 80

#Define default command.
CMD ["/container-entrypoint"]
