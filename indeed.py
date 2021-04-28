import requests
from bs4 import BeautifulSoup
from sys import exit
from misc import print_align_space

URLBASE = "https://kr.indeed.com"
limit = 50
query = f"/취업?q=python&limit={limit}"

def get_page_number():
    try:
        res = requests.get(URLBASE + query)
        if res.status_code == 200: # requests.get success
            soup = BeautifulSoup(res.text, "html.parser")
            res_top = soup.find("div", class_="searchCount-a11y-contrast-color")
            page_number = res_top.find("div", {"id": "searchCountPages"})

            page_number = (page_number.get_text().split(" "))[-1]
            page_number = int(page_number.replace(",", "")[:-1]) // limit
            # 한 페이지 당 최대로 볼 수 있는 글의 수 : 50 -> 총 글 수 / 페이지 당 최대 보기 수
            return page_number
        elif res.status_code == 404:
            print("[!] 404 not found.")
            exit()
        else:
            print("[!] Can't find any request.")
            exit()
    except AttributeError:
        print("[!] Can't find HTML Elements or HTML.")
        exit()
    except Exception:
        print("[!] Module 'requests' or 'BeautifulSoup' Error occured.")
        exit()

def get_need_link(number):
    return URLBASE + query + f"&start={number * limit}"

def extract_job(page):
    dict_list = []
    try:
        res = requests.get(page)
        if res.status_code == 200: # requests.get success
            soup = BeautifulSoup(res.text, "html.parser")
            job_search = soup.find_all("div", class_="jobsearch-SerpJobCard")

            for result in job_search:
                title = result.find("h2", class_="title")
                title = title.find("a")
                if title.string is not None:
                    dict_list.append({
                        "page_type": "indeed.com",
                        "job_name": title.string.strip(),
                        "job_link": str(URLBASE + title.get("href"))
                    })
                else:
                    continue
            return dict_list
        elif res.status_code == 404:
            print("[!] 404 not found.")
            exit()
        else:
            print("[!] Can't find any request.")
            exit()
    except AttributeError:
        print("[!] Can't find HTML Elements or HTML.")
        exit()
    except Exception:
        print("[!] Module 'requests' or 'BeautifulSoup' Error occured.")
        exit()

def get_job(number=0):
    if number == 0:
        page_number = get_page_number()
    else:
        page_number = number

    print("get job data from: 'indeed.com'...")
    dict_list = []
    for number in range(page_number):
        print(f"get page {number + 1}...", end='', flush=True)
        print_align_space(f"get page {number + 1}...", "success.")
        dict_list.extend(extract_job(get_need_link(number)))
        print("success.")
    return dict_list