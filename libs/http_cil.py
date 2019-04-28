from requests_toolbelt import MultipartEncoder
from libs.yaml_parse import ConfigParser
import requests
import logging
from libs.logs import log
import json
import urllib3
import os

urllib3.disable_warnings()  # 屏蔽https warning警告信息
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class HttpCil(object):

    def __init__(self, host=None, headers={}, session=None):
        """
        :param host: 测试服务地址
        :param headers: 请求头
        :param env:
        """
        self.host = host if host else ConfigParser().api_host
        self.headers = headers
        self.body = {}
        self._session = requests.session() if session is None else session

    def _api_address(self, uri):
        """
        :param uri: 接口路径
        :return:
        """
        return self.host.rstrip('/') + '/' + uri.lstrip('/')

    def get_request(self, uri=None, data=None, verify=False, allow_redirects=False):
        """
        :param uri: get请求路径
        :param data: 请求参数
        :param verify: 是否https验证
        :param allow_redirects: 是否允许重定向
        :return:
        """
        response = self._session.get(self._api_address(uri),
                                     params=data,
                                     headers=self.headers,
                                     verify=verify,
                                     allow_redirects=allow_redirects)
        self._log_response(response)
        return self._body_result(response)

    def json_request(self, uri, data, verify=False, allow_redirects=False):
        """
        :param uri: post请求路径
        :param data: 请求数据
        :param verify: 是否https验证
        :param allow_redirects: 是否允许重定向
        :return:
        """
        response = self._session.post(self._api_address(uri),
                                      data=json.dumps(data),
                                      headers=self.headers,
                                      verify=verify,
                                      allow_redirects=allow_redirects)
        self._log_response(response)
        return self._body_result(response)

    def data_request(self, uri, data, verify=False, allow_redirects=False):
        """
        :param uri:
        :param data:
        :param verify:
        :param allow_redirects:
        :return:
        """
        response = self._session.post(self._api_address(uri),
                                      data=data,
                                      headers=self.headers,
                                      verify=verify,
                                      allow_redirects=allow_redirects)
        self._log_response(response)
        return response

    def file_request(self, uri, file_path, verify=False, allow_redirects=False):
        file_name = os.path.split(file_path)[-1]
        files = {
            'file': (file_name, open(file_path, 'rb'))
        }
        response = self._session.post(self._api_address(uri),
                                      files=files,
                                      headers=self.headers,
                                      verify=verify,
                                      allow_redirects=allow_redirects)
        self._log_response(response)
        return self._body_result(response)

    def multipart_request(self, uri, file_path=None, file_field='file',  data=None, verify=False, allow_redirects=False):
        fields = {}
        if file_path:
            file_name = os.path.split(file_path)[-1]
            fields[file_field] = (file_name, open(file_path, 'rb'), 'text/plain')
        if data and isinstance(data, dict):
            for k, v in data.items():
                fields[k] = (None, v, None)
        m = MultipartEncoder(fields=fields)
        self.headers['Content-Type'] = m.content_type
        response = self._session.post(self._api_address(uri),
                                      data=m,
                                      headers=self.headers,
                                      verify=verify,
                                      allow_redirects=allow_redirects)
        self._log_response(response)
        return self._body_result(response)

    def _merge_headers(self, headers):
        if headers is None:
            headers = {}
        else:
            headers = headers.copy()
        headers.update(self._session.headers)
        return headers

    def _body_result(self, response):
        try:
            content = response.json()
        except (TypeError, ValueError):
            content = response.content.decode("utf-8")
        return content

    @staticmethod
    def _log_response(response):
        assert response.status_code in [200, 401, 204]
        headers_to_json = json.dumps(dict(response.headers), indent=4)
        log.debug('返回请求地址: {}\t{}\t{}ms'.format(
            response.url,
            response.status_code,
            response.elapsed.microseconds/1000)
        )
        log.debug('返回请求头:\n{}'.format(headers_to_json))
        try:
            content = json.loads(response.content)
            content = json.dumps(content, indent=4, ensure_ascii=False)
        except (TypeError, ValueError):
            content = response.content.decode("utf-8")
        log.debug('请求结果:\n{}\n'.format(content))

    def exec_request(self, method, uri, post_type='json',
                     data=None, file_path=None, file_field='file',
                     verify=False, allow_redirects=False):
        log.debug("发送请求地址: {}\t{}\t".format(self._api_address(uri), method, post_type))
        log.debug("发送请求数据: {}\t".format(data))
        if file_path:
            log.debug("发送文件数据数据: {}\t{}\t".format(file_field, file_path))
        if method == "GET":
            return self.get_request(uri, data=data, verify=verify, allow_redirects=allow_redirects)

        if method == "POST" and post_type == "json":
            return self.json_request(uri, data=data, verify=verify, allow_redirects=allow_redirects)

        if method == "POST" and post_type == "data":
            return self.data_request(uri, data=data, verify=verify, allow_redirects=allow_redirects)

        if method == "POST" and post_type == "file":
            return self.file_request(uri, file_path=file_path, verify=verify, allow_redirects=allow_redirects)

        if method == "POST" and post_type == "multipart":
            return self.file_request(uri, data=data, file_path=file_path, file_field=file_field, verify=verify,
                                     allow_redirects=allow_redirects)