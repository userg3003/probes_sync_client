import pytest
import aiohttp
from aiohttp import payload
from aiohttp.hdrs import CONTENT_DISPOSITION, CONTENT_ENCODING, CONTENT_TRANSFER_ENCODING, CONTENT_TYPE

import service1.tests as tests
from service1.client.methods import (HealthCheck, SeveralFiles,
                                     SeveralFilesSyncNoAuth,
                                     SeveralFilesAuth)


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
    assert resps_ans == "Len(files): 2"


def test_multiple_files_from_memory_sync_noauth():
    file1_out = "Test1 \n=====\n"
    file2_out = "Test2 \n=====\n"

    multiple_files = [('files', ("file1_out", file1_out)),
                      ('files', ("file2_out", file2_out))]

    m = SeveralFilesSyncNoAuth(multiple_files)
    client = tests.clientSync()
    resps_ans, status_code = client.request(m)
    assert status_code == 200
    assert resps_ans == "Len(files): 2"


# @pytest.mark.skip(reason=None)
@pytest.mark.asyncio
async def test_send_SeveralFiles_from_file_no_auth():
    file1_name = "file1.rst"
    file2_name = "file2.rst"

    multiple_files = [
        ('file', (file1_name, open(tests.src_path.joinpath("service1", "tests", "data", file1_name), 'rb'))),
        ('file', (file2_name, open(tests.src_path.joinpath("service1", "tests", "data", file2_name), 'rb')))
    ]

    method = SeveralFiles(multiple_files)
    client = tests.client()
    file_in, status_code = await client.request(method)
    assert status_code == 200


@pytest.mark.asyncio
async def test_send_SeveralFiles_FormData_no_auth():
    file1_out = "Test1 \n=====\n"
    # file2_out = "Test2 \n=====\n"
    # # multiple_files = {'file1.txt': file1_out,  'file1.txt': file2_out}
    #
    # data = aiohttp.MultipartWriter()
    # part = data.append(file1_out, {'CONTENT-TYPE': 'image/gif'})
    # part.set_content_disposition('attachment', filename='secret.txt')

    # files = [('files', file1_out),
    #          ('files', file2_out)]
    file1_name = "file1.rst"
    file2_name = "file2.rst"

    # Using FormData
    multiple_files = aiohttp.FormData()
    multiple_files.add_field('file', open(tests.src_path.joinpath("service1", "tests", "data", file1_name), 'rb'),
                             filename=file1_name,
                             content_type='multipart/form-data')

    # # Using MultipartWriter
    # mpwriter = aiohttp.MultipartWriter('multipart/form-data')
    # part = mpwriter.append(file1_out, {'CONTENT-TYPE': 'multipart/form-data'})
    # part.set_content_disposition('form-data')
    #
    # method_data = SeveralFiles(data)

    method = SeveralFiles(multiple_files)
    client = tests.client()
    file_in, status_code = await client.request(method)
    assert status_code == 200


@pytest.mark.asyncio
async def test_send_SeveralFiles_MultipartWriter_no_auth():
    file1_name = "file1.rst"
    file2_name = "file2.rst"

    # --------------
    # with aiohttp.MultipartWriter('multipart/form-data') as multiple_files:
    #     with aiohttp.MultipartWriter('files') as subwriter1:
    #         subwriter1.append(open(tests.src_path.joinpath("service1", "tests", "data", file1_name), 'rb'))
    #     multiple_files.append(subwriter1)
    #     with aiohttp.MultipartWriter('files') as subwriter2:
    #         subwriter2.append(open(tests.src_path.joinpath("service1", "tests", "data", file2_name), 'rb'))
    #     multiple_files.append(subwriter2)
    # ============
    with aiohttp.MultipartWriter('multipart/form-data') as multiple_files:
        with aiohttp.MultipartWriter('files') as files:
        # part.set_content_disposition('attachment', filename='secret.txt')
            files.append(open(tests.src_path.joinpath("service1", "tests", "data", file1_name), 'rb'),
                              {"Content-Type": "multipart/form-data"})
        files.append(open(tests.src_path.joinpath("service1", "tests", "data", file2_name), 'rb'),
                              {"Content-Type": "multipart/form-data"})
    multiple_files.append(files)
    # # # Using MultipartWriter
    # multiple_files = aiohttp.MultipartWriter('multipart/form-data')
    # # file1 = aiohttp.MultipartWriter('multipart/form-data')
    # part = multiple_files.append(open(tests.src_path.joinpath("service1", "tests", "data", file1_name), 'rb'),
    #                              {'CONTENT-TYPE': 'image/gif'})
    # part.set_content_disposition('attachment', filename='secret.txt')
    # multiple_files.append(file1)

    # file2 = aiohttp.MultipartWriter('multipart/form-data')
    # part = multiple_files.append(open(tests.src_path.joinpath("service1", "tests", "data", file2_name), 'rb'))
    # part.set_content_disposition('attachment', filename=file2_name)
    # multiple_files.append(file2)

    method = SeveralFiles(multiple_files)
    client = tests.client()
    file_in, status_code = await client.request(method)
    assert status_code == 200
