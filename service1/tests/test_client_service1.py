import service1.tests as tests
import pytest
from service1.client.methods import HealthCheck, OneFile

import aiohttp
from loguru import logger
from pathlib import Path

# @pytest.fixture(scope='session', autouse=True)
# def config():
#     """A module scope fixture."""
#     cfg = init_env_and_logger()
#     return cfg


@pytest.mark.asyncio
async def test_health():
    m = HealthCheck()
    client = tests.client()
    resp, code = await client.request(m)
    assert code == 200


@pytest.mark.asyncio
async def test_get_swagger_info():
    """Test get swagger info """
    client = tests.client()
    method = HealthCheck()
    resp, status_code = await client.request(method)
    assert status_code == status_code
    assert "Api" in resp['message']


@pytest.mark.asyncio
async def test_send_file():
    method = HealthCheck()
    client = tests.client()
    _, status_code = await client.request(method)
    assert status_code == 200
    file_out = "Test1 \n=====\n"
    files = {'file': file_out}
    method_parse = OneFile(files)
    file_in, status_code = await client.request(method_parse)
    assert status_code == 200
    assert len(file_out) == len(file_in)
    assert file_in == file_out