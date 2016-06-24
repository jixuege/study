# screen 用法

一般情况，如果我们需要运行一个命令很长时间，会使用nohup来进行，格式如下：

nohup command  argument  &

但是呢，有点太简陋，我们必须使用强大的实用程序screen来进行。

安装方法，很简单，直接yum即可

<pre>
# rpm -qa|grep screen
screen-4.1.0-0.23.20120314git3c2946.el7_2.x86_64
#yum install screen -y
</pre>

简单来说，screen是一个可以在多个进程之间多路复用一个物理终端的窗口管理器。screen中有会话的概念，用户可以在一个screen会话中创建多个screen窗口，在每一个screen窗口中就想操作一个真实的Telnet/SSH连接窗口那样。在screen中创建一个新的窗口有这样几个方式。

1. 直接在命令行键入screen命令<pre>screen</pre>
> screen 将创建一个执行shell的全屏窗口，你可以执行任意shell程序，就像在ssh窗口中那样。在该窗口中键入exit退出该窗口，如果这是该screen会话的唯一窗口，该screen会话退出，否则screen自动切换到前一个窗口。

-- 

2. 


##基本使用

* 如果会话处于detached状态，使用命令screen -r pid 可以重新连上：

<pre>
[root@node4-docker20-207 ~]# screen -ls
There are screens on:
	23123.test1	(Detached)
	23095.screen_session_name	(Dead ???)
	23023.pts-4.node4-docker20-207	(Detached)
	22998.pts-14.node4-docker20-207	(Detached)
Remove dead screens with 'screen -wipe'.
4 Sockets in /var/run/screen/S-root.

[root@node4-docker20-207 ~]# screen -r test1
[root@node4-docker20-207 opt]# screen -list
There are screens on:
        23123.test1     (Attached)

</pre>

* 如果有一个会话死掉，可以用screen -wipe命令来清楚该会话：

<pre>
[root@node4-docker20-207 opt]# screen -list
There are screens on:
        23123.test1     (Attached)
        23095.screen_session_name       (Dead ???)
        23023.pts-4.node4-docker20-207  (Detached)
        22998.pts-14.node4-docker20-207 (Detached)
Remove dead screens with 'screen -wipe'.
4 Sockets in /var/run/screen/S-root.

[root@node4-docker20-207 opt]# screen -wipe
There are screens on:
        23123.test1     (Attached)
        23095.screen_session_name       (Removed)
        23023.pts-4.node4-docker20-207  (Detached)
        22998.pts-14.node4-docker20-207 (Detached)


</pre>

