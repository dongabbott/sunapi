### pytest allure requests yaml接口测试框架

框架由pytest执行测试用列，测试用例自动生成，只需要编写yaml格式的测试数据文件，测试数据支持动态提取。 接口请求由requests完成， allure生成测试报告, 是一个方便美观的接口测试框架。

##### 安装
```python
pip install -r requirements.txt

```
#### 测试用列文件
```yaml

case_suite: saber_referral_active_test  # pytest测试用例的文件名
descrpiton: 测试文件描述
moduels:
  - moduel_class: TestReferralRules  # pytest测试类名
    desc: 测试类描述
    cases:
      - story: test_referral_rule_list  # pytest用例名
        desc: 默认规则列表查询   #用例描述
        uri: /saber/backend/rule  # 接口地址
        method: post   # 请求方式
        headers:      # 请求头
        type: data    # 请求类型 
        data:         # 测试数据
          activity_end_at: 
          activity_start_at: 
          division: 
          page: 1
          page_size: 30
        auth_user:   # 请求用户名， 跟据情况需要自定义登录入口
          u: dongjie02
        set_up:     # 前置条件  
        tear_down:  # 后置条件
        asserts:
          body.status: '00000'
          body.data.orgArr[0]: '测试数据'

```

数据、前后置条件及断言，可引入关键字，关键字用法${function(*args, **kw)|module}

#### 运行测试用例
```bash
python run.py --run 'testdir'
```