import requests


class Session:

	def __init__(self):
		self.__pool = []

	def generate_handle(self):
		sess = requests.session()
		self.__pool.append(sess)
		return sess

	def current_handle(self):
		if not self.__pool:
			raise Exception("pool is empty")
		return self.__pool[0]

	def handles(self):
		return self.__pool

session = Session()