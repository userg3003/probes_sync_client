import os

from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

from clients import http

src_path = Path.cwd()
load_dotenv(dotenv_path=src_path.joinpath(".deploy", ".envs", "local.env"))
token = os.environ.get("TOKEN")
port = os.environ.get("PORT")
host = os.environ.get("HOST")
schema = os.environ.get("SCHEMA")


service_endpoint = schema + '://' + host + ':' + port


def set_auth(m, t, n):
    if m.headers is None:
        m.headers = {}
    m.headers[n] = t
    return m


def client(token=None):
    """
    client creates individual client for each test of tested service. This is very famous for aiohttp event loop in tests
    :return:
    """
    # t = token
    # if token is None:
    #     t = f'{grader_v2_user_statistics_token}'
    # set_token_ = lambda m: set_auth(m, t, 'auth')
    # return http.AsyncClient(grader_v2_user_statistics_endpoint, mdws_nc=[set_token_])
    return http.AsyncClient(service_endpoint)

def clientSync(token=None):
    """
    client creates individual client for each test of tested service. This is very famous for aiohttp event loop in tests
    :return:
    """
    # t = token
    # if token is None:
    #     t = f'{grader_v2_user_statistics_token}'
    # set_token_ = lambda m: set_auth(m, t, 'auth')
    # return http.AsyncClient(grader_v2_user_statistics_endpoint, mdws_nc=[set_token_])
    return http.Client(service_endpoint)

