from typing import NamedTuple
import selenium
import re

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os
import sys

import time

# username=input("username:")
# passwd=input("password:")

dir_path="D://get_tweets"

username="ultramarine471"
passwd="xm111737"
search_name=input("who you want:")

# visit=input("")

firefox_path=r"C:\Program Files\Mozilla Firefox\geckodriver.exe"
options = Options()
# options.headless = True
options.headless = False

proxy="127.0.0.1:10087"

options.add_argument(f"--proxy-server=http:{proxy}")

driver=webdriver.Firefox(options=options,executable_path=firefox_path)

all_my_tweets_net="https://www.allmytweets.net/"

def login():
    driver.get(all_my_tweets_net)
    time.sleep(3)
    driver.get(all_my_tweets_net+'/redirect.php')
    # driver.find_element_by_xpath('//a[contains(@id,"redirect-link")]').click()
    time.sleep(3)
    if "api.twitter.com" in driver.current_url:
        print("one jump success.")
    driver.find_element_by_xpath('//input[contains(@id,"username_or_email")]').send_keys(username)
    driver.find_element_by_xpath('//input[contains(@id,"password")]').send_keys(passwd)
    time.sleep(3)
    driver.find_element_by_xpath('//input[contains(@id,"allow")]').click()
    time.sleep(3)

login()


node=driver.find_element_by_xpath('//input[contains(@placeholder,"Twitter User Name")]')
value=node.get_attribute("value")
if value!="":
    node.send_keys(Keys.CONTROL,'a')
    time.sleep(1)
    node.send_keys(Keys.BACK_SPACE)
    time.sleep(1)

node.send_keys(search_name)

time.sleep(3)

driver.find_element_by_xpath('//div[@id="load-user-btn"]').click()

time.sleep(3)

driver.find_element_by_xpath("//div[@id='tweets-btn']").click()

time.sleep(30)

nodes=driver.find_elements_by_xpath("//div[@id='results']/ul/li")

for i in range(1,5):
    nodes_left=[]
    last_node=nodes[-1]
    # 拉无可拉
    height1=driver.execute_script("return document.body.scrollHeight;")

    driver.execute_script("arguments[0].scrollIntoView();",last_node)
    
    time.sleep(10)
    nodes_left=driver.find_elements_by_xpath("//div[@id='results']/ul/li")
    first_node=nodes_left[0]
    print("last:",last_node.text)
    print("first:",first_node.text)
    height2=driver.execute_script("return document.body.scrollHeight;")
    nodes=nodes+nodes_left
    if height1 == height2:
        print("bottom.")
        break

# nodes=list(set(nodes))
lines=[]
date_len=len("Jan 23, 2022")
for node in nodes:
    text=node.text
    href=node.find_element_by_xpath("./a[@target='_blank']").get_attribute("href")
    date=text.strip()[-date_len:]
    text=text.strip()[:-date_len]
    line="{}\t{}\t{}".format(text,date,href)
    # tup=(text,date,href)
    lines.append(line)
    print("---")
    print(text)
    print(href)
    print("---")

lines_s="\n".join(lines)

file_path=r"{}//{}_tweet_date_links.txt".format(dir_path,search_name)
with open(file_path,"w",encoding="utf-8") as f:
    f.write(lines_s)

print("done.")