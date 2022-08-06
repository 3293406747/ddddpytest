import pytest
from utils.yaml_util import clear_extract


@pytest.fixture(scope="session",autouse=True)
def setup_session():
	clear_extract()


