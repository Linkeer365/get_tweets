# selenium <= 4.2.0 by https://pythoninoffice.com/fixing-attributeerror-webdriver-object-has-no-attribute-find_element_by_xpath/
from typing import NamedTuple
import selenium
import re

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os
import sys

import sqlite3

import time

from datetime import datetime

# username=input("username:")
# passwd=input("password:")

dir_path="D://get_tweets"

db_path=dir_path+"//twitter.db"
conn=sqlite3.connect(db_path)
cursor=conn.cursor()

username="ultramarine471"
passwd="Flsy19990107#"
# search_name=input("who you want:")
search_name="ultramarine471"

# cnt=cursor.execute("select count(*) from tw where u='{}'".format(search_name)).fetchall()[0][0]
collected_links=[each[0] for each in cursor.execute("select l from tw where u='{}'".format(search_name)).fetchall()]
# dates=[each[0] for each in cursor.execute("select d from tw where u like '%ul%'").fetchall()]
# print(links)
# print(cnt)
# sys.exit(0)

# visit=input("")

firefox_path=r"C:\Program Files (x86)\Mozilla Firefox\geckodriver.exe"
options = Options()
# options.headless = True
options.headless = False

proxy="127.0.0.1:10087"

options.add_argument(f"--proxy-server=http:{proxy}")

path_as_service=Service(firefox_path)
driver=webdriver.Firefox(options=options,service=path_as_service)
driver.implicitly_wait(20)

all_my_tweets_net="https://www.allmytweets.net/"

def get_tco_links(text):
    # tco_linkss = [(0,""),(1,"https://t.co")]
    pivot="https://t.co"
    tco_links=[]
    tco_link=""
    tco_starts=[m.start() for m in re.finditer(pivot,text)]
    if len(tco_starts)==0:
        tco_links.append("")
    elif len(tco_starts)>=1:
        for tco_start in tco_starts:
            tco_end=tco_start+23
            tco_link=text[tco_start:tco_end]
            tco_links.append(tco_link)
    # print(tco_links)
    # print(tco_starts)
    return tco_links

def translate(tco_link):
    try:
        driver.get(tco_link)
        if driver.current_url!=tco_link:
            real_link=driver.current_url
            if "bilibili" in real_link and "BV" in real_link:
                bv_len=len("BV18Z4y1u7Jd")
                bv_idx=real_link.find("BV")
                real_link=real_link[0:bv_idx+bv_len]
            # print("")
            # print("idx:{}".format(idx))
            print("fake:",tco_link)
            print("real:",real_link)
            # print("")
            return real_link
    except Exception:
        return tco_link

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

def get_date_from_link(link):
    print()
    print("link:",link)
    link_tail=link.replace("https://twitter.com","")
    driver.get(link+"/?lang=en")
    # time.sleep(5)
    # driver.add_cookie(cookies_dict)
    # driver.get(link)

    # driver.implicitly_wait(15)
    div_class_str="css-901oao r-14j79pv r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-1b7u577 r-bcqeeo r-qvutc0"
    # a_class_str="css-4rbku5 css-18t94o4 css-901oao css-16my406 r-14j79pv r-1loqt21 r-poiln3 r-bcqeeo r-qvutc0"
    a_class_str="css-4rbku5 css-18t94o4 css-901oao css-16my406 r-14j79pv r-1loqt21 r-xoduu5 r-1q142lx r-1w6e6rj r-poiln3 r-9aw3ui r-bcqeeo r-3s2u2q r-qvutc0"
    span_class_str="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"
    try:
        # date_str=driver.find_element(by=By.XPATH,value="//a[contains(@class,'{}')]/span[@class='{}']".format(a_class_str,span_class_str)).text
        date_str=driver.find_element(by=By.XPATH,value="//a[contains(@class,'{}')]".format(a_class_str)).get_attribute("aria-label")
        # print ("date_str:", date_str)
    except Exception:
        date_str=""
    print("\n\ndate-str:{}\n\n".format(date_str))
    format_date=get_format_date(date_str)
    return format_date

# print(get_date_from_link("https://twitter.com/ultramarine471/status/1497271102241837058"))
# sys.exit(0)

def login():
    driver.get(all_my_tweets_net)
    time.sleep(1)
    driver.get(all_my_tweets_net+'/redirect.php')
    time.sleep(3)
    # driver.find_element_by_xpath('//a[contains(@id,"redirect-link")]').click()
    # if "api.twitter.com" in driver.current_url:
    #     print("one jump success.")
    if not "api" in driver.current_url:
        driver.find_element(by=By.XPATH,value='//input[contains(@id,"username_or_email")]').send_keys(username)
        driver.find_element(by=By.XPATH,value='//input[contains(@id,"password")]').send_keys(passwd)
        driver.find_element(by=By.XPATH,value='//input[contains(@id,"allow")]').click()
    elif "api" in driver.current_url:
        driver.find_element(by=By.XPATH,value='//input[contains(@id,"allow")]').click()
        time.sleep(1)
        driver.find_element(by=By.XPATH,value="//input[@autocomplete='username']").send_keys(username)
        time.sleep(1)
        driver.find_element(by=By.XPATH,value="//input[@autocomplete='username']").send_keys(Keys.ENTER)
        time.sleep(1)
        driver.find_element(by=By.XPATH,value="//input[@autocomplete='current-password']").send_keys(passwd)
        time.sleep(1)
        driver.find_element(by=By.XPATH,value="//input[@autocomplete='current-password']").send_keys(Keys.ENTER)

