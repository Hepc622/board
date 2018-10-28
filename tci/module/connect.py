#!/usr/bin/python
# coding: utf-8

import traceback
from decimal import Decimal


# 链接对象
class Connect(object):
    # 链接对象
    __connect = None
    # 是否空闲
    __free = True

    def __new__(cls, *args, **kwargs):
        cls.__connect = args[0]
        return object.__new__(cls)

    # 获取真实的connect链接
    def get_original_conn(self):
        return self.__connect

    # 获取当前的链接是否空闲
    def get_free(self):
        return self.__free

    # 设置当前的链接是否空闲
    def set_free(self):
        self.__free = True

    # 设置为正在使用 
    def set_busy(self):
        self.__free = False

    # 关闭连接,设置为空闲状态
    def close(self):
        self.__free = True

    # 查询所有
    def select_all(self, sql):
        try:
            # 获取当前游标的位置
            cursor = self.__connect.cursor()
            # 执行sql
            cursor.execute(sql)
            # 获取所有的列
            index = cursor.description
            result = []
            for rows in cursor:
                # 组装当前行的字典数据
                row = {}
                for i in range(len(rows)):
                    data = rows[i]
                    # 如果是数字对象转为int
                    if type(data) == Decimal:
                        data = int(data)
                    row[index[i][0]]=data
                result.append(row)
        except Exception:
            traceback.print_exc()
        finally:
            cursor.close()
        # 返回数据
        return result

        # 插入数据
    def insert(self, sql):
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
    def update(self, sql):
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
