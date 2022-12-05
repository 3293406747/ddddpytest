import json,re,jsonpath


class Method:

	@classmethod
	def json(cls,data,pattern):
		obj = json.loads(data) if isinstance(data, str) else data
		result = jsonpath.jsonpath(obj=obj, expr=pattern)
		return result

	@classmethod
	def match(cls,data,pattern):
		obj = json.dumps(data, ensure_ascii=False) if isinstance(data, dict) else data
		result = re.findall(pattern=pattern, string=obj)
		return result