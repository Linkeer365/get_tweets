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

# username=input("username:")
username="mutilated_catal"
# filename=input("filename:")
filename=username

links_path=r"D:\get_tweets\{}_tweets.txt".format(filename)
links_path2=r"D:\get_tweets\{}.txt".format(filename)

already_links=[]

if not os.path.exists(links_path):
    open(links_path,"w").close()
else:
    with open(links_path,"r",encoding="utf-8") as f:
        already_links=[e.strip("\n").replace("Link: ","") for e in f.readlines() if "https" in e]

content_links=[]

with open(links_path2,"r",encoding="utf-8") as f:
    content_links=[e.strip("\n") for e in f.readlines()]


already_links_set=set(already_links)
# content_links_set=set(content_links)
# assert content_links_set!=None


max_delay=10

def find_element_by_xpath2(patt):
    try:
        res=WebDriverWait(driver,max_delay).until(EC.presence_of_element_located((By.XPATH, patt)))
    except selenium.common.exceptions.TimeoutException:
        res=""
    return res

def find_elements_by_xpath2(patt):
    # max_delay=5
    try:
        WebDriverWait (driver, max_delay).until (EC.presence_of_element_located ((By.XPATH, patt)))
        return driver.find_elements_by_xpath(patt)
    except selenium.common.exceptions.TimeoutException:
        return []


twi_with_replies_url=f"https://twitter.com/{username}/with_replies"

firefox_path=r"C:\Program Files\Mozilla Firefox\geckodriver.exe"
options = Options()
options.headless = True
# options.headless = False

proxy="127.0.0.1:10087"

options.add_argument(f"--proxy-server=http:{proxy}")

driver=webdriver.Firefox(options=options,executable_path=firefox_path)

# content_links=["https://twitter.com/mutilated_catal/status/1389244895202881542"]

# "css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"

# patt="//div[@class='css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']/span[@class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']"

# "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"
# "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"

patt="//div[contains(@class,'css-901oao r-18jsvk2')]/span[@class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']"

# patt_check=""

for content_link in content_links:
    if content_link in already_links_set:
        continue
    driver.get(content_link)
    nodes=find_elements_by_xpath2(patt)
    tweet=""
    # for node in nodes:
    if len(nodes)>=1:
        node=nodes[-1]
        try:
            tweet=tweet+"\n"+node.text
        except selenium.common.exceptions.StaleElementReferenceException:
            break
    print(tweet)
    my_str=f"Link: {content_link}\nTweet: {tweet}\n\n"
    with open(links_path,"a",encoding="utf-8") as f:
        f.write(my_str)
        # print()
    # break


