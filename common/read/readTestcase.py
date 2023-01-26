import json,yaml
from string import Template
from pathlib import Path
from common.case.verify import verify
from utils.readExcel import readExcel
from utils.readYaml import readYaml

basePath = Path(__file__).resolve().parent.parent.parent


def readTestcase(filename, item=0, encoding="utf-8"):
	""" 读取测试用例 """
	caseinfo = readYaml(file=basePath/"testcase"/filename, encoding=encoding)[item]
	caseinfo = verify(caseinfo)
	if not caseinfo.get("data_path"):
		return [caseinfo]
	dataPath = caseinfo.pop("data_path")
	sheet = caseinfo.pop("data_sheet") if caseinfo.get("data_sheet") else None
	caseinfo = json.dumps(caseinfo, ensure_ascii=False)
	data = readExcel(file=basePath/"data"/dataPath,sheet=sheet)
	return [yaml.load(stream=Template(caseinfo).safe_substitute(i), Loader=yaml.FullLoader) for i in data]