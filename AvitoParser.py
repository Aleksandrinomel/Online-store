import re
import requests
from datetime import datetime, timedelta
import time
from django.db import models
from bs4 import BeautifulSoup


def parser():
    proxies = {

        'https': 'https://194.135.75.74:41258'
    }

    avito_html = requests.get('https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/videokarty',
                              proxies=proxies)
    text = BeautifulSoup(avito_html.text, "html.parser")
    pages = text.select('.pagination-page')

    # Определяет кол-во страниц, на которых расположены нужные объявления
    for page in pages:
        if page.getText() == 'Последняя':
            m = re.search('(p=)\w+', page.get('href'))
            total_pages = int(m.group(0)[2:])

    # Ходит по страницам, ищет ссылки на товар и записывает их в список links
    links = []
    for number_page in range(1, total_pages + 1):
        link = 'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/videokarty?p=' + str(number_page)
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
        time.sleep(0.5)
    print(links)

    # Ходит по ссылкам на товар и заполняет список словарей
    data_dicts = []
    months = {'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06', 'июля': '07', 'августа': '08',
              'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12', 'января': '01', 'февраля': '02'}

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

#            info_dict['phone'] = item_text.select('.item-popup-content')

            image_tags = item_text.select('.gallery-img-frame')
            image_links = ''
            for image_tag in image_tags:
                image_links += image_tag['data-url'] + ','
            info_dict['photo_link'] = image_links
            data_dicts.append(info_dict)
            print(info_dict)
#Записываем данные из словарей в бд, через модель django
            good = Goods(avito_ad_number=info_dict['id'])
            good.save()
            good = Goods(avito_date_publication=info_dict['avito_date_publication'])
            good.save()
            good = Goods(avito_time_publication=info_dict['avito_time_publication'])
            good.save()
            good = Goods(price=info_dict['price'])
            good.save()
            good = Goods(adress=info_dict['adress'])
            good.save()
            good = Goods(ad_text=info_dict['ad_text'])
            good.save()
            good = Goods(name=info_dict['name'])
            good.save()
            good = Goods(photo_link=info_dict['photo_link'])
            good.save()
            time.sleep(0.5)
        except:
            continue
    return data_dicts


if __name__ == "__main__":
    parser()