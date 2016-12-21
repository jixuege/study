# Version 3.0.7
# Author: lc

#Base image
FROM template-centos7

RUN yum install -y gcc readline-devel pcre-devel openssl-devel openssl shellinabox

#ADD
ADD  package/openresty-1.9.7.5.tar.gz /usr/local/src
WORKDIR /usr/local/src/openresty-1.9.7.5/
RUN ./configure
RUN make && make install

ADD conf/nginx.conf /usr/local/openresty/nginx/conf/
ADD uploading_pro.py /root/

#give +x
RUN useradd test &&  echo "test:test"|chpasswd
#Env
ENV LANG zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8

#Add config
RUN rm -f /etc/sysconfig/shellinaboxd
COPY package_shellinabox/white-on-black.css /usr/share/shellinabox/white-on-black.css
COPY package_shellinabox/shellinaboxd /etc/sysconfig/shellinaboxd

ADD ./conf/supervisord.conf /etc/supervisord.conf
ADD container-entrypoint /container-entrypoint
RUN chmod +x /container-entrypoint
ADD uploading_pro.py /root/


#Port
EXPOSE 80 22 4200
CMD ["/container-entrypoint"]
