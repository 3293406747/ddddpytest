"""
操作mysql数据库
"""
from dataclasses import dataclass, astuple

import pymysql


@dataclass
class MysqlManagerConfig:
	host: str
	port: int
	user: str
	password: str
	db: str
	charset: str = 'utf8'


class MysqlManager:
	""" mysql数据库操作 """

	conn = None
	cursor = None

	def __init__(self, config: MysqlManagerConfig):
		""" 连接mysql数据库 """
		self.host, self.port, self.user, self.password, self.db, self.charset = astuple(config)

	def __enter__(self):
		self.connect()
		return self

	def connect(self):
		"""建立数据库连接"""
		try:
			self.conn = pymysql.connect(
				host=self.host, port=self.port, user=self.user, password=self.password, db=self.db, charset=self.charset
			)
			self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
		except Exception as why:
			self.close()
			msg = f"数据库连接失败，原因:{why}"
			raise MysqlManagerError(msg)

	def query(self, sql):
		""" 读取table中数据 """
		try:
			self.cursor.execute(sql)
			return self.cursor.fetchall()
		except Exception as why:
			self.close()
			msg = f"数据查询失败，原因:{why}"
			raise MysqlManagerError(msg)

	def modify(self, sql):
		""" 执行sql """
		try:
			self.cursor.execute(sql)
			self.conn.commit()
		except Exception as why:
			# self.conn.rollback()
			self.close()
			msg = f"sql执行失败，原因:{why}"
			raise MysqlManagerError(msg)

	def close(self):
		"""销毁数据库连接"""
		try:
			self.cursor and self.cursor.close()
			self.conn and self.conn.close()
		except Exception:
			pass

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()


class MysqlManagerError(Exception):
	pass
