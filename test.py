from bs4 import BeautifulSoup
import requests
import json
import time
import undetected_chromedriver
from seleniumbase import Driver
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import pickle


# options = webdriver.ChromeOptions()

# ua = UserAgent()
# user_agent = ua.random
# print(f"[INFO] {user_agent}")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_experimental_option("excludeSwitches", ['enable-automation'])
# options.add_experimental_option("useAutomationExtension", False)
# options.add_argument( r'--user-data-dir=C:\Users\User\AppData\Local\Google\Chrome\User Data\Default' )
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
# options.add_argument(f"--user-agent={user_agent}")
# options.add_argument('--proxy-server=34.154.161.152:80')
# options.headless = False


# Getting courses links
src = open('course_links.json')
courses = json.load(src)
src.close()
COURSE_LINKS = []
for course in courses:
    COURSE_LINKS.append([course['course_name'],course['course_link']])
# print(len(COURSE_LINKS))

def upload_course(course_name,html):

    soup = BeautifulSoup(html, 'lxml')
    sections = soup.find_all('section', class_="_cd5b488b4c57")
    print('[INFO] number of sections', len(sections))
    time.sleep(1)
    docs_count = soup.find('div', class_ ='_7ca67eec0070').find('span').text
    docs_true_count = 0
    course_files = []

    for section in sections:
        file_atributes = []
        section_name = section.find('h2', class_="_d9f2ae986446").text
        file_list = section.find('ul', class_ = 'list-unstyled')
        file_boxes = file_list.find_all('li', class_=["_6e62fae68223", 'hidden'])
        docs_true_count += len(file_boxes)
        for el in file_boxes:
            try:
                file_atributes.append({
                        'name': el.find('span', class_="_87277f5bff47").text,
                        'link': el.find('a', class_='_086d12a79881').get('href'),
                        'year': el.find('span', class_="_a8fa0495ca13 _28d067932777 hidden-xs").text
                        })
            except Exception:
                file_atributes.append({
                    'name': el.find('a').text,
                    'link': el.find('a').get('href'),
                    'year': 'hidden'
                })
        course_files.append({
            'section': section_name,
            'files': file_atributes
        })
    print('[INFO] number of files found',docs_true_count, '/', docs_count,'\n')
    course_docs = {
        'course_name': course_name,
        'sections': course_files
    }
    return course_docs



# Getting valid pages html





result_list = []
# driver = webdriver.Chrome()
try:

    for course_name,url in COURSE_LINKS[30:35]:
        try:
            driver = Driver(uc=True)
            driver.get(url)
            time.sleep(3)
            print(f'[INFO] {driver.title} \n{url}')
            try_count = 0
            # pickle.dump(driver.get_cookies(), open('cookies', 'wb'))
            """NO REDIRECTION"""
            while driver.title == 'Access to this page has been denied' and try_count<3:
                for cookie in pickle.load(open('cookies', 'rb')):
                    driver.add_cookie(cookie)
                time.sleep(2)
                driver.refresh()
                time.sleep(3)
                try_count += 1
            if try_count == 3:
                break


            buttons = driver.find_elements(By.CLASS_NAME,'_2b654edfc355')
            print('[INFO] number of buttons', len(buttons))
            for i, button in enumerate(buttons):
                if i%2 != 0:
                    button.click()
                    print('[INFO] button clicked')
            html = driver.page_source
            print('[INFO] Uploading course...')
            course_docs = upload_course(course_name,html)
            time.sleep(2)
            result_list.append(course_docs)
            driver.close()
            driver.quit()
        except Exception:
            continue

except Exception as ex:
    print(ex)
finally:
    with open('course_files_testing.json', 'a', encoding="utf-8") as file:
        json.dump(result_list,file, indent=4, ensure_ascii= True)
    driver.close()
    driver.quit()
    print('[INFO] Driver closed.')

