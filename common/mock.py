import random
import string

from faker import Faker


class Mock:
	locales = ['zh-CN', 'en-US']
	instance = None
	__init_flag = True

	def __new__(cls, *args, **kwargs):
		if cls.instance is None:
			cls.instance = object.__new__(cls)
			return cls.instance
		else:
			return cls.instance

	def __init__(self):
		if Mock.__init_flag:
			self.cn = self.locales[0]
			self.us = self.locales[1]
			self.faker = Faker(locale=self.locales)
			Mock.__init_flag = False

	def __getattr__(self, attr):
		match attr:
			case 'name' | 'phone' | 'ssn' | 'address' | 'company' | 'job' | 'country' | 'city' | 'word' | 'email' | 'card':
				elems = {
					'phone': 'phone_number',
					'card': 'credit_card_number'
				}
				attr = elems.get(attr) or attr
				return getattr(self.faker[self.us], attr)
			case 'cname' | 'cphone' | 'cssn' | 'caddress' | 'ccompany' | 'cjob' | 'ccountry' | 'ccity' | 'cword' | 'cemail' | 'ccard' | 'cprovince':
				elems = {
					'cphone': 'phone_number',
					'ccard': 'credit_card_number'
				}
				attr = elems.get(attr) or attr[1:]
				return getattr(self.faker[self.cn], attr)
			case _:
				raise AttributeError(f'Attribute {attr} not found')

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
