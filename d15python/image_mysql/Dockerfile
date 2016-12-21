# This dockerfile uses the centos 7 image
# Mariadb  Dockerfile
# Version 1.0
# Author: Leon xie

#Pull base images.
FROM template-centos7

#Define author info.
MAINTAINER jsjyw-yunjiayuan xie.di@jyall.com

#Commands
ADD ./supervisord.conf /etc/supervisord.conf

#Clean cache
RUN yum clean all
# Install mariadb
  #yum -y update; yum clean all && \
RUN  yum -y install mariadb-server mariadb 

#Install shellinabox
RUN  yum -y install shellinabox openssl 

#Add user for shellbox
RUN useradd test &&  echo "test:test"|chpasswd
# Define working directory.
WORKDIR /data

#Commands
RUN mysql_install_db --user=mysql --ldata=/var/lib/mysql/ > /dev/null 2>&1

# Yum ext4
RUN yum -y install e2fsprogs
RUN easy_install argon
RUN easy_install python-consul

#Run mysql
RUN /usr/libexec/mysqld --user=mysql >/dev/null 2>&1 &\
    sleep 5s &&\
    echo "GRANT ALL ON *.* TO  'admin'@'localhost' IDENTIFIED BY 'admin';GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' IDENTIFIED BY 'admin' WITH GRANT OPTION;FLUSH PRIVILEGES" | mysql

#ADD config
ADD ./supervisord.conf /etc/supervisord.conf
ADD container-entrypoint /container-entrypoint
ADD uploading_config.py /root/uploading_config.py
ADD cluster_mysql.py /root/cluster_mysql.py
RUN chmod +x /root/uploading_config.py
RUN chmod +x /root/cluster_mysql.py
RUN chmod +x /container-entrypoint

RUN rm -f /etc/sysconfig/shellinaboxd
COPY package/white-on-black.css /usr/share/shellinabox/white-on-black.css
COPY package/shellinaboxd /etc/sysconfig/shellinaboxd

#Env
ENV LANG zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8

# Expose ports.
EXPOSE 3306 22 4200

# Define default command.
CMD ["/container-entrypoint"]