login()


node=driver.find_element(by=By.XPATH,value='//input[contains(@placeholder,"Twitter User Name")]')
value=node.get_attribute("value")
if value!="":
    node.send_keys(Keys.CONTROL,'a')
    time.sleep(1)
    node.send_keys(Keys.BACK_SPACE)
    time.sleep(1)

node.send_keys(search_name)

time.sleep(1)

# driver.find_element_by_xpath('//div[@id="load-user-btn"]').click()
driver.find_element(by=By.XPATH,value='//div[@id="load-user-btn"]').click()
time.sleep(1)
driver.find_element(by=By.XPATH,value="//div[@id='tweets-btn']").click()

# 有些推文比较长
time.sleep(20)

nodes=driver.find_elements(by=By.XPATH,value="//div[@id='results']/ul/li")

while 1:
    nodes_left=[]
    last_node=nodes[-1]
    # 拉无可拉
    height1=driver.execute_script("return document.body.scrollHeight;")

    driver.execute_script("arguments[0].scrollIntoView();",last_node)
    nodes_left=driver.find_elements(by=By.XPATH,value="//div[@id='results']/ul/li")
    first_node=nodes_left[0]
    print("last:",last_node.text)
    print("first:",first_node.text)
    height2=driver.execute_script("return document.body.scrollHeight;")
    nodes=nodes+nodes_left
    if height1 == height2:
        print("bottom.")
        nodes=nodes_left[::-1]
        break

# print(len(nodes))
# nodes_len=len(nodes)
# assert nodes_len>=cnt
# nodes=nodes[cnt+1:]
# print(len(nodes2))
# sys.exit(0)

# nodes=list(set(nodes))
items=[]
date_len=len("Jan 23, 2022")

for idx,node in enumerate(nodes):
    text=node.text
    # print("text:",text)
    href_nodes=node.find_elements(by=By.XPATH,value="./a[@target='_blank' and @href]")
    hrefs=[each.get_attribute("href") for each in href_nodes]
    # print(hrefs)
    assert 1<=len(hrefs)
    href=""
    other_text=""
    for h in hrefs:
        if "status" in h:
            href=h
        elif "t.co" in h:
            tco_idx=h.find("t.co")
            tco_last=h[tco_idx+5:]
            # print(tco_last)
            if not tco_last in text:
                other_text="{} {}".format(other_text,h)
    assert href!=""
    date = text.strip ()[-date_len:]
    if href in collected_links:
        collected_date=cursor.execute("select d from tw where l='{}'".format(href)).fetchall()[0][0]
        if ":" in collected_date:
            # print(collected_date)
            print("ok.")
            continue
    text=text.strip()[:-date_len]
    text="{} {}".format(text,other_text)
    item=(search_name,text,date,href)
    # tup=(text,date,href)
    items.append(item)

print(items)

for idx,item in enumerate(items):
    search_name,text,date,link=item
    # print(item)
    # tco_translate
    tco_links=get_tco_links(text)
    # print(tco_links)
    if tco_links==[""]:
        pass
    else:
        for tco_link in tco_links:
            real_link=translate(tco_link)
            text=text.replace(tco_link,real_link)
    # date-sub
    newdate=get_date_from_link(link)
    print("\n\nnew date:",newdate)
    print("\n\n")
    if newdate!="":
        date=newdate
    new_item=(search_name,text,date,link)
    if link in collected_links:
        print("modify!")
        date_link=(date,link)
        cursor.execute("update tw set d = ? where l = ?",date_link)
    else:
        cursor.execute("insert into tw (u,t,d,l) values (?,?,?,?)",new_item)
    conn.commit()
    print("one done.")
    # items[idx]=new_item

# print(items)
# cursor.executemany("insert or replace into tw (u,t,d,l) values (?,?,?,?)",items)
# conn.commit()
print("done.")

# cursor.executemany("update tw set d = ? where l = ?")

    # print("---")
    # print(text)
    # print(href)
    # print("---")

# texts_s="\n".join(items)

# file_path="{}//{}_tweet_date_links.txt".format(dir_path,search_name)
# with open(file_path,"a",encoding="utf-8") as f:
#     f.write(texts_s)

