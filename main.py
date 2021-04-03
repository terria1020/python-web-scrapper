from indeed import get_job as get_indeed_job
import csv
from sys import exit

HEAD = ["타이틀", "링크"]

def csv_write(dict_list):
    print("write job data to: 'data.csv'...\t\t", end='')
    try:   
        with open("data.csv", "w") as csv_file:
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
    dict_list = get_indeed_job()
    csv_write(dict_list)

if __name__ == "__main__":
    main()