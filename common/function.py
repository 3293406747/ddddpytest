import base64
import hashlib

class Function:

	@classmethod
	def md5(cls,string):
		""" md5加密 """
		if not isinstance(string,str):
			raise TypeError('string must be a string')
		encode = string.encode()
		return hashlib.md5(encode).hexdigest()

	@classmethod
	def base64(cls,string):
		""" base64加密 """
		if not isinstance(string,str):
			raise TypeError('string must be a string')
		return base64.b64encode(string.encode()).decode()
