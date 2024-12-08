from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup


def get_proxy():
    url = "http://127.0.0.1:8080/get?count=1"
    response = requests.get(url)
    proxy = response.json()
    proxy = f"{proxy['Ip']}:{proxy['Port']}"
    return proxy


def update_proxies():
    url = "http://127.0.0.1:8080/verify"
    response = requests.get(url)
    print(response.text)


def fetch_image(headers, cookies, url):
    global count
    # if count % 200 == 0:
    # update_proxies()
    proxy = get_proxy()
    proxy_meta = f"http://{proxy}"
    proxy_dict = {"http": proxy_meta, "https": proxy_meta}

    try:
        response = requests.get(
            url, headers=headers, cookies=cookies, proxies=proxy_dict, timeout=10
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for img in soup.find_all("img"):
            src = img.get("src")
            if src.startswith("/image/"):
                img_response = requests.get(
                    "http://cas.bjtu.edu.cn" + src, headers=headers, cookies=cookies
                )
                with open("img/" + src.split("/")[-2] + ".png", "wb") as f:
                    f.write(img_response.content)
                count += 1
                print(f"第{count}次请求，{src}下载成功")
                break
    except Exception as e:
        print(f"请求失败: {e}")


def main():
    global count
    count = 0

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    }
    cookies = {
        "csrftoken": "olLBvuKlqjeDiFFb5CKQ12JHonwy4uJurE9qHEV4vLudiqMqjWuRpWaBM5EjLZ7T"
    }
    url = "http://mis.bjtu.edu.cn/home/"

    max_workers = 5  # Adjust the number of workers based on your needs
    num_requests = 43  # Total number of requests you want to make

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(fetch_image, headers, cookies, url)
            for _ in range(num_requests)
        ]
        for future in as_completed(futures):
            future.result()


if __name__ == "__main__":
    main()
    # update_proxies()
