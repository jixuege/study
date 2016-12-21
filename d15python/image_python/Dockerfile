# This dockerfile uses the centos 7 image
# Python 2.7 Dockerfile for mount
# Version 1.0
# Author: Leon xie

# Pull base images.
FROM centos

# Define author info.
MAINTAINER jsjyw-yunjiayuan xie.di@jyall.com


#ADD
ADD ./supervisord.conf /etc/supervisord.conf
ADD container-entrypoint /container-entrypoint
ADD uploading_config.py /uploading_config.py
RUN chmod +x  /container-entrypoint
RUN chmod +x  /uploading_config.py


RUN yum -y install wget
RUN mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak && \
        wget -O /etc/yum.repos.d/CentOS-Base.repo  http://mirrors.aliyun.com/repo/Centos-7.repo && \
        wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo

#ADD
RUN yum -y install shellinabox supervisor
ADD ./supervisord.conf /etc/supervisord.conf


RUN rm -f /etc/sysconfig/shellinaboxd
RUN useradd test &&  echo "test:test"|chpasswd
COPY package/cfg.json /root/cfg.json
COPY package/control /root/control
COPY package/white-on-black.css /usr/share/shellinabox/white-on-black.css
COPY package/shellinaboxd /etc/sysconfig/shellinaboxd

#give +x
RUN chmod +x /root/control

#yum pakege
RUN yum -y install vim tree lsof net-tools passwd unzip
#Env
ENV LANG zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8


# Define default port.
EXPOSE 22 4200 80

#Define default command.
CMD ["/container-entrypoint"]
