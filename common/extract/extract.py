from common.extract.factory import Factory


class Extract:
	""" 提取响应中的内容 """

	@staticmethod
	def json(data, pattern, index=None):
		""" json提取 """
		return Factory.create(method="json",data=data,pattern=pattern,index=index)

	@staticmethod
	def match(data,pattern,index=None):
		""" 正则提取 """
		return Factory.create(method="match", data=data, pattern=pattern, index=index)


extract = Extract()