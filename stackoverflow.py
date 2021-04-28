import requests
from bs4 import BeautifulSoup
from sys import exit
from misc import print_align_space

URLBASE = "https://stackoverflow.com"
limit = 25
page = 1
query = f"/jobs?q=python"

def get_page_number():
    try:
        req = requests.get(URLBASE + query)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, "html.parser")
            jobs = soup.find("div", class_="grid--cell js-search-title -header seo-header")
            jobs = jobs.find("span").string.split(" ")[0]
            jobs = int(jobs.replace(",", "")) // limit
            return jobs
        elif req.status_code == 404:
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
    return URLBASE + query + f"&pg={number}"

def extract_job(page):
    dict_list = []
    try:
        req = requests.get(page)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, "html.parser")
            title_search = soup.find_all("a", class_="s-link stretched-link")
            for result in title_search:
                dict_list.append({
                    "page_type": "StackOverflow.com",
                    "job_name": result["title"],
                    "job_link": str(URLBASE + result["href"])
                })
            return dict_list
        elif req.status_code == 404:
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
    print("get job data from: 'StackOverflow.com...")
    dict_list = []
    
    for number in range(page_number):
        print(f"get page {number + 1}...", end='', flush=True)
        print_align_space(f"get page {number + 1}...", "success.")
        dict_list.extend(extract_job(get_need_link(number)))
        print("success.")
    return dict_list
    