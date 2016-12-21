#!/usr/bin/env python
# coding=utf8

"""
此脚本用于配置MySQL 主从复制,主要功能有:
    --name cluster_name --consul 192.168.1.10:8500 create --mode MASTER  创建主
    --name cluster_name --consul 192.168.1.10:8500 create --mode SLAVE   创建从
    --name cluster_name --consul 192.168.1.10:8500 add    --mode SLAVE   添加从
    --name cluster_name --consul 192.168.1.10:8500 del    --mode SLAVE   删除从
    --name cluster_name --consul 192.168.1.10:8500 destroy               删除集群配置
    --name cluster_name --consul 192.168.1.10:8500 status                查看集群状态
"""

import sys
import os
import argon
import consul
import logging
import time
import random
import subprocess
import re
import gzip
import logging.handlers as log_handlers


MYSQL_MODE = {
        "master": "MASTER",
        "slave": "SLAVE"
        }

def main():
    app = argon.App(description="MySQL replication configure manage")

    # 定义全局选项
    app.arg("--name", default=False, required=True,
            help="Cluster unique name")

    app.arg("--consul", default=False, required=True,
            help="Consul host address and port")

    app.arg("--log", default="INFO", choices=["INFO", "WARING", "ERROR"],
            help="Open log set log level")

    # 定义 create sub commmand 和选项
    with app.command("create") as create:
        create.arg("--mode", default=False, required=True, choices=["MASTER", "SLAVE"],
                help="MySQL replication role")\
                        .arg("--service_id", default=False, required=True,
                                help="register server name")\
                        .arg("--ip", default=False, required=True, help="MySQL host address")\
                        .arg("--port", default=False, help="MySQL host address port")\
                        .arg("--admin_user", default="root", required=True, help="MySQL administrator user")\
                        .arg("--admin_pass", default="", required=True, help="MySQL administrator password")\
                        .arg("--rep_user", default="rep", help="grant replication user")\
                        .arg("--rep_pass", default="rep", help="grant replication password")\
                        .arg("--dbname", default="--all-databases", 
                                help="MySQL replication database name, default ALL")\
                        .handler(cluster_create)


    # 定义 add sub command 和选项
    with app.command("add") as add:
        add.arg("--mode", default="SLAVE", required=True, choices=["SLAVE"],
                help="Add MySQL slave role")\
                        .arg("--service_id", default=False, required=True,
                                help="register server name")\
                        .arg("--ip", default=False, required=True, help="MySQL host address")\
                        .arg("--port", default=False, required=True, help="MySQL host address port")\
                        .arg("--admin_user", default="root", required=True, help="MySQL administrator user")\
                        .arg("--admin_pass", default="", required=True, help="MySQL administrator password")\
                        .arg("--dbname", default="--all-databases", 
                                help="MySQL replication database name, default ALL")\
                        .handler(cluster_add)

    # 定义 del sub command 和选项
    with app.command("del") as dele:
        dele.arg("--mode", default="SLAVE", required=True,  choices=["SLAVE"],
                help="Del MySQL slave role")\
                        .arg("--service_id", default=False, required=True,
                                help="register server name")\
                        .handler(cluster_del)

    # 定义 destroy sub command 和选项
    with app.command("destroy") as destroy:
        destroy.arg("-f", "--force", default=False,action="store_true",
                help="Destroy cluster configure, when not slave. if use -f flag."
                "delete all configure, MASTER and SLAVE") \
                        .handler(cluster_destroy)

    # 定义 status sub command 和选项
    with app.command("status") as status:
        status.arg("--service_id", default=False,
                help="View the node status")\
                        .handler(cluster_status)


    app.run(sys.argv[1:])

def _conn_consul(host, port, scheme="http"):
    try:
        session = consul.Consul(host=host,
                port=port,
                scheme=scheme)
    except Exception as e:
        root_logger.error("consul connection error:%s" % e)
        sys.exit(1)

    return session

