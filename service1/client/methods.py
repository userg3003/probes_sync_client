import typing
from clients.http import Method


class OneFile(Method):
    url = "/onefile/"
    m_type = "POST"
    auth = None

    def __init__(self, files=""):
        Method.__init__(self)
        self.files = files


class HealthCheck(Method):
    _method = ""
    m_type = "GET"
    auth = None


class SeveralFiles(Method):
    url = "/severalfiles/"
    m_type = "POST"
    auth = None
    # headers = {"Content-Type": "multipart/form-data", "accept": "application/json"}

    def __init__(self, files):   #typing.List):
        Method.__init__(self)
        assert len("files") > 0, 'you must pass any users'
        self.files = files


class SeveralFilesSync(Method):
    url = "/severalfiles/"
    m_type = "POST"
    auth = None
    headers = {"Content-Type": "multipart/form-data", "accept": "application/json"}

    def __init__(self, files):   #typing.List):
        Method.__init__(self)
        assert len("files") > 0, 'you must pass any users'
        self.files = files


class SeveralFilesSyncNoAuth(Method):
    url = "/severalfiles/"
    m_type = "FILE"
    auth = None
    # headers = {"Content-Type": "multipart/form-data", "accept": "application/json"}

    def __init__(self, files: typing.List):
        Method.__init__(self)
        assert len("files") > 0, 'you must pass any users'
        # self.headers = {'token': token}
        self.files = files


class SeveralFilesSync(Method):
    url = "severalfiles"
    m_type = "FILE"
    auth = None
    # headers = {"Content-Type": "multipart/form-data", "accept": "application/json"}

    def __init__(self, files: typing.List, token):
        Method.__init__(self)
        assert len("files") > 0, 'you must pass any users'
        self.headers = {'token': token}
        self.files = files


class SeveralFilesAuth(Method):
    url = "/severalfiles_auth/"
    m_type = "POST"
    auth = None
    headers = {"Content-Type": "multipart/form-data", "accept": "application/json"}

    def __init__(self, files):   #typing.List):
        Method.__init__(self)
        assert len("files") > 0, 'you must pass any users'
        self.files = files

