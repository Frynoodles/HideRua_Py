import bilibili_dynamic
import download_image

urls = bilibili_dynamic.get_dynamics_image_urls_by_dynamic_url('https://space.bilibili.com/413023694/dynamic')
with open('list.txt', 'w', encoding='utf-8', newline='') as f:
    for url in urls:
        f.write(f'{url}\n')
download_image.download_images(urls)
