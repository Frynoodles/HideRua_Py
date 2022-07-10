# 下载一部动漫
# 查看一部动漫集数

import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}


def download_an_episode(url: str) -> bool:
    """
    下载一集动画，包括下载所有ts并处理成mp4

    :param url: 单集动画的地址
    :return: 执行结果
    """
    # 首先获取播放的页面，并从中提取到m3u8文件
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'

    pass
