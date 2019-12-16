from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from .views import home_page


# Create your tests here.

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        """测试home_page的url是否使lists/home_page/"""
        found = resolve('/lists/home_page/')
        self.assertEqual(found.func, home_page)

    def test_home_page_return_correct_html(self):
        """测试home_page页面能返回正常的页面"""
        request = HttpRequest()  #创建了一个 HttpRequest 对象
        response = home_page(request) #把这个 HttpRequest 对象传给 home_page 视图，得到响应。
        # self.assertTrue(response.content.startswith(b'<html>'))
        # self.assertIn(b'<title>To-Do lists</title>',response.content)  # ➍
        # self.assertTrue(response.content.endswith(b'</html>')) #➎
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