def _register_service(session, args):

    reg_service_id = args.service_id # 注册服务名，一个集群名可以有多个唯一的server-id
    reg_service_name = args.name # 注册集群名，必须唯一
    reg_service_ip = None  # 注册服务的ip
    reg_service_port = None  # 注册服务ip 的端口
    reg_tags=None # 注册服务的标记,例如"master" "slave"


    reg_check = None # 服务检测方式
    reg_check_interval = 120 # 服务检测间隔时间


    if args.ip is not None and args.port is not None:
        reg_service_ip = args.ip
        reg_service_port = int(args.port)
        reg_check = "/check_tcp %s %d" % (reg_service_ip, reg_service_port) # 服务检测方式
    else:
        root_logger.error("Please give MySQL address")
        sys.exit(0)

    if args.mode == MYSQL_MODE.get("master"):
        reg_tags = ["master"]

    if args.mode == MYSQL_MODE.get("slave"):
        reg_tags = ["slave"]

    # 注册服务到consul
    status = session.agent.service.register(
            name=reg_service_name,
            service_id=reg_service_id,
            address=reg_service_ip,
            port=reg_service_port,
            tags=reg_tags,
            script=reg_check,
            interval=reg_check_interval
            )
    if not status:
        root_logger.error("register service error:%s" % reg_service_name)
        sys.exit(1)
    root_logger.info("register service success:%s" % reg_service_name)

def _deregister_service(session, service_id):

    session = session

    status = session.agent.service.deregister(service_id=service_id)
    if not status:
        root_logger.error("delete register %s error"  % args.name)
        sys.exit(1)

def _cluster_master(session, args):
    session = session

    # 用户授权
    status = _mysql_grant(
            admin_user=args.admin_user,
            admin_pass=args.admin_pass,
            admin_host = args.ip,
            grant_user=args.rep_user,
            grant_pass=args.rep_pass
            )
    if not status:
        root_logger.error("replication grant error")
        sys.exit(1)

    # key 规则: "cluster/args.name/args.service_id/admin"
    key = "cluster/%s/%s/admin" % (args.name, args.service_id)
    value = "%s::%s" % (args.admin_user, args.admin_pass)
    _put_kv(session=session, key=key, value=value)

    key = "cluster/%s/%s/grant" % (args.name, args.service_id)
    value = "%s::%s" % (args.rep_user, args.rep_pass)
    _put_kv(session=session, key=key, value=value)

