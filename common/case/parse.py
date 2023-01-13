import re
import importlib


def parse(reMatch):
	""" repl解析 """
	obj = importlib.import_module("common.function.function")
	# obj = __import__("common.function.function",fromlist=True)
	data = re.findall(r"\.?(.+?)\((.*?)\)", reMatch.group(1))
	for i in data:
		name, args = i[0], i[1]
		obj = args and getattr(obj, name)(*args.split(",")) or getattr(obj, name)()
	return obj