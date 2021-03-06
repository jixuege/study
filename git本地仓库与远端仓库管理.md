#Git 使用

## linux 服务器创建本地仓库

* 登录一台Linux服务器，建立目录

* 初始化仓库
* 创建公私钥
* 拷贝公钥到github的 右上角头像--setting--SSH and GPG keys--New SSH key
* 在本地仓库克隆需要仓库地址（地址在点开仓库右边有个Clone or download）

具体操作如下
<pre>
mkdir /xiedi
cd /xiedi
git init
ssh-keygen -t rsa -C "linux_xd@sina.com"
cat .ssh/id_rsa.pub
复制到github 的pub key 即可

</pre>


## git远程仓库和本地仓库使用

* 拉仓库下来

找到仓库名，进去，查看右边的clone or download ，点开，选择Use SSH,这样会拿到一个地址git@github.com:jixuege/study.git，使用命令把这个仓库拉下来
<pre>
git clone git@github.com:jixuege/study.git
</pre>

* 推文件上去

在D盘的github文件夹下的study文件夹，打开Git bash here ，使用下面命令推文件上去
<pre>
git add *
git commit -m "second push"
git push origin master
</pre>

##
##解决多个ssh  key 的问题
有的时候，不仅github使用ssh key，工作项目或者其他云平台也需要使用ssh key来认证，如果每次都覆盖了原来的id_rsa文件，那么之前的认证就会失效。这个问题我们可以通过在~/.ssh目录下增加 config文件来解决。

配置如下：

<pre>
$ ssh-keygen -t rsa -f ~/.ssh/id_rsa.jyall -C "xie.di@jyall.com"

</pre>

上面的id_rsa.jyall就是我们指定的文件名，这时 ~/.ssh目录下会多出id_rsa.jyall 和id_rsa.jyall.pub这两个文件，id_rsa.jyall.pub里保存的就是我们要使用的key。

这里有个地方需要注意的是，需要在~/.ssh下面新增并配置config 文件

下面是我添加到gitlab 的配置，添加到存放 key的目录下，下面是config里面的内容
<pre>
[root@node3-docker20-206 .ssh]# cat config 
Host *.jyall.com 
    IdentityFile ~/.ssh/id_rsa.jyall
    User xie.di

</pre>
>第一行，指的是gitlib项目里面的地址，我的项目名称地址为：git@gitlab.jyall.com:cloud/bs_jyall_dockerFile.git
>所以我写成上面格式，接下来就是制定你的公钥的名称，然后就是用户名

接下来就是上传key到云平台，然后就是测试ssh key 是否配置成功。
以下是我的测试
<pre>
[root@node3-docker20-206 .ssh]# ssh -T git@gitlab.jyall.com
Welcome to GitLab, xiedi!

</pre>
完美解决这个头疼的问题。

感谢作者，参考地方[git生成ssh key及本地解决多个ssh key问题](http://riny.net/2014/git-ssh-key/)