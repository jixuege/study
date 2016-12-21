#!/usr/bin/env python
# coding:utf8
"""
    author:zhaoshen
"""
import optparse
import sys
import subprocess
from jinja2 import Template

class Constant():
    """
    常量
    """
    # VPN规则
    OPENVPN_RULE = "iptables -t nat -A POSTROUTING -s %s/24 -d %s/12 -o %s -j MASQUERADE"

    # VPN准备服务
    # 模板服务目录地址
    OPENVPN_TEMPLATE_FILE = "/pyscript/openvpn_template.conf"
    OPENVPN_DEST_CONFIG_FILE = "/%s/server.conf"
    PREPARE_OPENVPN_SERVER = [
        "mkdir -p /dev/net/",
        "mknod /dev/net/tun c 10 200",
        "chmod 600 /dev/net/tun"
    ]
    # VPN启动服务
    START_OPENVPN_SERVER = "openvpn --daemon --config %s"

    # VPN创建秘钥
    # 创建秘钥
    CREATE_OPENVPN_KEY = "cd /etc/openvpn/easy-rsa/2.0/ && source ./vars &&./build-key --batch %s"

    #获取秘钥
    KEY_FILE = "/etc/openvpn/easy-rsa/2.0/keys/%s.key"
    CRT_FILE = "/etc/openvpn/easy-rsa/2.0/keys/%s.crt"


    # nginx 服务
    # nginx 目录位置
    NGINX_PATH = "/usr/share/nginx/html"
    # nginx的模板位置
    NGINX_TMPLATE_FILT = "/pyscript/nginx_template.conf"
    # nginx目标位置
    NGINX_DEST_CONFIG_FILE = "/%s/nginx.conf"

    # 启动nginx服务
    START_NGINX_SERVER = "/usr/sbin/nginx -c %s"


def exec_command(_command):
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
    code = stat.returncode

    if len(err) == 0:
        return code,out
    elif len(out) == 0:
        return code,err
    else:
        return code,out

def create_config_file(_temp_path,_dest_path,_type,_arg_dt):
    """
    创建服务配置文件
    :param _temp_path: 模板路径
    :param _dest_path: 配置文件目标路径
    :param server: server服务信息
    :param route_rule: 路由规则
    :return:
    """
    # 打开模板文件
    with open(_temp_path,"r") as f:
        txt = f.read()

    template = Template(txt)

    if _type == "vpn":
        result = template.render(server=_arg_dt['server'],rules=_arg_dt["route_rule_lt"])
    elif _type == "nginx":
        result = template.render(nginx_path=_arg_dt['nginx_path'],rules=_arg_dt["rules"])
    else:
        raise Exception,"create template error. no type:%s" % _type

    with open(_dest_path,'w') as f:
        f.write(result)

    return  _dest_path

def _arg():
    """
    针对参数的处理
    :return:
    """
    # python create_openvpn_and_nginx.py --dev_name=/data --n_device=eth0 --openvpn_conn_ip=10.0.10.0 --user_gateway=172.16.100.254 --key_name=commmandzs --w_ip=10.10.22.200 --shellbox_port=4200
    parser = optparse.OptionParser()
    # 默认的配置文件列
    default_opts = optparse.OptionGroup(parser, u"说明", u"构建openvpn服务 和 nginx服务")
    default_opts.add_option("--dev_name", dest="dev_name",default="/tmp", help=u"用户文件的挂在点")
    default_opts.add_option("--n_device", dest="n_device", help=u"用户内网网卡设备名称")
    default_opts.add_option("--openvpn_conn_ip", dest="openvpn_conn_ip", help=u"openvpn需要的IP")
    default_opts.add_option("--user_gateway", dest="user_gateway", help=u"用户的网关")
    default_opts.add_option("--key_name", default='common', dest="key_name", help=u"创建openvpn秘钥的文件名")
    default_opts.add_option("--w_ip", dest="w_ip", help=u"用户外网ip")
    default_opts.add_option("--shellbox_port", dest="shellbox_port", default='4200',help=u"shellbox需要的端口")
    # 加入组
    parser.add_option_group(default_opts)

    # 获得全部的命令行参数
    arg_obj = parser.parse_args()[0]

    # 处理组对象
    arg_dt = {
        "dev_name":arg_obj.dev_name,
        "openvpn_conn_ip":arg_obj.openvpn_conn_ip,
        "n_device":arg_obj.n_device,
        "user_gateway":arg_obj.user_gateway,
        "key_name":arg_obj.key_name,
        "w_ip":arg_obj.w_ip,
        "shellbox_port":arg_obj.shellbox_port
    }
    return arg_dt


