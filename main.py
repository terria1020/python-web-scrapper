from indeed import get_job as get_indeed_job
from indeed import get_page_number as get_indeed_page_num
from stackoverflow import get_job as get_stackoverflow_job
from stackoverflow import get_page_number as get_stackoverflow_page_num
from misc import print_align_space
from time import sleep
import csv
from sys import exit

HEAD = ["홈페이지", "타이틀", "링크"]
CSV = 'data.csv'

def csv_write(dict_list):
    print(f"save data to: {CSV}...", end='', flush=True)
    print_align_space(f"save data to: {CSV}...", "success.")
    try:
        with open(CSV, "w") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(HEAD)
            for dicts in dict_list:
                dict_value = dicts.values()
                csv_writer.writerow(dict_value)
        print("success.")
    except Exception: # 파일 관련 예외처리
        print("[!] File Processing Error.")
        exit()

def main():
    try:
        print("'python'을 주제로 한 검색 결과 페이지 종합 중...")
        indeed_page = get_indeed_page_num()
        so_page = get_stackoverflow_page_num()
        print(f"  'indeed.com'에서의 'python' 검색 결과: 총 {indeed_page}페이지")
        print(f"  'StackOverflow.com'에서의 'python' 검색 결과: 총 {so_page}페이지")
        
        sleep(1)

        print("['indeed.com' scrapping]")
        indeed_job_list = get_indeed_job()

        print("['StackOverflow.com' scrapping]")
        so_job_list = get_stackoverflow_job()

        job_list = indeed_job_list + so_job_list

        sleep(1)
        csv_write(job_list)
    except KeyboardInterrupt:
        print("[!] program stopped bia Keyboard Interrupt.")

if __name__ == "__main__":
    main()