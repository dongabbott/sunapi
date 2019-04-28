class HttperApiTestBaseError(Exception):
    def __init__(self, msg=None):
        super(HttperApiTestBaseError, self).__init__(msg)


class YamlFormatError(HttperApiTestBaseError):
    def __init__(self, msg='文件格式错误'):
        HttperApiTestBaseError.__init__(self, msg=msg)


class ApiLoginError(HttperApiTestBaseError):
    def __init__(self, msg='登录失败'):
        HttperApiTestBaseError.__init__(self, msg=msg)


class CaseFileNotFound(HttperApiTestBaseError):
    def __init__(self, msg='未发现测试数据文件'):
        HttperApiTestBaseError.__init__(self, msg=msg)


class CaseStoryNotFound(HttperApiTestBaseError):
    def __init__(self, msg='未发现测试用例'):
        HttperApiTestBaseError.__init__(self, msg=msg)


class CaseStoryRepeat(HttperApiTestBaseError):
    def __init__(self, msg='未发现测试用例'):
        HttperApiTestBaseError.__init__(self, msg=msg)


class KeywordSyntaxError(HttperApiTestBaseError):
    def __init__(self, msg='关键字语法使用错误'):
        HttperApiTestBaseError.__init__(self, msg=msg)


class CaseAssertNotSport(HttperApiTestBaseError):
    def __init__(self, msg='斷言方式不支持'):
        HttperApiTestBaseError.__init__(self, msg=msg)


class CaseAssertFailed(HttperApiTestBaseError):
    def __init__(self, msg='断言失败'):
        HttperApiTestBaseError.__init__(self, msg=msg)


class ResponseNotJson(HttperApiTestBaseError):
    def __init__(self, msg='此断言对象必须为json'):
        HttperApiTestBaseError.__init__(self, msg=msg)


class HttpCodeError(HttperApiTestBaseError):
    def __init__(self, msg='接口请求失败'):
        HttperApiTestBaseError.__init__(self, msg=msg)