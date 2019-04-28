from ruamel import yaml
from libs.errors import YamlFormatError, CaseStoryNotFound, CaseStoryRepeat
import config
import os


class YamlJsonAttr(dict):
    """定义一个对象数据获取器"""

    def __init__(self, *args, **kwargs):
        super(YamlJsonAttr, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        value = None
        try:
            value = self[item]
        except Exception:
            pass
        if isinstance(value, dict):
            value = YamlJsonAttr(value)
        return value


class BaseYamlParser(object):
    """yaml文件解析器"""
    def __init__(self, path):
        """ymal文件路径"""
        self.path = os.path.abspath(path)

    @property
    def _reader(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            cont = f.read()
        try:
            yaml_content = yaml.safe_load(cont)
            return YamlJsonAttr(yaml_content)
        except yaml.scanner.ScannerError:
            msg = 'ymal文件{}格式不正确'.format(os.path.abspath(self.path))
            raise YamlFormatError(msg=msg)

    @property
    def to_json(self):
        return self._reader


class ConfigParser(BaseYamlParser):
    """配置文件解析器"""
    config_path = config.evn

    def __init__(self, yaml_path=config_path):
        BaseYamlParser.__init__(self, yaml_path)

    @property
    def api_host(self):
        """api服务地址"""
        return self._reader.address.host

    @property
    def api_pro_name(self):
        """api项目名称"""
        return self._reader.project

    @property
    def api_host_port(self):
        """api服务端口"""
        return self._reader.address.port

    @property
    def api_case_dir(self):
        """api测试用例目录"""
        return os.path.abspath(self._reader.testcase.casepath)

    @property
    def api_data_dir(self):
        """api测试数据目录"""
        return os.path.abspath(self._reader.testcase.casedata)

    @property
    def sql_con_pool(self):
        """api测试数据库连接地址"""
        database = self._reader.database
        chart_set = database.get('charset')
        if database['class'] == 'mysql':
            pool = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
                database['user'],
                database['password'],
                database['host'],
                database['port'],
                database['db'],
            )
            if chart_set:
                pool = pool + '?' + 'charset={}'.format(chart_set)
            return pool

    @property
    def log_level(self):
        """日志等级"""
        return self._reader.logger.level

    @property
    def log_path(self):
        """日志等级"""
        return self._reader.logger.path

    @property
    def email_option(self):
        """邮件配置"""
        return dict(self._reader.email)

    @property
    def redis_option(self):
        """redis配置"""
        return dict(self._reader.redis)


class CaseYamlParser(BaseYamlParser):
    """测试用例数据解析器"""
    def __init__(self, yaml_path):
        BaseYamlParser.__init__(self, yaml_path)

    @property
    def test_suite(self):
        """获取测试套件名称"""
        return self._reader.case_suite

    @property
    def suite_desc(self):
        """获取套件描述"""
        return self._reader.descrpiton

    @property
    def _case_modules(self):
        """获取测试用例信息"""
        return self._reader.moduels

    @property
    def suite_module_names(self):
        """获取所有的测试类"""
        return [m['moduel_class'] for m in self._case_modules]

    def _module_story(self, module_name):
        """获取指定模块的测试用例对象"""
        for mod in self._case_modules:
            if mod['moduel_class'] == module_name:
                return YamlJsonAttr(mod).cases

    def module_case_names(self, module_name):
        """获取所有测试用例名"""
        return [m['story'] for m in self._module_story(module_name)]

    def get_case_obj_by_name(self, story_name):
        """获取测试数据"""
        storys = []
        for m in self._case_modules:
            cases = m.get('cases', None)
            if cases:
                for case in cases:
                    case_data = case.get('story')
                    if case_data and case_data == story_name:
                        storys.append(case)
        if len(storys) == 0:
            raise CaseStoryNotFound
        if len(storys) > 1:
            raise CaseStoryRepeat
        return YamlJsonAttr(storys[0])

    def create(self):
        file_name = self.test_suite + '.py'
        case_file_name = os.path.join(ConfigParser().api_case_dir, file_name)
        import_ = """from libs.load import call_case
import allure
import pytest

"""
        for mod in self._case_modules:
            mod_obj = YamlJsonAttr(mod)
            mod_name = mod_obj.moduel_class
            mod_desc = mod_obj.desc
            mod_example = '''
@allure.feature('{}')
class {}(object):
'''.format(mod_desc, mod_name)
            for case in mod_obj.cases:
                case_obj = YamlJsonAttr(case)
                case_name = case_obj.story
                case_desc = case_obj.desc
                case_example = '''
    @allure.story('{}')
    @call_case('{}')
    def {}(self):
        pass
'''.format(case_desc, self.path, case_name)
                mod_example += case_example
            import_ += mod_example

        debug_info = ''' 
        
if __name__ == '__main__':
    pytest.main(['-s', '-q', '-v', '{}', '--alluredir', '../report'])
    
'''.format(file_name)
        import_ += debug_info
        with open(case_file_name, 'a', encoding='utf-8') as f:
            f.write(import_)