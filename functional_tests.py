# -*-coding:utf-8-*-

'''
functional test: 功能测试
'''
from selenium import webdriver

options = webdriver.ChromeOptions()
options.binary_location = "D:\soft\Google\Chrome\Application\chrome.exe"

browser = webdriver.Chrome(chrome_options=options)
browser.get('http://localhost:8000')

assert 'Django' in browser.title
