from common import dp


def task1(data):
	base_url = dp.variables().get('base_url')
	url = base_url + "/post"
	method = "POST"
	dp.variables().set("value","123456")
	data = dp.case_parse(data)
	response = dp.requests().request(method=method,url=url,data=data)
	value = response.extractVariable().json('$..value',0)
	dp.asserion().equal("123456",value,"相等断言")

