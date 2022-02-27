from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
  
# create instance of Chrome webdriver

firefox_path=r"C:\Program Files\Mozilla Firefox\geckodriver.exe"

driver=webdriver.Firefox(executable_path=firefox_path)
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

