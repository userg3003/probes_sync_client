import pytest

import service1.tests as tests
from service1.client.methods import (HealthCheck, SeveralFiles,
                                     SeveralFilesSyncNoAuth,
                                     SeveralFilesAuthToken)


@pytest.mark.asyncio
async def test_health():
    m = HealthCheck()
    client = tests.client()
    resp, code = await client.request(m)
    assert code == 200


def test_multiple_files_from_file_sync_noauth():
    file1_name = "file1.rst"
    file2_name = "file2.rst"

    multiple_files = [
        ('files', (file1_name, open(tests.src_path.joinpath("service1", "tests", "data", file1_name), 'rb'))),
        ('files', (file2_name, open(tests.src_path.joinpath("service1", "tests", "data", file2_name), 'rb')))
    ]
    m = SeveralFilesSyncNoAuth(multiple_files)
    client = tests.clientSync()
    resps_ans, status_code = client.request(m)
    assert status_code == 200
    assert resps_ans['count_files'] == 2
    assert resps_ans['files'][0]['name'] == file1_name
    assert resps_ans['files'][1]['name'] == file2_name


def test_multiple_files_from_memory_sync_noauth():
    file1_out = "Test1 \n=====\n"
    file2_out = "Test2 \n=====\n"
    file1_name = "file1_out"
    file2_name = "file2_out"
    multiple_files = [('files', (file1_name, file1_out)),
                      ('files', (file2_name, file2_out))]

    m = SeveralFilesSyncNoAuth(multiple_files)
    client = tests.clientSync()
    resps_ans, status_code = client.request(m)
    assert status_code == 200
    assert resps_ans['count_files'] == 2
    assert resps_ans['files'][0]['name'] == file1_name
    assert resps_ans['files'][1]['name'] == file2_name


@pytest.mark.asyncio
async def test_send_SeveralFiles_from_file_no_auth():
    file1_name = "file1.rst"
    file2_name = "file2.rst"

    multiple_files = [
        (file1_name, open(tests.src_path.joinpath("service1", "tests", "data", file1_name), 'rb')),
        (file2_name, open(tests.src_path.joinpath("service1", "tests", "data", file2_name), 'rb')),
    ]

    method = SeveralFiles(multiple_files)
    client = tests.client()
    file_in, status_code = await client.request(method)
    assert status_code == 200
    assert file_in['count_files'] == 2
    assert file_in['files'][0]['name'] == file1_name
    assert file_in['files'][1]['name'] == file2_name


@pytest.mark.asyncio
async def test_send_SeveralFiles_from_file_auth_token():
    file1_name = "file1.rst"
    file2_name = "file2.rst"

    multiple_files = [
        (file1_name, open(tests.src_path.joinpath("service1", "tests", "data", file1_name), 'rb')),
        (file2_name, open(tests.src_path.joinpath("service1", "tests", "data", file2_name), 'rb')),
    ]

    method = SeveralFilesAuthToken(multiple_files)
    client = tests.client_auth_token()
    file_in, status_code = await client.request(method)
    assert status_code == 200
    assert file_in['count_files'] == 2
    assert file_in['files'][0]['name'] == file1_name
    assert file_in['files'][1]['name'] == file2_name
