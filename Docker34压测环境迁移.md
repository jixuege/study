# Docker 压测环境迁移

## 具体细节

* 基于模板名称：

template-java8

34网段网桥名为： ovs-docker2 

* 创建脚本

位于/opt/下面
<pre>
# more  touch_34.sh 
for i in {1..180}
do
docker run -d -it --net=none -h java34-$i  -m 2048m --name java34-$i -v /docker-data/works/data34-$i:/data/server -v /docker-data/logs/data34-$i:/data/logs  template-
java8 /usr/sbin/sshd -D
pipework ovs-docker2 java34-$i 10.10.34.$i/19@10.10.32.254
done

</pre>

执行ping命令

<pre>

# more ping.sh 
for n in {1..180}
    do
docker exec java34-$n ping -c 2 10.10.32.254
	done

</pre>

* 删除一下ovs错误的port

<pre>

for i in $(ovs-vsctl show|grep error|awk -F ' ' '{print $7}') ; do ovs-vsctl del-port ovs-docker2 $i; done

</pre>

