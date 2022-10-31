import threading


class thread:
	""" 多线程装饰器 """
	def __init__(self,num):
		if not isinstance(num,int):
			msg = f"{num} must be a int"
			raise TypeError(msg)
		self.__num = num

	@staticmethod
	def __parse(cases):
		if not isinstance(cases,list|tuple|set):
			msg = f"{cases} must be a list or tuple or set"
			raise TypeError(msg)
		newCases = []
		for index,case in enumerate(cases):
			if isinstance(case,str):
				newCases.append((case,))
			elif isinstance(case,list|tuple|set):
				newCases.append(case)
			else:
				msg = f"{case} must is string or list or tuple or set"
				raise TypeError(msg)
		return newCases

	def __handle(self,cases):
		for case in cases:
			self.func(*case)

	def __call__(self, func):
		self.func = func
		def wapper(cases):
			temp = None
			caseslist = self.__parse(cases)
			for i in range(self.__num):
				temp = threading.Thread(target=self.__handle, args=(caseslist[i::self.__num],))
				temp.start()
			return temp
		return wapper