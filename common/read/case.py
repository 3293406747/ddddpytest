from abc import ABC, abstractmethod
import json
from string import Template
import yaml

from pathlib import Path

from common.case.verify_case import verify_case
from utils.read_excel import read_excel
from utils.read_yaml import read_yaml
from utils.single_instance import singleton

TESTCASE_DIR = Path(__file__).resolve().parent.parent.parent.joinpath("testcase")
DATA_DIR = Path(__file__).resolve().parent.parent.parent.joinpath("data")


class TestcaseReader(ABC):

	@abstractmethod
	def _validate_testdata(self, test_case: dict) -> None:
		"""校验测试用例信息"""
		pass

	@abstractmethod
	def _read_testcase(self, filename: str, case_index: int, encoding: str) -> dict:
		"""读取测试用例"""
		pass

	@abstractmethod
	def _merge_testcase_and_testdata(self, test_case: dict) -> list:
		"""合并测试用例和测试数据"""
		pass

	def read(self, filename: str, index: int = 0, encoding: str = "utf-8") -> list:
		"""读取测试用例"""
		testcase = self._read_testcase(filename, index, encoding)
		self._validate_testdata(testcase)
		return self._merge_testcase_and_testdata(testcase)


@singleton
class YamlTestcaseReader(TestcaseReader):

	def _read_testcase(self, filename: str, case_index: int, encoding: str) -> dict:
		return read_yaml(TESTCASE_DIR.joinpath(filename), encoding)[case_index]

	def _validate_testdata(self, test_case: dict) -> None:
		verify_case(test_case)

	def _merge_testcase_and_testdata(self, test_case: dict) -> list:
		test_case_dir = test_case.pop("data_path", None)
		if test_case_dir is None:
			return [test_case]

		sheet = test_case.pop("data_sheet", None)
		test_case_str = json.dumps(test_case, ensure_ascii=False)
		test_data_list = read_excel(DATA_DIR.joinpath(test_case_dir), sheet)
		return [yaml.safe_load(self._render_template(test_case_str, test_data)) for test_data in test_data_list]

	@staticmethod
	def _render_template(template: str, variables: dict):
		return Template(template).safe_substitute(variables)


def read_case(filename: str, case_index: int = 0, encoding: str = "utf-8") -> list:
	""" 读取测试用例 """
	return YamlTestcaseReader().read(filename, case_index, encoding)