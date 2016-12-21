手动测试：
#启动容器命令格式
#docker run  --cap-add SYS_ADMIN   --device=/dev/test1:/dev/test1   -e DEV=/dev/test1 -e LOCATION=/tmp  -itd --name test123 镜像名
例如：
docker run  --cap-add SYS_ADMIN   --device=/dev/test123:/dev/sdb   -e DEV=/dev/sdb -e LOCATION=/tmp  -itd --name test13 mount_python2.7
#注意：
上面的设备.dev.test1需要创建

新建块
dd if=/dev/zero of=/opt/dev6-backstore bs=1M count=100
mknod /dev/test123 b 7 209
losetup /dev/test123 /opt/dev6-backstore
mkfs.ext4 /dev/test123
这里需要修改的是每次的209数字版本号需要修改，不能相同，不然不能格式化
可以修改/dev/xxx 

##每次修改的时候，需要填写版本号文本 VERSION，并注明修改信息
