#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/12 10:23
@Author  : alexanderwu
@File    : test_project_manager.py
"""
import pytest

from metagpt.logs import logger
from metagpt.roles import ProjectManager
from tests.metagpt.roles.mock import MockMessages


@pytest.mark.asyncio
async def test_project_manager():
    project_manager = ProjectManager()
    rsp = await project_manager.handle(MockMessages.system_design)
    logger.info(rsp)
