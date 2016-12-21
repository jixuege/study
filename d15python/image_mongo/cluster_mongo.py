#!/usr/bin/env python
# coding=utf8

"""
此脚本用于配置MySQL 主从复制,主要功能有:
    --name cluster_name --consul 192.168.1.10:8500 create               创建集群并加入集群
    --name cluster_name --consul 192.168.1.10:8500 add                  添加节点到集群
    --name cluster_name --consul 192.168.1.10:8500 del                  删除节点从指定集群
    --name cluster_name --consul 192.168.1.10:8500 destroy              删除集群配置
    --name cluster_name --consul 192.168.1.10:8500 status               查看集群状态
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


def main():
    app = argon.App(description="Mongo replication cluster configure manage")

    # 定义全局选项
    app.arg("--name", default=False, required=True,
            help="Cluster unique name")

    app.arg("--consul", default=False, required=True,
            help="Consul host address and port")

    app.arg("--log", default=False, choices=["INFO", "WARING", "ERROR"],
            help="Open log set log level")

    # 定义 create sub commmand 和选项
    with app.command("create") as create:
        create.arg("--service_id", default=False, required=True,
                                help="register server name")\
                        .arg("--repl_name", default="rs0", help="Mongo replication name")\
                        .arg("--ip", default=False, required=True, help="Mongo host address")\
                        .arg("--port", default=27017, help="Mongo host address port")\
                        .arg("--admin_user", default="", help="Mongo administrator user")\
                        .arg("--admin_pass", default="", help="Mongo administrator password")\
                        .handler(cluster_create)


    # 定义 add sub command 和选项
    with app.command("add") as add:
        add.arg("--service_id", default=False, required=True,
                                help="register server name")\
                        .arg("--repl_name", default="rs0", help="Mongo replication name")\
                        .arg("--ip", default=False, required=True, help="Mongo host address")\
                        .arg("--port", default=27017, help="Mongo host address port")\
                        .arg("--admin_user", default="", help="Mongo administrator user")\
                        .arg("--admin_pass", default="", help="Mongo administrator password")\
                        .handler(cluster_add)

    # 定义 del sub command 和选项
    with app.command("del") as dele:
        dele.arg("--service_id", default=False, required=True,
                                help="register server name")\
                        .arg("--repl_name", default="rs0", help="Mongo replication name")\
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
        root_logger.error("Please give Mongo address")
        sys.exit(0)

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

def _execute_mongo(cmd):
    cmd = ["mongo"] + cmd
    return _execute(cmd)

def _discover_service(session, service, tag=None, passing=True):
    result = session.health.service(service=service, tag=tag, passing=passing)
    if not result:
        root_logger.error("Can't found master")
        sys.exit(1)

    return result

def _mongo_initiate(rsname, ip, port):
    
    rsname = rsname
    ip = ip
    port = port
    host = ip+":"+str(port)

    initiate_arg = {'_id': rsname, 'version': 1, 'members':[{'_id' :0, 'host': host}] }
    initiate_command = 'rs.initiate(%s)' % initiate_arg

    cmd = ['--eval', initiate_command]
    return _execute_mongo(cmd)

def _mongo_add(host, ip, port):
    
    host = host

    add_host = ip+":"+str(port)

    add_arg = add_host
    initiate_command = 'rs.add("%s")' % add_arg

    cmd = ["--host", host, '--eval', initiate_command]
    return _execute_mongo(cmd)

def _mongo_remove(host, ip, port):
    host = host

    remove_host = ip+":"+str(port)

    remove_arg = remove_host
    initiate_command = 'rs.remove("%s")' % remove_arg

    cmd = ["--host", host, '--eval', initiate_command]
    return _execute_mongo(cmd)

def _mongo_ismaster(host):
    host = host
    initiate_command = 'rs.isMaster()["primary"]'
    cmd = ["--host", host, '--quiet', '--eval', initiate_command]
    return _execute_mongo(cmd)

def _parse_host(result):

    host = ""

    if result:
        result = result[1]
        num = len(result)
        n = 0
        for i in result:
            n += 1
            if n == num:
                host += i.get('Service').get('Address').encode('utf8') +':'\
                        +str(i.get('Service').get('Port'))
            else:
                host += i.get('Service').get('Address').encode('utf8') +':'\
                        +str(i.get('Service').get('Port')) + ','
    return host

def _parse_host_one(result):
    result = result[0]
    if result:
        host = result.get('Service').get('Address').encode('utf8') +':'\
                +str(result.get('Service').get('Port'))
    else:
        return None
    return host

def _fmt_status(body):
    status = {}
    node = []
    result = body

    host = _parse_host_one(result)
    master_host = _mongo_ismaster(host=host)[1]

    for i in result:
        status['ID'] = i.get('Service').get('ID')
        status['IP'] = i.get('Service').get('Address')
        status['Port'] = i.get('Service').get('Port')
        status['Status'] = i.get('Checks')[0].get('Status')
        if master_host == "%s:%s" % (i.get('Service').get('Address'),i.get('Service').get('Port') ):
            status['Tag'] = ["master"]
        else:
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

    if args.consul:
        consul_ip, consul_port = _consul_host(args.consul)

    if consul_ip is not None and consul_port is not None:
        session = _conn_consul(host=consul_ip, port=consul_port)
    else:
        root_logger.error("Please give consul address")
        sys.exit(0)

    # 以args.name 为server name , 以args.service_id 为service_id 注册服务
    _register_service(session, args)

    rc, out, error = _mongo_initiate(rsname=args.repl_name, ip=args.ip, port=args.port)
    if rc != 0:
        root_logger.error("initiate mongo replication cluster error:%s" % error)
        sys.exit(1)
        
    sys.exit(0)

def cluster_add(args):

    session = None  #连接consul 的回话
    consul_ip = None # consul 连接地址
    consul_port = None # consul 连接端口

    master_host = None

    if args.consul:
        consul_ip, consul_port = _consul_host(args.consul)

    if consul_ip is not None and consul_port is not None:
        session = _conn_consul(host=consul_ip, port=consul_port)
    else:
        root_logger.error("Please give consul address")
        sys.exit(0)

    # 得到集群现有的主机信息 host 的格式为'host:port, host:port, ...'
    result = _discover_service(session=session, service=args.name)
    result = result[1]
    host = _parse_host_one(result)

    master_host = _mongo_ismaster(host=host)[1]

    rc , out, error =_mongo_add(host=master_host, ip=args.ip, port=args.port)
    if rc != 0:
        root_logger.error("Mongo rs.add error:%s " % error)
        sys.exit(1)

    # 以args.name 为server name , 以args.service_id 为service_id 注册服务
    _register_service(session, args)

    sys.exit(0)

def cluster_del(args):
    session = None  #连接consul 的回话
    consul_ip = None # consul 连接地址
    consul_port = None # consul 连接端口

    rm_host_ip = None
    rm_host_port = None

    master_host = None

    if args.consul:
        consul_ip, consul_port = _consul_host(args.consul)

    if consul_ip is not None and consul_port is not None:
        session = _conn_consul(host=consul_ip, port=consul_port)
    else:
        root_logger.error("Please give consul address")
        sys.exit(0)

    # 得到集群随机主机信息 host 的格式为'host:port'
    # 通过随机主机得到master主机
    result = _discover_service(session=session, service=args.name)
    result = result[1]
    host = _parse_host_one(result)

    master_host = _mongo_ismaster(host=host)[1]


    # 得到删除主机信息
    if result:
        for i in result:
            if i.get('Service').get('ID') == args.service_id:
                rm_host_ip = i.get('Service').get('Address')
                rm_host_port = i.get('Service').get('Port')

    if rm_host_ip is None or rm_host_port is None:
        root_logger.error("invalid %s" % args.service_id)
        sys.exit(1)

    # 如果删除主机是master 则异常
    if master_host == "%s:%s" %(rm_host_ip, str(rm_host_port)):
        root_logger.error("Delete %s is master, can't delete." % master_host)
        sys.exit(1)

    rc, out, error =_mongo_remove(
            host=master_host,
            ip=rm_host_ip,
            port=rm_host_port
            )
    if rc != 0:
        root_logger.error("Mongo rs.remove error:%s " % error)
        sys.exit(1)

    _deregister_service(session=session, service_id=args.service_id)

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

    # 查询集群所有信息
    result = _discover_service(session=session,service=args.name)
    result = result[1]

    # 取得master
    host = _parse_host_one(result)
    master_host = _mongo_ismaster(host=host)[1]

    # 处理每一个节点
    for i in result:
        rm_host_ip = i.get('Service').get('Address')
        rm_host_port = i.get('Service').get('Port')
        service_id = i.get('Service').get('ID')
        if master_host == "%s:%s" % (rm_host_ip, str(rm_host_port)):
            if args.force:
                _deregister_service(session=session, service_id=service_id)
                continue
            else:
                root_logger.error("Delete %s is master, can't delete." % master_host)
                sys.exit(1)
        else:
            rc, out, error =_mongo_remove(
                    host=master_host,
                    ip=rm_host_ip,
                    port=rm_host_port
                    )
            if rc != 0:
                root_logger.error("Mongo rs.remove error:%s " % error)
                sys.exit(1)
            _deregister_service(session=session, service_id=service_id)
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
