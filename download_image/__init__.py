import time

import requests
import aiohttp
import asyncio
import aiofiles
import os

HEADERS: dict[str, str] = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}


def download_image(url: str, headers: dict = HEADERS, path: str = './') -> bool:
    """
    下载一张图片，默认下载到当前目录，可选择添加headers和path

    :param path: 下载路径，默认为当前文件夹
    :param headers: 请求头，默认只有user-agent
    :param url: 图片链接
    :return: 执行结果
    """
    # 消除windows特有问题:RuntimeError: Event loop is closed
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        if not os.path.exists(path):  # 检测文件夹是否存在
            os.makedirs(path)  # 不存在创建
        with open(f"{path.strip('/')}/{url.split('/')[-1]}", 'wb') as f:
            f.write(requests.get(url, headers=headers).content)
            print(f'下载{url.split("/")[-1]}成功')
        return True
    except BaseException as err:
        print(f"下载{url.split('/')[-1]}失败,err={err}")
        return False


def download_images(urls: list[str], headers: dict = HEADERS, path: str = './resource') -> bool:
    """


    :param urls: 链接列表
    :param headers: 请求头，默认只有user-agent
    :param path: 存放路径，默认为第一张图片的名称
    :return: 执行结果
    """
    # 消除windows特有问题:RuntimeError: Event loop is closed
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        if len(urls) == 0:  # 检测是否有链接
            return True
        # 存放的文件夹问题
        if not path == './resource':
            path = path.strip('/')
        if not os.path.exists(path):
            os.makedirs(path)
        # 开始下载，执行协程任务
        # 提供的协程锁没用我就只好自己加锁了
        u = []
        for i, url in enumerate(urls):
            if i % 50 == 0 and i != 0:
                print(f'执行一次协程任务，数量{len(u)}')
                asyncio.get_event_loop().run_until_complete(__download_images_async_task(u, path, headers))
                u.clear()
            else:
                u.append(url)
            time.sleep(2)  # 总之先睡两秒吧
        return True
    except BaseException as err:
        print(err)
        return False


async def __download_images_async_task(urls: list[str], path: str, headers: dict):
    """
    使用协程下载图片，创建任务

    :param headers: 请求头
    :param path: 存放路径
    :param urls: 图片链接列表
    :return: None
    """
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(__download_images_async_fun(url, path, headers)))
    await asyncio.wait(tasks)


async def __download_images_async_fun(url, path, headers):
    """
    真正执行下载的协程函数


    :type semaphore: asyncio.Semaphore(n) 限制并发数
    :param headers: 请求头
    :param url: 链接
    :param path: 存放路径
    :return: None
    """
    # try:
    async with aiohttp.ClientSession() as session:
        print(url)
        async with session.get(url, headers=headers) as resp:
            async with aiofiles.open(path + '/' + url.strip().split('/')[-1], 'wb') as f:
                await f.write(await resp.content.read())
                print(f'下载{url}成功')
    await asyncio.sleep(1)
# except Exception:
#     async with aiofiles.open(path + '/' + 'log.txt', 'a') as log:
#         await log.write(f'{url}')


if __name__ == '__main__':
    # print(download_images(['https://i0.hdslb.com/bfs/new_dyn/dc4197525a7297ba86170da74a07c947413023694.png',
    #                        'https://i0.hdslb.com/bfs/new_dyn/d4e353a82418f9fe209c96973bffacd7413023694.jpg',
    #                        'https://i0.hdslb.com/bfs/new_dyn/5a8c9b2e97fb859c940bb4063f3d4af2413023694.jpg']))
    download_image('https://i0.hdslb.com/bfs/new_dyn/673027a762a1dec347939f127b8cff5f413023694.jpg')
