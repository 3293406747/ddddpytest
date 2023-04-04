import re
from pathlib import Path


def get_areas(searchCode):
	"""根据身份证前6位获取所在地区"""

	def add_to_list(data):
		"""移除数字和空格"""
		data = re.sub('\d', '', data)
		data = data.strip()
		data = data.replace('[', '')
		data = data.replace(']', '')
		resList.append(data)

	# 加载所在地区数据   数据来源:http://www.zxinc.org/gb2260.htm
	with open(Path(__file__).parent/"data"/"areas.txt", encoding="utf-8") as file:
		dataList = file.readlines()
	splitSign = '　'
	level = -1
	resList = []

	for i in range(len(dataList) - 1, 0, -1):
		if level == 0:
			break
		item = dataList[i]

		if item[0:6] == searchCode:
			add_to_list(item)
			level = item.count(splitSign) - 1
			continue

		if item.count(splitSign) == level:
			add_to_list(item)
			level -= 1
			continue

	# 反转list
	resList.reverse()

	# list转字符串
	return ''.join(resList)