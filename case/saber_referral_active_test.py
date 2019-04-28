from libs.load import call_case
import allure
import pytest


@allure.feature('转介绍规则')
class TestReferralRules(object):

    @allure.story('默认规则列表查询')
    @call_case('D:\code\python\cronusweb\data\saber_referral_active_test.yaml')
    def test_referral_rule_list(self):
        pass

    @allure.story('规则列表子军团查询')
    @call_case('D:\code\python\cronusweb\data\saber_referral_active_test.yaml')
    def test_referral_rule_org_search(self):
        pass

    @allure.story('创建奖金活动规则')
    @call_case('D:\code\python\cronusweb\data\saber_referral_active_test.yaml')
    def test_referral_rule_add_reward(self):
        pass
 
        
if __name__ == '__main__':
    pytest.main(['-s', '-q', '-v', 'saber_referral_active_test.py', '--alluredir', '../report'])
    
