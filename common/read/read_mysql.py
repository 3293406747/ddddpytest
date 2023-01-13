from common.mysql.mysql import Mysql
from common.read.read_config import read_config
from utils.singleinstance import singleInstance


@singleInstance
class ReadMysql:
	""" sql查询 """
	def __init__(self):
		self.config = read_config()["mysql"]
		if not self.config:
			raise Exception("config/local.yaml中未配置数据库连接")

	def execute(self,sql,key,item=None):
		""" 执行sql查询 """
		with Mysql(**self.config) as mysql:
			result = mysql.select(sql)
		return item is None and [dict(dt).get(key) for dt in result] or dict(result[item]).get(key)