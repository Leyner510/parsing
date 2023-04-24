import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
from pprint import pprint
import json

def get_headers():
    return Headers(browser='Yandex', os='win').generate()

# Начало парсинга
head_hunter_html = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page=0', headers=get_headers()).text
head_hunter_soup = BeautifulSoup(head_hunter_html, 'lxml')
head_hunter_all_vacancy = head_hunter_soup.find_all('div', class_='serp-item')


parsed_list = []

for hh_vacancy in head_hunter_all_vacancy:
    h3_tag = hh_vacancy.find('h3')
    a_tag = h3_tag.find('a')
    a_tag_text = a_tag.text

    if 'Django' in a_tag_text or 'Flack' in  a_tag_text:
        name_company = a_tag_text
        link = a_tag['href']

        wage_fork = hh_vacancy('span')[2]
        wage_fork1 = wage_fork.text.replace('\u202f', ' ')

        company = hh_vacancy('a')[1]
        company1 = company.text

        linking = BeautifulSoup(requests.get(link, headers=get_headers()).text, 'lxml')
        city_text = linking.find('div', class_='vacancy-company-redesigned')
        for city1 in city_text:
                city = city1.text
                pprint(city)
        
        parsed_list.append(
            {
            'title': name_company,
            'link': link,
            'wage_fork': wage_fork1,
            'company': company1,
            'city': city
            }
        )
with open ('company.json', 'w') as f:
     json.dump(parsed_list, f, indent=1)

    

