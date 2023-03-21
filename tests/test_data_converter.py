import os

from data_converter.module import parse

import pytest

class TestParser:
	@pytest.mark.positive
	def test_runner(self):
		parse.runner('../data_converter/data/collections.xml', '../data_converter/data/collections.json')
		assert os.path.isfile('../data_converter/data/collections.json')
		assert os.path.getsize('../data_converter/data/collections.json')
