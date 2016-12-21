# This dockerfile uses the centos 7 image
# Python 2.7 Dockerfile for mount
# Version 1.0
# Author: Leon xie

# Pull base images.
FROM centos

# Define author info.
MAINTAINER jsjyw-yunjiayuan xie.di@jyall.com

#Commands
RUN \
        yum -y install  wget vim tree lsof net-tools openssh-server passwd unzip  && \
	echo "root:shellboxuser"|chpasswd  &&  \
	useradd shellboxuser && \
        echo "shellboxuser:shellboxuser" | chpasswd && \
	mkdir /var/run/sshd && \
	ssh-keygen -q -t rsa -b 2048 -f /etc/ssh/ssh_host_rsa_key -N '' && \
	ssh-keygen -q -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key -N '' && \
	ssh-keygen -q -t ecdsa -f /etc/ssh/ssh_host_ed25519_key -N '' && \
	mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak && \
        wget -O /etc/yum.repos.d/CentOS-Base.repo  http://mirrors.aliyun.com/repo/Centos-7.repo && \	
	wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo && \
  	\cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \ 
	yum -y install supervisor shellinabox openssl e2fsprogs 

RUN yum -y install  java

#ADD
ADD ./supervisord.conf /etc/supervisord.conf
ADD container-entrypoint /container-entrypoint
ADD uploading_config.py /root/uploading_config.py
RUN chmod +x  /container-entrypoint
RUN chmod +x /root/uploading_config.py

RUN rm -f /etc/sysconfig/shellinaboxd
COPY package/cfg.json /root/cfg.json
COPY package/control /root/control
COPY package/white-on-black.css /usr/share/shellinabox/white-on-black.css
COPY package/shellinaboxd /etc/sysconfig/shellinaboxd

#Give +x
RUN chmod +x /root/control
RUN useradd test &&  echo "test:test"|chpasswd

#Env
ENV LANG zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8



# Define default port.
EXPOSE 22 4200 80

#Define default command.
CMD ["/container-entrypoint"]

