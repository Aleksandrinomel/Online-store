# -*- coding: utf-8 -*-
import csv
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
#good = Goods.objects.get(avito_ad_number=1064138442)
#good.deletion_date = datetime.today()
#good.save()
photo_links = Goods.objects.get(avito_ad_number="483225").photo_link
photo_links = photo_links.split(',')
print(photo_links)
#print(photo_links2)


#print(good.deletion_date)