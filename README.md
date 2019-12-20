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
2.