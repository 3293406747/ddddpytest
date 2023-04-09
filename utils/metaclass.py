from abc import ABC

from utils.single_instance import SingletonMeta


class Singleton(metaclass=SingletonMeta):
	...


class SingletonABCMeta(type(ABC), type(Singleton)):
	pass
