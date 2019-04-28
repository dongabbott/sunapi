import pytest
import allure


@allure.feature('3.8妇女节活动')
class TestHolidaysWoman(object):

    @allure.story('创建语录')
    def test_holidays_add(self):
        """ 测试abbott
        """
        assert 1 == 2

    @allure.story('获取语录列表')
    def test_get_holidays_ana(self):
        """ 测试dongjie
        """
        assert 1 == 1


if __name__ == '__main__':
    pytest.main(['-s', '-q', '--alluredir', '../report'])