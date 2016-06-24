# Docker环境初始化流程

## Docker  服务安装

* 最简单的安装，但是不会是最新版本

<pre>

yum install docker -y

</pre>

> 如果对这个版本不满意，可以使用下面方法卸载，然后重新安装自己想要的版本

<pre>

yum list installed |grep docker
yum -y remove docker.x86_64
rm -rf /var/lib/docker/

</pre>

> 官网卸载方法
<pre>

#yum list installed | grep docker
docker-engine.x86_64   1.7.1-1.el7 @/docker-engine-1.7.1-1.el7.x86_64.rpm

#yum -y remove docker-engine.x86_64
#rm -rf /var/lib/docker

</pre>





* 如果想安装最新版本

<pre>

yum -y update
curl -sSL https://get.docker.com/ | sh
yum install -y docker-selinux
systemctl start docker

</pre>

> 官方安装方法

<pre>
$ sudo yum update
$ curl -fsSL https://get.docker.com/ | sh
$ sudo service docker start

</pre>

* 直接添加docker.repo来进行安装

<pre>

cat >/etc/yum.repos.d/docker.repo <<-EOF
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF

yum install -y docker-engine
systemctl start docker

</pre>


## 给容器更大的空间

<pre>
mkdir /data/devicemapper
 touch /data/devicemapper/data
 dd if=/dev/zero of=/data/devicemapper/data bs=1G count=0 seek=1000
systemctl stop docker
rm -rf /var/lib/docker/*
mkdir -p /var/lib/docker/devicemapper/devicemapper/

ln -s /data/devicemapper/data  /var/lib/docker/devicemapper/devicemapper/data

 systemctl start docker

</pre>

> 给docker 1个T的空间，使用命令docker info即可查看是否生效。


## 修改配置文件

* 消除创建容器时的警告语句 “Usage of loopback devices is strongly discouraged for production use.”

<pre>

 sed -i 's@DOCKER_STORAGE_OPTIONS=@DOCKER_STORAGE_OPTIONS=--storage-opt dm.no_warn_on_loop_devices=true @g' /etc/sysconfig/docker-storage

systemctl restart docker


</pre>

* docker 的配置文件/etc/sysconfig/docker也需要修改

> 指定镜像仓库地址，这个地方需要进行仓库的域名与DNS的解析动作。

例如：
<pre >

OPTIONS='--selinux-enabled  --insecure-registry registry.cloud.jyall.com  --insecure-registry  -H tcp://0.0.0.0:5555 -H unix://var/run/docker.sock'
需要注意的是，不在允许IP出现在配置文件中，一切都是域名，通过DNS来进行解析
或者，直接追加进去：
echo "OPTIONS='--selinux-enabled  --insecure-registry registry.cloud.jyall.com  --insecure-registry  -H tcp://0.0.0.0:5555 -H unix://var/run/docker.sock'" >>/etc/sysconfig/docker
重启服务
systemctl restart docker


</pre>

* 添加命令补全（最小化安装的时候默认没有补全）

</pre>

yum install -y bash-completion

</pre>


* 拉取官方镜像，直接从本地拉取即可，位置：2016空杯心态

