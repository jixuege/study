# This dockerfile uses the centos 7 image
# Python 2.7 Dockerfile for mount
# Version 1.0
# Author: Leon xie

# Pull base images.
FROM centos

# Define author info.
MAINTAINER jsjyw-yunjiayuan xie.di@jyall.com

#Commands
RUN  yum -y install  wget vim tree lsof net-tools openssh-server passwd unzip
RUN  ssh-keygen -q -t rsa -b 2048 -f /etc/ssh/ssh_host_rsa_key -N ''
RUN  ssh-keygen -q -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key -N ''
RUN  ssh-keygen -q -t ecdsa -f /etc/ssh/ssh_host_ed25519_key -N ''
RUN  mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak
RUN  wget -O /etc/yum.repos.d/CentOS-Base.repo  http://mirrors.aliyun.com/repo/Centos-7.repo
RUN  wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
RUN  cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN  yum -y install supervisor shellinabox openssl e2fsprogs 
RUN  yum -y install  java

#ADD
ADD ./supervisord.conf /etc/supervisord.conf
ADD container-entrypoint /container-entrypoint
ADD uploading_config.py /root/uploading_config.py
RUN chmod +x  /container-entrypoint
RUN chmod +x /root/uploading_config.py

RUN rm -f /etc/sysconfig/shellinaboxd
COPY package/white-on-black.css /usr/share/shellinabox/white-on-black.css
COPY package/shellinaboxd /etc/sysconfig/shellinaboxd

#Give +x
RUN useradd test &&  echo "test:test"|chpasswd
RUN  echo "root:root123"|chpasswd 
RUN mkdir /data/server -p
RUN yum install git -y
#Env
#ENV LANG zh_CN.UTF-8
#ENV LC_ALL zh_CN.UTF-8
RUN yum install lrzsz openssh-clients -y


# Define default port.
EXPOSE 22 4200 80

#Define default command.
CMD ["/container-entrypoint"]

