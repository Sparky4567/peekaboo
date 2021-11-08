import requests
import basicauth
import requests
from config import peekaboo_admin
from config import peekaboo_password
from config import peekaboo_ip
from config import peekaboo_port
from config import webdriver_path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# REQUESTS TEST

headers = basicauth.encode(peekaboo_admin,peekaboo_password)
endpoint = "helper"
url_to_test = "https://www.artefaktas.eu/2021/10/pssst-nori-parodysiu-kaip-veikia-tikras.html"
headers_to_pass = {
    "Authorization":headers,
    "Check-Url": url_to_test,
    "User-Agent":"googlebot"
}
r = requests.get("http://{}:{}/{}".format(peekaboo_ip,peekaboo_port,endpoint),headers=headers_to_pass)
print(r.text)

#SELENIUM TEST

# agent = {
#     "User-Agent":"googlebot"
# }
# weboptions = Options()
# weboptions.add_argument("user-agent=[{}]".format(agent))
# weboptions.add_argument("--headless")
# weboptions.add_argument("--no-sandbox")
# driver_path = webdriver_path
# driver = webdriver.Chrome(driver_path,options=weboptions)
# driver.get(url_to_test)
# print(driver.page_source)
# time.sleep(8)
# driver.close()