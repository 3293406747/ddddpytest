import json, yaml
from abc import ABC, abstractmethod
from string import Template
from pathlib import Path
from common.case.verificationCase import verificationCase
from utils.excelReader import excelReader
from utils.yamlReader import yamlReader
from utils.singleinstance import singleton

TESTCASE_DIR = Path(__file__).resolve().parent.parent.parent.joinpath("testcase")
DATA_DIR = Path(__file__).resolve().parent.parent.parent.joinpath("data")


class TestcaseReader(ABC):

	@abstractmethod
	def _validate_caseinfo(self, caseinfo: dict) -> None:
		"""校验测试用例信息"""
		pass

	@abstractmethod
	def _read_testcase(self, filename: str, index: int, encoding: str) -> dict:
		"""读取测试用例"""
		pass

	@abstractmethod
	def _read_caseinfo(self, caseinfo: dict) -> list:
		"""读取测试用例信息"""
		pass

	def read(self, filename: str, index: int = 0, encoding: str = "utf-8") -> list:
		"""读取测试用例"""
		caseinfo = self._read_testcase(filename, index, encoding)
		self._validate_caseinfo(caseinfo)
		return self._read_caseinfo(caseinfo)


@singleton
class YamlTestcaseReader(TestcaseReader):

	def _read_testcase(self, filename: str, index: int, encoding: str) -> dict:
		return yamlReader(TESTCASE_DIR.joinpath(filename), encoding)[index]

	def _validate_caseinfo(self, caseinfo: dict) -> None:
		verificationCase(caseinfo)

	def _read_caseinfo(self, caseinfo: dict) -> list:
		dataPath = caseinfo.pop("data_path", None)
		if dataPath is None:
			return [caseinfo]

		sheet = caseinfo.pop("data_sheet", None)
		caseinfo = json.dumps(caseinfo, ensure_ascii=False)
		datas = excelReader(DATA_DIR.joinpath(dataPath), sheet)
		return [yaml.safe_load(self._render_template(caseinfo, data)) for data in datas]

	@staticmethod
	def _render_template(template: str, data: dict):
		return Template(template).safe_substitute(data)


def readTestcase(filename: str, index: int = 0, encoding: str = "utf-8") -> list:
	""" 读取测试用例 """
	return YamlTestcaseReader().read(filename, index, encoding)