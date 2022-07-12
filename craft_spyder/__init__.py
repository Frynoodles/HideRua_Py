import time

import requests
import re
from bs4 import BeautifulSoup
from lxml import etree
import csv
from concurrent.futures import ThreadPoolExecutor
import pprint
import json
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'cookie': 'experiment-number=4637; _ga=GA1.2.1985203777.1657603929; _gid=GA1.2.2083243159.1657603929; hubspotutk=7182d9f834285f1d42de66421bd3913c; __hssrc=1; __hs_opt_out=no; __hs_initial_opt_in=true; _gcl_au=1.1.385417059.1657603954; sid=b4d1da23-d794-4211-b50e-0ef470cfeb09; connect.sid=s%3AIuMnrnRam5_oX5hXugsiWyJo3NXEaQeM.mZa%2Bu7hMXuZeUjBlxNa%2FFynnKgZ3fZNnAI11FKPDd6c; _fbp=fb.1.1657604317579.774821171; __cf_bm=z2fTHm9a.f.GNarMM9R6ts1lRJstWUw9wp8pWEp.zbs-1657609849-0-AaaOhVOw5jze6otueP0frPLvB5x7jxsKmV3ZEGCi+ENJ3OnuU/E/uLgl2Kb2efTiaK0fCv4CEuHqqvUWI8ztluNt8BkJfmYLHFfr+VdNAX8/; __hstc=134641070.7182d9f834285f1d42de66421bd3913c.1657603931165.1657603931165.1657609853127.2; __hssc=134641070.1.1657609853127; _gat_gtag_UA_50801432_1=1; mp_3f90bac5a699bef918e5477f9edfdff4_mixpanel=%7B%22distinct_id%22%3A%20%22181f0e4b277786-02ade5b9bc629a-26021a51-1fa400-181f0e4b278e55%22%2C%22%24device_id%22%3A%20%22181f0e4b277786-02ade5b9bc629a-26021a51-1fa400-181f0e4b278e55%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D'
}
url = 'https://craft.co/graphql'