def _cluster_slave(session, args):

    master_ip = None
    master_port = None
    master_user = None
    master_pass = None

    master_admin_key = None
    master_grant_key = None

    master_admin_user = None
    master_admin_pass = None

    master_grant_user= None
    master_grant_pass= None

    back_name = "/tmp/back_db.sql.gz"
    file_name = "/tmp/back_db.sql"

    if os.path.exists(back_name):
        cmd = ["rm", "-r", back_name]
        rc, out, error = _execute(cmd)
        if rc != 0:
            root_logger.error("delete backup [%s] error:%s" % (back_nam, error))
            sys.exit(1)

    if os.path.exists(file_name):
        cmd = ["rm", "-r", file_name]
        rc, out, error = _execute(cmd)
        if rc != 0:
            root_logger.error("delete backup [%s] error:%s" % (file_nam, error))
            sys.exit(1)

    result = _discover_service(
            session=session,
            service=args.name,
            tag="master"
            )
    if result:
        result = result[1][0]
        master_ip = result.get('Service').get('Address').encode('utf8')
        master_port = result.get('Service').get('Port')
        master_admin_key = "cluster/%s/%s/admin" % (result.get('Service').get('Service'),
                result.get('Service').get('ID'))
        master_grant_key = "cluster/%s/%s/grant" % (result.get('Service').get('Service'),
                result.get('Service').get('ID'))

    kv = _get_kv(session, key=master_admin_key)
    master_admin_user = kv[1].get('Value').split('::')[0]
    master_admin_pass = kv[1].get('Value').split('::')[1]

    kv = _get_kv(session, key=master_grant_key)
    master_grant_user = kv[1].get('Value').split('::')[0]
    master_grant_pass = kv[1].get('Value').split('::')[1]


    # 备份主库数据
    cmd = ["-h", master_ip, "-P", str(master_port), "-u", master_admin_user,
            "-p"+master_admin_pass, args.dbname]

    rc, out, error = _execute_mysqldump_cmd(cmd)
    if rc != 0:
        root_logger.error("Backup master db error:%s" % error)
        sys.exit(1)

    with gzip.open(back_name, "wb") as output:
        output.write(out)

    # 导入主库数据

    cmd = ["gzip", "-d", back_name]
    rc , out, error = _execute(cmd)
    if rc != 0:
        root_logger.error("decompress %s error:%s", (back_name, error))
        sys.exit(1)

    SQL = "source %s" % file_name
    
    if args.admin_user == "root" and args.admin_pass == "":
        cmd_op = ["-u", args.admin_user, "-h", args.ip, "-e" ]
    else:
        cmd_op = ["-u", args.admin_user, "-p"+args.admin_pass, "-h", args.ip, "-e" ]

    cmd = cmd_op + [SQL]
    rc , out, error = _execute_mysql_cmd(cmd)
    if rc != 0:
       root_logger.error("import  %s error:%s", (back_name, error))

    # 连接主库
    SQL = "CHANGE MASTER TO MASTER_HOST='%s',MASTER_USER='%s', \
            MASTER_PASSWORD='%s',MASTER_PORT=%d, MASTER_CONNECT_RETRY=30" \
            % (master_ip, master_grant_user, master_grant_pass, master_port)
    cmd = cmd_op + [SQL]
    rc, out, error = _execute_mysql_cmd(cmd)
    if rc != 0:
        root_logger.error("slave connection master error:%s" % error)
        sys.exit(1)

    SQL = "start slave"
    cmd = cmd_op + [SQL]
    rc, out, error = _execute_mysql_cmd(cmd)
    if rc != 0:
       root_logger.error("start slave  error:%s" % error)
       sys.exit(1)

    # key 规则: "cluster/args.name/args.service_id/admin"
    key = "cluster/%s/%s/admin" % (args.name, args.service_id)
    value = "%s::%s" % (args.admin_user, args.admin_pass)
    _put_kv(session=session, key=key, value=value)

def _consul_host(host):
    consul_ip = host.split(':')[0]
    consul_port = int(host.split(':')[1])
    return (consul_ip, consul_port)

def _execute(cmd):
    """ Execute command """
    proc = subprocess.Popen(cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )
    out, err = proc.communicate()
    return (proc.returncode, out.strip(), err.strip())

def _execute_mysql_cmd(cmd):
    """ Execute gluster command """
    cmd = ["mysql"] + cmd
    return _execute(cmd)

def _execute_mysqldump_cmd(cmd):
    """ Execute gluster command """
    cmd = ["mysqldump"] + cmd
    return _execute(cmd)

def _mysql_grant(admin_user="root",
        admin_pass=None,
        admin_host=None,
        grant_user=None,
        grant_pass=None,
        grant="REPLICATION SLAVE"):

    SELECT_SQL = "select user from mysql.user where user='%s';" % grant_user

    SQL = "CREATE USER '%s' @'%%' IDENTIFIED BY '%s'" % (grant_user, grant_pass)

    if admin_user == "root" and admin_pass == "":
        cmd_op = ["-u", admin_user, "-h", admin_host, "-e"]
    else:
        cmd_op = ["-u", admin_user, "-p"+admin_pass,"-h", admin_host, "-e"]

    cmd = cmd_op + [SELECT_SQL]
    rc, out, err = _execute_mysql_cmd(cmd)
    if rc != 0:
        print(rc, out, err)
        root_logger.error("select %s error:%s", (grant_user, err))
        return False
    if out == "":
        cmd = cmd_op + [SQL]
        rc, out, err = _execute_mysql_cmd(cmd)
        if rc != 0:
            print(rc, out, err)
            root_logger.error("create %s error:%s", (grant_user, err))
            return False

    SQL = "GRANT %s ON *.* TO '%s'@'%%'" % (grant, grant_user)
    cmd = cmd_op + [SQL]
    rc, out, err = _execute_mysql_cmd(cmd)
    if rc != 0:
        print(rc, out, err)
        root_logger.error("grant %s error:%s", (grant_user, err))
        return False

    cmd = cmd_op + ["reset master"]
    rc, out, err = _execute_mysql_cmd(cmd)
    if rc != 0:
        print(rc, out, err)
        root_logger.error("reset master error:%s", err)
        return False

    return True

