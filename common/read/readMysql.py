from utils.mysql import Mysql
from common.read.readConfig import readConfig
from utils.singleinstance import singleton


@singleton
class MysqlReader:
	""" sql查询 """

	def __init__(self):
		config = readConfig()["mysql"]
		if not config:
			# if not (config := readConfig()["mysql"]):
			msg = "config/local.yaml中未配置数据库连接"
			raise Exception(msg)

		self.mysqlConnectionPool: [Mysql] = []
		self._current_connection: Mysql | None = None

		mysql = Mysql(**config)
		self.add_connection(mysql)
		self.current_connection = 0

	def add_connection(self, mysql: Mysql):
		"""添加mysql连接"""
		mysql.connect()
		self.mysqlConnectionPool.append(mysql)

	@property
	def current_connection(self):
		"""获取当前连接"""
		return self._current_connection

	@current_connection.setter
	def current_connection(self, pink: int):
		"""设置当前连接"""
		if not isinstance(pink, int):
			raise TypeError("pink必须是整数")

		if not self.mysqlConnectionPool:
			raise Exception("连接池中没有可用连接")

		self._current_connection = self.mysqlConnectionPool[pink]

	def execute(self, sql, key, item=None):
		""" 执行sql查询 """
		if not self.current_connection:
			raise Exception("当前没有可用的数据库连接")
		result = self.current_connection.query(sql)
		# return item is None and [dict(dt).get(key) for dt in result] or dict(result[item]).get(key)
		return ",".join([dict(dt).get(key) for dt in result]) if item is None else dict(result[item]).get(key)

	def __del__(self):
		for connection in self.mysqlConnectionPool:
			try:
				connection.close()
			except Exception:
				pass


def readMysql(sql, key, item=None):
	"""mysql查询"""
	mysql = MysqlReader()
	return mysql.execute(sql, key, item)
