from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve

from .views import home_page


# Create your tests here.

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        """测试home_page的url是否使lists/home_page/"""
        found = resolve('/lists/home_page/')
        self.assertEqual(found.func, home_page)

    # def test_home_page_return_correct_html(self):
    #     """测试home_page页面能返回正常的页面"""
    #     request = HttpRequest()  # 创建了一个 HttpRequest 对象
    #     response = home_page(request)  # 把这个 HttpRequest 对象传给 home_page 视图，得到响应。
    #
    #     expected_html = render_to_string('home.html')
    #     self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        """测试home_page视图可以保存一个post请求"""
        # 设置测试背景
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        # 执行代码
        response = home_page(request)
        # 编写断言
        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'}
        )
        self.assertEqual(response.content.decode(), expected_html)
