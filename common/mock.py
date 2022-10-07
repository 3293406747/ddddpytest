# from faker import Faker
#
#
# class Mock(Faker):
#
# 	DEFUALT = 'zh-CN'
#
# 	def __init__(self,locale=DEFUALT):
# 		Faker.__init__(self,locale=locale)
#
# 	def goto(self,language='en-US'):
# 		print('aaaa')
# 		Mock.__init__(self, locale=language)
#
# 	def cname(self):
# 		print('bbbb')
# 		self.goto(Mock.DEFUALT)
# 		return self.name()
#
# 	def name(self):
# 		self.goto()
# 		return self.name()
# mock = Mock()
# print(mock.cname())
# print(mock.name())
from faker import Faker

f = Faker(locale=['zh-CN','en-US'])
s=f['zh-CN']
print(s.name())


