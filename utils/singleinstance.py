"""
单例模式装饰器
"""
import functools
import threading
import contextlib


def singleton(cls):
	instances = {}
	lock = threading.Lock()		# 生成锁

	@contextlib.contextmanager	# 上下文管理器 与yield一起用
	def get_lock():
		lock.acquire()		# 获取锁
		try:
			yield
		finally:
			lock.release()		# 解锁

	@functools.wraps(cls)
	def getInstance(*args, **kwargs):
		with get_lock():
			if not cls in instances:
				instances[cls] = cls(*args,**kwargs)
			return instances[cls]
	return getInstance