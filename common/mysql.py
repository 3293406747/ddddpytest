import pymysql
from common.read import read_config


class Mysql:
	""" mysql数据库操作 """
	def __init__(self,host,port,user,password,db,charset='utf8'):
		""" 连接mysql数据库 """
		try:
			self.conn = pymysql.connect(
				host=host,port=port,user=user,password=password,db=db, charset=charset
			)
			self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
		except Exception as why:
			msg = f"数据库连接失败，原因:{why}"
			raise Exception(msg) from None

	def select(self, sql):
		""" 读取table中数据 """
		try:
			self.cursor.execute(sql)
			r = self.cursor.fetchall()
			return r
		except Exception as why:
			msg = f"数据查询失败，原因:{why}"
			raise Exception(msg) from None

	def commit(self, sql):
		""" 执行sql """
		try:
			self.cursor.execute(sql)
			self.conn.commit()
		except Exception as why:
			self.conn.rollback()
			msg = f"sql执行失败，原因:{why}"
			raise Exception(msg) from None


	def __del__(self):
		if hasattr(Mysql, "cursor") and self.cursor:
			try:
				self.cursor.close()
			except Exception as why:
				msg = f"cursor关闭失败，原因:{why}"
				raise Exception(msg) from None
		if hasattr(Mysql, "conn") and self.conn:
			try:
				self.conn.close()
			except Exception as why:
				msg = f"conn关闭失败，原因:{why}"
				raise Exception(msg) from None

class SqlSelect:
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
		if SqlSelect.__init_flag:
			config = read_config()["mysql"]
			if not config:
				raise Exception("config.yaml中未配置数据库连接")
			self.__mysql = Mysql(**config)
			SqlSelect.__init_flag = False

	def execute(self,sql,key,item=None):
		""" 执行sql查询 """
		result = self.__mysql.select(sql)
		if item is None:
			keylist = []
			for dt in result:
				value = dict(dt).get(key)
				keylist.append(value)
			return keylist
		else:
			value = dict(result[item]).get(key)
			return value