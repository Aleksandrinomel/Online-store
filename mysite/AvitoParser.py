# -*- coding: utf-8 -*-
import re
import requests
from datetime import datetime, timedelta
import time
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
import django
django.setup()
from django.db import models
from bs4 import BeautifulSoup
from goods.models import Goods


def parser():
    proxies = {

        'https': 'https://12.2.202.242:8080'
    }

    category_list =['https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/cd_dvd_i_blu-ray_privody',
                     'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/bloki_pitaniya',
                     'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/videokarty',
                     'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/zhestkie_diski',
                     'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/zvukovye_karty',
                     'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/kontrollery',
                     'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/korpusy',
                     'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/materinskie_platy',
                     'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/operativnaya_pamyat',
                     'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/protsessory',
                     'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/sistemy_ohlazhdeniya']

    category_dict = {'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/cd_dvd_i_blu-ray_privody':
                      'CD, DVD и Blu-ray приводы', 'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/bloki_pitaniya':
                      'Блоки питания', 'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/videokarty':
                      'Видеокарты', 'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/zhestkie_diski':
                      'Жёсткие диски', 'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/zvukovye_karty':
                      'Звуковые карты', 'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/kontrollery':
                      'Контролеры', 'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/korpusy': 'Корпусы',
                     'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/materinskie_platy': 'Материнские платы',
                     'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/operativnaya_pamyat': 'Оперативная память',
                     'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/protsessory': 'Процессоры',
                     'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/sistemy_ohlazhdeniya': 'Системы охлаждения'}

    for category in category_list:

        avito_html = requests.get(category, proxies=proxies)
        text = BeautifulSoup(avito_html.text, "html.parser")
        pages = text.select('.pagination-page')
    
        # Определяет кол-во страниц, на которых расположены нужные объявления
        for page in pages:
            if page.getText() == 'Последняя':
                m = re.search('(p=)\w+', page.get('href'))
                total_pages = int(m.group(0)[2:])

        # Ходит по страницам, ищет ссылки на товар и записывает их в список links
        links = []
        y = 0 
        for number_page in range(1, total_pages + 1):
            link = category + '?p=' + str(number_page)
            #Обработка исключений без прерывания цикла
            try:
                avito_html = requests.get(link, proxies=proxies)
            except Exception as e:
                print(e)
                continue    
            text = BeautifulSoup(avito_html.text, "html.parser")
            items = text.select('.item-description-title-link')
            for i in items:
                href = 'https://www.avito.ru' + i.get('href')
                links.append(href)
                print(href)
            y += 1
            if y == 1:
                break
            time.sleep(0.5)
        print(links)

        # Ходит по ссылкам на товар и заполняет список словарей

        months = {'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06', 'июля': '07', 'августа': '08',
                  'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12', 'января': '01', 'февраля': '02'}

        x = 0
        for item_link in links:
            try:
                item_html = requests.get(item_link, proxies=proxies)
                item_text = BeautifulSoup(item_html.text, "html.parser")
                info_dict = {}

                meta_data_list = item_text.select('.title-info-metadata-item')[0].getText().split()
                if meta_data_list[3] == "сегодня":
                    info_dict['avito_date_publication'] = datetime.now().strftime('%Y-%m-%d')
                elif meta_data_list[3] == 'вчера':
                    yesterday = datetime.now() - timedelta(days=1)
                    info_dict['avito_date_publication'] = yesterday.strftime('%Y-%m-%d')
                else:
                    info_dict['avito_date_publication'] = datetime.now().strftime('%Y') + '-' + months[
                        meta_data_list[4]] + '-' + meta_data_list[3]

                info_dict['avito_time_publication'] = meta_data_list[-1]

                info_dict['id'] = meta_data_list[1].strip(',')

                info_dict['name'] = item_text.select('.title-info-title-text')[0].getText()

                info_dict['price'] = item_text.select('.js-item-price')[0].getText()

                info_dict['adress'] = ''.join(item_text.select('.item-map-location')[0].getText().split()[1:-2])

                info_dict['ad_text'] = item_text.select('.item-description-text')[0].getText()

#               info_dict['phone'] = item_text.select('.item-popup-content')

                image_tags = item_text.select('.gallery-img-frame')
                image_links = ''
                for image_tag in image_tags:
                    image_links += image_tag['data-url'] + ','
                info_dict['photo_link'] = image_links
#                
                #Записываем данные из словарей в бд, через модель django
                good = Goods(name=info_dict['name'], avito_ad_number=info_dict['id'],
                             publication_date=info_dict['avito_date_publication'],
                             publication_time=info_dict['avito_time_publication'], text=info_dict['ad_text'],
                             photo_link=info_dict['photo_link'], adress=info_dict['adress'], price=info_dict['price'],
                             category=category_dict[category])
                good.save()

                x += 1
                if x == 1:
                    break
                time.sleep(0.5)
            except BaseException as er:
                print(er)
                continue


if __name__ == "__main__":
    parser()