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
- [第九章:使用Fabric部署您的网站](https://github.com/evilmao/python_web_tdd/tree/v9.0)

### 本章知识点
**当前位于第 [9](https://github.com/evilmao/python_web_tdd/tree/v9.0) 章**

使用 Fabric 可以在服务器中自动执行命令。可以系统全局安装 Fabric，因为它不是网站的 核心功能，所以不用放到虚拟环境中.
本地电脑中执 行下述命令安装 Fabric：

`$ pip2 install fabric` # python2

`$ pip3 install fabric3` # python3

Fabric需要依赖pycrypto.所以也需要安装pycrypto
`$ pip install pycrypto`

> 说明: linux可以正常执行, windows安装的时候会提示错误, 如
`unable to find vcvarsall.bat`,此时建议使用whl文件来安装
以python 3.5为例, 参考[pycrypto](https://github.com/sfbahr/PyCrypto-Wheels)下载对应版本的pycrypto后,
`pip install --no-index --find-links=https://github.com/sfbahr/PyCrypto-Wheels/raw/master/pycrypto-2.6.1-cp35-none-win_amd64.whl pycrypto
`
### 9.1 Fabric部署脚本

1. 每一个部署步骤,写一个独立的函数.通过main主函数,来关联所有的步骤, 最后通过fab命令行传递参数

    - 创建目录结构的方法:`_create_directory_structure_if_necessary`
    - 拉取源码: `_get_latest_source`
    - 更新新配置文件: `_update_settings`
    - 创建虚拟环境: ` _update_virtualenv`
    - 更新数据库文件: `_update_database`
2. fab常见的函数

    - `run`:作用是在服务器中执行指定的 shell 命令
    - `local`: 在本地电脑中执行命令,是对subprocess.Popen的再包装.
    - `sed`: 在文件中替换字符串,类似于正则
    - `append`: 在文件末尾添加一行内容

### 9.2 试用部署脚本

1. 将脚本放入到需要部署的服务器中;
2. 执行指令 `fab deploy:host=faily@failytodo-superlist.tk`

#### 9.2.1 部署到线上服务器
1. 执行fab deploy --host=failytodo-superlist.tk

#### 9.2.2 使用sed配置Nginx和Gunicorn
把网站放到生产环境之前还要做什么呢？根据配置笔记，还要使用模板文件创建 Nginx 虚拟主机和 Upstart 脚本

-  `"s/SITENAME/failytodo.superlist.tk/g"  deploy_tools/nginx.template.conf | sudo tee   /etc/nginx/sites-available/failytodo-superlist.conf`
    -  s/replaceme/withthis/g 句法把字符串 SITENAME 替换成 网站的地址
    - 使用管道操作（|）把文本流传给一个有 root 权限的用户处
- 激活这个文件配置的虚拟主机：
    - `sudo ln -s ../sites-available/failytodo-superlist.tk     /et/nginx/sites-enabled/failytodo-superlist.tk`
- 然后编写 Upstart 脚本：
    -  `sed "s/SITENAME/failytodo-superlist.tk/g"   deploy_tools/gunicorn-upstart.template.conf | sudo tee    /etc/init/gunicorn-failytodo-superlist.tk`
- 启动两个服务
    - `systectl reload nginx`
    - `start gunicorn-failytodo-superlist.tk`

### 使用Git标签标注发布状态

为了保留历史标记，使用 Git 标签（tag）标注代码库的状态，指明服务器中当前使用的是哪个版本：
1. 执行以下指令
    ``` python
    $ git tag LIVE
    $ export TAG=`date +DEPLOYED-%F/%H%M` # 生成一个时间戳
    $ echo $TAG                           # 会显示“DEPLOYED-”和时间戳
    $ git tag $TAG                        # 生成一个标签
    $ git push origin LIVE $TAG           # 推送标签到远程仓库
    ```
2. 查看历史标签
    `git log --graph --oneline --decorate`


### 总结-自动部署

- Fabric

    Fabric 允许在 Python 脚本中编写可在服务器中执行的命令。这个工具很适合自动执 行服务器管理任务。
- 幂等

    如果部署脚本要在已经配置的服务器中运行，就要把它设计成既可在全新的服务器 中运行，又能在已经配置的服务器中运行。
• 把配置文件纳入版本控制

    一定不能只在服务器中保存一份配置文件副本。配置文件对应用来说非常重要，应 该和其他文件一样纳入版本控制。
- 自动配置

    最终，所有操作都要实现自动化，包括配置全新的服务器和安装所需的全部正确软 件。配置的过程中会和主机供应商的 API 交互。
• 配置管理工具

    Fabric 很灵活，但其逻辑还是基于脚本的。高级工具使用声明式的方法，用起来更 方便。Ansible和Vagrant都值得一试（参见附录 C），此外还有很多同类工具，例如Chef、Puppet、Salt和Juju 等

