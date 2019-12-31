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

### 8.3 注册域名
如果你从未注册过域名，随便选一个 老牌注册商买一个便宜的就行，只要花 5 美元左右，甚至还能找到免费域名。
这里推荐一个域名免费注册:[Freenom](https://my.freenom.com/clientarea.php)

- 这里注册了免费的域名为: `failytodo-superlist.tk`
### 8.4 手动配置托管网站的服务器

1. 配置新的服务器, 用于托管代码.

2. 把新的代码部署到配置好的服务器中.

#### 8.4.1 选择在哪里托管你的网站
- 运行自己的服务器(可能是虚拟服务器)
- 使用"平台即服务"(Platform-As-A-Service,PaaS)提供商,例如 `Heroku`、`DotCloud`、 `OpenShift` 或 `PythonAnywhere`。

对小型网站而言，PaaS 的优势尤其明显，我强烈建议你考虑使用 PaaS。

#### 8.4.2 搭建服务器
满足以下条件即可
- 服务器的系统使用 Ubuntu（13.04 或以上版本）/Centos 6以上；
- 有访问服务器的 root 权限；
- 外网可访问；
- 可以通过 SSH 登录

### 8.4.3 用户账户、SSH和权限
节假定你的用户账户没有 root 权限，但有使用 sudo 的权限，因此执行需要 root 权限的 操作时，我们可以使用 sudo。

如果需要 创建非 root 用户，可以这么做：

```shell
# 这些命令必须以root用户的身份执行
root@server:$ useradd -m -s /bin/bash faily # 添加用户，名为faily
# -m表示创建家目录， -s表示elspeth默认能使用bash
root@server:$ usermod -a -G sudo faily # 把faily添加到sudo用户组
root@server:$ passwd faily # 设置faily的密码
root@server:$ su - faily # 把当前用户切换为faily
failyh@server:$
```

> 通过 SSH 登录时，建议你别用密码，应该学习如何使用私 钥认证。若想使用私钥认证，要从自己的电脑中获取公钥，然后将其附加到服务器用户账户 下的 ~/.ssh/authorized_keys 文件中

#### 8.4.4 安装Nginx

1. Ubuntu使用 apt-get 指令安装
    - sudo apg-get install nginx  # 安装
    - sudo service nginx start    # 启动
2. Centos 安装
    - yum install nginx
    - systemctl start nginx.service

#### 8.4.5 解析过渡环境和线上环境所用的域名

在 DNS 系统中，把域名指向一个确切的 IP 地址叫作"A记录"。不想总是使用 IP 地址，所以要把过渡环境和线上环境所用的域名解析到服务器上.

在这里可以使用国内的腾讯云进行域名解析, 我使用的是新加坡注册商: [`GoDaddy`](https://dcc.godaddy.com/domains/)

步骤:
1. 首先在官网注册账号: https://sg.godaddy.com/zh
2. 登录后进入(域名管理器/添加 DNS 托管): https://dcc.godaddy.com/domains/dnsHosting/add
3. 在"域名"框中添加需要托管的域名: failytodo-superlist.tk
4. 成功后会显示域名服务器如下图:

    ![](../superlists/doc/img/Godaddy_domain_1.png)


5. 进入freenom页面: https://my.freenom.com/clientarea.php

   登录后

   依次 `Services-->My Domains--> Manage Domain`

   ![](../superlists/doc/img/freenom_domain_1.png)

   依次:`Management Tools--> Nameservers-->Use custom nameservers (enter below)`

   ![](../superlists/doc/img/freenom_domain_2.png)

   将 `4`中获取的 dns连接填入, 确认保存

   ![](../superlists/doc/img/freenom_domain_3.png)

6. 回到Godaddy中,解析域名, 选择需要解析的域名: `failytodo-superlist.tk`
    在"记录" 列表的右下方点击`添加`, 类型选择 `A`,主机 `@`,指向需要解析到的 服务器ip地址 `x.x.x.x`. 保存

7. 验证域名是否解析到正确的ip上: `ping failytodo-superlist.tk` 如果出现正确的ip则说明解析成功.


#### 8.4.6 使用功能测试确认域名可用且Nginx正在运行

### 8.5 手动部署代码

接着要让过渡网站运行起来，检查 Nginx 和 Django 之间能否通信,在部署的过程中，要思考如何自动化这些操作。


#### 8.5.1 注意的点

1. 需要一个文件夹用来存放源码
2. 不论使用什么主机， 一定要以非 root 用户身份运行 Web 应用
3. 按照下面的文件结构存放网站的代码:
    ```markdown
    /home/elspeth
    ├─ sites
    │   ├─ www.failytodo-superlist.tk
    │   │    ├─ database
    │   │    │    └─ db.sqlite3
    │   │    ├─ source
    │   │    │    ├─ manage.py
    │   │    │    ├─ superlists
    │   │    │    ├─ etc...
    │   │    │
    │   │    ├─ static
    │   │    │    ├─ base.css
    │   │    │    ├─ etc...
    │   │    │
    │   │    └─ virtualenv
    │   │         ├─ lib
    │   │         ├─ etc...
    │   │
    │   ├─ www.faily-blog.xyz
    │   │    ├─ database
    │   │    ├─ etc...
    ```

    1. 每个网站都放在各自的文件夹中
    2. 各个文件夹有单独的子文件夹，分别存放`源码`、`数据库`和`静态文件`。

    **好处是**: 不同版本的网站源码可能会变，但数据库始终不变;静态文件夹也在同一个相对位置， 即 ../static;又独立的virtualenv


#### 8.5.2 调整数据库的位置

1. setting中设置DATABASES路径
2. 项目下新建目录: `mkdir database`
3. 执行新的数据库迁移: `python manage.py migrate --noinput`

借助代码托管网站将代码上传到服务器: `gitlab`, `github`, `码云`...

1. 为网站新建独立的文件夹:
    ``` shell
    faily@server:$ export SITENAME=failytodo-superlist.tk
    faily@server:$ mkdir -p ~/sites/$SITENAME/database
    faily@server:$ mkdir -p ~/sites/$SITENAME/static
    faily@server:$ mkdir -p ~/sites/$SITENAME/virtualenv
    ```
2. 将代码拉取至服务器:
    `git clone https://github.com/evilmao/python_web_tdd.git`

3. 配置相同的虚拟环境: 使用 virtualenv 注意相对路径,参考项目结构

4. 安装依赖包: `pip install  -i https://pypi.tuna.tsinghua.edu.cn/simple  -r requirements.txt`

5. 运行测试: `python manage.py test lists`

#### 8.5.3 简单配置Nginx
1. 为每一个单独的应用新建一个独立的配置文件, 配置文件统一放在
    `/etc/nginx/conf.d/`
2. 编写如下配置:
    ```yaml
    server {
        listen 80;
        server_name failytodo-superlist.tk;

        location / {
            proxy_pass http://localhost:8000;
        }
    }
    ```

### 8.6 生产环境部署
Django自带的服务器为wsgi, 效率低下. 使用gunicorn可以很好的解决多用户访问性能问题.

#### 8.6.1 使用gunicorn 启动服务
1. 安装: `pip install gunicorn`
2. 运行: `../virtualenv/bin/gunicorn superlist.wsgi:application`

#### 8.6.2 nginx伺服静态文件

1. 使用`collectstatic`命令，把所有静态文件复制到一个 Nginx 能找到的文件夹中
2. 指令 :`../virtualenv/bin/python manage.py collectstatic --noinput`
3. 修改nginx配置:
    ```shell
    server {
        listen 80;
        server_name failytodo-superlist.tk;

        location / {
            proxy_pass http://localhost:8000;
        }

        location /static {
            alias /home/faily/sites/failytodo-superlist.tk/static;
        }
    }
    ```







