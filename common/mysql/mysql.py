import pymysql


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
			# self.conn.rollback()
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
