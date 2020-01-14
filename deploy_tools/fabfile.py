# -*-coding:utf-8-*-

# 使用fabric自动部署网站

import random

from fabric.api import env, local, run
from fabric.contrib.files import append, exists, sed

REPO_URL = "https://github.com/evilmao/python_web_tdd.git"


def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    """为项目创建目录
    :param site_folder:网站目录如:failytodo-superlist.tk
    :return:
    """
    for sub_folder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p {0}/{1}'.format(site_folder, sub_folder))  # ➊➋


def _get_latest_source(source_folder):
    """获取最新的项目代码
    :param source_folder: 项目路径
    :return:
    """
    if exists(source_folder + '/.git'):  # ➊判断是否存在源码库
        run('cd {} && git fetch'.format(source_folder, ))  # 使用git fetch 更新新的代码
    else:
        run('git clone {0} {1}'.format(REPO_URL, source_folder))  # 如果没有代码库,clone新的代码
        current_commit = local("git log -n 1 --format=%H", capture=True)  # 获取本地仓库中当前提 交的哈希值。这么做的结果是，服务器中代码将和本地检出的代码版本一致
        run('cd {0} && git reset --hard {1}'.format(source_folder,
                                                    current_commit))  # ➏切换到指定的提交。这个命令会撤销在服务器中对代码 仓库所做的任何改动。


def _update_settings(source_folder, site_name):
    """更新配置文件
    :param source_folder:
    :param site_name:
    :return:
    """
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")  # ➊设置 ALLOWED_HOSTS 和 DEBUG
    # 使用sed调整 ALLOWED_HOSTS 的值，使用正则表达式匹配正确的代码行
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["{}"]'.format(site_name, )  # ➋
        )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):  # ➌Django 有几处加密操作要使用 SECRET_KEY：cookie 和 CSRF 保护
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '{}'".format(key))  # append 的作用是在文件末尾添加一行内容。（
        append(settings_path, '\nfrom .secret_key import SECRET_KEY')  # ➍➎


def _update_virtualenv(source_folder):
    """为项目创建虚拟环境"""
    virtualenv_folder = source_folder + '../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=$(which python) {}'.format(virtualenv_folder))
    run('{0}/bin/pip install -r {1}/requirements.txt'.format(virtualenv_folder, source_folder))


def _update_static_files(source_folder):
    """为项目创建静态文件路径"""
    run('cd {}&&../virtualenv/bin/python3 manage.py collectstatic --noinput'.format(source_folder))


def _update_database(source_folder):
    """数据库迁移"""
    run('cd {} && ../virtualenv/bin/python manage.py migrate --noinput'.format(source_folder))
