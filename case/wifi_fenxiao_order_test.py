from libs.load import call_case
import allure
import pytest


@allure.feature('分校预约')
class TestFenXiaoOrder(object):

    @allure.story('获取客顾详细')
    @call_case('D:\code\python\cronusweb\data\wifi_fenxiao_ order_test.yaml')
    def test_get_adivser_detail(self):
        pass

    @allure.story('获取课顾排班')
    @call_case('D:\code\python\cronusweb\data\wifi_fenxiao_ order_test.yaml')
    def test_get_adivser_scheduling(self):
        pass

    @allure.story('获取校区课顾')
    @call_case('D:\code\python\cronusweb\data\wifi_fenxiao_ order_test.yaml')
    def test_get_school_adivser(self):
        pass

    @allure.story('获取校区线路指导')
    @call_case('D:\code\python\cronusweb\data\wifi_fenxiao_ order_test.yaml')
    def test_get_school_directions(self):
        pass

    @allure.story('获取校区详细信息')
    @call_case('D:\code\python\cronusweb\data\wifi_fenxiao_ order_test.yaml')
    def test_get_school_detail(self):
        pass

    @allure.story('获取个人预约单')
    @call_case('D:\code\python\cronusweb\data\wifi_fenxiao_ order_test.yaml')
    def test_get_user_orders(self):
        pass
 
        
if __name__ == '__main__':
    pytest.main(['-s', '-q', '-v', 'wifi_fenxiao_order_test.py', '--alluredir', '../report'])
