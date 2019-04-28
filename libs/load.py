from libs.yaml_parse import YamlJsonAttr, CaseYamlParser
from libs.auth_utils import login
from config import token_field
from libs.http_cil import HttpCil
from libs.errors import CaseFileNotFound, CaseAssertNotSport, ResponseNotJson, CaseAssertFailed
from libs.reflex import ReactData
from libs.logs import log
import os
import re
import json


def call_case(file_path=None):
    def middle(func):
        def wrapper(*args, **kwargs):
            func_name = getattr(func, '__name__')
            if os.path.exists(file_path) is False:
                raise CaseFileNotFound
            case_obj = CaseFileRequest(file_path, func_name)
            case_asserts = case_obj.asserts()
            case_before = case_obj.tear_down()
            response = case_obj.run()
            if case_asserts:
                AssertActions(case_asserts, response).exec_assert()
            if case_before:
                CaseTearDownAction(case_before, response).action()
            return func(*args, **kwargs)
        return wrapper
    return middle


class AssertActions(object):
    """断言处理器"""
    def __init__(self, asserts_dict, response):
        self.asserts_dict = asserts_dict
        self.response = response
        self.assert_type = ['body', 'headers', 'http_code']

    def assert_parse(self):
        pass

    def body_assert_parse(self, key):
        body_rule = key.split('.')
        body_data = self._format_response_body()
        if len(body_rule) == 1:
            return body_data
        try:
            json.dumps(body_data)
        except (ValueError, TypeError):
            raise ResponseNotJson

        for rule in body_rule[1:]:
            section = re.findall(r"\[(.*)\]$", rule, re.I | re.M)
            if len(section) == 0:
                body_data = body_data[rule]
            elif len(section) == 1:
                rule_new = rule.split('[')[0]
                body_data = body_data[rule_new]
                try:
                    s = int(section[0])
                    body_data = body_data[s]
                except ValueError:
                    raise CaseAssertNotSport
        return body_data

    def headers_assert_parse(self, key):
        headers_rule = key.split('.')
        if len(headers_rule) == 2:
            return self._format_response_headers()[headers_rule[-1]]
        else:
            raise CaseAssertNotSport

    def http_code_assert_parse(self, key):
        key_rule = key.split('.')
        if len(key_rule) == 1 and key_rule[0] == 'http_code':
            return self.response.status_code
        else:
            raise CaseAssertNotSport

    def exec_assert(self):
        for k, v in self.asserts_dict.items():
            log.debug('断言对象:{}'.format(k))
            mod = k.split('.')[0]
            if mod not in self.assert_type:
                raise CaseAssertNotSport
            if mod == 'body':
                k_str = self.body_assert_parse(k)
            elif mod == 'headers':
                k_str = self.headers_assert_parse(k)
            elif mod == 'http_code':
                k_str = self.http_code_assert_parse(k)
            log.debug('断言对象取值:{}'.format(k_str))
            v_str = ReactData(v).reflex_variable()
            try:
                assert k_str == v_str
            except AssertionError:
                raise CaseAssertFailed('断言失败:{} != {}'.format(k_str, v_str))

    def _format_response_body(self):
        try:
            content = self.response.json()
        except (TypeError, ValueError):
            content = self.response.content.decode("utf-8")
        return content

    def _format_response_headers(self):
        return dict(self.response.headers)


class CaseTearDownAction(object):

    def __init__(self, tear_dict, response):
        self.tear_dict = tear_dict
        self.response = response
        self.tear_type = ['sql', 'redis']

    def action(self):
        if isinstance(self.tear_dict, dict):
            for k, v in self.tear_dict.items():
                if k == 'sql':
                    ReactData(v).reflex_variable()
                elif k == 'redis':
                    pass


class CaseFileRequest(object):

    def __init__(self, data_file, story_func):
        self.d = data_file
        self.f = story_func
        self.case_data = YamlJsonAttr(CaseYamlParser(self.d).get_case_obj_by_name(story_func))

    def _method(self):
        return self.case_data.method.upper()

    def _uri(self):
        return self.case_data.uri

    def _headers(self):
        headers = self.case_data.headers if self.case_data.headers else {}
        if self._auth_user():
            headers.update({token_field: login(**self._auth_user())})
        return headers

    def _auth_user(self):
        return self.case_data.auth_user

    def set_up(self):
        if self.case_data.set_up:
            return dict(self.case_data.set_up)

    def tear_down(self):
        if self.case_data.tear_down:
            return dict(self.case_data.tear_down)

    def _data(self):
        return {k: ReactData(str(v)).reflex_variable() for k, v in (dict(self.case_data.data)).items()}

    def _data_type(self):
        return self.case_data.type

    def asserts(self):
        return dict(self.case_data.asserts)

    def run(self):
        data = HttpCil(headers=self._headers()).exec_request(
            method=self._method(),
            uri=self._uri(),
            post_type=self._data_type(),
            data=self._data(),
            file_path=None,
            file_field='file',
            verify=False,
            allow_redirects=False
        )
        return data




