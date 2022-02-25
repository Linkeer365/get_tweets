import selenium
import re

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


# 解决点不动的问题
# https://stackoverflow.com/questions/21350605/python-selenium-click-on-button

from selenium.webdriver.support.ui import WebDriverWait

# 一出现就马上点，这个操作好啊！！！

# https://stackoverflow.com/questions/62868434/button-click-only-works-when-time-sleep-added-for-selenium-python
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os
import sys

import time

firefox_path=r"C:\Program Files\Mozilla Firefox\geckodriver.exe"
options = Options()
options.headless = True
# options.headless = False

proxy="127.0.0.1:10087"

options.add_argument(f"--proxy-server=http:{proxy}")

driver=webdriver.Firefox(options=options,executable_path=firefox_path)
driver.set_page_load_timeout(20)

def get_tco_lists(lines):
    # tco_lists = [(0,""),(1,"https://t.co")]
    pivot="https://t.co"
    tco_lists=[]
    tco_link=""
    for idx,line in enumerate(lines):
        tco_list=[idx]
        tco_starts=[m.start() for m in re.finditer(pivot,line)]
        if len(tco_starts)==0:
            tco_list.append("")
        elif len(tco_starts)>=1:
            for tco_start in tco_starts:
                tco_end=tco_start+23
                tco_link=line[tco_start:tco_end]
                tco_list.append(tco_link)
        # print(tco_list)
        tco_lists.append(tco_list)
        # print(tco_starts)
    return tco_lists

def translate(tco_link):
    try:
        driver.get(tco_link)
        if driver.current_url!=tco_link:
            real_link=driver.current_url
            # print("")
            # print("idx:{}".format(idx))
            print("fake:",tco_link)
            print("real:",real_link)
            # print("")
            return real_link
    except Exception:
        return tco_link


def main():
    filedir="D://get_tweets//"
    filenames=["ultramarine471_tweet_date_links","mutilated_catal_tweet_date_links"]
    # filepaths=[filedir+filename for filename in filenames]
    lines=[]

    for filename in filenames:
        filepath=filedir+filename+".txt"
        with open(filepath,"r",encoding="utf-8") as f:
            lines=f.readlines()
        tco_lists=get_tco_lists(lines)
        for tco_list in tco_lists:
            idx=tco_list[0]
            tco_links=tco_list[1:]
            print("")
            print("idx:{}".format(idx))
            # print("gan",tco_links)
            if tco_links==[""]:
                continue
            for tco_link in tco_links:
                real_link=translate(tco_link)
                lines[idx]=lines[idx].replace(tco_link,real_link)
            print("")
        lines_s="".join(lines)
        newname=filename+"_modified"
        newpath=filedir+newname+".txt"
        with open(newpath,"w",encoding="utf-8") as f:
            f.write(lines_s)

if __name__=="__main__":
    main()

