"""
生成mock数据
"""
import random
import re
import string
from faker import Faker

from utils.singleinstance import singleton

attrset = ['name', 'phone', 'ssn', 'address', 'company', 'job', 'country', 'city', 'word', 'email', 'card']
cattrset = ['cname', 'cphone', 'cssn', 'cjob', 'ccountry', 'ccity', 'cword', 'cemail', 'ccard', 'cprovince']

@singleton
class Mock:
	""" 生成mock数据 """
	__locales = ['zh-CN', 'en-US']

	def __init__(self):
		self.__cn = self.__locales[0]
		self.__en = self.__locales[1]
		self.__faker = Faker(locale=self.__locales)

	def __getattr__(self, attr):
		if attr in attrset:
			elems = {
				'phone': 'phone_number',
				'card': 'credit_card_number'
			}
			attr = elems.get(attr) or attr
			return getattr(self.__faker[self.__en], attr)
		elif attr in cattrset:
			elems = {
				'cphone': 'phone_number',
				'ccard': 'credit_card_number'
			}
			attr = elems.get(attr) or attr[1:]
			return getattr(self.__faker[self.__cn], attr)
		else:
			raise AttributeError(f'Attribute {attr} not found')

	def caddress(self):
		""" 国内地址 """
		return re.sub(r"[a-zA-Z]\w\s\d{3}", "", self.__faker[self.__cn].address()) + "号"

	def ccompany(self):
		""" 国内公司名 """
		return self.__faker[self.__cn].province().rstrip('省') + self.__faker[self.__cn].company()

	@staticmethod
	def randchar(length: int) -> str:
		""" 生成指定长度的字母数字组合的字符串 """
		if not isinstance(length, int):
			raise TypeError('length must be int')
		elif length < 2:
			raise ValueError('length must >1')
		numcount = random.randint(1, length - 1)
		lettercount = length - numcount
		num_arry = [random.choice(string.digits) for _ in range(numcount)]
		letter_arry = [random.choice(string.ascii_letters) for _ in range(lettercount)]
		all_arry = num_arry + letter_arry
		random.shuffle(all_arry)
		random_string = ''.join(all_arry)
		return random_string

	def __call__(self,item):
		return self.__faker[item]