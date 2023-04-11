"""
生成mock数据
"""
import random
import re
import string
from datetime import datetime

from faker import Faker

from utils.generate_mock_data.geta_areas import get_areas
from utils.single_instance import SingletonMeta
from utils.generate_mock_data.sucreditcode import CreditIdentifier


class GenerateMockData(metaclass=SingletonMeta):
	""" 生成mock数据 """

	def __init__(self):
		self._faker = Faker(locale='zh-CN')

		self.emails = (
		'126.com', 'sina.com', 'qq.com', '163.com', 'gmail.com', 'outlook.com', 'hostmail.com', 'aliyun.com')

		self._attrset = {
			'name': 'name',
			'phone': 'phone_number',
			'ssn': 'ssn',
			'job': 'job',
			'country': 'country',
			'city': 'city',
			'word': 'word',
			'card': 'card',
			'province': 'province',
			'email': lambda: GenerateMockData().generate_random_string(random.randint(6, 16)) + "@" + random.choice(
				self.emails),
			'address': lambda: re.sub(r"[a-zA-Z]\w\s\d{3}", "", self._faker.address()) + "号",
			'company': lambda: self._faker.province().rstrip('省') + self._faker.company(),
		}

	def __getattr__(self, attr):
		if attr in self._attrset:
			if callable(self._attrset[attr]):
				return self._attrset[attr]
			return getattr(self._faker, self._attrset[attr])
		raise AttributeError(f'Attribute {attr} not found')

	@property
	def faker(self):
		return self._faker

	@staticmethod
	def generate_random_string(length: int) -> str:
		""" 生成指定长度的字母数字组合的字符串 """
		if not isinstance(length, int):
			raise TypeError('length must be int')
		elif length < 2:
			raise ValueError('length must >1')
		num_count = random.randint(1, length - 1)
		letter_count = length - num_count
		num_array = random.choices(string.digits, k=num_count)
		letter_array = random.choices(string.ascii_letters, k=letter_count)
		all_array = num_array + letter_array
		random.shuffle(all_array)
		return ''.join(all_array)

	@staticmethod
	def analyze_id_card(id_card):
		""" 获取身份证号信息 """
		# 解析身份证号码
		district_code = id_card[:6]
		birth_year = int(id_card[6:10])
		birth_month = int(id_card[10:12])
		birth_day = int(id_card[12:14])
		gender_code = int(id_card[-2])
		gender = "女" if gender_code % 2 == 0 else "男"

		# 计算年龄
		now = datetime.now()
		age = now.year - birth_year - ((now.month, now.day) < (birth_month, birth_day))

		# 获取所在地名称
		location = get_areas(district_code)
		if not location.endswith("市辖区"):
			location = location.replace("市辖区", "")
		location = location.replace("地区", "市") or "未知"

		# 构造结果字典
		result = {
			"身份证号": id_card,
			"所在地区": location,
			"出生日期": f"{birth_year:04}-{birth_month:02}-{birth_day:02}",
			"年龄": age,
			"性别": gender,
		}
		return result

	@staticmethod
	def generate_credit_code():
		""" 生成统一社会信用代码 """
		creditIdentifier = CreditIdentifier()
		random_credit_code = creditIdentifier.gen_random_credit_code()
		assert creditIdentifier.valid(random_credit_code["code"])
		return random_credit_code["code"]
