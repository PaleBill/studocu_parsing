from bs4 import BeautifulSoup
import requests
import json

"""CREATING COURSE LINKS AND NAMES JSON"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'

}


# request = requests.get(url= 'https://www.studocu.com/cs/institution/ceska-zemedelska-univerzita-v-praze/2773', headers=headers)
# with open('courses_links.html', 'w', encoding='utf8') as file:
#     file.write(request.text)

with open('courses_links.html',encoding='utf8') as file:
    src = file.read()
soup = BeautifulSoup(src, 'lxml')


courses_links = []
r = soup.find('ul', class_="_add59da3a56f").find_all('a')
for el in r:
    courses_links.append({
        'course_name': el.text,
        'course_link':el.get('href')
    })

with open('course_links.json', 'a',encoding='utf8') as file:
    json.dump(courses_links,file, indent=4, ensure_ascii= True)


