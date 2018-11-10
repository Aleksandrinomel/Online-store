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


def list_of_id_bd_creator():
    goods = Goods.objects.all()
    list_of_id_bd = []
    for good in goods:
        list_of_id_bd.append(good.avito_ad_number)
    return list_of_id_bd
    print(list_of_id_bd)

category ='https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/materinskie_platy'
pr_list = ['https://23.92.26.210:8000', 'https://156.237.192.227:1080', 'https://203.109.86.185:8888', 'https://45.32.195.95:8124', 'https://45.32.195.95:8111', 'https://91.235.42.20:3130', 'https://159.8.114.37:80', 'https://181.41.215.96:1080', 'https://178.128.21.245:3128', 'https://74.208.83.188:80', 'https://24.30.70.57:8080', 'https://45.32.195.95:8118', 'https://94.124.1.66:8080', 'https://35.240.29.142:3128', 'https://51.68.177.232:1080', 'https://178.128.19.104:3128', 'https://54.39.138.148:3128', 'https://173.192.21.89:25', 'https://35.185.201.225:8080', 'https://149.56.69.5:1080', 'https://178.128.21.245:8080', 'https://180.210.201.57:3130', 'https://67.209.67.231:5555', 'https://173.192.21.89:80', 'https://188.40.166.196:3128', 'https://178.128.101.234:8080', 'https://45.32.195.95:8123', 'https://51.38.234.95:8080', 'https://200.70.46.238:3128', 'https://51.75.109.89:3128', 'https://198.50.142.47:3128', 'https://142.44.242.57:3128', 'https://80.106.195.144:3128', 'https://51.75.109.85:3128', 'https://161.202.226.194:8123', 'https://66.70.167.123:3128', 'https://104.237.138.105:8118', 'https://41.76.245.106:8888', 'https://125.99.34.93:8080', 'https://200.21.90.246:8080', 'https://178.128.31.194:8080', 'https://196.0.109.146:8888', 'https://163.172.182.164:3128', 'https://163.172.134.194:3128', 'https://202.181.232.229:1080', 'https://201.20.99.10:3130', 'https://51.15.169.6:8118', 'https://188.165.132.181:3128', 'https://200.178.236.210:3128', 'https://47.89.37.177:3128', 'https://41.208.20.50:8888', 'https://90.84.240.81:3128', 'https://185.38.216.122:8888', 'https://200.152.78.48:8888', 'https://185.85.162.32:83', 'https://41.160.246.212:3128', 'https://88.204.154.155:3128', 'https://181.47.169.81:8888', 'https://95.78.157.140:8888', 'https://212.237.30.203:8888', 'https://51.75.25.8:3133', 'https://95.216.15.79:3128', 'https://51.75.109.94:3128', 'https://178.128.101.158:80']
proxies = {

        'https': 'https://185.38.216.122:8888'
    }
# Определяет кол-во страниц, на которых расположены нужные объявления
def create_total_pages():

    avito_html = requests.get(category, proxies=proxies)
    text = BeautifulSoup(avito_html.text, "html.parser")
    print(text)
    pages = text.select('.pagination-page')
    for page in pages:
        if page.getText() == 'Последняя':
            m = re.search('(p=)\w+', page.get('href'))
            total_pages = int(m.group(0)[2:])
    return total_pages

# Ходит по страницам, ищет id товара и записывает их в список
def list_of_id_avito_creator(total_pages, category):
    list_of_id_avito = []
    for number_page in range(1, total_pages + 1):
        link = category + '?p=' + str(number_page)
        # Обработка исключений без прерывания цикла
        try:
            avito_html = requests.get(link, proxies=proxies)
        except Exception as e:
            print(e)
            continue
        text = BeautifulSoup(avito_html.text, "html.parser")
        items = text.select('.js-item-extended')
        for i in items:
            list_of_id_avito.append(i.get('data-item-id'))
        time.sleep(1)
        print(list_of_id_avito)
        break
    print(list_of_id_avito)
    return list_of_id_avito


def deletion_date_creator(list_of_id_bd, list_of_id_avito):
    for id_bd in list_of_id_bd:
        if id_bd not in list_of_id_avito:
            good = Goods.objects.get(avito_ad_number=id_bd)
            if good.deletion_date is None:
                good.deletion_date = datetime.today()
                good.save()

category_dict = {'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/videokarty':
                      'videokarty'}


def new_goods_creator(list_of_id_avito, list_of_id_bd, pr_list):
    pr_check = 0
    months = {'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06', 'июля': '07', 'августа': '08',
              'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12', 'января': '01', 'февраля': '02'}
    for id_avito in list_of_id_avito:
        if id_avito not in list_of_id_bd:
            item_link = 'https://www.avito.ru/moskva/tovary_dlya_kompyutera/' + '_' + id_avito
            for i in range(len(pr_list)):
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

                    try:
                        info_dict['price'] = item_text.select('.js-item-price')[0].getText()
                    except IndexError:
                        info_dict['price'] = 'Цена не указана'


                    info_dict['adress'] = ''.join(item_text.select('.item-map-location')[0].getText().split()[1:-2])

                    info_dict['ad_text'] = item_text.select('.item-description')[0].getText()

                    #info_dict['phone'] = item_text.select('.item-popup-content')

                    image_tags = item_text.select('.gallery-img-frame')
                    image_links = ''
                    for image_tag in image_tags:
                        image_links += image_tag['data-url'] + ','
                    info_dict['photo_link'] = image_links
                    print(info_dict)

                    # Записываем данные из словарей в бд, через модель django
                    good = Goods(name=info_dict['name'], avito_ad_number=info_dict['id'],
                                 publication_date=info_dict['avito_date_publication'],
                                 publication_time=info_dict['avito_time_publication'], text=info_dict['ad_text'],
                                 photo_link=info_dict['photo_link'], adress=info_dict['adress'], price=info_dict['price'],
                                 category='materinskie_platy')
                    good.save()

                    #                x += 1
                    #                if x == 2:
                    #                   break
                    time.sleep(1)
                    break
                except BaseException as er:
                    print(er)
                    print(info_dict)
                    if info_dict == {}:
                        proxies['https'] = pr_list[pr_check]
                        pr_check += 1
                        continue
                    else:
                        break




total_pages = create_total_pages()
list_of_id_avito = list_of_id_avito_creator(total_pages, category)
list_of_id_bd = list_of_id_bd_creator()
deletion_date_creator(list_of_id_bd, list_of_id_avito)
new_goods_creator(list_of_id_avito, list_of_id_bd, pr_list)