def _discover_service(session, service, tag=None, passing=True):
    result = session.health.service(service=service, tag=tag, passing=passing)
    if not result:
        root_logger.error("Can't found master")
        sys.exit(1)

    return result

def _put_kv(session, key, value):
    session = session

    session.kv.put(key=key, value=value)

def _del_kv(session, key):
    session = session

    session.kv.delete(key=key)

def _get_kv(session, key):
    session = session
    result = session.kv.get(key=key)
    return result

def _del_mysql(session, service, service_id, tag=None):
    admin_host = None
    admin_port = None
    admin_user = None
    admin_pass = None
    admin_key = None
    service = service
    service_id = service_id
    tag = tag

    result = _discover_service(
            session=session,
            service=service,
            tag=tag
            )
    if result:
        result = result[1]
        for i in result:
            if i.get('Service').get('ID') == service_id:
                admin_host = i.get('Service').get('Address').encode('utf8')
                admin_port = i.get('Service').get('Port')
                admin_key = "cluster/%s/%s/admin" % (i.get('Service').get('Service'),
                        i.get('Service').get('ID'))
            else:
                continue
        if admin_key is None:
            root_logger.error("invalid %s" % service_id )
            sys.exit(1)
    kv = _get_kv(session, key=admin_key)
    admin_user = kv[1].get('Value').split('::')[0]
    admin_pass = kv[1].get('Value').split('::')[1]

    if tag == "slave":
        SQL = "stop slave;reset slave"
    else:
        SQL = "stop slave; reset slave"

    cmd = ["-h",admin_host , "-P", str(admin_port), "-u", admin_user, "-p"+admin_pass, "-e"] + [SQL]
    rc, out, error = _execute_mysql_cmd(cmd)
    if rc != 0:
       root_logger.error("reset slave  error:%s" % error)
       sys.exit(1)
    _del_kv(session, admin_key)

def _fmt_status(body):
    status = {}
    node = []
    result = body
    for i in result:
        status['ID'] = i.get('Service').get('ID')
        status['IP'] = i.get('Service').get('Address')
        status['Port'] = i.get('Service').get('Port')
        status['Status'] = i.get('Checks')[0].get('Status')
        status['Tag'] = i.get('Service').get('Tags')
        node.append(status)
        status = {}
    return node

def cluster_create(args):
    """
    创建指定名称集群
    """
    session = None  #连接consul 的回话

    consul_ip = None # consul 连接地址
    consul_port = None # consul 连接端口

    if args.log:
        log_level = args.log
        _config_log(log_level)

    if args.consul:
        consul_ip, consul_port = _consul_host(args.consul)

    if consul_ip is not None and consul_port is not None:
        session = _conn_consul(host=consul_ip, port=consul_port)
    else:
        root_logger.error("Please give consul address")
        sys.exit(0)

    # 根据mode 类型注册服务
    _register_service(session, args)

    #根据mode 类型配置MySQL
    if args.mode and args.mode == MYSQL_MODE.get('master'):
        return _cluster_master(session, args)

    if args.mode and args.mode == MYSQL_MODE.get('slave'):
        return _cluster_slave(session, args)

