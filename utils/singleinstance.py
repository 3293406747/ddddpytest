"""
单例模式装饰器
"""
import functools
import threading
# import contextlib


def singleton(cls:type):
	"""单例模式装饰器"""
	if not isinstance(cls,type):
		raise TypeError
	instance = None
	lock = threading.Lock()		# 生成锁

	@functools.wraps(cls)
	def get_instance(*args, **kwargs):
		nonlocal instance
		if instance is None:		# 避免每次获取锁消耗资源
			with lock:
			# with get_lock():
				if instance is None:		# 对这段代码加锁
					instance = cls(*args,**kwargs)
		return instance

	# @contextlib.contextmanager	# 上下文管理器 与yield一起用
	# def get_lock():
	# 	lock.acquire()		# 获取锁
	# 	try:
	# 		yield
	# 	finally:
	# 		lock.release()		# 解锁

	return get_instance