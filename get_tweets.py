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

def login():
    driver.get("https://twitter.com/login")
    username="117010155@link.cuhk.edu.cn"
    # password=input("your password:")
    password="xm111737"

    time.sleep(10)
    
    # find the element where we have to 
    # enter the xpath
    # fill the number or mail
    driver.find_element_by_xpath('//input[contains(@name,"username_or_email")]').send_keys(username)

    time.sleep(1)
    
    # find the element where we have to 
    # enter the xpath
    # fill the password
    driver.find_element_by_xpath('//input[contains(@name,"password")]').send_keys(password)

    time.sleep(3)
    
    # find the element log in 
    # request using xpath 
    # clicking on that element 
    driver.find_element_by_xpath('//div[@data-testid="LoginForm_Login_Button"]').click()

    time.sleep(3)

username=input("username:")
# filename=input("filename:")
filename=username

links_path=r"D:\get_tweets\{}.txt".format(filename)

already_links=[]

if not os.path.exists(links_path):
    open(links_path,"w").close()
else:
    with open(links_path,"r",encoding="utf-8") as f:
        already_links=[e.strip("\n") for e in f.readlines()]

already_links_set=set(already_links)

max_delay=10

def find_element_by_xpath2(patt):
    try:
        res=WebDriverWait(driver,max_delay).until(EC.presence_of_element_located((By.XPATH, patt)))
    except selenium.common.exceptions.TimeoutException:
        res=""
    return res

twi_with_replies_url=f"https://twitter.com/{username}/with_replies"

firefox_path=r"C:\Program Files\Mozilla Firefox\geckodriver.exe"
options = Options()
# options.headless = True
options.headless = False

proxy="127.0.0.1:10087"

options.add_argument(f"--proxy-server=http:{proxy}")

driver=webdriver.Firefox(options=options,executable_path=firefox_path)

login()
print("login success.")

driver.get(twi_with_replies_url)

# 保险一点
time.sleep(10)

patt="//a[contains(@href,'status')]"

js1="window.scrollBy(0,100)"
times=10**10

cnt=0

links=[]

cur_link=""
waste=0

while cnt<=times:
# while cnt<=20:
    driver.execute_script(js1)
    time.sleep(1)
    node=find_element_by_xpath2(patt)
    link=node.get_attribute("href")
    if link==cur_link:
        waste+=1
        print("waste:",waste)
        continue
    else:
        if not link in already_links_set:
            links.append(link)
            print(link)
            with open(links_path,"a",encoding="utf-8") as f:
                f.write(link+"\n")
        cnt+=1
        cur_link=link
        waste=0