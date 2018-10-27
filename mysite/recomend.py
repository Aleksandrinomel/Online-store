import re
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
import django
django.setup()
from django.db import models
from goods.models import Goods
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# сбор всех описаний наших объявлений

all_goods = Goods.objects.all()
avito_id = 1193530238

dataset = []

for good in all_goods:
    good_text = good.text
    good_text = re.sub("^\s+|\n|\r|\s+$", '', good_text)
    dataset.append(good_text)

for number, goods in enumerate(all_goods):
	if goods.avito_ad_number == avito_id:
		print(number)


# Векторизация текста с помощью sklearn
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(dataset)

result = cosine_similarity(tfidf_matrix, tfidf_matrix)




all_cosine = list(enumerate(result[number], 1))

all_cosine_number_sorted = sorted(all_cosine,key=lambda all_cosine: all_cosine[1])

five_cosine_number_sorted = all_cosine_number_sorted[-6:-1]
nearest_avito_ad_number = []
for i in five_cosine_number_sorted:
	[nearest_avito_ad_number.append(value.avito_ad_number) for num, value in enumerate(all_goods) if num == i[0]]


print(nearest_avito_ad_number)




