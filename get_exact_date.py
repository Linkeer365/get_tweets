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


import sqlite3
from datetime import datetime
import sys

firefox_path=r"C:\Program Files\Mozilla Firefox\geckodriver.exe"
options = Options()
options.headless = True
# options.headless = False

proxy="127.0.0.1:10087"

options.add_argument(f"--proxy-server=http:{proxy}")

driver=webdriver.Firefox(options=options,executable_path=firefox_path)
driver.implicitly_wait(20)

def login():
    driver.get("https://twitter.com/?lang=en")
    time.sleep(15)
    signin_btn_node=driver.find_element_by_xpath("//span[text()='Sign in']")
    signin_btn_node.click()
    time.sleep(5)
    username="ultramarine471"
    passwd="xm111737"
    driver.execute_script("window.scrollBy(0,200)")
    user_input_node=driver.find_element_by_xpath("//input[@type='text' and @dir='auto']")

    next_btn_node=driver.find_element_by_xpath("//span[text()='Next']")
    user_input_node.send_keys(username)
    time.sleep(5)
    next_btn_node.click()
    time.sleep(5)
    passwd_input_node=driver.find_element_by_xpath("//input[@name='password' and @type='password']")
    login_btn_node = driver.find_element_by_xpath ("//span[text()='Log in']")
    passwd_input_node.send_keys(passwd)
    time.sleep(5)
    login_btn_node.click()
    time.sleep(5)
    if not "login" in driver.current_url:
        print("login!")


def get_format_date(raw_date_str):
    # 12:23 PM · Nov 8, 2021

    # 有争议: https://stackoverflow.com/questions/9525944/python-datetime-formatting-without-zero-padding
    # https://docs.python.org/3/library/time.html#time.strftime
    if raw_date_str=="":
        return ""
    time_patt="%I:%M %p · %b %d, %Y"
    date_obj=datetime.strptime(raw_date_str, time_patt)
    format_date_str=date_obj.strftime("%Y-%m-%d %H:%M")
    print("raw:", raw_date_str)
    print("format:",format_date_str)
    return format_date_str

# get_format_date("12:23 PM · Nov 8, 2021")
# sys.exit(0)

conn=sqlite3.connect("twitter.db")
cursor=conn.cursor()

dates_links=cursor.execute("select d,l from tw").fetchall()
# print(dates_links[0])
# sys.exit(0)
date_strs=[]

cookies_dict= {
        "name": "{'volume','_grecaptcha','branch_session_first'}",
        "value": "{'1','09ANblmnimoA9QXKtegNFngugeaCgGphUJHFOvAA3uU3AhsB7i60oFmuVMAhV7fxY23NZtkFQWjVeUeF5fFqe95pU','{\"session_id\":\"1026041173524199533\",\"identity_id\":\"766686930977424817\",\"link\":\"https://twitter.app.link?%24identity_id=766686930977424817\",\"identity\":\"Br9/nhesDgWD/r/b95DAJy1Puyr8ABJyHvGZRAf1Epg=\",\"data\":\"{\\\"+clicked_branch_link\\\":false,\\\"+is_first_session\\\":true}\",\"browser_fingerprint_id\":\"NzY3NjAwODAxMDA5MDY0MTI1\",\"has_app\":false}'}",
        # "volume": "1",
        # "_grecaptcha": "09ANblmnimoA9QXKtegNFngugeaCgGphUJHFOvAA3uU3AhsB7i60oFmuVMAhV7fxY23NZtkFQWjVeUeF5fFqe95pU",
        # "branch_session_first": "{\"session_id\":\"1026041173524199533\",\"identity_id\":\"766686930977424817\",\"link\":\"https://twitter.app.link?%24identity_id=766686930977424817\",\"identity\":\"Br9/nhesDgWD/r/b95DAJy1Puyr8ABJyHvGZRAf1Epg=\",\"data\":\"{\\\"+clicked_branch_link\\\":false,\\\"+is_first_session\\\":true}\",\"browser_fingerprint_id\":\"NzY3NjAwODAxMDA5MDY0MTI1\",\"has_app\":false}"
    }

# login()
# driver.get("https://twitter.com")
# cnt=0
date_link_tups=[]

chuck_size=200
for date,link in dates_links:
    # print(date,link)
    if ":" in date:
        print("Already.")
        continue
    print("link:",link)
    link_tail=link.replace("https://twitter.com","")
    driver.get(link+"/?lang=en")
    # time.sleep(5)
    # driver.add_cookie(cookies_dict)
    # driver.get(link)

    # driver.implicitly_wait(15)
    div_class_str="css-901oao r-14j79pv r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-1b7u577 r-bcqeeo r-qvutc0"
    a_class_str="css-4rbku5 css-18t94o4 css-901oao css-16my406 r-14j79pv r-1loqt21 r-poiln3 r-bcqeeo r-qvutc0"
    span_class_str="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"
    try:
        date_str=driver.find_element_by_xpath("//a[contains(@href,'{}')]/span[@class='{}']".format(link_tail,span_class_str)).text
        # print ("date_str:", date_str)
    except Exception:
        date_str=""
    format_date=get_format_date(date_str)
# link: https://twitter.com/ultramarine471/status/1424814390839324672
# raw: 3:26 AM · Aug 10, 2021
# format: 2021-08-10 03:26
# link: https://twitter.com/ultramarine471/status/1424925631708495874
# raw: 10:48 AM · Aug 10, 2021
# format: 2021-08-10 10:48
# link: https://twitter.com/ultramarine471/status/1424926209012600832
    if date_str != "":
        date_link_tup=(format_date,link)
        date_link_tups.append(date_link_tup)
    if len(date_link_tups)==chuck_size:
        cursor.executemany("update tw set d = ? where l = ?",date_link_tups)
        conn.commit()
        print("{} commit!".format(chuck_size))
        date_link_tups=[]
if date_link_tups:
    cursor.executemany("update tw set d = ? where l = ?",date_link_tups)

conn.commit()
print("all done.")





# print(links)