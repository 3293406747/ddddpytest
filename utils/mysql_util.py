import pymysql
from utils.logger_util import logger
from utils.yaml_util import read_config

mysql_text = read_config()["mysql"]

class Mysql:

	@logger.catch()
	def __init__(self):
		""" 连接mysql数据库 """
		host = mysql_text["host"]
		port = mysql_text["port"]
		user = mysql_text["user"]
		password = mysql_text["password"]
		db = mysql_text["db"]

		try:
			self.conn = pymysql.connect(
				host=host, port=port, user=user, password=password, db=db, charset='utf8'
			)
			self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
			logger.info(f"数据库连接成功，地址:{host},端口:{port},用户:{user},密码{password},连接库:{db}")
		except Exception as why:
			raise Exception(f"数据库连接失败，连接失败原因:{why}")

	@logger.catch()
	def select(self, sql):
		""" 读取table中数据 """
		try:
			self.cursor.execute(sql)
			r = self.cursor.fetchall()
			logger.info("数据select成功")
			return r
		except Exception as why:
			self.conn.rollback()
			raise Exception(f"数据select失败，select失败原因:{why}") from None

	@logger.catch()
	def insert(self, sql):
		""" 将数据写入table中 """
		try:
			self.cursor.execute(sql)
			self.conn.commit()
			logger.success("数据inset成功")
		except Exception as why:
			self.conn.rollback()
			raise Exception(f"数据insert失败，insert失败原因:{why}") from None

	@logger.catch()
	def update(self, sql):
		""" 更新table中数据 """
		try:
			self.cursor.execute(sql)
			self.conn.commit()
			logger.success("数据update成功")
		except Exception as why:
			self.conn.rollback()
			raise Exception(f"数据update失败，update失败原因:{why}") from None

	@logger.catch()
	def delete(self, sql):
		""" 删除table中数据 """
		try:
			self.cursor.execute(sql)
			self.conn.commit()
			logger.success("数据delete成功")
		except Exception as why:
			self.conn.rollback()
			raise Exception(f"数据delete失败，delete失败原因:{why}") from None

	@logger.catch()
	def __del__(self):
		if hasattr(Mysql, "cursor") and self.cursor:
			try:
				self.cursor.close()
			except Exception as why:
				raise Exception(f"cursor关闭失败，关闭失败原因:{why}")
		if hasattr(Mysql, "conn") and self.conn:
			try:
				self.conn.close()
			except Exception as why:
				raise Exception(f"conn关闭失败，关闭失败原因:{why}")


