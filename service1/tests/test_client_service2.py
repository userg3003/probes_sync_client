import pytest
import service1.tests as tests
from service1.client.methods import HealthCheck, SeveralFiles, SeveralFilesAuth


@pytest.mark.asyncio
async def test_health():
    m = HealthCheck()
    client = tests.client()
    resp, code = await client.request(m)
    assert code == 200


# @pytest.mark.skip(reason=None)
@pytest.mark.asyncio
async def test_send_SeveralFiles_no_auth():
    client = tests.client()
    file1_out = "Test1 \n=====\n"
    file2_out = "Test2 \n=====\n"
    multiple_files = [('file', file1_out, 'application/json'),
                      ('file', file2_out)
                      ]
    method = SeveralFiles(multiple_files)
    file_in, status_code = await client.request(method)
    assert status_code == 200
    # assert len(file_out) == len(file_in)
    # assert file_in == file_out

    # src_path = Path.cwd().joinpath("grader_v2_course_creator", "tests", "data", "files")
    # f_good_json = 'course_one_class_title_level_inconsistent.json'
    # f1 = 'class2_title_level_inconsistent.rst'
    # logger.debug(f"")
    # multiple_files = [('file', (f_good_json, open(src_path.joinpath(f_good_json), 'rb'), 'application/json')),
    #                   ('file', (f1, open(src_path.joinpath(f1), 'rb')))
    #                   ]
    # # files = [("attachment", ("test.jpg", open("files/test.jpg", "rb").read())),
    # #          ("attachment", ("test.txt", open("files/test.txt", "rb").read()))]
    # logger.debug(f"")
    # # data = FormData()
    # # data.add_field('file',
    # #                open('report.xls', 'rb'),
    # #                filename='report.xls',
    # #                content_type='application/vnd.ms-excel')
    #
    # # m = client_course_creator.AddCourse(multiple_files, cfg["course_creator_token"])
    # # with aiohttp.MultipartWriter('mixed') as mpwriter:
    # file1 =open(src_path.joinpath(f_good_json), 'rb')
    # js = file1.read()
    # file2 =open(src_path.joinpath(f1), 'rb')
    # rst = file2.read()
    # fData = aiohttp.FormData()
    # fData.add_field('file', js, filename=f_good_json)
    # fData.add_field('file', rst, filename=f1)
    # # mpwriter = aiohttp.MultipartWriter()
    # # mpwriter.append(js, {'files': f_good_json, 'CONTENT-TYPE': 'application/json'})
    # # mpwriter.append(rst, {'files': f1})
    #
    # # fData = aiohttp.MultipartWriter()
    # # part = fData.append(js, {'CONTENT-TYPE': 'application/json'})
    # # part.set_content_disposition('attachment', filename=f_good_json)
    # # part = fData.append(rst)
    # # part.set_content_disposition('attachment', filename=f1)
    # m = AddCourse(files=fData)
    # logger.debug(f"")
    # resps_ans, status_code = await client_course_creator.request(m)
    # err_info = resps_ans[0]['message'].split(":")
    # assert status_code == 400
    # assert "<rst-doc>" in err_info[3]
    # assert "44" in err_info[2]
    # assert "(SEVERE/4) Title level inconsistent" in err_info[4]
#

