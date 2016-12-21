# This dockerfile uses the centos 7 image
# Gw  Dockerfile for mount
# Version 1.0
# Author: Leon xie

# Pull base images.
FROM gw-server20160922 

# Define author info.
MAINTAINER jsjyw-yunjiayuan xie.di@jyall.com

#Install openvpn and iptables
#RUN yum install openvpn easy-rsa -y
#RUN yum install iptables-services -y

#ADD
RUN mkdir /pyscript/
ADD ./supervisord.conf /etc/supervisord.conf
ADD container-entrypoint /container-entrypoint
ADD conf/* /pyscript/
RUN chmod +x /pyscript/create_openvpn_and_nginx.py 
RUN chmod +x  /container-entrypoint

ADD package/MarkupSafe-0.23.tar.gz /pyscript
ADD package/Jinja2-2.8.tar.gz /pyscript
ADD package/setuptools-28.6.1.tar.gz /pyscript

RUN yum -y install python-devel 
#RUN curl https://bootstrap.pypa.io/get-pip.py | python
RUN cd /pyscript/setuptools-28.6.1 && python setup.py install
RUN cd /pyscript/MarkupSafe-0.23 && python setup.py install 
RUN cd /pyscript/Jinja2-2.8 && python setup.py install

#ADD
RUN yum -y install shellinabox supervisor nginx
ADD ./supervisord.conf /etc/supervisord.conf


RUN rm -f /etc/sysconfig/shellinaboxd
RUN echo "root:root123"|chpasswd
RUN useradd test &&  echo "test:test"|chpasswd
COPY package/white-on-black.css /usr/share/shellinabox/white-on-black.css
COPY package/shellinaboxd /etc/sysconfig/shellinaboxd
COPY package/server.conf /etc/openvpn/
COPY package/openssl-1.0.0.cnf /etc/openvpn/easy-rsa/2.0/openssl-1.0.0.cnf

#for openvpn
RUN mkdir -p /dev/net/ && \
    mknod /dev/net/tun c 10 200 && \
    chmod 600 /dev/net/tun

#Env
ENV LANG zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8

#Define default command.
CMD ["/container-entrypoint"]
