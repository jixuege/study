#!/usr/bin/env python
# coding=utf8


"""
此脚本用于配置Redis 主从复制,主要功能有:
    --name cluster_name --consul 192.168.1.10:8500 create --mode MASTER  创建主
    --name cluster_name --consul 192.168.1.10:8500 create --mode SLAVE   创建从
    --name cluster_name --consul 192.168.1.10:8500 add    --mode SLAVE   添加从
    --name cluster_name --consul 192.168.1.10:8500 del    --mode SLAVE   删除从
    --name cluster_name --consul 192.168.1.10:8500 destroy               删除集群配置
    --name cluster_name --consul 192.168.1.10:8500 status                查看集群状态
"""

import sys
import argon
import consul
import logging
import subprocess



# Set up root logger
log_format = '%(asctime)s %(name)s [%(levelname)s]: %(message)s'
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
formatter = logging.Formatter(log_format)

# Set up console output
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
root_logger.addHandler(console_handler)

REDIS_MODE = {
        "master": "MASTER",
        "slave": "SLAVE"
        }

def main():
    app = argon.App(description="Redis replication configure manage")

    # 定义全局选项
    app.arg("--name", default=False, required=True,
            help="Cluster unique name")

    app.arg("--consul", default=False, required=True,
            help="Consul host address and port")

    app.arg("--log", default=False, choices=["INFO", "WARING", "ERROR"],
            help="Open log set log level")

    # 定义 create sub commmand 和选项
    with app.command("create") as create:
        create.arg("--mode", default=False, required=True, choices=["MASTER", "SLAVE"],
                help="Redis replication role")\
                        .arg("--service_id", default=False, required=True,
                                help="register server name")\
                        .arg("--ip", default=False, help="Redis host address")\
                        .arg("--port", default=6379, help="Redis host address port")\
                        .arg("--admin_user", default="", help="Redis administrator user")\
                        .arg("--admin_pass", default="", help="Redis administrator password")\
                        .handler(cluster_create)


    # 定义 add sub command 和选项
    with app.command("add") as add:
        add.arg("--mode", default="SLAVE", required=True, choices=["SLAVE"],
                help="Add Redis slave role")\
                        .arg("--service_id", default=False, required=True,
                                help="register server name")\
                        .arg("--ip", default=False, help="Redis host address")\
                        .arg("--port", default=6379, help="Redis host address port")\
                        .arg("--admin_user", default="", help="Redis administrator user")\
                        .arg("--admin_pass", default="", help="Redis administrator password")\
                        .handler(cluster_add)

    # 定义 del sub command 和选项
    with app.command("del") as dele:
        dele.arg("--mode", default="SLAVE", required=True,  choices=["SLAVE"],
                help="Del Redis slave role")\
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

def _discover_service(session, service, tag=None, passing=True):
    result = session.health.service(service=service, tag=tag, passing=passing)
    if not result:
        root_logger.error("Can't found master")
        sys.exit(1)

    return result

def _consul_host(host):
    consul_ip = host.split(':')[0]
    consul_port = int(host.split(':')[1])
    return (consul_ip, consul_port)

def _execute(cmd):
    """ Execute command """
    print(cmd)
    proc = subprocess.Popen(cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )
    out, err = proc.communicate()
    return (proc.returncode, out.strip(), err.strip())

def _execute_redis(cmd):
    cmd = ["redis-cli"] + cmd
    return _execute(cmd)

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
        root_logger.error("Please give Redis address")
        sys.exit(0)

    if args.mode == REDIS_MODE.get("master"):
        reg_tags = ["master"]

    if args.mode == REDIS_MODE.get("slave"):
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

def _deregister_service(session, service_id):

    session = session

    status = session.agent.service.deregister(service_id=service_id)
    if not status:
        root_logger.error("delete register %s error"  % args.name)
        sys.exit(1)

def _put_kv(session, key, value):
    session = session

    session.kv.put(key=key, value=value)

def _del_kv(session, key):
    session = session

    session.kv.delete(key=key)

