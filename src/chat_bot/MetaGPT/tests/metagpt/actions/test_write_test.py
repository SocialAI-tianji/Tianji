#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 17:45
@Author  : alexanderwu
@File    : test_write_test.py
"""
import pytest

from metagpt.actions.write_test import WriteTest
from metagpt.logs import logger


@pytest.mark.asyncio
async def test_write_test():
    code = """
    import random
    from typing import Tuple

    class Food:
        def __init__(self, position: Tuple[int, int]):
            self.position = position

        def generate(self, max_y: int, max_x: int):
            self.position = (random.randint(1, max_y - 1), random.randint(1, max_x - 1))
    """

    write_test = WriteTest()

    test_code = await write_test.run(
        code_to_test=code,
        test_file_name="test_food.py",
        source_file_path="/some/dummy/path/cli_snake_game/cli_snake_game/food.py",
        workspace="/some/dummy/path/cli_snake_game",
    )
    logger.info(test_code)

    # We cannot exactly predict the generated test cases, but we can check if it is a string and if it is not empty
    assert isinstance(test_code, str)
    assert "from cli_snake_game.food import Food" in test_code
    assert "class TestFood(unittest.TestCase)" in test_code
    assert "def test_generate" in test_code


@pytest.mark.asyncio
async def test_write_code_invalid_code(mocker):
    # Mock the _aask method to return an invalid code string
    mocker.patch.object(WriteTest, "_aask", return_value="Invalid Code String")

    # Create an instance of WriteTest
    write_test = WriteTest()

    # Call the write_code method
    code = await write_test.write_code("Some prompt:")

    # Assert that the returned code is the same as the invalid code string
    assert code == "Invalid Code String"
