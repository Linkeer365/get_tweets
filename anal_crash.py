import tempfile

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Custom profile folder to keep the minidump files
profile = tempfile.mkdtemp(".selenium")
print("*** Using profile: {}".format(profile))

# Use the above folder as custom profile
opts = Options()
opts.add_argument("-profile")
opts.add_argument(profile)
opts.binary = r"C:\Program Files\Mozilla Firefox\firefox.exe"

driver = webdriver.Firefox(options=opts,
    # hard-code the Marionette port so geckodriver can connect
    service_args=["--marionette-port", "2828"])
