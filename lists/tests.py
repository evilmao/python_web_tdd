from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from .models import Item, List
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

        # 实例化List模板
        list_ = List()
        list_.save()

        # 实例化Item模型，并插入数据
        first_item = Item()                             # 实例化一个Item 数据模型
        first_item.text = 'The first (ever) list item'  # 定义model的一个字段text并赋值
        first_item.list = list_                         # 为Item实例的list（字段）赋值
        first_item.save()                               # 保存数据

        # 插入第二条
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        # 获取已插入的数据数目
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        # 检查两次插入的值是否插入成功
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)                      # 检查item第一次插入数据时，是否成功关联list
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)                      # 检查item第二次插入数据时，是否成功关联list



class ListViewTest(TestCase):

    def test_displays_only_items_for_that_list(self):
        """检查每一个代办事项都有唯一的URL"""
        # 设置测试背景
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)
        # 使用Django 测试客户端。
        response = self.client.get('/lists/{}/'.format(correct_list.id))
        # 编写断言
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response,'other list item 1')
        self.assertNotContains(response,'other list item 2')

    def test_users_list_template(self):
        """检查是否使用了不同的模板"""
        list_ = List.objects.create()                                # 插入一条新的List数据，返回queryset对象
        response = self.client.get('/lists/{}/'.format(list_.id))    # 获取当前queryset的id属性
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        """检测"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get('/lists/{}/'.format(correct_list.id))
        self.assertEqual(response.context['list'],correct_list)

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
        new_list = List.objects.first()
        # 编写断言

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/lists/{}/'.format(new_list.id,))


class NewItemTest(TestCase):

    def test_can_save_a_POST_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/{}/add_item'.format(correct_list.id),
            data = {'item_text': 'A new item for an existing list'}
        )
        # 断言
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)


    def test_redirect_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/{}/add_item'.format(correct_list.id),
            data={'item_text': 'A new item for an existing list'}
         )

        self.assertRedirects(response, '/lists/{}/'.format(correct_list.id))
