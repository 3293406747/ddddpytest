def formatTemplate(func):
	""" 校验用例格式 """
	def wapper(template):
		cases = func(template)
		elems = ["name", "base_url", "request", "validata"]
		for elem in elems:
			for case in cases:
				if elem not in case.keys():
					raise Exception("yaml用例必须有的四个一级关键字: name,base_url,request,validata") from None
				elif elem == "request":
					for item in ["url", "method"]:
						if item not in case["request"]:
							raise Exception("yaml用例在request一级关键字下必须包括两个二级关键字:method,url") from None
		return cases
	return wapper