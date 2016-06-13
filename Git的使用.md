#Git
>我只是为了练习Markdown语法而已。

##Git简介

* git是什么？

git是目前为止，全宇宙最先进的分布式版本控制系统，记住，没有之一。

*  git有哪些特点？

简单来讲就是高端大气上档次

* 什么是版本控制系统？

打个比方，比如，我平时习惯使用word来记录文档知识库体系，有时候同一件事情，可能我会有多个word文档，因为要不停的修改，但是呢，又怕哪一天要找回。过了一段时间，你如果想找回你的某一个版本，就需要自己一个一个文件去找，麻烦不？
看着一堆文件，又想保留最新一个，然后把其他删除，但是又怕哪天又会用上，还不敢删，蛋疼吧！！
还有就是你同事如果好心帮你改动了某个地方，你觉得你会发现么？
SO，它来了
终于结束了手动管理多个版本的时代，进入到版本控制的20世纪。

## git的诞生

by Linus

##git的安装

可以安装在Linus，Windows，Unix，Mac这几大平台

1. 在Linux上安装Git

尝试输入git ，看看系统有没有安装
<pre>
[root@59abe0c54a80 /]# git
bash: git: command not found
</pre>
提示没有命令，需要安装，安装如下
<pre>
yum install git -y
</pre>

2. 在Windows上安装

