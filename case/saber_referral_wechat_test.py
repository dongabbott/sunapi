from libs.load import call_case
import allure
import pytest


@allure.feature('转介绍小程序人个中心')
class TestUserPersonal(object):

    @allure.story('领取信息提交')
    @call_case('D:\code\python\cronusweb\data\saber_referral_wechat_test.yaml')
    def test_card_information_add(self):
        pass
 
        
if __name__ == '__main__':
    pytest.main(['-s', '-q', '-v', 'saber_referral_wechat_test.py', '--alluredir', '../report'])
    
