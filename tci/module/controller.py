from flask import Blueprint, json, request

from module.logger import *
from module.db import Connect
from module.config import Config
import threading
import time

log = get_logger()
bc = Blueprint('bc', __name__)
lock = threading.Lock()
connect = Connect()
conf = Config().conf


# 设备加工看板
@logger
@bc.route("/deviceMachining", methods=["POST"])
def device_machining():
    lock.acquire()
    # 获取参数
    prams = request.json
    # 获取当前页
    page_num = int(prams.get("page_num")) - 1
    page_size = int(prams.get("page_size"))
    # 重新计算page_num
    page_num = page_num * page_size
    current_time = time.strftime("%Y%m%d", time.localtime())
    base_sql = conf.get("sys")['sql']['device_machining'][0] % (current_time)
    page_sql = "SELECT TOP %d B.* FROM (%s) B WHERE B.ZROW > %d" % (page_size, base_sql, page_num)
    count_sql = "SELECT count(1) total from (%s) as A" % (base_sql)
    # 排产开工设备台数 停机数
    c_run_stop = conf.get("sys")["sql"]['device_machining'][1] %(current_time)
    # 排产无开工设备台数
    c_not_work = conf.get("sys")["sql"]['device_machining'][2] %(current_time)
    data = {}
    data['data'] = connect.select_all(page_sql)
    data['total'] = connect.select_all(count_sql)[0].get("total")
    data["run_stop"] = connect.select_all(c_run_stop)
    data["not_work"] = connect.select_all(c_not_work)
    lock.release()
    return json.dumps(data)

# 设备产能异常看板
@logger
@bc.route("/deviceUnusual", methods=["POST"])
def device_unusual():
    lock.acquire()
    # 获取参数
    prams = request.json
    # 获取当前页
    page_num = int(prams.get("page_num")) - 1
    page_size = int(prams.get("page_size"))
    # 重新计算page_num
    page_num = page_num * page_size
    current_time = time.strftime("%Y%m%d", time.localtime(time.time()-86400))
    base_sql = conf.get("sys")['sql']['device_unusual'][0] % (current_time)
    page_sql = "SELECT TOP %d B.* FROM (%s) B WHERE B.ZROW > %d" % (page_size, base_sql, page_num)
    count_sql = "SELECT count(1) total from (%s) as A" % (base_sql)
    uaual_count = conf.get("sys")["sql"]['device_unusual'][1] %(current_time)
    unuaual_count = conf.get("sys")["sql"]['device_unusual'][2] %(current_time)
    data = {}
    data['data'] = connect.select_all(page_sql)
    data['total'] = connect.select_all(count_sql)[0].get("total")
    data["uaual"] = connect.select_all(uaual_count)
    data["unusual"] = connect.select_all(unuaual_count)
    lock.release()
    return json.dumps(data)

# 人员产能异常看板
@logger
@bc.route("/personUnusual", methods=["POST"])
def person_unusual():
    lock.acquire()
    # 获取参数
    prams = request.json
    # 获取当前页
    page_num = int(prams.get("page_num")) - 1
    page_size = int(prams.get("page_size"))
    # 重新计算page_num
    page_num = page_num * page_size
    current_time = time.strftime("%Y%m%d", time.localtime(time.time()-86400))
    base_sql = conf.get("sys")['sql']['person_unusual'][0] % (current_time)
    page_sql = "SELECT TOP %d B.* FROM (%s) B WHERE B.ZROW > %d" % (page_size, base_sql, page_num)
    uaual_count = conf.get("sys")["sql"]['person_unusual'][1] %(current_time)
    unuaual_count = conf.get("sys")["sql"]['person_unusual'][2] %(current_time)
    data = {}
    data['data'] = connect.select_all(page_sql)
    data['total'] = connect.select_all(count_sql)[0].get("total")
    data["uaual"] = connect.select_all(uaual_count)
    data["unusual"] = connect.select_all(unuaual_count)
    lock.release()
    return json.dumps(data)

