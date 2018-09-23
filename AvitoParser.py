import re

from bs4 import BeautifulSoup
import requests

avito_html = requests.get('https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/videokarty')
text = BeautifulSoup(avito_html.text, "html.parser")
pages = text.select('.pagination-page')
for page in pages:
    if page.getText() == 'Последняя':
        m = re.search('(p=)\w+', page.get('href'))
        total_pages = int(m.group(0)[2:])

links = []
l = 0
for number_page in range(1, total_pages + 1):
    link = 'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/videokarty?p=' + str(number_page)
    avito_html = requests.get(link)
    text = BeautifulSoup(avito_html.text, "html.parser")
    items = text.select('.item-description-title-link')
    for i in items:
        href = 'https://www.avito.ru' + i.get('href')
        links.append(href)
        l += 1
