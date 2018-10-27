#!/usr/bin/ python
# vim: set fileencoding:utf-8
import time
from module.connect_pool import ConnectPool
from module.config import Config
conf = Config()
connect = ConnectPool().get_connect()  
if __name__ == '__main__':

	start=time.time()
	for x in range(1,20):
		connect = ConnectPool().get_connect() 
	end=time.time()
	# print(data)
	print(end-start)
