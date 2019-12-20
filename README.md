[toc]
# python_web_tdd

python web 驱动测试代码demo及各章知识点

### 各章知识点传送门
- [第一章:使用功能测试协助安装Django](https://github.com/evilmao/python_web_tdd/tree/v1.0)
- [第二章:使用unittest模块扩展功能测试](https://github.com/evilmao/python_web_tdd/tree/v2.0)
- [第三章:使用单元测试测试简单的页面](https://github.com/evilmao/python_web_tdd/tree/v3.1)
- [第四章:编写这些测试有什么用](https://github.com/evilmao/python_web_tdd/tree/v4.0)
- [第五章:保存用户输入到数据库](https://github.com/evilmao/python_web_tdd/tree/v5.0)
- [第六章:完成简单的可用网站](https://github.com/evilmao/python_web_tdd/tree/v6.0)

### 本章知识点
**当前位于第 [6](https://github.com/evilmao/python_web_tdd/tree/v6.0) 章**

*上一章遗留的问题:功能测试运行结束后的清理,每运行一次测试,都会向数据库提交一次数据???*


### 6.1 确保功能测试之间相互隔离
如何隔离测试。运行功能测试后待办事项一直 存在于数据库中，这会影响下次测试的结果。

运行单元测试时，Django 的测试运行程序会自动创建一个全新的测试数据库（和应用真正 使用的数据库不同），运行每个测试之前都会清空数据库，等所有测试都运行完之后，再 删除这个数据库。但是功能测试目前使用的是应用真正使用的数据库 db.sqlite3。

- 解决方法之一是自己动手，在 functional_tests.py 中添加执行清理任务的代码。 这样的任务最适合在 setUp 和 tearDown 方法中完成。
- 从 1.4 版开始，Django 提供的一个新类，LiveServerTestCase，它可以代我们完成这 一任务

#### 只运行单元测试
1. 如果执行 manage.py test 命令，Django 会运行功能测试和单元测试
2. 如果只想运行单元测试，可以指定只运行 lists 应用中的测试`python manage.py test lists`
3. 运行功能测试: `python manage.py test functional_tests`


### 6.2 必要时做少量的设计

1. 敏捷理念则认为，在实践中解决问题比理论分析能学到更多，而且让应用尽 早接受真实用户的检验效果更好
2. 无需花这么多时间提前设计，而要尽早把最简可用的应 用放出来，根据实际使用中得到的反馈逐步向前推进设计
3. 守敏捷理念的另一个信条:`YAGNI`(You aint gonna need it)简称（“你不需要这个”）,抵御内心某个想法并想把他创造出来的冲动.

#### 6.2.2 REST API

"表现层状态转化"（Representational State Transfer，REST）是 Web 设计的一种方式，经 常用来引导基于 Web 的 API 设计.

### 6.3 每一个视图函数对应一个模板(html)

1. assertTemplateUsed 是 Django 测试客户端提供的强大方法之一, 用来判断返回的视图对象是否属于某个存在的模板文件
    `assertTemplateUsed(response, 'base.html')`

### 6.4 重构

1. 不同类型的测试放进不同的类中.

### 6.5 数据库表之间的关联

1. 使用外键实现的关联:
    > 若想保存对象之间的关系，要告诉 Django 两个类之间的关系，这种关系使用 ForeignKey 字段表示：
    ```python
    from django.db import models

    class List(models.Model):
        pass


    class Item(models.Model):
        text = models.TextField(default='')
        list = models.ForeignKey(List, default=None,on_delete=True) # 使用Foreignkey关联
    ```
2. django在执行迁移文件后，如果想删除迁移文件，重新修改，则需要删除生成的迁移文件
    `rm lists/migrations/0004_item_list.py`,然后重新执行迁移.

3. **django2.0中**`ForeignKey`参数`on_delete`为必填参数，关于各参数的说明如下：
    1. `on_delete=None`                # 删除关联表中的数据时,当前表与其关联的field的行为
    2. `on_delete=models.CASCADE`,     # 删除关联数据,与之关联的表也删除
    3. `on_delete=models.DO_NOTHING`,  # 删除关联数据,什么也不做
    4. `on_delete=models.PROTECT`      # 删除关联数据,引发错误ProtectedError
    5. `models.ForeignKey('关联表', on_delete=models.SET_NULL, blank=True, null=True)`
    6. `on_delete=models.SET_NULL`,    # 删除关联数据,与之关联的值设置为null（前提FK字段需要设置为可空,一对一同理）
    7. `models.ForeignKey('关联表', on_delete=models.SET_DEFAULT, default='默认值')`
    8. `on_delete=models.SET_DEFAULT`, # 删除关联数据,与之关联的值设置为默认值（前提FK字段需要设置默认值,一对一同理）
    9. `on_delete=models.SET`,         # 删除关联数据,

### 6.6 视图函数返回对象

1. 示例代码
    ```python
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/{}/'.format (correct_list.id))
        self.assertEqual(response.context['list'], correct_list)
    ```
    视图函数返回为HttpResponse对象，通过`对象.context` 可以获取视图函数传递给前端的上下文。response.context 表示要传入 render 函数的上下文.


### 6.7 ORM反向查询

1. 关于反向查询概念：一对多关联的两个表（model）,存在ForeignKey字段所在的model的我们成为正向表，而关联的model称为反向表。
    如下：
    ```python
    # coding:utf-8
    from django.db import models

    # Create your models here.

    class List(models.Model):
        pass


    class Item(models.Model):
        text = models.TextField(default="")
        list = models.ForeignKey('List', on_delete=models.CASCADE)
    ```
    1. 上面两个模型，其中ForeignKey存在于Item 模型中，所以通过Item查询list称之`正向查询`: `Item.objects.filter(list=list_)`
    2. List模型是被关联的模型，称为反向表，即`一个List下面可以包含多个item`,所以通过List表来查询item的条目称为反向查询： `List.object.get(id=1).item_set().all()`
    3. 反向查询同样可以用于模板标签中 `{% for item in list.item_set.all %}...{% endfor %}`


### 总结

**有用的 TDD 概念和经验法则**
- 测试隔离和全局状态
   - 不同的测试之间不能彼此影响，也就是说每次测试结束后都要还原所做的永久性操 作。Django 的测试运行程序可以帮助我们创建一个测试数据库，每次测试结束后都 会清空数据库（详情参见第 19 章）。
- 从一个可运行状态到另一个可运行状态（又叫测试山羊与重构猫）
  - 本能经常驱使我们直接动手一次修正所有问题，但如果不小心，最终可能像重构猫 一样，改动了很多代码但都不起作用。测试山羊建议我们一次只迈一步，从一个可 运行状态走到另一个可运行状态。
- YAGNI
  - "You ain’t gonna need it"（你不需要这个）的简称，劝诫你不要受诱惑编写当时看 起来可能有用的代码。很有可能你根本用不到这些代码，或者没有准确预见未来的 需求。第 18 章给出了一种方法，可以让你避免落入这个陷阱