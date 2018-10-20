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
dataset = []

for i in range(1, len(all_goods) + 1):
    try:
        good = Goods.objects.get(id=i)
        good_text = good.text
        good_text = re.sub("^\s+|\n|\r|\s+$", '', good_text)

    except BaseException as er:
        print(er)
        continue  

    dataset.append(good_text)

#print(dataset)

# Векторизация текста с помощью sklearn
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(dataset)
print(tfidf_matrix.shape)
result = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
print(result)
sorted_result = np.sort(result)
indices = [-5, -4, -3, -2, -1]
nearest_five = np.take(sorted_result, indices)
print(nearest_five.shape)

nearest_five_list = list(nearest_five)
print(nearest_five_list)
result_list = list(result)
index_list = []
for ii in range(len(nearest_five_list) + 1):
    [i for i,x in enumerate(result_list) if x==nearest_five_list[ii]]
    index_list.append(i)

print(index_list)
