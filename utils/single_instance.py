# 单例模式
import functools
import threading


# 单例模式装饰器缺点：1.装饰类无法使用类属性和方法。2.装饰类无法被继承。3.使用装饰器难以调试。
def singleton(cls: type):
	"""单例模式装饰器"""
	instance = None		# 装饰类时instance变为None
	lock = threading.Lock()  # 生成锁

	@functools.wraps(cls)
	def get_instance(*args, **kwargs):
		nonlocal instance
		if instance is None:  # 避免每次获取锁消耗资源
			with lock:
			# with get_lock():
				if instance is None:  # 对这段代码加锁
					instance = cls(*args, **kwargs)
		return instance

	# @contextlib.contextmanager	# 上下文管理器 与yield一起用
	# def get_lock():
	# 	lock.acquire()		# 获取锁
	# 	try:
	# 		yield
	# 	finally:
	# 		lock.release()		# 解锁

	return get_instance

# 继承元类
class SingletonMeta(type):
	_instances = {}
	_instance_lock = threading.Lock()

	def __call__(cls, *args, **kwargs):
		# 类调用时判断类是否在_instances中，不在_instances中时才调用
		if cls not in cls._instances:
			with SingletonMeta._instance_lock:
				if cls not in cls._instances:
					cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

# 继承元类 写法二 子类会继承元类的_instances属性
# class SingletonMeta(type):
# 	_instance_lock = threading.Lock()
#
# 	def __init__(cls,*args,**kwargs):
# 		super(SingletonMeta, cls).__init__(*args,**kwargs)
# 		cls._instances = None	# 被继承时instance变为None
#
# 	def __call__(cls, *args, **kwargs):
# 		if cls._instances is None:
# 			with SingletonMeta._instance_lock:
# 				if cls._instances is None:
# 					cls._instances = super(SingletonMeta, cls).__call__(*args, **kwargs)
# 		return cls._instances
