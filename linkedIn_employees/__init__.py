import time

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import json

# 主页
LINKEDIN_INDEX_URL = r'https://www.linkedin.com/'


def init_webdriver() -> Chrome():
    """
    初始化，添加 options （反爬）

    :return: selenium.webdriver.Chrome()
    """
    options = ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    return Chrome(options=options)


def get_and_save_cookie() -> list[dict]:
    """
    获取保存cookies

    :return: cookie列表
    """
    if not os.path.exists('../cookies.text'):  # 不存在，登录获取，存放，返回
        options = ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        web = Chrome(options=options)
        web.get(LINKEDIN_INDEX_URL)
        # 等待2s，让浏览器加载
        time.sleep(5)
        # 进入登录页
        web.find_element(By.XPATH, '/html/body/nav/div/a[2]').click()
        # 等待2s，让浏览器加载
        # 填入信息
        web.find_element(By.XPATH, '//input[@id="username"]').send_keys(input('请输入账号，没做处理，瞎搞后果自负:\n'))  # 输入账号
        web.find_element(By.XPATH, '//input[@id="password"]').send_keys(input('请输入密码，没做处理，瞎搞后果自负:\n'))  # 输入密码
        web.find_element(By.XPATH, '//button[@data-litms-control-urn="login-submit"]').send_keys(Keys.ENTER)  # 登录
        time.sleep(5)  # 休眠5s
        print('休眠5s，等待浏览器刷新')
        # 获取cookie
        cookies = web.get_cookies()
        # 存储
        with open('../cookies.text', 'w', encoding='utf-8') as f:
            f.write(json.dumps(cookies))  # 将cookies保存为json格式
    # 读取cookies
    with open('../cookies.text', 'r', encoding='utf-8') as f:
        my_cookies = json.load(f)

        # 删除不需要的字段 expiry:cookie的生命周期
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
        return my_cookies


def get_employees_data(company_homepage_url) -> list[dict]:
    """
    获取职员信息

    :param company_homepage_url: 公司主页链接
    :return: [{name,description,position}]的list[dict]
    """
    web = init_webdriver()
    # 打开网页
    web.get(company_homepage_url)
    print('休眠2s')
    time.sleep(2)
    cookies = get_and_save_cookie()
    for cookie in cookies:
        web.add_cookie(cookie)
    time.sleep(2)
    web.refresh()
    print('休眠2s')
    # 点击跳转至员工
    web.find_element(By.XPATH, '//a[starts-with(@id,"ember")]').click()
    print('休眠2s')
    time.sleep(2)
    list = web.find_elements(By.XPATH, '//div[@class="entity-result__item"]')
    for one in list:
        pass  # 未完待续
    pass


if __name__ == '__main__':
    web = init_webdriver()
    web.get(input('请输入目标主页:\n'))
    pass
