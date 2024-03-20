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

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.headless = False
options.add_experimental_option("excludeSwitches", ['enable-automation'])
options.add_experimental_option("useAutomationExtension", False)
# options.add_argument('proxy-server=85.26.146.169')
options.add_argument( r'--user-data-dir=C:\Users\User\AppData\Local\Google\Chrome\User Data\Default' )



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'

}
def get_page(headers):
    url = 'https://www.studocu.com/cs/course/ceska-zemedelska-univerzita-v-praze/zemedelske-systemy-i/3126043'
    driver = webdriver.Chrome(options = options)
    # blocker_solver(driver,url)
    # driver = Driver(uc=True)
    try:
        driver.get(url)
        print('Got it')
        time.sleep(3)
        buttons = driver.find_elements(By.CLASS_NAME, '_2b654edfc355')
        print(len(buttons))
        for i, button in enumerate(buttons):
            if i%2 != 0:
                button.click()
                print('[INFO] + button')
                time.sleep(1)
        time.sleep(15)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        print('[INFO] Driver closed.')

    # request = requests.get(url= url, headers= headers)
    # with open('index_test.html', 'w',encoding="utf-8") as file:
    #     file.write(request.text)

def get_data_file(headers):


    with open('index.html',encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    sections = soup.find_all('section', class_="_cd5b488b4c57")
    # section_names = [ el.find('h2', class_="_d9f2ae986446").text for el in sections]
    # print(section_names)

    course_files = []
    file_atributes = []
    for section in sections:
        file_atributes = []
        section_name = section.find('h2', class_="_d9f2ae986446").text
        file_list = section.find('ul', class_ = 'list-unstyled')
        file_boxes = file_list.find_all('li', class_=["_6e62fae68223", 'hidden'])
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
        course_files= {
            'section': section_name,
            'files': file_atributes
        }
    print(course_files, '\n', len(file_atributes))

    # with open('course_files.json', 'a', encoding="utf-8") as file:
    #     json.dump(course_files,file, indent=4, ensure_ascii= True)


def main():
    get_page(headers)
    # get_data_file(headers)


if __name__ == '__main__':
    main()


