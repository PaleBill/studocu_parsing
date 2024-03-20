import time
from seleniumbase import Driver
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import pickle


url = 'https://www.studocu.com/cs/course/ceska-zemedelska-univerzita-v-praze/zemedelske-systemy-i/3126043'
driver = Driver(uc=True)
driver.get(url)
for cookie in pickle.load(open('cookies2', 'rb')):
    driver.add_cookie(cookie)
time.sleep(2)
driver.refresh()
# time.sleep(2)
# driver.get('https://www.studocu.com/cs/course/ceska-zemedelska-univerzita-v-praze/zoologie-ii/3273618')
time.sleep(60)
pickle.dump(driver.get_cookies(), open('cookies2', 'wb'))