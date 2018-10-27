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

category ='https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/videokarty'
pr_list = ['https://178.47.131.21:3128', 'https://195.208.172.70:8080', 'https://46.228.2.178:3128', 'https://178.128.26.169:8080', 'https://119.81.71.27:80', 'https://118.174.211.219:81', 'https://35.199.96.12:80', 'https://43.231.184.32:1080', 'https://74.208.83.188:80', 'https://149.202.87.93:9999', 'https://88.204.154.155:8080', 'https://180.210.206.52:3128', 'https://80.211.95.112:3128', 'https://180.210.205.107:3128', 'https://76.69.192.176:3128', 'https://103.240.161.109:6666', 'https://185.31.159.62:3128', 'https://180.210.201.54:3128', 'https://163.172.182.164:3128', 'https://88.204.154.155:80', 'https://178.62.193.217:3128', 'https://181.10.230.90:3128', 'https://94.177.173.225:3128', 'https://180.210.205.104:3128', 'https://178.128.96.106:3128', 'https://173.212.204.122:3128', 'https://192.99.226.30:3128', 'https://5.9.58.22:3128', 'https://51.38.234.95:8080', 'https://159.8.114.37:25', 'https://51.140.202.119:8080', 'https://23.253.54.249:3128', 'https://35.196.254.123:3128', 'https://67.209.67.231:5555', 'https://51.38.71.101:8080', 'https://202.139.192.16:3128', 'https://180.210.205.110:3129', 'https://119.81.71.27:8123', 'https://37.61.224.240:8195', 'https://159.8.114.37:8123', 'https://192.99.226.30:80', 'https://173.192.128.238:8123', 'https://158.69.206.181:8888', 'https://131.161.42.6:8090', 'https://71.6.46.151:443', 'https://173.192.21.89:80', 'https://212.112.97.27:3128', 'https://202.63.243.236:8888', 'https://52.206.108.231:3128', 'https://64.214.77.66:8080', 'https://173.192.21.89:8123', 'https://119.81.189.194:25', 'https://62.129.12.74:8888', 'https://159.8.114.37:80', 'https://138.118.173.123:8080', 'https://202.29.238.161:3128', 'https://202.139.192.16:8080', 'https://69.51.6.201:8080', 'https://118.174.211.219:8080', 'https://14.36.4.200:3128', 'https://190.254.192.131:3128', 'https://104.152.179.76:808', 'https://35.185.201.225:8080', 'https://125.25.202.21:3128']
proxies = {

        'https': 'https://195.208.172.70:8080'
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
                                 category='videokarty')
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