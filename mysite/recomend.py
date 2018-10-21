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

for good in all_goods:
    try:
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
result = cosine_similarity(tfidf_matrix, tfidf_matrix)
print(result)
print(result.shape)
sorted_result = np.sort(result)
indices = [-6, -5, -4, -3, -2]
nearest_five = np.take(sorted_result, indices)
print(nearest_five.shape)


max_index = np.argpartition(result, -7)[-2:-1]
print(max_index)

#for ii in range(len(nearest_five_list) + 1):
#print(nearest_five_list[0])
    #[i for i,x in enumerate(result_list) if x==nearest_five_list[ii]]
    #index_list.append(i)

#print(index_list)
