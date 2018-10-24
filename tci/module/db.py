#!/usr/bin/python
# coding: utf-8

import pymssql
import re
import traceback
from module.config import Config
import module.logger as logger
from decimal import Decimal
import os
import yaml

conf = Config().conf
log = logger.get_logger()


# 链接对象
class Connect(object):
    # 链接对象
    __connect = None

    def __new__(cls, *args, **kwargs):
        db = conf['db']
        cls.__connect = pymssql.connect(server=db["server"], port=db["port"],
                                       user=db["user"], password=db["password"],
                                      database=db["database"])
        return object.__new__(cls)

    # 处理sql
    def deal_sql(self, sql, params):
        re_compile = re.compile("[\'=-]")
        for item in params:
            # 判断是否有敏感字符
            if len(re_compile.findall(item)) > 0:
                return None
        if sql.find("?") > 0:
            for item in params:
                sql = sql.replace("?", "'" + str(item) + "'", 1)
            return sql
        elif sql.find("#") > 0:
            # 创建正则表达式
            re_compile = re.compile("#[\w]+")
            # 将参数设置到sql语句中
            for item in params[0]:
                for key in re_compile.findall(sql):
                    if key.find(item) > 0:
                        sql = sql.replace(key, "'" + str(params[0][item]) + "'", 1)
            # 将没有的参数至为1=1
            re_compile = re.compile("[\w]+=#[\w]+")
            findall = re_compile.findall(sql)
            for repl in findall:
                sql = sql.replace(repl, '1=1', 1)
            return sql
        return sql

    # 查询所有
    def select_all(self, sql, *params):
        sql = self.deal_sql(sql, params)
        try:
            # 获取当前游标的位置
            cursor = self.__connect.cursor()
            # 执行sql
            cursor.execute(sql)
            # 获取所有的列
            index = cursor.description
            result = []
            rows = cursor.fetchall()
            # 获取所有数据数据
            for res in rows:
                row = {}
                for i in range(len(index)):
                    data = res[i]
                    if type(data) == Decimal:
                        data = int(data)
                    row[index[i][0]] = data

                result.append(row)
            # 返回数据
            return result
        except Exception:
            traceback.print_exc()
        finally:
            cursor.close()
            log.debug("close")

            # 插入数据

    def insert(self, sql, *params):
        sql = self.deal_sql(sql, params)
        try:
            # 获取当前游标的位置
            cursor = self.__connect.cursor()
            # 执行sql
            cursor.execute(sql)
            # 将数据提交到数据库中
            self.__connect.commit()
            return True
        except Exception:
            traceback.print_exc()
            # 回滚数据
            self.__connect.rollback()
            return False
        finally:
            # 关闭链接
            cursor.close()

            # 更新数据

    def update(self, sql, *params):
        sql = self.deal_sql(sql, params)
        try:
            # 获取当前游标的位置
            cursor = self.__connect.cursor()
            # 执行sql
            cursor.execute(sql)
            # 将数据提交到数据库中
            self.__connect.commit()
            return True
        except Exception:
            traceback.print_exc()
            # 回滚数据
            self.__connect.rollback()
            return False
        finally:
            # 关闭链接
            cursor.close()



