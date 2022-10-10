import pymysql
from common.logger import logger

class Mysql:
	""" mysql数据库操作 """
	instance = None
	__init_flag = True

	def __new__(cls, *args, **kwargs):
		if cls.instance is None:
			cls.instance = object.__new__(cls)
			return cls.instance
		else:
			return cls.instance

	def __init__(self,host,port,user,password,db,charset='utf8'):
		""" 连接mysql数据库 """
		if Mysql.__init_flag:
			try:
				self.conn = pymysql.connect(
					host=host,port=port,user=user,password=password,db=db, charset=charset
				)
				self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
				logger.debug(f"数据库连接成功")
			except Exception as why:
				raise Exception(f"数据库连接失败，连接失败原因:{why}") from None
			Mysql.__init_flag = False

	def select(self, sql):
		""" 读取table中数据 """
		try:
			self.cursor.execute(sql)
			r = self.cursor.fetchall()
			logger.debug("数据select成功")
			return r
		except Exception as why:
			self.conn.rollback()
			raise Exception(f"数据select失败，select失败原因:{why}") from None

	def insert(self, sql):
		""" 将数据写入table中 """
		try:
			self.cursor.execute(sql)
			self.conn.commit()
			logger.debug("数据inset成功")
		except Exception as why:
			self.conn.rollback()
			raise Exception(f"数据insert失败，insert失败原因:{why}") from None

	def update(self, sql):
		""" 更新table中数据 """
		try:
			self.cursor.execute(sql)
			self.conn.commit()
			logger.debug("数据update成功")
		except Exception as why:
			self.conn.rollback()
			raise Exception(f"数据update失败，update失败原因:{why}") from None

	def delete(self, sql):
		""" 删除table中数据 """
		try:
			self.cursor.execute(sql)
			self.conn.commit()
			logger.debug("数据delete成功")
		except Exception as why:
			self.conn.rollback()
			raise Exception(f"数据delete失败，delete失败原因:{why}") from None

	def __del__(self):
		if hasattr(Mysql, "cursor") and self.cursor:
			try:
				self.cursor.close()
			except Exception as why:
				raise Exception(f"cursor关闭失败，关闭失败原因:{why}") from None
		if hasattr(Mysql, "conn") and self.conn:
			try:
				self.conn.close()
			except Exception as why:
				raise Exception(f"conn关闭失败，关闭失败原因:{why}") from None