def cluster_add(args):

    session = None  #连接consul 的回话
    consul_ip = None # consul 连接地址
    consul_port = None # consul 连接端口

    if args.log:
        log_level = args.log
        _config_log(log_level)

    if args.consul:
        consul_ip, consul_port = _consul_host(args.consul)

    if consul_ip is not None and consul_port is not None:
        session = _conn_consul(host=consul_ip, port=consul_port)
    else:
        root_logger.error("Please give consul address")
        sys.exit(0)

    # 发现主，如果不存在，则异常
    result = _discover_service(
            session=session,
            service=args.name,
            tag="master"
            )
    if result:
        _register_service(session, args)

    if args.mode and args.mode == MYSQL_MODE.get('slave'):
        return _cluster_slave(session, args)
    else:
        root_logger("Only add slave")
        sys.exit(1)
    sys.exit(0)

def cluster_del(args):
    session = None  #连接consul 的回话
    consul_ip = None # consul 连接地址
    consul_port = None # consul 连接端口

    if args.log:
        log_level = args.log
        _config_log(log_level)

    if args.consul:
        consul_ip, consul_port = _consul_host(args.consul)

    if consul_ip is not None and consul_port is not None:
        session = _conn_consul(host=consul_ip, port=consul_port)
    else:
        root_logger.error("Please give consul address")
        sys.exit(0)

    if args.mode == MYSQL_MODE.get("slave"):
        _del_mysql(session, service=args.name, service_id=args.service_id, tag="slave")
        _deregister_service(session, service_id=args.service_id)
    else:
        root_logger.error("Only del slave")
    sys.exit(0)

def cluster_destroy(args):
    session = None  #连接consul 的回话
    consul_ip = None # consul 连接地址
    consul_port = None # consul 连接端口

    if args.log:
        log_level = args.log
        _config_log(log_level)

    if args.consul:
        consul_ip, consul_port = _consul_host(args.consul)

    if consul_ip is not None and consul_port is not None:
        session = _conn_consul(host=consul_ip, port=consul_port)
    else:
        root_logger.error("Please give consul address")
        sys.exit(0)

    # 判断是否使用-f 标记
    result = _discover_service(session=session,service=args.name)
    result = result[1]
    cluster_key_dir = "cluster/%s" % args.name
    if args.force:
        for i in result:
            service_id = i.get('Service').get('ID')
            _del_mysql(session, service=args.name, service_id=service_id)
            _deregister_service(session, service_id=service_id)
            _del_kv(session=session, key=cluster_key_dir)
    else:
        for i in result:
            tag = i.get('Service').get('Tags')[0]
            if tag == "slave":
                root_logger.error("Can't destroy cluster %s, if have slave%s" % (
                    args.name, i.get('Service').get('ID')))
                sys.exit(1)
            service_id = i.get('Service').get('ID')
            _del_mysql(session, service=args.name, service_id=service_id)
            _deregister_service(session, service_id=service_id)
            _del_kv(session=session, key=cluster_key_dir)
    sys.exit(0)

def cluster_status(args):
    session = None  #连接consul 的回话
    consul_ip = None # consul 连接地址
    consul_port = None # consul 连接端口
    body = {"Name": args.name}

    if args.log:
        log_level = args.log
        _config_log(log_level)

    if args.consul:
        consul_ip, consul_port = _consul_host(args.consul)

    if consul_ip is not None and consul_port is not None:
        session = _conn_consul(host=consul_ip, port=consul_port)
    else:
        root_logger.error("Please give consul address")
        sys.exit(0)

    result = _discover_service(
            session=session,
            service=args.name,
            )
    result = result[1]

    node = _fmt_status(result)
    if args.service_id:
        for i in node:
            if i.get('ID') == args.service_id:
                body['Node'] = i
                print(body)
                return 
    else:
        body['Node'] = node
        print(body)
        return 

def _config_log(level, log_file='cluster_mysql.log'):

    global root_logger

    # 创建root_logger对象
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # 创建文件handler

    file_handler = log_handlers.TimedRotatingFileHandler(log_file, 'D', 1 )
    file_handler.setLevel(level)

    # 创建控制台handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)


    # 配置handler 输出格式
    formatters = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s \
            - [%(filename)s:%(lineno)s] - %(funcName)s - %(message)s')
    file_handler.setFormatter(formatters)
    console_handler.setFormatter(formatters)

    # 给root_logger对象配置handler
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

if __name__ == '__main__':
    main()
