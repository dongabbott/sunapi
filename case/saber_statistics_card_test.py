from libs.load import call_case
import allure
import pytest


@allure.feature('测试名片数据分析')
class TestCardStatistics(object):

    @allure.story('测试总计')
    @call_case('D:\code\python\cronusweb\data\saber_statistics_card_test.yaml')
    def test_total_statistics(self):
        pass
 
        
if __name__ == '__main__':
    pytest.main(['-s', '-q', '-v', 'saber_statistics_card_test.py', '--alluredir', '../report'])
    