def _cluster_master(session, args):

    # key 规则: "cluster/args.name/args.service_id/admin"
    # key = "cluster/%s/%s/admin" % (args.name, args.service_id)
    # value = "%s::%s" % (args.admin_user, args.admin_pass)
    # _put_kv(session=session, key=key, value=value)
    pass

def _cluster_slave(session, args):
    master_ip = None
    master_port = None

    result = _discover_service(
            session=session,
            service=args.name,
            tag="master"
            )
    if result:
        result = result[1][0]
        master_ip = result.get('Service').get('Address').encode('utf8')
        master_port = result.get('Service').get('Port')

    cmd = ["-h", args.ip, "-p", str(args.port), "SLAVEOF", master_ip, str(master_port)]
    return _execute_redis(cmd)

def _get_kv(session, key):
    session = session
    result = session.kv.get(key=key)
    return result

def _del_redis(session, service, service_id, tag=None):

    admin_host = None
    admin_port = None
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
            else:
                continue
    if tag == "slave":
        cmd = ["-h", admin_host, "-p", str(admin_port), "SLAVEOF", "NO", "ONE"]
    else:
        cmd = []

    rc, out, error = _execute_redis(cmd)
    if rc != 0:
       root_logger.error("reset slave  error:%s" % error)
       sys.exit(1)

def cluster_create(args):
    """
    创建指定名称集群
    """
    session = None  #连接consul 的回话

    consul_ip = None # consul 连接地址
    consul_port = None # consul 连接端口
    if args.consul:
        consul_ip, consul_port = _consul_host(args.consul)

    if consul_ip is not None and consul_port is not None:
        session = _conn_consul(host=consul_ip, port=consul_port)
    else:
        root_logger.error("Please give consul address")
        sys.exit(0)

    # 根据mode 类型注册服务
    _register_service(session, args)

    #根据mode 类型配置Redis
    if args.mode and args.mode == REDIS_MODE.get('master'):
        return _cluster_master(session, args)


    if args.mode and args.mode == REDIS_MODE.get('slave'):
        return _cluster_slave(session, args)

def cluster_add(args):

    session = None  #连接consul 的回话
    consul_ip = None # consul 连接地址
    consul_port = None # consul 连接端口

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

    if args.mode and args.mode == REDIS_MODE.get('slave'):
        return _cluster_slave(session, args)
    else:
        root_logger("Only add slave")
        sys.exit(1)
    sys.exit(0)

def cluster_del(args):
    session = None  #连接consul 的回话
    consul_ip = None # consul 连接地址
    consul_port = None # consul 连接端口

    if args.consul:
        consul_ip, consul_port = _consul_host(args.consul)

    if consul_ip is not None and consul_port is not None:
        session = _conn_consul(host=consul_ip, port=consul_port)
    else:
        root_logger.error("Please give consul address")
        sys.exit(0)

    if args.mode == REDIS_MODE.get("slave"):
        _del_redis(session, service=args.name, service_id=args.service_id, tag="slave")
        _deregister_service(session, service_id=args.service_id)
    else:
        root_logger.error("Only del slave")
    sys.exit(0)

def cluster_destroy(args):
    session = None  #连接consul 的回话
    consul_ip = None # consul 连接地址
    consul_port = None # consul 连接端口

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
    if args.force:
        for i in result:
            service_id = i.get('Service').get('ID')
            _del_redis(session, service=args.name, service_id=service_id)
            _deregister_service(session, service_id=service_id)
    else:
        for i in result:
            tag = i.get('Service').get('Tags')[0]
            if tag == "slave":
                root_logger.error("Can't destroy cluster %s, if have slave %s" % (
                    args.name, i.get('Service').get('ID')))
                sys.exit(1)
            service_id = i.get('Service').get('ID')
            _del_redis(session, service=args.name, service_id=service_id)
            _deregister_service(session, service_id=service_id)
    sys.exit(0)

def cluster_status(args):
    session = None  #连接consul 的回话
    consul_ip = None # consul 连接地址
    consul_port = None # consul 连接端口
    body = {"Name": args.name}

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

if __name__ == '__main__':
    main()
