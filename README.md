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

运行程序, 使用浏览器打开网站发现, 网页非常丑陋, 如果想使用户对我们设计的网站有更大的吸引力,内容很重要,当然界面的美化也及其关键? 那么如何使用测试来测试布局和样式?
1. assertAlmostEqual 的作用 是帮助处理舍入误差，这里指定计算结果在正负五像素范围内为可接受。

