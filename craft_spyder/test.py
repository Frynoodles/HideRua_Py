import json
import time
import pprint
import csv
from lxml import etree
from craft_spyder import get_cookies

import requests

from requests.cookies import RequestsCookieJar

from concurrent.futures import ThreadPoolExecutor

headers = {
    'user-agent': 'Mozilla/5.0',
    'referer': 'https://craft.co/search?layout=list&order=relevance&q=&tags%5B0%5D=health&tags%5B1%5D=medical-devices',
    'accept': '*/*',
    'content-type': 'application/json',
    'origin': 'https://craft.co',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,ja-CN;q=0.8,ja;q=0.7',
}


def get_data(n) -> str:
    return json.dumps([
        {
            "operationName": "CompanySearchForCompaniesList",
            "variables": {
                "filter": {
                    "and": [
                        {
                            "companyTypes": []
                        },
                        {
                            "employeeCount": {}
                        },
                        {
                            "tags": [
                                "health",
                                "medical-devices"
                            ]
                        },
                        {
                            "or": []
                        }
                    ]
                },
                "first": 12,
                "offset": 12 * n,
                "query": "",
                "sort": [
                    {
                        "field": "score",
                        "order": "Desc"
                    }
                ]
            },
            "query": "query CompanySearchForCompaniesList($filter: SearchCompaniesFilter, $first: Int, $offset: Int, $query: String!, $sort: [CompanySortInput!]) {\n  companySearch(filter: $filter, first: $first, offset: $offset, query: $query, sort: $sort) {\n    items {\n      id\n      companyType\n      displayName\n      employeeCount\n      employeeGrowth\n      foundedYear\n      hqLocation {\n        city\n        countryCode\n        state\n        __typename\n      }\n      logo {\n        id\n        url\n        __typename\n      }\n      revenue {\n        valueInUsd\n        __typename\n      }\n      slug\n      shortDescription\n      tags {\n        id\n        name\n        slug\n        __typename\n      }\n      totalValuation {\n        valueInUsd\n        __typename\n      }\n      __typename\n    }\n    itemsCount\n    __typename\n  }\n}\n"
        }
    ])


def get_raw_data(n):
    """
    抓取第n页的数据

    :param n: 第几页，一页12个
    :return: None
    """
    # 获取每页的链接
    url = 'https://craft.co/graphql'
    for item in session.post(url, data=get_data(n)).json()[0]['data']['companySearch']['items']:
        display_name = item['displayName']
        company_type = item['companyType']
        employee_count = item['employeeCount']
        founded_year = item['foundedYear']
        country_code = item['hqLocation']['countryCode']
        short_description = item['shortDescription']
        _slug = item['slug']
        profile_url = 'https://craft.co/' + _slug
        print(profile_url)
        _profileText = session.get(profile_url).text
        _page_etree = etree.HTML(_profileText)
        description = _page_etree.xpath('//div[contains(@class,"summary__description")]//text()')
        social_link = []
        _social = _page_etree.xpath('//div[@class="summary__social-icons"]/ul/li')
        # if len(_social) == 0:
        #     _social = _page_etree.xpath('//div[@class="cp-summary__social-links"]/div/a')
        #     for a in _social:
        #         social_link.append(a.xpath('./@href')[0])
        #         print(a.xpath('./@href')[0])
        # else:
        #     for li in _social:
        #         social_link.append(li.xpath('./a/@href')[0])
        #         print(li.xpath('./a/@href')[0])
        recent_news = []
        for item in _page_etree.xpath('//li[@class="summary__news-item"]'):
            recent_news.append(item.xpath('./a/text()')[0])
        metrics = []
        for li in _page_etree.xpath('//ul[@class="summary__top-metrics"]/li'):
            metrics.append(li.xpath('./div/span[1]/text()')[0] + li.xpath('./div/span[2]/span[1]/text()')[0] + li.xpath(
                './div/span[2]/span[2]/text()')[0])
        social_link = "\n".join(social_link)
        recent_news = "\n".join(recent_news)
        metrics = "\n".join(metrics)
        csvwriter.writerow([display_name, company_type, employee_count, founded_year, country_code, short_description,
                            description, company_type, social_link, recent_news
                               , metrics, profile_url])


if __name__ == '__main__':
    rj = requests.cookies.RequestsCookieJar()
    for cookie in get_cookies():
        rj.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'])
    session = requests.session()
    session.cookies.update(rj)
    session.headers.update(headers)
    f = open('data.csv', 'w', encoding='utf-8', newline='')
    csvwriter = csv.writer(f)
    csvwriter.writerow(['displayName', 'companyType', 'employeeCount', 'foundedYear', 'countryCode', 'shortDescription',
                        'description', 'type', 'social_link',
                        'recent_news', 'metrics', 'profileUrl'])
    print('开始任务')
    # with ThreadPoolExecutor(5) as t:
    #     for i in range(1, 571):
    #         t.submit(get_raw_data, n=i)
    #         print(f'分配任务{i}')
    for i in range(1, 30):
        get_raw_data(i)
    print('任务结束')
    f.close()