def main():
    """
    主函数
    :return:
    """
    constant = Constant()

    try:
        arg_dt = _arg()
    except Exception as e:
        print("arg error. info : %s" % str(e))
        sys.exit(-1)

    # 规则操作
    try:
        user_gateway = arg_dt['user_gateway']
        n_ip = ".".join(user_gateway.split('.')[0:3]) + ".0"
        openvpn_conn_ip,n_device = arg_dt['openvpn_conn_ip'],arg_dt['n_device']
        _command = constant.OPENVPN_RULE % (openvpn_conn_ip,n_ip,n_device)
        code,info = exec_command(_command)
        if code <> 0:
            raise Exception,"exec openvpn rule command error!"
    except Exception as e:
        print("rule error! info:%s" % str(e) )
        sys.exit(-2)

    # 创建配置文件
    try:
        _temp_path = constant.OPENVPN_TEMPLATE_FILE
        _dest_path = constant.OPENVPN_DEST_CONFIG_FILE % arg_dt['dev_name']
        server = "%s 255.255.255.0" % arg_dt['openvpn_conn_ip']
        route_rule_lt = ["%s 255.255.255.0" % n_ip,]
        _arg_dt = {
            "server":server,
            "route_rule_lt":route_rule_lt,
        }
        _dest_path = create_config_file(_temp_path,_dest_path,"vpn",_arg_dt)
    except Exception as e:
        print("create_openvpn_config_file error. info: %s " % str(e) )
        sys.exit(-3)

    # 启动openvpn服务
    try:
        for _command in constant.PREPARE_OPENVPN_SERVER:
            code,info = exec_command(_command)
        exec_command(constant.START_OPENVPN_SERVER % _dest_path )
        if code <> 0:
            raise Exception,"exec openvpn server command error!"
    except Exception as e:
        print("start openvpn error. info: %s " % str(e) )
        sys.exit(-4)

    # 生成秘钥
    try:
        exec_command(constant.CREATE_OPENVPN_KEY % arg_dt["key_name"])
        if code <> 0:
            raise Exception,"exec key command error!"
    except Exception as e:
        print("create key error. info: %s " % str(e) )
        sys.exit(-5)

    # 创建nginx服务
    try:
        nginx_path = constant.NGINX_PATH
        exec_command(_command="mkdir -p %s" % nginx_path)
        _move_key_file = [
            "cp -fr %s  %s/%s.key" % (constant.KEY_FILE % arg_dt['key_name'],nginx_path,arg_dt['key_name']),
            "cp -fr %s  %s/%s.crt" % (constant.CRT_FILE % arg_dt['key_name'],nginx_path,arg_dt['key_name']),
            "chmod 665 %s/%s.key" % (nginx_path,arg_dt['key_name']),
            "chmod 665 %s/%s.crt" % (nginx_path,arg_dt['key_name'])
        ]
        for _command in _move_key_file:
            code,info = exec_command(_command)
        if code <> 0:
            raise Exception,"exec prepare nginx error!"
    except Exception as e:
        print("prepare nginx error. info: %s " % str(e) )
        sys.exit(-6)

    # 创建nginx配置文件
    try:
        _temp_path = constant.NGINX_TMPLATE_FILT
        _dest_path = constant.NGINX_DEST_CONFIG_FILE % arg_dt['dev_name']
        # 该IP段的全部IP
        rules = []
        user_gateway = arg_dt['user_gateway']
        name_txt = "".join(user_gateway.split('.')[0:3])
        ip_txt = ".".join(user_gateway.split('.')[0:3])
        for x in xrange(1,254):
            x = str(x)
            _dt = {
            }
            #名称的构成是1721661
            _dt['name'] = name_txt + x
            _dt['ip'] = ip_txt.strip(".") + "." + x
            _dt['port'] = arg_dt['shellbox_port']
            rules.append(_dt)
        _arg_dt = {
            "rules":rules,
            "nginx_path":nginx_path
        }
        _dest_path = create_config_file(_temp_path,_dest_path,"nginx",_arg_dt)
    except Exception as e:
        print("create_nginx_config_file error. info: %s " % str(e) )
        sys.exit(-7)

    # 启动nginx服务
    try:
        code,info = exec_command(constant.START_NGINX_SERVER % _dest_path )
        if code <> 0:
            raise Exception,"exec nginx server command error!"
    except Exception as e:
        print("start nginx error. info: %s " % str(e) )
        sys.exit(-8)

    print "http://" + arg_dt['w_ip'] + "/" + "%s.key" % arg_dt['key_name']
    print "http://" + arg_dt['w_ip'] + "/" + "%s.crt" % arg_dt['key_name']
    print "success"
    sys.exit(0)

if __name__ == '__main__':
    main()