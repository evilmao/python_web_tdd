配置新网站 =========

## 需要安装的包：

* nginx
* Python 3
* Git
* pip
* virtualenv

以Centos为例，可以执行下面的命令安装：

    yum install nginx git python3 python3-pip
    pip3 install virtualenv

## 配置Nginx虚拟主机

* 参考nginx.template.conf
* 把SITENAME替换成所需的域名，例如staging.my-domain.com

## Upstart任务

* 参考gunicorn-upstart.template.conf * 把SITENAME替换成所需的域名，例如staging.my-domain.com

## 文件夹结构：

假设有用户账户，家目录为/home/username

/home/username
└─ sites
    └─ SITENAME
        ├─ database
        ├─ source
        ├─ static
        └─ virtualenv