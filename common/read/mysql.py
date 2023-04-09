from abc import ABC, abstractmethod

from common.read.config import read_config
from utils.mysql_manager import MysqlManager, MysqlManagerConfig


class SqlReader(ABC):

	@abstractmethod
	def query(self, sql: str, key: str, index: int | None = None) -> str:
		pass


class MysqlReader(SqlReader):
	""" sql查询 """

	def __init__(self, mysql: MysqlManager):
		self.mysql = mysql

	def __enter__(self):
		self.mysql.connect()
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.mysql.close()

	def query(self, sql: str, key: str, index: int | None = None) -> str:
		""" sql查询 """
		queried_data_list: list = self.mysql.query(sql)

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


class MysqlReaderError(Exception):
	pass


def read_mysql(sql: str, key: str, config_path: str, index: int | None = None):
	"""sql查询"""
	# 读取数据库配置文件
	mysql_config = read_config(config_path)["mysql"]
	# if not (config := readConfig()["mysql"]):
	if not mysql_config:
		msg = "未配置数据库连接"
		raise MysqlReaderError(msg)

	# 创建MysqlManager实例
	mysql_manager = MysqlManager(MysqlManagerConfig(**mysql_config))

	# sql查询
	with MysqlReader(mysql_manager) as mysql_reader:
		return mysql_reader.query(sql, key, index)
