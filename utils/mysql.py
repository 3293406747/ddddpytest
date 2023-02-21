"""
操作mysql数据库
"""
import pymysql


class Mysql:
	""" mysql数据库操作 """

	conn = None
	cursor = None

	def __init__(self,host,port,user,password,db,charset='utf8'):
		""" 连接mysql数据库 """
		self.host = host
		self.port = port
		self.user = user
		self.password = password
		self.db = db
		self.charset = charset

	def __enter__(self):
		self.connect()
		return self

	def connect(self):
		"""建立数据库连接"""
		try:
			self.conn = pymysql.connect(
				host=self.host,port=self.port,user=self.user,password=self.password,db=self.db, charset=self.charset
			)
			self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
		except Exception as why:
			self.close()
			msg = f"数据库连接失败，原因:{why}"
			raise Exception(msg) from None

	def select(self, sql):
		""" 读取table中数据 """
		try:
			self.cursor.execute(sql)
			return self.cursor.fetchall()
		except Exception as why:
			self.close()
			msg = f"数据查询失败，原因:{why}"
			raise Exception(msg) from None

	def commit(self, sql):
		""" 执行sql """
		try:
			self.cursor.execute(sql)
			self.conn.commit()
		except Exception as why:
			# self.conn.rollback()
			self.close()
			msg = f"sql执行失败，原因:{why}"
			raise Exception(msg) from None

	def close(self):
		"""销毁数据库连接"""
		try:
			self.cursor and self.cursor.close()
			self.conn and self.conn.close()
		except Exception:
			pass

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()

