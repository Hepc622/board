#!/usr/bin/ python
# vim: set fileencoding:utf-8
import time
from module.connect_pool import ConnectPool
from module.logger import *
from module.config import Config
conf = Config()
connect = ConnectPool()

@logger
def test():
	connect = ConnectPool().get_connect() 
	data = connect.select_all("select * from [dbo].[ZboardMachineWork ] ('20181024')")
	print(data)

test()