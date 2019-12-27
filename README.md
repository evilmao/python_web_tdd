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
- [第七章:美化您的网站](https://github.com/evilmao/python_web_tdd/tree/v7.0)

### 本章知识点
**当前位于第 [7](https://github.com/evilmao/python_web_tdd/tree/v7.0) 章**


### 7.1如何在功能测试中测试布局和样式

1. 运行程序, 使用浏览器打开网站发现, 网页非常丑陋, 如果想使用户对我们设计的网站有更大的吸引力,内容很重要,当然界面的美化也及其关键? 那么可以把通用代码放在一起。谢天谢地，Django 使用 的模板语言可以轻易做到这一点，这种功能叫作“模板继承”。

### 7.2 模板继承
1. 步骤:先弄清了两个模板之间共通以及有差异的地方;找到共同之处放进公用模板中;标记出各个'块', 块中的内容留给子模版
2. 如下代码:

    原home.html
    ```html
    <html>
    <head>
      <meta charset="UTF-8">
      <title>To-Do lists</title>
    </head>
    <body>
        <h1>Start a new To-Do list</h1>
        <form method="POST" action="/lists/new">
           <input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />
           <!--get 请求方式时,测试无法通过,此时csrf_token渲染不了模板里面-->
           {% csrf_token %}
        </form>
    </body>
    </html>
    ```

    原list.html
    ```html
    <html>
    <head>
      <meta charset="UTF-8">
      <title>To-Do lists</title>
    </head>
    <body>
        <h1>Your To-Do</h1>
        <form method="POST" action="/lists/{{ list.id }}/add_item">
           <input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />
           <!--get 请求方式时,测试无法通过,此时csrf_token渲染不了模板里面-->
           {% csrf_token %}
        </form>
        <table id="id_list_table">
           {% for item in list.item_set.all %} <!--使用反向查询-->
             <tr><td>{{ forloop.counter }}: {{ item.text }}</td></tr>
           {% endfor %}
        </table>
    </body>
    </html>
    ```

    提取通用代码:base.html
    ```html
    <html xmlns="http://www.w3.org/1999/html">
    <head>
      <meta charset="UTF-8">
      <title>To-Do lists</title>
    </head>
    <body>
        <h1>{% block header_text %}{% endblock %}</h1>
        <form method="POST" action="{% block form_action %}{% endblock %}">
         <input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />
         <!--get 请求方式时,测试无法通过,此时csrf_token渲染不了模板里面-->
         {% csrf_token %}
        </form>
        {% block table %}
        {% endblock %}
    </body>
    </html>
    ```

    使用模板继承后的代码如下
    home.html
    ```html
    {% extends 'base.html' %}

    {% block header_text %}Start a new To-Do list{% endblock %}

    {% block form_action %}/lists/new{% endblock %}
    ```

    list.html
    ```html
    {% extends 'base.html' %}

    {% block header_text %}Your To-Do list{% endblock %}

    {% block form_action %}/lists/{{ list.id }}/add_item{% endblock %}
    {% block table %}
        <table id="id_list_table">
        {% for item in list.item_set.all %}
            <tr><td>{{ forloop.counter }}: {{ item.text }}</td></tr>
        {% endfor %}
        </table>
    {% endblock %}
    ```
3. 模板继承使用 `{% extends 'xx.html' %}`

> 注意: 原书中说明"虽 然 runserver 启 动 的 开 发 服 务 器 能 自 动 找 到 静 态 文 件， 但 LiveServerTestCase 找不到。" 再使用django 2.1.7版本中发现并未发现此问题.所以此处代码未做修改.



### 7.3 使用bootstrap中的组件改进网站外观.

1. 使用jumbotron用于特别突出地显示页面中的元素.

### 7.4 collectstatic命令和其他静态目录

1. 在真正的 Web 服务器中，并不需要让 Django 伺服静态内容，因为使用 Python 伺服原始文件速度慢而且效率低，Apache、Nginx 等 Web 服务器能更好 地完成这项任务
2. 如果项目中有多个app, 每个app下都有自己独立的静态文件,要把分散在各个应用文件夹中的所有静态文件集中起来，复制一份放在一个位 置，为部署做好准备。collectstatic 命令的作用就是完成这项操作。
3. 静态文件集中放置的位置由 `settings.py` 中的 `STATIC_ROOT` 定义

    settings.py
    ```python
    ...
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ...
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../static'))
    ```
4. 执行指令: `python3 manage.py collectstatic`


### TDD总结

1. 不应该为设计和布局编写测试。因为这太像是测试常量，所以写出的测试 不太牢靠。
2. 可以编写一 些简单的“冒烟测试”，确认静态文件和 CSS 起作用即可.