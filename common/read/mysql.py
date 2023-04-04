from common.read.config import readConfig
from utils.mysql_manager import MysqlManager, MysqlManagerConfig
from utils.single_instance import singleton


@singleton
class MysqlReader:
	""" sql查询 """

	def __init__(self):
		# if not (config := readConfig()["mysql"]):
		config = readConfig()["mysql"]
		if not config:
			msg = "config/local.yaml中未配置数据库连接"
			raise MysqlReaderError(msg)

		self.mysqlConnectionPool: [MysqlManager] = []
		self._current_connection: MysqlManager | None = None

		mysql = MysqlManager(MysqlManagerConfig(**config))
		self.add_connection(mysql)
		self.current_connection = 0

	def add_connection(self, mysql: MysqlManager):
		"""添加mysql连接"""
		mysql.connect()
		self.mysqlConnectionPool.append(mysql)

	@property
	def current_connection(self):
		"""获取当前连接"""
		return self._current_connection

	@current_connection.setter
	def current_connection(self, index: int):
		"""设置当前连接"""
		if not isinstance(index, int):
			raise TypeError("pink必须是整数")

		if not self.mysqlConnectionPool:
			raise Exception("连接池中没有可用连接")

		self._current_connection = self.mysqlConnectionPool[index]

	def query(self, sql: str, key: str, index: int | None = None) -> str:
		""" sql查询 """
		if not self.current_connection:
			raise Exception("当前没有可用的数据库连接")

		queried_data_list: list = self.current_connection.query(sql)

		results = []
		if index is None:
			for queried_data in queried_data_list:
				result = dict(queried_data).get(key)
				results.append(result)
			return ",".join(results)
		else:
			queried_data = queried_data_list[index]
			result = dict(queried_data).get(key)
			return result

	def __del__(self):
		for connection in self.mysqlConnectionPool:
			try:
				connection.close_all_session()
			except Exception:
				pass


class MysqlReaderError(Exception):
	pass


def readMysql(sql: str, key: str, index: int | None = None):
	"""mysql查询"""
	mysql = MysqlReader()
	return mysql.query(sql, key, index)
