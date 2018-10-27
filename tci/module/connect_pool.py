#!/usr/bin/python
# coding: utf-8

import os
import pymysql
import pymssql
import threading
import time
import traceback
import yaml

from module.connect import Connect
from module.config import Config
from module.logger import *
log = get_logger()
# 链接池
class ConnectPool(object):
    # 这是yml配置文件读出来后,转为字典
    __db_dict = None
    # 链接池
    __connects = []
    # 当前对象锁
    __lock = threading.Lock()
    # 连接池对象
    __pool = None

    def __new__(cls, *args, **kwargs):
        if cls.__pool is None:
            # 调用创建连接池
            cls.__init_pool(cls)
            # 插件对象,实例其父类
            cls.__pool = super(ConnectPool, cls).__new__(cls)
        return cls.__pool

    # 返回连接池总大小
    def get_pool_size(self):
        size = len(self.__connects_using)+len(self.__connects_remain)
        return size

    # 获取连接池所剩的数量
    def get_pool_free(self):
        count = 0
        for connect in self.__connects:
            if connect.get_free():
                count += 1
        return count

    # 获取连接池使用的数量
    def get_pool_using(self):
        count = 0
        for connect in self.__connects:
            if not connect.get_free():
                count += 1
        return count

    # 初始化方法,创建链接池
    def __init_pool(self):
        # 初始化默认配置
        self.__db_dict = Config().get('db')
        try:
            # 获取配置文件配置参数
            p_max = self.__db_dict.get('maxPoolSize')
            p_min = self.__db_dict.get('minPoolSize')
            p_init = self.__db_dict.get('initPoolSize')
            # 判断一下连接池最小值是否大于连接池最大值
            if p_min > p_max:
                raise Exception('''链接池的最小值大于最大值,请重新设定''')
            # 初始化链接池大小
            for i in range(p_init):
                connect = self.__create_connect(self)
                # 判断链接池的大小是否小于最大值
                if len(self.__connects) <= p_max:
                    self.__connects.append(connect)
                else:
                    raise Exception('初始化大小,大于最大值')
        except IOError:
            # 打印异常
            traceback.print_exception()
            # 打印执行过程
            traceback.print_exc()
        log.debug("连接池初始化完成")

    # 获取链接
    def get_connect(self):
        # 开启同步
        self.__lock.acquire()
        # 需要返回的数据链接
        connect = None
        # 获取一个空闲的连接,不知道是否有效
        connect = self.__get_real_connect()
        if connect is None:
            # 如果没有空闲连接了,就看看链接池的最大是有没有达到配置的最大值,没有的话就去创建,有的等待其他连接释放连接
            if len(self.__connects) < self.__db_dict.get("maxPoolSize"):
                # 没有达到最大值,所以就再去创建链接了
                connect = self.__create_connect()
                #  把状态设置为忙碌
                connect.set_busy()
                self.__connects.append(connect)
            else:
                # 达到最大值了,在这里等等吧
                while connect is None:
                    time.sleep(self.__db_dict.get("waitTime"))
                    # 获取线程池也有的空闲连接
                    connect = self.__get_real_connect()
        else:
            #  把状态设置为忙碌
            connect.set_busy()
        #  释放,关闭同步
        self.__lock.release()
        return connect

    # 获取真实有效的连接
    def __get_real_connect(self):
        connect = None
        # 获取线程池也有的空闲连接
        for index in range(len(self.__connects)):
            # 获取一个连接
            conn = self.__connects[index];
            # 判断是否为空闲连接
            if conn.get_free():
                try:
                    # 如果ping不通说明是无效链接,如果ping通了直接返回就行
                    conn.get_original_conn().cursor()
                except Exception:
                    traceback.print_exc()
                    # 如果是无用的连接就将他删除
                    self.__connects.remove(conn)
                    # 没有ping通,重新生成一个链接
                    conn = self.__create_connect()
                    # 添加到池中去
                    self.__connects.append(conn)
                connect = conn
                break
        return connect
    # 显示数据池中的链接情况
    def __show_pool_num(self,strs,connect):
        count = 0
        for con in self.__connects:
            if con.get_free():
                count += 1
        log.debug("当前线程"+threading.current_thread().name+": "+str(connect)+
                  " 当前连接池数总数: "+str(len(self.__connects))+
                  " 正在使用的链接数: "+str(len(self.__connects)-count)+
                  " 空闲连接数: "+str(count))

    # 创建链接
    def __create_connect(self):
        kind = self.__db_dict.get('kind')
        user = self.__db_dict.get('user')
        password = self.__db_dict.get('password')
        host = self.__db_dict.get('host')
        port = self.__db_dict.get('port')
        databases = self.__db_dict.get('database')
        charset = self.__db_dict.get('charset')
        con = None
        if kind == "mysql" :
            con = pymysql.connect(host=host, port=port, user=user, passwd=password, db=databases, charset=charset)
        elif kind == "sqlserver" :
            con = pymssql.connect(server=host, port=port,user=user, password=password,database=databases, charset=charset)
        return Connect(con) 