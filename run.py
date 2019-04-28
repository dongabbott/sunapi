# -*-coding:utf-8 -*-
from libs.yaml_parse import ConfigParser, CaseYamlParser
import os
import subprocess
from ruamel import yaml
import click
import sys


def create_project(dir_name):
    """创建项目"""
    setting_content = {}
    cur_path = os.path.abspath(dir_name)
    if os.path.exists(dir_name) is False:
        os.makedirs(cur_path)
    set_path = os.path.join(cur_path, 'setting.yaml')
    # 输入测试项目名称
    project_name = input("请输入项目名称:")
    setting_content['project'] = project_name
    # 输入api测试地址
    host = input("请输入接口地址:")
    setting_content["address"] = {}
    setting_content['address']['host'] = host
    setting_content['address']['port'] = 80
    # 请输入测试用例目录
    data_dir = input("请输入用例目录(默认为{}):".format(os.path.join(cur_path, 'case')))
    setting_content["testcase"] = {}
    data_dir = data_dir if data_dir != '' else os.path.join(cur_path, 'case')
    if os.path.exists(data_dir) is False:
        os.makedirs(data_dir)
    setting_content['testcase']['casedata'] = data_dir
    # 请输入测试用例数据目录data
    case_dir = input("请输入用例目录(默认为{}):".format(os.path.join(cur_path, 'data')))
    case_dir = case_dir if case_dir != '' else os.path.join(cur_path, 'data')
    if os.path.exists(case_dir) is False:
        os.makedirs(case_dir)
    setting_content['testcase']['casepath'] = case_dir
    # 日志配置
    setting_content["logger"] = {}
    setting_content['logger']['path'] = os.path.join(cur_path, 'logs')
    setting_content['logger']['level'] = 'debug'
    # 数据库配置
    setting_content['database'] = {
        "class": "mysql",
        "host": "172.16.225.15",
        "port": 3306,
        "db": "zeus",
        "user": "root",
        "password": "123456"
        # charset: utf-8
    }
    with open(set_path, 'w', encoding='utf-8') as s:
        content = yaml.dump(setting_content, Dumper=yaml.RoundTripDumper)
        s.write(content)


def get_set_dict(path):
    """获取配置内容"""
    with open(path, 'r', encoding='utf-8') as f:
        cont = f.read()
    setting = yaml.safe_load(cont)
    return setting


def create_tmp_case_file(data_path=None):
    if not data_path:
        data_path = ConfigParser().api_data_dir
    files = [os.path.join(data_path, x) for x in os.listdir(data_path) if x.endswith('.yaml')]
    print("开始创建测试临时文件")
    for f in files:
        CaseYamlParser(f).create()
    return True


def start_test(test_dir):
    """执行测试用列"""
    command = "pytest -s -q {} --alluredir=./report".format(test_dir)
    print("开始执行测试用例")
    p = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    if p.returncode == 1:
        print(p.stdout.readlines())
    print("开始生成测试报告")
    command_report = 'allure generate report/ -o ./report/html --clean'
    p2 = subprocess.Popen(
        command_report,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    p2.wait()
    if p2.returncode == 1:
        print(p2.stdout.readlines())


@click.command()
@click.option('--init', type=str, help="初始化一个接口测试项目")
@click.option('--cache', type=str, help="自动创建测试用例可执行文件")
@click.option('--run', type=str, help="执行指定目录的测试用例")
@click.option('--s', type=str, default='./setting.yaml', help="指定配置文件")
def run(**options):
    print(options)
    if options['run']:
        start_test(options['run'])
    elif options['init']:
        create_project(options['init'])
    elif options['cache']:
        create_tmp_case_file(options['cache'])


if __name__ == "__main__":
    sys.path.append(os.path.dirname(__file__))
    run()