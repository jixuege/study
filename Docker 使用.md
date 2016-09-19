#Docker
###2016-9-20
##Docker 使用

###网络
默认情况下启动一个容器，它会自动获取一个跟docker0同网段的IP，而且重启container之后其IP一般会发生变化，但有时候我们需要一个固定的IP。

docker run 启动一个容器的命令有一个--net参数来指定容器网络类型。

举例：

<pre>
docker run -i -t --rm --net='none' centos /bin/bash
root@db84e747c362:/# ifconfig -a
lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
</pre>

