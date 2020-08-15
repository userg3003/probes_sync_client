import service1.tests as tests
import pytest
from service1.client.methods import HealthCheck, OneFile, OneFileAuth

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
async def test_send_file_from_memory():
    method = HealthCheck()
    client = tests.client()
    _, status_code = await client.request(method)
    assert status_code == 200
    file_out = "Test1 \n=====\n"
    files = {'file': file_out}
    # files = ('files', ("file1_name", file_out))
    method_parse = OneFile(files)
    file_in, status_code = await client.request(method_parse)
    assert status_code == 200
    assert len(file_out) == len(file_in)
    assert file_in == file_out


@pytest.mark.asyncio
async def test_send_file_from_memory_auth():
    method = HealthCheck()
    client = tests.client_auth_token()
    _, status_code = await client.request(method)
    assert status_code == 200
    file_out = "Test1 \n=====\n"
    files = {'file': file_out}
    # files = ('files', ("file1_name", file_out))
    method_parse = OneFileAuth(files=files)
    file_in, status_code = await client.request(method_parse)
    assert status_code == 200
    assert len(file_out) == len(file_in)
    assert file_in == file_out


@pytest.mark.asyncio
async def test_send_file_from_file():
    file1_name = "file1.rst"
    with open(tests.src_path.joinpath("service1", "tests", "data", file1_name), 'rb') as f:
        file_data = f.read()
    files = {'file': open(tests.src_path.joinpath("service1", "tests", "data", file1_name), 'rb')}
    # files = ('files', ("file1_name", file_out))
    method_parse = OneFile(files)
    client = tests.client()
    file_in, status_code = await client.request(method_parse)
    assert status_code == 200
    assert len(file_in) == len(file_data)
    assert file_in == file_data.decode("utf-8")


@pytest.mark.asyncio
async def test_send_file_from_file_auth():
    file1_name = "file1.rst"
    with open(tests.src_path.joinpath("service1", "tests", "data", file1_name), 'rb') as f:
        file_data = f.read()
    files = {'file': open(tests.src_path.joinpath("service1", "tests", "data", file1_name), 'rb')}
    # files = ('files', ("file1_name", file_out))
    method_parse = OneFileAuth(files=files)
    client = tests.client_auth_token()
    file_in, status_code = await client.request(method_parse)
    assert status_code == 200
    assert len(file_in) == len(file_data)
    assert file_in == file_data.decode("utf-8")