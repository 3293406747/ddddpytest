import re
import importlib


def parse(reMatch):
	""" repl解析 """
	obj = importlib.import_module("common.function.function")
	# obj = __import__("common.function.function",fromlist=True)
	data = re.findall(r"\.?(.+?)\((.*?)\)", reMatch.group(1))
	for i in data:
		name, args = i[0], i[1]
		if args:
			obj = getattr(obj, name)(*args.split(","))
		else:
			obj = getattr(obj, name)()
	return obj