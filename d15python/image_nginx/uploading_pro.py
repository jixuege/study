#!/usr/bin/env python
# coding:utf8
"""
    author:zhaoshen

    下载项目到执行的目录
"""
import sys
import urllib
import time
import uuid
import optparse
import os
import shutil
import subprocess

def _arg():
    """
    针对参数的处理
    :return:
    """

    parser = optparse.OptionParser()

    # 默认的配置文件列
    default_opts = optparse.OptionGroup(parser, "DEFAULT","Default Arguments.", )
    default_opts.add_option("--download_url", dest="download_url",help=u"下载的地址")
    default_opts.add_option("--download_dir", dest="download_dir",help=u"下载的目录")
    default_opts.add_option("--target_path", dest="target_path",help=u"目标的完整路径包含文件名称")
    # 加入组
    parser.add_option_group(default_opts)

    # 获得全部的命令行参数
    arg_dt = parser.parse_args()[0]
    # 查看命令中是否有配置文件

    # 处理组对象
    new_arg_dt = {}
    for group_obj in parser.option_groups:
        _arg_lt = [_o.dest for _o in group_obj.option_list]
        _dt = {group_obj.title:{}}
        for _arg in _arg_lt:
            _dt[group_obj.title].update({
                _arg:eval("arg_dt.%s" %_arg )
            })
        new_arg_dt.update(_dt)
    return new_arg_dt['DEFAULT']

class Config(object):
    def __init__(self,arg_dt):
        """
        配置方法
        arg_dt 配置参数
        :return:
        """
        #下载地址
        self.download_dir = "/" + arg_dt["download_dir"].strip('/') + "/"
        # 目标完全路径
        self.target_path = "/" + arg_dt["target_path"].strip('/')
        # 下载链接地址
        self.download_url = arg_dt["download_url"]

    def __exec_command(self,_command):
        """
            执行命令方法
        :return:
        """
        stat = subprocess.Popen(_command,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,)
        msg = "y\n"
        out, err = stat.communicate(msg)
        out, err =  out.strip(), err.strip()
        code = str(stat.returncode)
        if len(err) == 0:
            return code,out
        elif len(out) == 0:
            return code,err
        else:
            return code,out

    def __get_random_file(self):
        """
        获得一个随机的分集名称
        :return:_name 文件名称
        """
        _name = str(uuid.uuid5(uuid.NAMESPACE_DNS,str(time.time()))).replace('-','')
        return _name

    def __delete_file(self,file_path):
        """
        删除文件
        :return:
        """
        file_path = str(file_path)
        if os.path.isfile(file_path):
            os.remove(file_path)


    def download_config_file(self):
        """
        下载配置文件
        :return:
        """
        file_path = urllib.urlretrieve(url=self.download_url,filename=self.download_dir + self.__get_random_file())[0]
        return file_path


    def main(self):
        """
        主函数
        :return:
        """
        # 下载配置文件到本地
        file_path = self.download_config_file()
        # 创建文件夹
        self.__exec_command("mkdir -p %s" % (self.target_path))
        # 解压缩到执行位置
        self.__exec_command("tar -zxvf %s -C %s" % (file_path,self.target_path))




if __name__ == '__main__':
    # 获取参数字典
    """
    python uploading_config.py --download_url=http://10.10.20.221:80/autoconf/4791cae2f4cc59a6b6c8426c4f2d43f5mysql --download_dir=/data/download --backups_dir=/data/backups --target_path=/data/target/mysql --restart_order=ifconfig
    """
    arg_dt = _arg()

    # 统一处理格式


    # 出入参数检查，如果没有传入的参数报错
    if  None in arg_dt.values():
        sys.stderr.write(" *********** arg error! *********** ")
        sys.exit(-1)

    try:
        Config(arg_dt).main()
        sys.stdout.write("success")
        sys.exit(0)
    except Exception as e:

        sys.stderr.write(" *********** config error! err:%s***********  " % str(e))
        sys.exit(-2)