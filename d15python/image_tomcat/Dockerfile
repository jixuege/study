# This dockerfile uses the centos 7 image
# Tomcat 7.0.59 Dockerfile
# Version 1.0
# Author: Leon xie

# Pull base images.
FROM template-centos7

# Define author info.
MAINTAINER jsjyw-yunjiayuan xie.di@jyall.com

# ADD files.
ADD  package/jdk-7u79-linux-x64.tar.gz /usr/local/src
ADD  package/apache-tomcat-7.0.59.tar.gz /usr/local/src
ADD ./supervisord.conf /etc/supervisord.conf

# Install jdk adn tomcat.
RUN \
	mv /usr/local/src/jdk1.7.0_79 /usr/local/jdk && \
	chown -R root:root /usr/local/jdk && \
	mv /usr/local/src/apache-tomcat-7.0.59 /tomcat && \
	chown -R root:root /tomcat
	
# Define environment variables.
ENV JAVA_HOME=/usr/local/jdk
ENV PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH
ENV CLASSPATH=.$CLASSPATH:$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$JAVA_HOME/lib/tools.jar
ENV TOMCAT_HOME=/tomcat
	

#Define working directory.
WORKDIR /tomcat/data

# Yum ext4
RUN yum -y install e2fsprogs

#ADD config
RUN yum -y install shellinabox openssl
RUN useradd test &&  echo "test:test"|chpasswd
ADD ./supervisord.conf /etc/supervisord.conf
ADD container-entrypoint /container-entrypoint
ADD uploading_config.py /root/uploading_config.py
RUN chmod +x /container-entrypoint
ADD uploading_pro.py /root/

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
EXPOSE 8080 22 4200

# Define default command.
CMD ["/container-entrypoint"]

