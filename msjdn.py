from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.support.select import Select

import sys
import re
import requests

import os

from PIL import Image

# you need to have a specified driver.
## I use selenium because I dont know whether the page source will change or not.

firefox_path=r"C:\Program Files\Mozilla Firefox\geckodriver.exe"
options = Options()
# options.headless = True
options.headless = False

proxy="127.0.0.1:10087"

options.add_argument(f"--proxy-server=http:{proxy}")

driver=webdriver.Firefox(options=options,executable_path=firefox_path)
driver.implicitly_wait(20)

target_url="https://hk.sz.gov.cn:8118/userPage/login"
driver.get(target_url)

btn_node=driver.find_element_by_xpath("//button[@onclick='closeLoginHint()']")
btn_node.click()

print("btn clicked.")

# select obj
select_certificate_node=Select(driver.find_element_by_id("select_certificate"))
print(select_certificate_node.options)
sys.exit(0)

for idx,s1 in enumerate(select_certificate_node.options,1):
    print(s1)
    if "选择" in s1:
        continue
    print("选项 {}: {}".format(idx,s1))

# display the choices
print("")
idx_str=input("您选择第 1/2/3/4/5 项?")
if idx_str.isdigit():
    idx=int(idx_str)-1

# select the choice
select_certificate_node.select_by_index(idx)

# id card input

idcard_no_node=driver.find_element_by_id("input_idCardNo")
idcard_no=input("您的证件号码：")
idcard_no_node.send_keys(idcard_no)

pwd_node=driver.find_element_by_id("input_pwd")
pwd=input("您的密码：")
pwd_node.send_keys(pwd)

capcha_pic_node=driver.find_element_by_id("img_verify")
capcha_pic_link_tail=capcha_pic_node.get_attribute("src")

capcha_pic_link=""
if "gov.cn" in capcha_pic_link:
    capcha_pic_link=capcha_pic_link_tail
else:
    capcha_pic_link="https://hk.sz.gov.cn:8118"+capcha_pic_link_tail

r=requests.get(capcha_pic_link)
with open("capcha.jpg","wb") as f:
    f.write(r.content)

print("capcha obtained.")

capcha_img=Image.open(os.getcwd()+os.sep+"capcha.jpg")
capcha_img.show()

capcha_code=input("输入图形验证码：")

capcha_code_node=driver.find_element_by_id("input_verifyCode")

if capcha_code.isdigit():
    capcha_code_node.send_keys(capcha_code)

enter_btn_node=driver.find_element_by_id("btn_login")
enter_btn_node.click()



