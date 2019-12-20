from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from .models import Item
from .views import home_page


# Create your tests here.

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        """测试home_page的url是否使lists/home_page/"""
        found = resolve('/lists/')
        self.assertEqual(found.func, home_page)

    # def test_home_page_return_correct_html(self):
    #     """测试home_page页面能返回正常的页面"""
    #     request = HttpRequest()  # 创建了一个 HttpRequest 对象
    #     response = home_page(request)  # 把这个 HttpRequest 对象传给 home_page 视图，得到响应。
    #
    #     expected_html = render_to_string('home.html')
    #     self.assertEqual(response.content.decode(), expected_html)


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        """测试Item model保存一条数据"""
        first_item = Item()  # 实例化一个model
        first_item.text = 'The first (ever) list item'  # 定义model的一个字段text并赋值
        first_item.save()  # 保存数据

        # 插入第二条
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        # 获取已插入的数据数目
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        # 检查两次插入的值是否插入成功
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')


class ListViewTest(TestCase):

    def test_display_all_items(self):
        """测试首页展示所有条目"""
        # 设置测试背景
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        # 使用Django 测试客户端。
        response = self.client.get('/lists/the-only-list-in-the-world/')
        # 编写断言
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

    def test_users_list_template(self):
        """检查是否使用了不同的模板"""
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')


class NewListTest(TestCase):

    # def test_home_page_can_save_a_POST_request(self):
    # 重命名
    def test_saving_a_Post_request(self):
        """测试可以保存一个post请求(新的视图)"""
        ''''
        # 设置测试背景
          request = HttpRequest()
          request.method = 'POST'
          request.POST['item_text'] = 'A new list item'
        # 使用django 测试客户端 self.client
        '''
        self.client.post(
            "/lists/new",
            data={'item_text': 'A new list item'}
        )

        # 编写断言
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()  # ➋
        self.assertEqual(new_item.text, 'A new list item')  # ➌

    def test_redirects_after_POST(self):
        """测试POST重定向"""
        # 使用django 测试客户端 self.client
        response = self.client.post(
            "/lists/new",
            data={'item_text': 'A new list item'}
        )
        # 编写断言
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/lists/the-only-list-in-the-world/')