# cookies = {
#     'experiment-number': '4637',
#     '_ga': 'GA1.2.1985203777.1657603929',
#     '_gid': 'GA1.2.2083243159.1657603929',
#     '__hstc': '134641070.7182d9f834285f1d42de66421bd3913c.1657603931165.1657603931165.1657603931165.1',
#     'hubspotutk': '7182d9f834285f1d42de66421bd3913c',
#     '__hssrc': '1',
#     '__hs_opt_out': 'no',
#     '__hs_initial_opt_in': 'true',
#     '_gcl_au': '1.1.385417059.1657603954',
#     'sid': 'b4d1da23-d794-4211-b50e-0ef470cfeb09',
#     'connect.sid': 's%3AIuMnrnRam5_oX5hXugsiWyJo3NXEaQeM.mZa%2Bu7hMXuZeUjBlxNa%2FFynnKgZ3fZNnAI11FKPDd6c',
#     '_fbp': 'fb.1.1657604317579.774821171',
#     '__cf_bm': 'HUdwFJvh142hYvS6npY7cj3QFzmzZfmUjGLyeHZ7IEE-1657606057-0-ATUxd9R4WDlBUkM6SPIhVRmMJvuRiEV6rwcLOwp+nLbNCWeU9nMeQvPOAGtltR3752z+eLAxmAm89GsKey+jKvnoSHmdONZo1O883yR9uo0b',
#     'mp_3f90bac5a699bef918e5477f9edfdff4_mixpanel': '%7B%22distinct_id%22%3A%20%22181f0e4b277786-02ade5b9bc629a-26021a51-1fa400-181f0e4b278e55%22%2C%22%24device_id%22%3A%20%22181f0e4b277786-02ade5b9bc629a-26021a51-1fa400-181f0e4b278e55%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D',
#     '__hssc': '134641070.12.1657603931166'
# }
def get_cookies():
    with open('cookies.text', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


# def get_data(n):
#     return {"operationName": "CompanySearchForCompaniesList", "variables": {"filter": {
#         "and": [{"companyTypes": []}, {"employeeCount": {}}, {"tags": ["health", "medical-devices"]}, {"or": []}]},
#         "first": 12, "offset": 12, "query": "",
#         "sort": [
#             {"field": "score", "order": "Desc"}]},
#             "query": "query CompanySearchForCompaniesList($filter: SearchCompaniesFilter, $first: Int, $offset: Int, $query: String!, $sort: [CompanySortInput!]) {\n  companySearch(filter: $filter, first: $first, offset: $offset, query: $query, sort: $sort) {\n    items {\n      id\n      companyType\n      displayName\n      employeeCount\n      employeeGrowth\n      foundedYear\n      hqLocation {\n        city\n        countryCode\n        state\n        __typename\n      }\n      logo {\n        id\n        url\n        __typename\n      }\n      revenue {\n        valueInUsd\n        __typename\n      }\n      slug\n      shortDescription\n      tags {\n        id\n        name\n        slug\n        __typename\n      }\n      totalValuation {\n        valueInUsd\n        __typename\n      }\n      __typename\n    }\n    itemsCount\n    __typename\n  }\n}\n"}
#

#     return [{
#         "operationName": "CompanySearchForCompaniesList",
#         "query": """query CompanySearchForCompaniesList($filter: SearchCompaniesFilter, $first: Int, $offset: Int, $query: String!, $sort: [CompanySortInput!]) {
#   companySearch(filter: $filter, first: $first, offset: $offset, query: $query, sort: $sort) {
#     items {
#       id
#       companyType
#       displayName
#       employeeCount
#       employeeGrowth
#       foundedYear
#       hqLocation {
#         city
#         countryCode
#         state
#         __typename
#       }
#       logo {
#         id
#         url
#         __typename
#       }
#       revenue {
#         valueInUsd
#         __typename
#       }
#       slug
#       shortDescription
#       tags {
#         id
#         name
#         slug
#         __typename
#       }
#       totalValuation {
#         valueInUsd
#         __typename
#       }
#       __typename
#     }
#     itemsCount
#     __typename
#   }
# }
# """,
#         "variables": {
#             "first": 12, "offset": n * 12, "query": "",
#             "and": [{"companyTypes": []}, {"employeeCount": {}}, {"tags": ["health", "medical-devices"]},
#                     {"or": []}],
#             "sort": [{"field": "score", "order": "Desc"}]
#         }
#     }]
# @retry(wait_fixed=10, stop_max_attempt_number=1)
# def click():
#     web.find_element(By.XPATH, '//button[@class="_3_Ozh E_CaI _3Mo3q"]').click()

def get_company_data():
    with open('list.text', 'r', encoding='utf-8') as f:
        urls = f.readlines()
    for url in urls:
        web.get(url)
        # 提取数据

        with open('data.csv', 'a', encoding='utf-8', newline='') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow()


if __name__ == '__main__':
    # resp = requests.post(url, headers=headers, data=get_data(2), cookies=cookies)
    # print(resp)
    # pass
    # web = Chrome()
    # web.get('https://craft.co/search?layout=list&order=relevance&q=&tags%5B0%5D=health&tags%5B1%5D=medical-devices')
    # print(requests.get('https://craft.co/johnson-johnson', headers=headers).ok)
    # time.sleep(80)
    # cookies = web.get_cookies()
    # with open('cookies.text', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(cookies))



    options = ChromeOptions()
    options.page_load_strategy = 'eager'
    web = Chrome(options=options)
    web.get('https://craft.co/search?layout=list&order=relevance&q=&tags%5B0%5D=health&tags%5B1%5D=medical-devices')
    time.sleep(2)
    js = "var q=document.documentElement.scrollTop=100000"
    web.execute_script(js)
    time.sleep(1)
    for cookie in get_cookies():
        web.add_cookie(cookie)
    web.refresh()
    time.sleep(1)
    try:
        while (True):
            print('开始')
            web.execute_script(js)
            WebDriverWait(web, 20, 0.5).until(
                EC.presence_of_element_located((By.XPATH, '//button[@class="_3_Ozh E_CaI _3Mo3q"]')))
            web.find_element(By.XPATH, '//button[@class="_3_Ozh E_CaI _3Mo3q"]').click()
            print('结束')
    except NoSuchElementException as err:
        print('错误')
        # 全部加载完毕
        lis = web.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/ul').find_elements(By.XPATH, './/li')
        urls = []
        for li in lis:
            urls.append(f"https://craft.co{li.find_element(By.XPATH, './a').get_attribute('href')}")
        with open('list.text', 'w', encoding='utf-8') as f:
            for url in urls:
                f.write(f'{url}\n')
