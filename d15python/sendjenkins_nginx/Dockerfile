# This dockerfile uses the centos 7 image
# Nginx Dockerfile
# Version 1.0
# Author: Leon xie

# Pull base images.
FROM registry.cloud.jyall.com/centos7:1.0

# Define author info.
MAINTAINER jsjyw-yunjiayuan xie.di@jyall.com

# Add files.
ADD package/nginx-1.10.1.tar.gz /usr/local/src
ADD nginx.conf /date/nginx.conf
ADD mime.types /date/mime.types
ADD uploading_config.py /root/
# Define working directory.
WORKDIR /usr/local/src/nginx-1.10.1

# Install Nginx.
RUN \
	yum install -y  gcc  glibc gcc-c++ pcre-devel make openssl-devel openssl shellinabox && \
	useradd -s /sbin/nologin -M www && \
	./configure --prefix=/usr/local/nginx-1.10.1 --user=www --group=www --with-http_ssl_module  --with-http_gzip_static_module --with-http_stub_status_module && \
	make && \
	make install && \
	ln -s /usr/local/nginx-1.10.1/ /usr/local/nginx 


#ADD config
ADD ./supervisord.conf /etc/supervisord.conf
ADD container-entrypoint /container-entrypoint
RUN chmod +x /container-entrypoint
ADD uploading_pro.py /root/

RUN rm -f /etc/sysconfig/shellinaboxd
COPY package_shellinabox/white-on-black.css /usr/share/shellinabox/white-on-black.css
COPY package_shellinabox/shellinaboxd /etc/sysconfig/shellinaboxd

#give +x
RUN useradd test &&  echo "test:test"|chpasswd

#Env
ENV LANG zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8

# Expose ports.
EXPOSE 80 22 4200

# Define default command.
CMD ["/container-entrypoint"]
