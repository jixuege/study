#git 使用错误集合

##push不上去
提示错误信息如下
<pre>
[root@node4-docker20-207 bs_jyall_dockerFile]# git push origin master
To git@gitlab.jyall.com:cloud/bs_jyall_dockerFile.git
 ! [rejected]        master -> master (fetch first)
error: 无法推送一些引用到 'git@gitlab.jyall.com:cloud/bs_jyall_dockerFile.git'
提示：更新被拒绝，因为远程版本库包含您本地尚不存在的提交。这通常是因为另外
提示：一个版本库已推送了相同的引用。再次推送前，您可能需要先合并远程变更
提示：（如 'git pull'）。
提示：详见 'git push --help' 中的 'Note about fast-forwards' 小节。
</pre>

解决办法：

强行push
<pre>
git push origin +master
</pre>

参考：[关于push到gitlib错误](http://mooc.guokr.com/note/9146/)