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