从[git](https://git-for-windows.github.io)下载，如果你网速慢可以到这里下载[百度云盘](http://pan.baidu.com/s/1skFLrMt#path=%252Fpub%252Fgit)，然后安装默认选项安装即可。

安装完成以后，在开始菜单里找到"Git"->"Git Bash", 蹦出一个命令框的东西，说明安装成功。
安装完成之后，还需要最后一步设置，在命令行输入：
<pre>
git config --global user.name "Your Name"
git config --global user.email "email@example.com"
</pre>

因为Git是分布式版本控制系统，所以，每个机器都必须自保家门：你的名字和Email地址。

注意git config 命令的--global 参数，用了这个参数，表示你这台机器上所有的Git仓库都会使用这个配置，当然也可以对某个仓库指定不同的用户名和Email地址。


##创建版本库

什么是版本库？版本库又名仓库，英文名repository，你可以简单理解成一个目录，这个目录里面的所有文件都可以被Git管理起来，每个文件的修改，删除，Git都能跟踪，以便任何时刻都可以追踪历史，或者在将来某个时刻可以"还原"。

所以创建一个版本库非常简单

**第一步：**

首先，选择一个合适的地方，创建一个空目录：
我选择在我的测试机上执行10.10.20.207
<pre>
[root@node4-docker20-207 ~]# mkdir learngit
[root@node4-docker20-207 ~]# cd learngit/
[root@node4-docker20-207 learngit]# pwd
/root/learngit
</pre>

上面是我在Linux服务器上创建的仓库，位置位于我根目录下/root/learngit

**第二步**

通过git init命令把这个目录变成Git可以管理的仓库：
<pre>
[root@node4-docker20-207 learngit]# pwd
/root/learngit
[root@node4-docker20-207 learngit]# ll
总用量 0
[root@node4-docker20-207 learngit]# git init
初始化空的 Git 版本库于 /root/learngit/.git/
</pre>

瞬间Git就把仓库建立好了，而且告诉你是一个空的仓库，发现没有，多了一个.git目录，这个目录是Git来跟踪管理版本库的，没特殊需求，不要更改这个目录里文件。
>注意，不是说必须要是一个空目录，可以选择一个已经有东西的目录来进行创建git仓库。

##把文件添加到版本库

我在仓库里，编写一个readme.txt文件，内容如下：
<pre>
[root@node4-docker20-207 learngit]# pwd
/root/learngit
[root@node4-docker20-207 learngit]# more readme.txt 
Git is a version control system.
Git is free software.

</pre>

>注意，一定要放在learngit目录下（子目录也行），因为这是一个Git仓库，放在其他地方Git再厉害也找不到这个文件。

**和把大象放到冰箱需要3步比起来，把一个文件放到Git仓库只需要两步**

第一步：用命令 git add 告诉Git，把文件添加到仓库
<pre>
[root@node4-docker20-207 learngit]# ll
总用量 4
-rw-r--r-- 1 root root 55 6月  12 16:31 readme.txt
[root@node4-docker20-207 learngit]# git add readme.txt 
</pre>

执行上面命令，没有任何显示，这就对了，Unix的哲学是"没有消息就是好消息"，说明添加成功。

第二步： 用命令 git commit 告诉 Git，把文件提交到仓库：

<pre>
[root@node4-docker20-207 learngit]# git commit -m "wrote a readme file"

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity.
Omit --global to set the identity only in this repository.

fatal: unable to auto-detect email address (got 'root@node4-docker20-207.(none)')

很明显，它提示我不知道我是谁，需要我Run下面的命令，我很听话的
[root@node4-docker20-207 learngit]# git config --global user.email "linux_xd@sina.com"
[root@node4-docker20-207 learngit]# git config --global user.name  "xie di"

然后我再次提交到仓库
[root@node4-docker20-207 learngit]# git commit -m "wrote a readme file"
[master（根提交） 0811670] wrote a readme file
 1 file changed, 2 insertions(+)
 create mode 100644 readme.txt

</pre>

>简单说明一下：git commit 命令，-m后面输入的是本次提交的说明，可以输入任意内容，当然最好是有意义的，这样你就能从历史记录里方便找到改动的记录。

git commit  命令执行成功后会告诉你，1个文件被改动（我们新添加的readme.txt文件），插入了两行内容（readme.txt 有两行内容）。

为什么Git添加文件需要add ，commit 一共两步呢？
因为commit 可以一次提交很多文件，所以你可以多次add不同的文件，比如：
<pre>
git add file1.txt
git add file2.txt file3.txt
git commit -m "add 3 files"
</pre>

**小结**

1. 初始化一个Git仓库，使用  git init  命令
2. 添加文件到Git仓库，需要两步：

* 第一步：使用命令  git add  file 。
>注意可反复多次使用，添加多个文件。

* 第二步： 使用命令 git commit -m "描述" ，完成。
>尽量写描述，这样可以清晰记录修改的过程


##

##时光机穿梭

我们已经成功的添加了并提交了一个readme.txt文件，现在，是时候继续工作了，于是，我们继续修改readme.txt文件，改成如下内容：
<pre>
[root@node4-docker20-207 learngit]# cat readme.txt 
Git is a distributed version control system.
Git is free software.
[root@node4-docker20-207 learngit]# git status
# 位于分支 master
# 尚未暂存以备提交的变更：
#   （使用 "git add <file>..." 更新要提交的内容）
#   （使用 "git checkout -- <file>..." 丢弃工作区的改动）
#
#	修改：      readme.txt
#
修改尚未加入提交（使用 "git add" 和/或 "git commit -a"）
</pre>

>很明显 ，gitstatus可以让我们时刻仓库仓库当前的状态，上面的命令告诉我们，readme.txt 被修改过了，但还没有准备提交的修改。

虽然Git告诉我们readme.txt被修改了，但如果能看看具体修改了什么内容，自然是很好的。比如你休假回来，第一天上班，已经记不清上传怎么修改的readme.txt，所以需要用git diff 这个命令看看
<pre>
[root@node4-docker20-207 learngit]# git diff
diff --git a/readme.txt b/readme.txt
index 46d49bf..9247db6 100644
--- a/readme.txt
+++ b/readme.txt
@@ -1,2 +1,2 @@
-Git is a version control system.
+Git is a distributed version control system.
 Git is free software.

</pre>

>git diff 顾名思义就是查看different，显示的格式正式Unix通用的diff格式，可以从上面的命令输出看到，我们在第一行添加了一个单词

知道了对readme.txt做了什么修改后，再把它提交到仓库就放心多了，提交修改和提交新文件操作是一样的，也是两步，第一步 git add：

<pre>
[root@node4-docker20-207 learngit]# git add readme.txt 
没有输出，执行第二步  git commit 之前，我们在运行git status 来查看当前仓库的状态
[root@node4-docker20-207 learngit]# git status
# 位于分支 master
# 要提交的变更：
#   （使用 "git reset HEAD <file>..." 撤出暂存区）
#
#	修改：      readme.txt
#

git status 告诉我们，将要被提交的修改包括readme.txt ，下一步就可以放心提交了
[root@node4-docker20-207 learngit]# git commit -m "add distributed"
[master f8b9e3e] add distributed
 1 file changed, 1 insertion(+), 1 deletion(-)
提交后，我们在用 git status  命令来查看仓库的当前状态
[root@node4-docker20-207 learngit]# git status
# 位于分支 master
无文件要提交，干净的工作区

git 告诉我们当前灭有需要提交的修改，而且，工作目录是干净的。

</pre>

**小结**
1. 要随时掌握工作区的状态，就需要使用 git status 命令
2. 如果 git  status 告诉你有文件被修改过，用   git diff 就可以查看修改的内容。

##

##版本回退
现在呢，我已经学会了修改文件，然后把修改后的提交到Git版本库，现在，在练习一次，修改readme.txt文件如下：

<pre>
[root@node4-docker20-207 learngit]# cat readme.txt 
Git is a distributed version control system.
Git is free software distributed under the GPL .

我查看一下当前状态
[root@node4-docker20-207 learngit]# git status
# 位于分支 master
# 尚未暂存以备提交的变更：
#   （使用 "git add <file>..." 更新要提交的内容）
#   （使用 "git checkout -- <file>..." 丢弃工作区的改动）
#
#	修改：      readme.txt
#
修改尚未加入提交（使用 "git add" 和/或 "git commit -a"）

查看具体修改了什么
[root@node4-docker20-207 learngit]# git diff
diff --git a/readme.txt b/readme.txt
index 9247db6..124646b 100644
--- a/readme.txt
+++ b/readme.txt
@@ -1,2 +1,2 @@
 Git is a distributed version control system.
-Git is free software.
+Git is free software distributed under the GPL .

添加到仓库
[root@node4-docker20-207 learngit]# git add readme.txt 

提交，并写清楚修改了什么
[root@node4-docker20-207 learngit]# git commit -m "append GPL"
[master a5c1022] append GPL
 1 file changed, 1 insertion(+), 1 deletion(-)

</pre>

>像这样，不断的对该文件进行修改，然后不断提交修改到版本库里，就好比玩游戏一样，通过一关就会自动把游戏状态存盘，如果某一关没过去，还可以选择读取前一关的状态。每当你觉得文件修改到一定程度的时候，就可以"保存一个快照"，这个快照在Git中被称为commit。一旦你把文件改乱了，或者误删除了文件，还可以从最近的一个commit 恢复，然后继续工作，而不是把几个月的工作成果全部丢失。

现在我们可以回顾一下readme.txt文件一共有几个版本被提交到Git仓库里了：

版本1： wrote a readme file
<pre>
Git is a version control system.
Git is free software.
</pre>

版本2： add distributed
<pre>
Git is a distributed version control system.
Git is free software.
</pre>

版本3： append GPL
<pre>
Git is a distributed version control system.
Git is free software distributed under the GPL.
</pre>

>需要说明的是，在实际工作中，我们不可能去记住每次对文件进行了什么修改，不然要版本控制系统干什么，版本控制系统肯定有某个命令可以告诉我们历史记录，在Git中，我们用 git log 来进行查看：

<pre>
[root@node4-docker20-207 learngit]# git log
commit a5c1022bdf07772a5fde20ec0b5f40761d24e2ec
Author: xie di <linux_xd@sina.com>
Date:   Sun Jun 12 17:11:43 2016 +0800

    append GPL

commit f8b9e3ebee2d6853ccf99e5d7b8ac2c40c3bcae0
Author: xie di <linux_xd@sina.com>
Date:   Sun Jun 12 17:04:29 2016 +0800

    add distributed

commit 08116705a1e805e90fa5c7a6cd8089d5e5c2d642
Author: xie di <linux_xd@sina.com>
Date:   Sun Jun 12 16:40:26 2016 +0800

    wrote a readme file

</pre>

>git log 命令显示从最近到最远的提交日志，我们可以看到3次提交，最近的一次是append  GPL，上一次是add distributed，最早的一次是wrote a readme file。如果嫌弃输出信息太多，可以试试加上参数 --pretty=oneline

<pre>
[root@node4-docker20-207 learngit]# git log --pretty=oneline
a5c1022bdf07772a5fde20ec0b5f40761d24e2ec append GPL
f8b9e3ebee2d6853ccf99e5d7b8ac2c40c3bcae0 add distributed
08116705a1e805e90fa5c7a6cd8089d5e5c2d642 wrote a readme file

</pre>

>大家可能注意到了，前面一大串数字，为什么不是1，2，3呢？
>这是因为Git是分布式的版本控制系统，后面我们还要研究多人在同一个版本库里工作，如果大家都用1，2，3，....作为版本号的话，那肯定会冲突。

好了，说了这么多，开始干点正事了。
我们需要启动时光穿梭机，准备把readme.txt回退到上一个版本，也就是"add distributed"的那个版本，怎么做呢？

首先，Git必须知道当前版本是哪个版本，在Git中，用 HEAD 表示当前版本，也就是最新的提交，上一个版本就是HEAD^，上上一个版本就是HEAD^^,当然往上100个版本写100个^会不会很傻，所以写成HEAD~100.


现在，我们要把当前版本"append GPL"回退到上一个版本"add distributed",就可以使用 git reset 命令
<pre>
[root@node4-docker20-207 learngit]# cat readme.txt 
Git is a distributed version control system.
Git is free software distributed under the GPL .

回退到上一个版本，至于参数--hard 稍后再说
[root@node4-docker20-207 learngit]# git reset --hard HEAD^
HEAD 现在位于 f8b9e3e add distributed

查看，果然回退到上一个版本
[root@node4-docker20-207 learngit]# cat  readme.txt 
Git is a distributed version control system.
Git is free software.

看日志，发现只有2个版本，那么问题来了，那我要到最新的版本该怎么办呢？
[root@node4-docker20-207 learngit]# git log
commit f8b9e3ebee2d6853ccf99e5d7b8ac2c40c3bcae0
Author: xie di <linux_xd@sina.com>
Date:   Sun Jun 12 17:04:29 2016 +0800

    add distributed

commit 08116705a1e805e90fa5c7a6cd8089d5e5c2d642
Author: xie di <linux_xd@sina.com>
Date:   Sun Jun 12 16:40:26 2016 +0800

    wrote a readme file

最新的那个版本已经看不到了，但是，只要窗口没有关闭，你知道找到序号，就可以了，如下：
[root@node4-docker20-207 learngit]# git reset --hard a5c1022bdf07772a5fde20ec0b5f40761d24e2ec
HEAD 现在位于 a5c1022 append GPL
[root@node4-docker20-207 learngit]# cat readme.txt 
Git is a distributed version control system.
Git is free software distributed under the GPL .
版本号没必要写全，前几位就可以了，Git会自动去找。当然也不能只写前一两位，因为Git可能会找到多个版本号，就无法确定是哪一个了。

</pre>

>Git的版本回退速度非常快，因为Git在内部有个指向当前版本的HEAD指针，当你回退版本的时候，Git仅仅是把HEAD 从指向append GPL。

现在，你回退到了某个版本，关掉了电脑，第二天早上你就后悔了，想恢复到新版本怎么办？找不到新版本的commit id  怎么办？

Git提供了一个命令  git reflog用来记录你的每一次命令：
<pre>
[root@node4-docker20-207 learngit]# git reflog
f8b9e3e HEAD@{0}: reset: moving to HEAD^
a5c1022 HEAD@{1}: reset: moving to a5c1022bdf07772a5fde20ec0b5f40761d24e2ec
0811670 HEAD@{2}: reset: moving to HEAD^
f8b9e3e HEAD@{3}: reset: moving to HEAD^
a5c1022 HEAD@{4}: commit: append GPL
f8b9e3e HEAD@{5}: commit: add distributed
0811670 HEAD@{6}: commit (initial): wrote a readme file

</pre>
第4 个里面提示了append GPL的ID 是a5c1022，现在砸门就可以在此回到最新版本，测试如下：

<pre>
[root@node4-docker20-207 learngit]# cat readme.txt 
Git is a distributed version control system.
Git is free software.
[root@node4-docker20-207 learngit]# git reset --hard a5c1022
HEAD 现在位于 a5c1022 append GPL
[root@node4-docker20-207 learngit]# cat readme.txt 
Git is a distributed version control system.
Git is free software distributed under the GPL .
没错，他又回来了
</pre>

**小结**

1. HEAD 指向的版本就是当前版本，因此，Git允许我们在版本的历史之间穿梭，使用命令 git reset --hard commit_id。
2. 穿梭前，用 git log 可以查看提交历史，以便确定要回退到哪个版本。
3. 要重返未来，用 git reflog 查看命令历史，以便确定要回到未来的哪个版本。

##

##工作区和暂存区
Git和其他版本控制系统如SVN的一个不同之处就是有暂存区的概念。

首先是名词解释

工作区：

就是在电脑上能看到的目录，比如我的learngit 文件夹就是一个工作区。

版本库（repository）

工作区有一个隐藏目录 .git ，这个不算工作区，而是Git的版本库。

Git的版本库里存放了很多东西，其中最重要的就是称为stage（或者叫做index）的暂存区，还有Git为我们自动创建的第一个分支master ，以及指向master的一个指针叫HEAD。

前面讲了我们把文件往Git版本库里添加的时候，是分两步执行的：

第一步： git add 把文件添加进去，实际上就是把文件修改添加到暂存区；

第二步： git commit 提交更改，实际上就是把暂存区的所有内容提交到当前分支；

>因为我们创建Git版本库时，Git自动为我们创建了唯一一个master分支，所以，现在，git commit 就是往master分支上提交更改。
>你可以简单的理解为，需要提交的文件修改通通放到暂存区，然后，一次性提交暂存区的所有修改。

我们再次练习一遍，先对readme.txt 进行修改，比如说加上一行内容，然后我在新增一个文件LICENSE：

<pre>
加入一行文字
[root@node4-docker20-207 learngit]# cat readme.txt 
Git is a distributed version control system.
Git is free software distributed under the GPL .
Git  has a mutable index called stage.

新增一个文件
[root@node4-docker20-207 learngit]# cat LICENSE 
just test

很明确提示，readme.txt被修改了，而LICENSE还没有被添加过
[root@node4-docker20-207 learngit]# git status
# 位于分支 master
# 尚未暂存以备提交的变更：
#   （使用 "git add <file>..." 更新要提交的内容）
#   （使用 "git checkout -- <file>..." 丢弃工作区的改动）
#
#	修改：      readme.txt
#
# 未跟踪的文件:
#   （使用 "git add <file>..." 以包含要提交的内容）
#
#	LICENSE
修改尚未加入提交（使用 "git add" 和/或 "git commit -a"）

</pre>

现在，使用两次添加命令，然后再查看
<pre>
[root@node4-docker20-207 learngit]# git add LICENSE 
[root@node4-docker20-207 learngit]# git status
# 位于分支 master
# 要提交的变更：
#   （使用 "git reset HEAD <file>..." 撤出暂存区）
#
#	新文件：    LICENSE
#	修改：      readme.txt
#

</pre>

>很明确说明了，已经提交到了暂存区，所以git add 命令实际上就是把要提交的所有修改放到暂存区（stage），然后，执行 git commit 就可以一次性把暂存区的所有修改提交到分支。

<pre>
[root@node4-docker20-207 learngit]# git commit -m "understand how stage works"
[master 209b9cd] understand how stage works
 2 files changed, 2 insertions(+)
 create mode 100644 LICENSE

一旦提交后，如果你又没有对工作区做任何修改，那么工作区就是“干净” 的
[root@node4-docker20-207 learngit]# git status
# 位于分支 master
无文件要提交，干净的工作区

</pre>

现在暂存区就没有任何内容了。

**小结**

1. 暂存区是Git非常重要的概念，弄明白了暂存区，就弄明白了Git的很多操作到底干了什么。

##

##管理修改

现在，如果你完全掌握了暂存区的概率。下面，就需要讨论为什么Git比其他版本控制系统设计的优秀，因为Git跟踪并管理的是修改，而非文件。

你会问，什么是修改？比如你新增了一行，这就是一个修改，删除了一行，也是一个修改，更改了某些字符，也是一个修改，删了一些又加了一些，也是一个修改，甚至创建一个新文件，也算一个修改。

为什么说Git管理的是修改，而不是文件呢？实践出真理。

第一步：对readme.txt做一个修改，比如加一行内容：
<pre>
[root@node4-docker20-207 learngit]# cat readme.txt 
Git is a distributed version control system.
Git is free software distributed under the GPL .
Git  has a mutable index called stage.
Git tracks changes.

</pre>

然后，添加：
<pre>
[root@node4-docker20-207 learngit]# git add readme.txt 
[root@node4-docker20-207 learngit]# git status
# 位于分支 master
# 要提交的变更：
#   （使用 "git reset HEAD <file>..." 撤出暂存区）
#
#	修改：      readme.txt
#

</pre>

然后在此修改
<pre>
[root@node4-docker20-207 learngit]# cat readme.txt 
Git is a distributed version control system.
Git is free software distributed under the GPL .
Git  has a mutable index called stage.
Git tracks changes of files.
</pre>

提交：
<pre>
[root@node4-docker20-207 learngit]# git commit -m "git tracks changes"
[master daa81bc] git tracks changes
 1 file changed, 1 insertion(+)

</pre>

提交后，查看状态

<pre>
[root@node4-docker20-207 learngit]# git status
# 位于分支 master
# 尚未暂存以备提交的变更：
#   （使用 "git add <file>..." 更新要提交的内容）
#   （使用 "git checkout -- <file>..." 丢弃工作区的改动）
#
#	修改：      readme.txt
#
修改尚未加入提交（使用 "git add" 和/或 "git commit -a"）
</pre>

>发现，第二次修改没有被提交？
>我们回顾一下操作的过程：
>第一次修改-->git add -->第二次修改-->git commit 
>你看，我们前面说过，Git管理的是修改，当你用git add命令后，在工作区的第一次修改被放入暂存区，准备提交，但是，在工作区的第二次修改并没有放入暂存区，所以，git commit 只负责把暂存区的修改提交了，也就是第一次修改被提交了，第二次次修改不会被提交。
>提交后，用 git diff HEAD -- readme.txt 命令可以查看工作区和版本库里面最新版本的区别：
<pre>
[root@node4-docker20-207 learngit]# git diff HEAD -- readme.txt 
diff --git a/readme.txt b/readme.txt
index c1670ab..de803f7 100644
--- a/readme.txt
+++ b/readme.txt
@@ -1,4 +1,4 @@
 Git is a distributed version control system.
 Git is free software distributed under the GPL .
 Git  has a mutable index called stage.
-Git tracks changes.
+Git tracks changes of files.

</pre>

可以看到第二次修改没有被提交。

那么如何去提交第二次修改呢？可以继续git add 再 git commit ，也可以先不着急去提交第一次修改，先git add 第二次修改，然后在git  commit ，这样就相当于把两次修改合并后一块提交了。
流程图如下：

第一次修改--> git add -->第二次修改--> git add --> git commit 。

好了，现在，把第二次修改提交了，就可以了。

**小结**

现在，我想应该理解了Git是如何进行跟踪修改的，每次修改，如果不add 到暂存区，那就不会加入到commit中。


##

##撤销修改
如果你在readme.txt中添加了一行不那么厚道的文字：
<pre>
[root@node4-docker20-207 learngit]# cat readme.txt 
Git is a distributed version control system.
Git is free software distributed under the GPL .
Git  has a mutable index called stage.
Git tracks changes of files.
My stupid boss still prefers SVN.
</pre>

当你准备提交前，一杯咖啡起了作用，你猛然发现了"stupid boss"可能会让你死的很惨，既然发现错误了，就可以很容器的纠正它。这个时候，你可以删掉最后一行，手动把文件恢复到上一个版本的状态。如果用 git status 查看一下：

<pre>
[root@node4-docker20-207 learngit]# git status
# 位于分支 master
# 尚未暂存以备提交的变更：
#   （使用 "git add <file>..." 更新要提交的内容）
#   （使用 "git checkout -- <file>..." 丢弃工作区的改动）
#
#	修改：      readme.txt
#
修改尚未加入提交（使用 "git add" 和/或 "git commit -a"）
</pre>

你可以发现，Git会告诉你，使用命令  git checkout -- file 可以丢弃工作区的修改：

<pre>
[root@node4-docker20-207 learngit]# git checkout -- readme.txt 
</pre>

命令 git checkout -- readme.txt  意思就是，把readme.txt 文件在工作区的修改全部撤销，这里有两种情况：

第一就是 readme.txt自修改后还没有放入暂存区，现在，撤销修改就回到和版本库一模一样的状态；

第二就是 readme.txt已经添加到暂存区，又作了修改，现在，撤销修改就回到添加到暂存区后的状态。

总之，就是让这个文件回到最近一次  git commit 或git  add 时的状态。

现在，我们看readme.txt的文件内容：

<pre>
[root@node4-docker20-207 learngit]# cat readme.txt 
Git is a distributed version control system.
Git is free software distributed under the GPL .
Git  has a mutable index called stage.
Git tracks changes.

</pre>
文件果然恢复了。

git  checkout -- file 命令中的 -- 很重要，没有 -- ，就变成了"切换到另一个分支"的命令，我们在后面的分支管理中会再次遇到 git  checkout命令。

现在假定是凌晨3点，你不但写了一些胡话，还git add 到暂存区了。
<pre>
[root@node4-docker20-207 learngit]# cat readme.txt 
Git is a distributed version control system.
Git is free software distributed under the GPL .
Git  has a mutable index called stage.
Git tracks changes.
My stupid boss still prefers SVN.
[root@node4-docker20-207 learngit]# git add readme.txt 
</pre>

庆幸的是，在commit 之前，你发现了这个问题，用git status 查看一下，修改只是添加到了暂存区，还没有提交。

<pre>
[root@node4-docker20-207 learngit]# git status
# 位于分支 master
# 要提交的变更：
#   （使用 "git reset HEAD <file>..." 撤出暂存区）
#
#	修改：      readme.txt
#

</pre>

Git明确告诉我们，用命令  git reset  HEAD  file，可以把暂存区的修改撤销，重新放回工作区
<pre>
[root@node4-docker20-207 learngit]# git reset HEAD readme.txt 
重置后撤出暂存区的变更：
M	readme.txt

</pre>

git reset 命令即可以回退版本，也可以把暂存区的修改回退到工作区。当我们用HEAD 时，表示最新的版本。

再用 git status 查看一下，现在暂存区是干净的，工作区有修改：

<pre>
[root@node4-docker20-207 learngit]# git status
# 位于分支 master
# 尚未暂存以备提交的变更：
#   （使用 "git add <file>..." 更新要提交的内容）
#   （使用 "git checkout -- <file>..." 丢弃工作区的改动）
#
#	修改：      readme.txt
#
修改尚未加入提交（使用 "git add" 和/或 "git commit -a"）

</pre>

这个时候我们需要丢弃工作区的修改.
<pre>
[root@node4-docker20-207 learngit]# git checkout -- readme.txt 
[root@node4-docker20-207 learngit]# git status
# 位于分支 master
无文件要提交，干净的工作区

整个世界安静了，我们在查看readme.txt，发现还原了。
[root@node4-docker20-207 learngit]# cat readme.txt 
Git is a distributed version control system.
Git is free software distributed under the GPL .
Git  has a mutable index called stage.
Git tracks changes.

</pre>

现在，假设你不但改错了东西，还从暂存区提交到了版本库，怎么办？还记得版本回退吗？可以回退到上一个版本。不过，这是有条件的，就是你还没有把自己的本地版本库推送到远程。还记得Git是分布式版本控制系统吗？一旦你把"stupid boss" 提交推送到远程版本库，你就真的惨了....

**小结**

场景1： 当你改乱了工作区某个文件的内容，想直接丢弃工作区的修改时，用命令

git checkout  -- file

场景2 ： 当你不但改乱了工作区某个文件的内容，还添加到了暂存区，想丢弃修改，分两步：第一步，用命令 git reset HEAD file ，就回到场景1，第二步按照场景1来操作。

场景3： 已经提交了不合适的修改到版本库时，想要撤销本次提交，参考版本回退，不过前提是没有推送到远程库。

##
##删除文件

在Git中，删除也是一个修改操作，我们实战一下，先添加一个新文件 test.txt 到Git并提交：

<pre>
[root@node4-docker20-207 learngit]# cat test.txt 
just test
[root@node4-docker20-207 learngit]# git add test.txt 
[root@node4-docker20-207 learngit]# git commit -m "add test.txt"
[master 0c3255a] add test.txt
 1 file changed, 1 insertion(+)
 create mode 100644 test.txt
[root@node4-docker20-207 learn
</pre>

一般情况下，你通常直接在文件管理器中把没用的文件删除了，或者用rm命令删了：
<pre>
[root@node4-docker20-207 learngit]# rm test.txt 
rm：是否删除普通文件 "test.txt"？y

</pre>

这个时候，Git知道你删除了文件，因此，工作区和版本库就不一致了，git status 命令会立刻告诉你哪些文件被删除了：
<pre>
[root@node4-docker20-207 learngit]# git status
# 位于分支 master
# 尚未暂存以备提交的变更：
#   （使用 "git add/rm <file>..." 更新要提交的内容）
#   （使用 "git checkout -- <file>..." 丢弃工作区的改动）
#
#	删除：      test.txt
#
修改尚未加入提交（使用 "git add" 和/或 "git commit -a"）
</pre>

现在你有两个选择，一是确实要从版本库删除该文件，那就用命令 git rm 删掉，并且git commit 
<pre>
[root@node4-docker20-207 learngit]# git rm test.txt
rm 'test.txt'
[root@node4-docker20-207 learngit]# git commit -m "remove test.txt"
[master 3655526] remove test.txt
 1 file changed, 1 deletion(-)
 delete mode 100644 test.txt

</pre>
现在，文件就从版本库中被删除了。

另一种情况是删错了，因为版本库里还有呢。所有可以轻松地把误删除的文件恢复到最新版本：
<pre>
git checkout -- test.txt
</pre>
>git checkout 其实是用版本库里的版本替换工作区的版本，无论工作区是修改还是删除，都可以"一键还原"

**小结**

命令  git rm  用于删除一个文件。如果一个文件已经被提交到版本库，那么你永远不用担心误删，但是要小心，你只能恢复文件到最新版本，你会丢失最近一次提交后你修改的内容。


##
##远程仓库

到目前为止，我们已经知道了如何在Git仓库里对一个文件进行时光穿梭，你再也不用担心文件备份或者丢失的问题了。

Git最牛逼的功能：远程仓库。

Git是分布式版本控制系统，同一个Git仓库，可以分布到不同的机器上。怎么分布呢？最早，肯定只有一台机器有一个原始版本库，此后，别的机器可以"克隆"这个原始版本库，而且每台机器的版本库其实都是一样的，并没有主次之分。
你肯定会想，至少需要两台机器才能玩远程库不是？但是我只有一台电脑，怎么玩？


其实一台电脑上也是可以克隆多个版本库的，只要不在同一个目录下。不过，现实生活中，不会有人这么傻在一台电脑上搞几个远程库来玩，因为一台电脑上搞几个远程库完全没有意义，而且硬盘挂了会导致所有库都挂掉。

实际情况往往是这样的，找一台电脑充当服务器的角色，每天24小时开机，其他每个人都从这个"服务器"仓库克隆一份到自己的电脑上，并且各自把各自的提交推送到服务器仓库里，也从服务器仓库中拉取别人的提交。


完全可以自己搭建一台运行Git的服务器，不过现阶段，为了学Git先搭个服务器绝对是小题大做。好在这个世界上有个叫做github 的神奇网站，你只要注册一个Github 的账号，就可以免费获得Git的远程仓库。

由于本地的Git仓库和Github仓库之间的传输是通过SSH加密的，所以，需要一点设置：

第一步： 创建SSH Key。在用户主目录下，看看有没有.ssh目录

如果是在Windows下创建的，那么默认会在 c盘创建这个目录，注意提示
<pre>
$ ssh-keygen -t rsa -C "linux_xd@sina.com"
</pre>
需要把邮件换成自己的邮件地址，然后一路回车即可。

添加这个key到GitHub即可。

为什么GitHub需要SSH key呢？

因为GitHub需要识别出你推送的提交确实是你推送的，而不是别人冒充的，而Git支持SSH协议，所有GitHUB只要知道了你的公钥，就可以确定只有你自己才能推送。


##
##添加远程库

现在的情况是这样的，你已经在本地创建了一个git仓库，又想在Github上创建一个git仓库，并且让这两个仓库进行远程同步，这样，github上的仓库既可以作为备份，又可以让其他人通过该仓库来协作，真是一举多得。

首先，登录Github，然后，在右上角找到"create a  new repo" 按钮，创建一个新的仓库：













