import json,yaml
from string import Template
from common.read.read_excel import read_excel
from common.read.read_yaml import read_yaml
from common.case.verify import verify


def read_testcase(filename, item=0, encoding="utf-8"):
	""" 读取测试用例 """
	caseinfo = read_yaml(filename=filename, encoding=encoding)[item]
	caseinfo = verify(caseinfo)
	if not caseinfo.get("data_path"):
		return [caseinfo]
	data_path = caseinfo.pop("data_path")
	sheet = caseinfo.pop("data_sheet") if caseinfo.get("data_sheet") else None
	caseinfo = json.dumps(caseinfo, ensure_ascii=False)
	data = read_excel(filename=data_path,sheet=sheet)
	return [yaml.load(stream=Template(caseinfo).safe_substitute(i), Loader=yaml.FullLoader) for i in data]