[toc]
# python_web_tdd

python web 驱动测试代码demo及各章知识点

### 各章知识点传送门
- [第一章:使用功能测试协助安装Django](https://github.com/evilmao/python_web_tdd/tree/v1.0)
- [第二章:使用unittest模块扩展功能测试](https://github.com/evilmao/python_web_tdd/tree/v2.0)
- [第三章:使用单元测试测试简单的页面](https://github.com/evilmao/python_web_tdd/tree/v3.1)
- [第四章:编写这些测试有什么用](https://github.com/evilmao/python_web_tdd/tree/v4.0)
- [第五章:保存用户输入到数据库](https://github.com/evilmao/python_web_tdd/tree/v5.0)

### 本章知识点
**当前位于第 [5](https://github.com/evilmao/python_web_tdd/tree/v5.0) 章**

#### 5.1 代码错误几种调试方式

1. 添加 print 语句，输出页面中当前显示的文本是什么
2. 改进错误消息，显示当前状态的更多信息
3. 亲自手动访问网站(web)
4. 在测试执行过程中使用 time.sleep 暂停

#### 5.2 CSRF 错误
1. “跨站请求伪造”（Cross-Site Request Forgery，CSRF）漏洞
2. Django 针对 CSRF 的保护措施是在生成的每个表单中放置一个自动生成的令牌，通过这个 令牌判断 POST 请求是否来自同一个网站。
3. Django解决POST请求, 使用“模板标签” （template tag）添加 CSRF 令牌--- `{% csrf_token %}`,渲染模板时，Django 会把这个模板标签替换成一个 <input type="hidden"> 元

#### 5.3 编写测试函数格式(建议)

1. “设置配置 - 执行代 码 - 编写断言”是单元测试的典型结构。
2. 如下为实例代码
    ```python
    def test_home_page_display_all_list_items(self):
        """测试首页展示所有条目"""
        # 设置测试背景
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        # 执行代码
        request = HttpRequest()
        response = home_page(request)
        # 编写断言
        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())
    ```

#### 5.4 Python变量传入模板中渲染
1. 再HTML中使用 `{{ ... }}`，它会以字符串的形式显示对象
2. 如 ` <tr><td>{{ new_item_text }}</td></tr>`, 其中`new_item_text`就是python视图函数中,需要传递的变量.
3. `render_to_string`使用: 第一个参数是html文件,第二个是需要传递到模板文件的变量,返回的是html源文件
    ```python
    expected_html = render_to_string(
        'home.html',
        {'new_item_text':  'A new list item'}
    )
    ```

#### 5.5 遇红 / 变绿 / 重构和三角法
"单元测试/编写代码"循环有时也叫 "遇红/变绿/重构"

- 先写一个会失败的单元测试（遇红）
- 编写尽可能简单的代码让测试通过（变绿），就算作弊也行；
- 重构，改进代码，让其更合理

*在重构阶段应该做些什么呢？*

- 一种方法: 消除重复如果测试中使用了神奇常量（例如列表项目前面的“1:”),而 且应用代码中也用了这个常量，这就算是重复, 此时就应该重复
- 三角法:
    如果编写无法让你满意的作弊代码（例如返回一个神奇的常量）就能让测试通过,就 再写一个测试，强制自己编写更好的代码

#### 5.6 事不过三，三则重构

> 编程中有个原则叫作"不要自我重复"（Don’t Repeat Yourself， DRY），按照真言"事不过三，三则重构"的说法，运用这个原则。复制粘贴一次，可能 还不用删除重复，但如果复制粘贴了三次，就该删除重复了。


#### 5.7 Django ORM

> "对象关系映射器"（Object-Relational Mapper，ORM）是一个数据抽象层，描述存储在数 据库中的表、行和列.

在 ORM 的概念中，`类对应数据库中的表，属性对应列，类的单个实例表示数据库中的一 行数据`

**ORM一些函数**

1. `M.objects.all()` 获取M所有的数据, 结果是一个类 似列表的对象，叫 QuerySet
2. `M.save()`先创建一个对象，再为一些属 性赋值，然后调用 .save() 函数.
3. `M.objects.all().count()` 获取查询实例条数
4. `M.objects.first()`获取第一个数据文件.


#### 5.8 Django数据库迁移

> 在 Django 中，ORM 的任务是模型化数据库。创建数据库其实是由另一个系统负责的，叫 作“迁移”（migration）。迁移的任务是，根据你对 models.py 文件的改动情况，添加或删 除表和列。

1. 数据库迁移执行指令 `python manage.py makemigrations `
2. 使用迁移创建生产数据库
    1. 默认情况下，Django 把数据库保存为 db.sqlite3, Django 的 settings.py 中
    2. `python3 manage.py migrate `


**更好的单元测试实践方法：一个测试只测试一件事**

> 良好的单元测试实践方法要求，一个测试只能测试一件 事。因为这样便于查找问题。如果一个测试中有多个断言，一旦前面的断言导致测试失 败，就无法得知后面的断言情况如何

#### 5.9 Django 模板标签使用

django 有很便于使用的模板标签总结如下

1. 变量
    1. 格式：`{{ variable }}`
2. 过滤器
    1. 格式：`{{ name|lower }}`
    2. 过滤器是可以链式连接的，如`{{ text|escape|linebreaks }}`
    3. 过滤器也是可以带参数的，如`{{ bio|truncatewords:30 }}`
    4. 过滤器参数如果有空格必须引号加起来，如`{{ list|join:", " }}`
3. 标签
    1. 格式：`{% tag %}`
    2. 一些需要开始的tag和结束的tag，例如：{% tag %} ... tag contents ... {% endtag %}
    3. django 内置常用标签
        1. for循环: `{% for i in item_list %}...{% endfor %}`
        2. if 判断: `{% if %}...{% else %}...{% endif %}`
4. 注释
    1. `格式：{# comment #}`

5. 模板继承
    1. 父模板`base.html`

        ```html
        <!DOCTYPE html>
        <html lang="zh">
        <head>
            <link rel="stylesheet" href="style.css" />
            <title>{% block title %}My home page{% endblock %}</title>
        </head>

        <body>
            <div id="nav">
                {% block nav %}
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/Article/">Blog</a></li>
                </ul>
                {% endblock %}
            </div>

            <div id="content">
                {% block content %}{% endblock %}
            </div>
        </body>
        </html>
       ```
    2. 子模版
        ```HTML
        {% extends "base.html" %}

        {% block title %}My  blog{% endblock %}

        {% block content %}
            {% for article in articles %}
                <h2>{{ article.title }}</h2>
                <p>{{ article.body }}</p>
            {% endfor %}
        {% endblock %}
        ```
    3. 如果在模板中使用了`{% extends %}`,如果需要使用父模板中的block中的内容可以使用{{ block.super }}
模板的tag不要重名,django默认加入了 auto-escaping 防止XSS,取消的话，针对变量可以加入safe，如{{variable|safe}}

    4. 更多内置标签参见官方文档


### 总结
- 回归
  > 新添加的代码破坏了应用原本可以正常使用的功能。
-  意外失败
    > 测试在意料之外失败了。这意味着测试中有错误，或者测试帮我们发现了一个回 归，因此要在代码中修正。
-  遇红 / 变绿 / 重构
    > 描述 TDD 流程的另一种方式。先编写一个测试看着它失败（遇红），然后编写代码 让测试通过（变绿），最后重构，改进实现方式。
- 三角法
    >添加一个测试，专门为某些现有的代码编写用例，以此推断出普适的实现方式（在 此之前的实现方式可能作弊了）。
- 事不过三， 三则重构
    >判断何时删除重复代码时使用的经验法则。如果两段代码很相似，往往还要等到第 三段相似代码出现，才能确定重构时哪一部分是真正共通、可重用的。
- 记在便签上的待办事项清单
    >在便签上记录编写代码过程中遇到的问题，等手头的工作完成后再回过头来解决