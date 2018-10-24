#!/usr/bin/ python
# vim: set fileencoding:utf-8
import time

if __name__ == '__main__':
	print(time.localtime(time.time()-86400))
	# print((time.localtime(time.time()-8640000)).strftime("%Y-%m-%d"))