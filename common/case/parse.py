import re
import importlib


def parse(reMatch):
	""" repl解析 """
	obj = importlib.import_module("utils.function")
	# obj = __import__("utils.function",fromlist=True)
	data = re.findall(r"\.?(.+?)\((.*?)\)", reMatch.group(1))
	for i in data:
		name, args = i[0], i[1]
		obj = args and getattr(obj, name)(*args.split(",")) or getattr(obj, name)()
	return obj