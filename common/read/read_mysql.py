from common.mysql.mysql import Mysql
from common.read.read_config import read_config


class ReadMysql:
	""" sql查询 """
	__instance = None
	__init_flag = True

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = object.__new__(cls)
			return cls.__instance
		else:
			return cls.__instance

	def __init__(self):
		if ReadMysql.__init_flag:
			config = read_config()["mysql"]
			if not config:
				raise Exception("config/local.yaml中未配置数据库连接")
			self.__mysql = Mysql(**config)
			ReadMysql.__init_flag = False

	def execute(self,sql,key,item=None):
		""" 执行sql查询 """
		result = self.__mysql.select(sql)
		if item is None:
			keylist = [dict(dt).get(key) for dt in result]
			return keylist
		else:
			value = dict(result[item]).get(key)
			return value