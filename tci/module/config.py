#!/usr/bin/ python
# vim: set fileencoding:utf-8
import os
import yaml


class Config(object):
    conf=None

    def __init_config(self):
        if self.conf is None:
            self.conf = dict()
            conf_name = "conf"
            # 获取配置文件
            path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), conf_name+".yml")
            tmp = None
            # 打开配置文件
            with open(file=path, mode='rt', encoding='utf-8') as f:
                # 用yaml读取出来,再转为字典对象,获取配置中的db配置
                tmp = dict(yaml.load(f))
                # 获取指定配置文件
                active = tmp.get('conf').get('profiles').get('active')
                conf_name = conf_name+"-"+active
                path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), conf_name+".yml")
                with open(file=path, mode='rt',encoding='utf8') as cf:
                    tmp = dict(yaml.load(cf))
                    db = tmp.get('db') if tmp.get('db') != None else {}
                    web = tmp.get('web') if tmp.get('web') != None else {}
                    sys = tmp.get('sys') if tmp.get('sys') != None else {}
                    self.conf["db"] = db
                    self.conf["web"] = web
                    self.conf["sys"] = sys
                    # 初始化默认配置
                    if db.get('server') is None:
                        self.conf["db"]['server'] = 'localhost'
                    if db.get('port') is None:
                       self.conf["db"]['port'] = 1433
                    if db.get('user') is None:
                        self.conf["db"]['user'] = 'sa'
                    if db.get('password') is None:
                        self.conf["db"]['password'] = ''
                    if db.get('database') is None:
                        self.conf["db"]['database'] = 'db'
                    if db.get('charset') is None:
                        self.conf["db"]['charset'] = 'utf8'

                    # web配置
                    if web.get('host') is None:
                        self.conf["web"]["host"]='0.0.0.0'
                    if web.get('port') is None:
                        self.conf["web"]["port"]=80
                    if web.get('debug') is None:
                        self.conf["web"]["debug"]=True

                    # 系统配置
                    if sys.get("sql") is None:
                        self.conf['sys']["sql"]={}

    def __new__(cls, *args, **kwargs):
        cls.__init_config(cls)
        return object.__new__(cls)
