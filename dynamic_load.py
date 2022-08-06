import random
import re
import string
from faker import Faker
from utils.logger_util import logger


@logger.catch()
def generate_userinfo(key):
	""" 生成随机用户信息 """
	faker = Faker(locale='zh-CN')
	ssn = faker.ssn()
	name = faker.name()
	phone = faker.phone_number()
	address = re.sub(r"[a-zA-Z]\w\s\d{3}", "", faker.address()) + "号"
	email = faker.email()
	company = faker.province().replace('省', '') + faker.company()
	card = faker.credit_card_number()
	info = {
		'username': name,
		'ssn': ssn,
		'phone': phone,
		'address': address,
		'email': email,
		'company': company,
		'card': card
	}
	return info[key]

@logger.catch()
def generate_string(length: int) -> str:
	""" 生成指定长度的字母数字组合的字符串 """
	if length < 2 or not isinstance(length, int):
		raise Exception("输入的值需要为长度至少两位且为整数")
	numcount = random.randint(1, length - 1)
	lettercount = length - numcount
	num_arry = [random.choice(string.digits) for _ in range(numcount)]
	letter_arry = [random.choice(string.ascii_letters) for _ in range(lettercount)]
	all_arry = num_arry + letter_arry
	random.shuffle(all_arry)
	random_string = ''.join(all_arry)
	return random_string

@logger.catch()
def generate_string2(length: int) -> str:
	""" 生成指定长度的字母数字组合的字符串 """
	if length < 2 or not isinstance(length, int):
		raise Exception("输入的值需要为长度至少两位且为整数")
	lettercount = random.randint(1, length - 1)
	punctuacount = length - lettercount
	letter_arry = random.choices(string.ascii_letters, k=lettercount)
	punctua_arry = random.choices(string.punctuation, k=punctuacount)
	all_arry = letter_arry + punctua_arry
	random.shuffle(all_arry)
	random_string = ''.join(all_arry)
	return random_string