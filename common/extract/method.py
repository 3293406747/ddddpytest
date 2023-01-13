import json,re,jsonpath


class Method:

	@classmethod
	def json(cls,data,pattern):
		obj = json.loads(data) if isinstance(data, str) else data
		return jsonpath.jsonpath(obj=obj, expr=pattern)

	@classmethod
	def match(cls,data,pattern):
		obj = json.dumps(data, ensure_ascii=False) if isinstance(data, dict) else data
		return re.findall(pattern=pattern, string=obj)