from utils.mysql import Mysql
from common.read.readConfig import readConfig
from utils.singleinstance import singleton


@singleton
class ReadMysql:
	""" sql查询 """

	def __init__(self):
		if not (config := readConfig()["mysql"]):
			raise Exception("config/local.yaml中未配置数据库连接")
		self.mysql = Mysql(**config)
		self.mysql.connect()

	def execute(self, sql, key, item=None):
		""" 执行sql查询 """
		result = self.mysql.select(sql)
		return item is None and [dict(dt).get(key) for dt in result] or dict(result[item]).get(key)

	def __del__(self):
		self.mysql.close()
