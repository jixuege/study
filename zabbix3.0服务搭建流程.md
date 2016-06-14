#CentOS 7 安装zabbix 3.0

##快速安装
*  添加可以安装zabbix3.0的 yum源，一条命令即可。
<pre>
[root@linux-node1 ~]# rpm -ivh http://mirrors.aliyun.com/zabbix/zabbix/3.0/rhel/7/x86_64/zabbix-release-3.0-1.el7.noarch.rpm

</pre>

* 安装相关软件，这里我要对自身也做一个监控
<pre>
[root@linux-node1 ~]# yum install zabbix-server zabbix-web zabbix-server-mysql zabbix-web-mysql mariadb-server mariadb zabbix-agent  -y

</pre>

* 修改时区为亚洲上海
<pre>
[root@linux-node1 ~]# sed -i 's@# php_value date.timezone Europe/Riga@php_value date.timezone Asia/Shanghai@g' /etc/httpd/conf.d/zabbix.conf
</pre>

* 启动数据库

<pre>
[root@linux-node1 ~]# systemctl status mariadb
</pre>

* 创建zabbix所需用的用户和数据库

<pre>
mysql
create database zabbix character set utf8 collate utf8_bin;
grant all on zabbix.* to zabbix@'localhost' identified by 'jixuege';
exit
cd /usr/share/doc/zabbix-server-mysql-3.0.3
zcat create.sql.gz |mysql -uzabbix -pjixuege zabbix
</pre>

* 修改zabbix的配置

<pre>
# vim /etc/zabbix/zabbix_server.conf
DBHost=localhost    #数据库所在主机
DBName=zabbix       #数据库名 
DBUser=zabbix       #数据库用户 
DBPassword=jixuege   #数据库密码 
</pre>

* 修改本地agent 的server服务
<pre>
# vim /etc/zabbix/zabbix_agentd.conf
Server=192.168.56.11
</pre>

* 启动服务
<pre>
# systemctl start zabbix-server
# systemctl start zabbix-agent
# systemctl start httpd
</pre>

* IE登录配置: [ip/zabbix](http://192.168.56.11/zabbix/)

登录初始用户和密码分别为：Admin  zabbix

![图片](file:///D:\github\study\1.PNG)
