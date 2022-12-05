import json
from common.assertion.method import Method


class Factory:

	@classmethod
	def create(cls, method, expect, actual, name=None):
		if method in ["equal", "unequal"]:
			list(map(lambda x: [x] if isinstance(x, (str, int, float)) else x, [expect, actual]))
			Method.equal_unqual(method=method, expect=expect, actual=actual, name=name)
		elif method in ["contain", "uncontain"]:
			actual = json.dumps(actual, ensure_ascii=False) if isinstance(actual, dict) else actual
			expect = [expect] if isinstance(expect, str) else expect
			Method.contain_uncontain(method=method, expect=expect, actual=actual, name=name)
		else:
			msg = "断言格式不支持。"
			raise Exception(msg)