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
- [第八章:部署您的网站](https://github.com/evilmao/python_web_tdd/tree/v8.0)

### 本章知识点
**当前位于第 [8](https://github.com/evilmao/python_web_tdd/tree/v8.0) 章**

### 8.1 TDD以及部署的危险区域
部署过程中的一些危险区域如下:

1. 静态文件（CSS、JavaScript、图片等
     - Web 服务器往往需要特殊的配置才能伺服静态文件。
2. 数据库
     -  可能会遇到权限和路径问题，还要小心处理，在多次部署之间不能丢失数据。
3. 依赖
    - 要保证服务器上安装了网站依赖的包，而且版本要正确。

如何解决这些问题?
1. 使用与生产环境一样的基础架构部署“过渡网站”（staging site），这么做可以测试部署 的过程，确保部署真正的网站时操作正确
2. 可以在过渡网站中运行功能测试，确保服务器中安装了正确的代码和依赖包。而且为了 测试网站的布局，我们编写了冒烟测试，这样就能知道是否正确加载了 CSS
3. 在可能运行多个 Python 应用的设备中，可以使用 virtualenv 管理包和依赖。
4. 最后，一切操作都自动化完成。使用自动化脚本部署新版本，使用同一个脚本把网站部 署到过渡环境和生产环境，这么做能尽量保证过渡网站和线上网站一样。

### 8.2 先写测试

修改功能测试, 让它能在过渡网站中运行