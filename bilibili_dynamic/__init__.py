import pprint
import time
from typing import Any
import requests


# 已测试
def get_dynamic_data_headers(dynamic_url: str) -> dict:
    """
    获取爬取一个人b站动态所需要的headers，参数是爬取对象的b站动态

    :param dynamic_url: 动态链接
    :return: headers，包括refer,user-agent
    """
    return {
        'referer': f'{dynamic_url}',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }


# 已测试
def get_all_dynamics_by_dynamic_url(dynamic_url: str) -> list:
    """
    获取一个b站用户的所有动态的信息，列表返回

    :param dynamic_url: b站动态链接
    :return:  所有动态的json列表 [jsons]
    """
    print(f'接到动态爬取任务{dynamic_url}')
    dynamics: list[Any] = []  # 存放所有的动态
    mid = dynamic_url.split("/")[-2]  # 获取mid
    offset: str = ''  # 偏移量，第一次为空，之后在循环中获得
    try:
        # 开始循环，访问所有的动态
        while True:
            resp = requests.get(
                f'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset={offset}&host_mid={mid}&timezone_offset=-480',
                headers=get_dynamic_data_headers(dynamic_url))
            json_data = resp.json()  # 获取json数据
            resp.close()  # 关闭连接
            offset = json_data['data']['offset']  # 下个数据的偏移量,不为空获取下一页，为空跳出循环，完成函数
            items = json_data['data']['items']  # 当前页面所有的动态的信息
            print(f'获取到{len(items)}个动态')
            for item in items:
                dynamics.append(item)
            if offset.strip() == '':
                print(f'供获取{len(dynamics)}个动态')
                return dynamics
            else:
                time.sleep(0.1)  # 暂停1s
    except TimeoutError:
        return dynamics


# 已测试
def get_last_dynamic_by_dynamic_url(dynamic_url: str) -> dict:
    """
    获取一个b站用户最新一条动态的数据，直接返回json，不做处理

    :param dynamic_url: 动态链接
    :return: 最新的动态的json
    """
    resp = requests.get(
        f'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset=&host_mid={dynamic_url.split("/")[-2]}&timezone_offset=-480',
        headers=get_dynamic_data_headers(dynamic_url))
    items = resp.json()['data']['items']  # 总数据
    resp.close()
    try:
        if items[0]['modules']['module_tag']['text'] == '置顶':  # 查看是否有置顶，有返回下一个，没有直接返回第一个
            return items[1]
        else:
            return items[0]
    except KeyError:
        return items[0]


# 已测试
def get_top_dynamic_by_dynamic_url(dynamic_url: str) -> dict:
    """
    获取一个b站用户的置顶动态，无则返回空字典，记得处理空值

    :param dynamic_url: 动态链接
    :return: 置顶动态的json或者空字典
    """
    resp = requests.get(
        f'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset=&host_mid={dynamic_url.split("/")[-2]}&timezone_offset=-480',
        headers=get_dynamic_data_headers(dynamic_url))
    items = resp.json()['data']['items']  # 总数据
    resp.close()
    try:
        if items[0]['modules']['module_tag']['text'] == '置顶':
            return items[0]
        else:
            return {}
    except KeyError:
        return {}


# 已测试
def get_dynamics_image_urls_by_dynamic_url(dynamic_url: str) -> list[str]:
    """
    通过主页链接获取所有的图片动态的图片链接，本质调用get_all_dynamics_by_homepage_url()和get_dynamics_image_urls_from_dynamic_items()两个函数

    :param dynamic_url: 动态链接
    :return: 结果
    """
    return get_dynamics_image_urls_from_dynamic_items(get_all_dynamics_by_dynamic_url(dynamic_url))


# 已测试
def get_dynamics_image_urls_from_dynamic_items(items: list) -> list[str]:
    """
    提取所有动态的图片动态的图片链接

    :param items: 所有动态的json对象的列表
    :return: 图片链接列表
    """

    # 提取所有图片的链接
    images_urls = []
    image_items = get_all_image_dynamics_from_dynamics_list(items)

    for item in image_items:
        images = item['modules']['module_dynamic']['major']['draw']['items']
        for image in images:
            images_urls.append(image['src'])
    print(f'共获取{len(images_urls)}条链接')
    return images_urls


# 已测试
def get_all_image_dynamics_from_dynamics_list(items: list) -> list:
    """
    从一个存放动态的列表中提取出所有的图片动态，包括转发动态中的图片动态

    :param items: 动态json列表
    :return: 图片动态的列表
    """
    image_list: list = []
    for item in items:
        if item['type'] == 'DYNAMIC_TYPE_DRAW':  # 类型是图片
            image_list.append(item)
        elif item['type'] == 'DYNAMIC_TYPE_FORWARD' and item['orig']['type'] == 'DYNAMIC_TYPE_DRAW':  # 类型是转发且转发的是图片
            image_list.append(item['orig'])
    return image_list


# 已测试
def get_image_dynamics_data(item: dict) -> dict:
    """
    将动态json转化为重要信息的json
    包括 author_name(谁发的),mid,pub_time(更新时间),description(图片以外的文字),image_urls(图片链接，列表)

    :param item: 一个动态的json
    :return: 一个指定数据的json
    """
    try:
        modules = item['modules']
        author_name = modules['module_author']['name']
        mid = modules['module_author']['mid']
        pub_time = modules['module_author']['pub_time']
        description = modules['module_dynamic']['desc']['text']
        try:
            pic_items = modules['module_dynamic']['major']['draw']['items']
        except TypeError:
            pic_items = []
        image_urls = []
        for pic in pic_items:
            image_urls.append(pic['src'])
        return {"author_name": author_name, "mid": mid, "pub_time": pub_time, "description": description,
                "image_urls": image_urls}
    except KeyError as err:
        print(err)
        return {}


if __name__ == '__main__':
    url = 'https://space.bilibili.com/29325500/dynamic'
    pprint.pprint(get_image_dynamics_data(get_last_dynamic_by_dynamic_url(url)))
    pass
