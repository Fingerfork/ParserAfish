import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://afisha.relax.by/conserts/minsk/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0', 'accept': '*/*'}# Во избежании блокировки
HOST = 'https://afisha.relax.by'
FILE='event.csv'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

concert = []# Пустой список для сохраниения

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_content=soup.find_all('div', class_="schedule__list")
    #please = soup.find_all('a', class_="schedule__place-link link")
    #event = soup.find_all('a', class_="schedule__event-link link")
    #time = soup.find_all('a', class_="schedule__event-link link")
    date=soup.find_all('h5', class_="h5 h5--compact h5--bolder u-mt-6x")
    print(date)#----Здесь есть проблема с датированием событий---------

    for item in all_content:

        concert.append({

            'Place': item.find('a', class_="schedule__place-link link").get_text(strip=True), # Перемненной присваиваим значение места
            'Event': item.find('a', class_="schedule__event-link link").get_text(strip=True),# Перемненной присваиваим значение события
            'Link': item.find('a', class_="schedule__event-link link").get("href"),# Перемненной присваиваим значение адреса
            'Time': item.find('div', class_="schedule__time").get_text(strip=True),# Перемненной присваиваим значение времени

        })
    print(concert)# Список ключ значений

def save_concert(all_content, path):# Функция для сохранения событий в csv формате
    with open(path, 'w', newline='') as file:
        writer= csv.writer(file, delimiter=';')
        writer.writerow(['Место', 'Событие', 'Ссылка','Время'])
        for item in all_content:
            writer.writerow([item['Place'], item['Event'], item['Link'], item['Time']])



def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
        save_concert(concert, FILE)# Вызываем и запускаем сохраниение
        print(f'Получено {len(concert)} концертов!') # Количество событий
    else:
        print("Error")
parse()






