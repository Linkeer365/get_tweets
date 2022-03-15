from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import re
import requests

# you need to have a specified driver.
## I use selenium because I dont know whether the page source will change or not.

firefox_path=r"C:\Program Files\Mozilla Firefox\geckodriver.exe"
options = Options()
options.headless = True
# options.headless = False

proxy="127.0.0.1:10087"

options.add_argument(f"--proxy-server=http:{proxy}")

driver=webdriver.Firefox(options=options,executable_path=firefox_path)
driver.implicitly_wait(20)

driver.get("https://money.cnn.com/data/fear-and-greed/")

url_str=driver.find_element_by_id("needleChart").get_attribute("style")

url=re.findall("https://.*?png",url_str)[0]

# This is the url of image.

print(url)

driver.get(url)

# I use requests library to download the image. This can be good.

r=requests.get(url)



with open("fear_greed_index.png","wb") as f:
    f.write(r.content)