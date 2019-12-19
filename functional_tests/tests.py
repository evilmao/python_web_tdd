# -*-coding:utf-8-*-

'''
functional test: 功能测试
'''
import unittest
from django.test import  LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.binary_location = "D:\soft\Google\Chrome\Application\chrome.exe"


class NewVisitorTest(LiveServerTestCase):
    """使用LiveServerTestCase 隔离测试"""

    def setUp(self):
        self.browser = webdriver.Chrome(chrome_options=options)
        self.browser.implicitly_wait(3)  # 隐式等待几秒,以便页面加载完成

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self,row_text):
        """重构:辅助函数, 用来检测row是否在table list"""
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # allen听说有一个很酷的在线待办事项应用
        # 她去看了这个应用的首页
        self.browser.get('http://localhost:8000/lists/home_page/')
        # self.browser.get(self.live_server_url)

        # 她注意到网页的标题和头部都包含“To-Do”这个词
        self.assertIn('To-Do', self.browser.title)  # ➎
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 应用邀请她输入一个待办事项
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # 她在一个文本框中输入了 “Buy peacock feathers”（购买孔雀羽毛）
        # allen的爱好是使用假蝇做饵钓鱼
        input_box.send_keys('Buy peacock feathers')

        # 她按回车键后，页面更新了
        # 待办事项表格中显示了“1: Buy peacock feathers
        input_box.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 她输入了“Use peacock feathers to make a fly”（使用孔雀羽毛做假蝇）
        # 伊迪丝做事很有条理
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)

        # 页面再次更新，她的清单中显示了这两个待办事项
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # 伊迪丝想知道这个网站是否会记住她的清单
        # 她看到网站为她生成了一个唯一的URL # 而且页面中有一些文字解说这个功能

        # 她访问那个URL，发现她的待办事项列表还在

        # 她很满意，去睡觉了
        self.fail('Finish the test!')  # ➏


# if __name__ == '__main__':  # ➐
#     unittest.main(warnings='ignore')  # ➑
