from concurrent.futures import ThreadPoolExecutor,as_completed
# import concurrent.futures
import requests
# import urllib.request

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://www.baidu.com/',
        'http://www.hao123.com/',
        'http://some-made-up-domain.com/']

def load_url(url):
    with requests.get(url, timeout=60) as conn:
        return conn.status_code

with ThreadPoolExecutor(max_workers=5) as executor:
    future_to_url = {executor.submit(load_url, url): url for url in URLS}
    for future in future_to_url:
        url = future_to_url[future]
        data = future.result()
        print(data,url)

with ThreadPoolExecutor(max_workers=5) as executor:
    for url,data in zip(URLS,executor.map(load_url,URLS)):
        print(url,data)

# for url in URLS:
#     print(url,load_url(url))


