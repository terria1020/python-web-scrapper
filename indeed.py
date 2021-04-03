import requests
from bs4 import BeautifulSoup
import csv
from sys import exit

URLBASE = "https://kr.indeed.com"
limit = 50
query = f"/취업?q=python&limit={limit}"

def get_page_number():
    res = requests.get(URLBASE + query)
    if res.status_code >= 200:
        try:
            soup = BeautifulSoup(res.text, "html.parser")
            res_top = soup.find("div", class_="searchCount-a11y-contrast-color")
            page_number = res_top.find("div", {"id": "searchCountPages"})
        except AttributeError:
            print("[!] Can't find HTML Elements or HTML.")
            exit()
    else:
        print("[!] not find any request.")
        exit()
    page_number = (page_number.get_text().split(" "))[-1]
    page_number = int(page_number.replace(",", "")[:-1]) // 50
    # 한 페이지 당 최대로 볼 수 있는 글의 수 : 50 -> 총 글 수 / 페이지 당 최대 보기 수
    return page_number

def get_need_link(number):
    return URLBASE + query + f"&start={number * limit}"

def extract_job(page):
    dict_list = []

    res = requests.get(page)
    if res.status_code >= 200: # 활성 상태
        try:
            soup = BeautifulSoup(res.text, "html.parser")
            job_search = soup.find_all("div", class_="jobsearch-SerpJobCard")

            for result in job_search:
                title = result.find("h2", class_="title")
                title = title.find("a")
                if title.string is not None:
                    dict_list.append({
                        "job_name": title.string.strip(),
                        "job_link": str(URLBASE + title.get("href"))
                    })
                else:
                    continue
            return dict_list
        except AttributeError:
            print("[!] Can't find HTML Elements or HTML.")
            exit()
    else:
        print("[!] Can't find any request.")
        exit()

def get_job():
    print("get job data from: 'indeed.com'...\t\t" , end='')
    dict_list = []
    page_number = get_page_number()
    
    for number in range(page_number):
        dict_list.extend(extract_job(get_need_link(number)))
    print("success.")
    return dict_list