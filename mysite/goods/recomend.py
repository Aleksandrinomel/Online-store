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
from goods.models import Recomend



# сбор всех описаний наших объявлений
def get_recomendation(avito_id):
    all_goods = Goods.objects.all()


    dataset = []

    for good in all_goods:
        try:
            good_text = good.text
            good_text = re.sub("^\s+|\n|\r|\s+$", '', good_text)
            dataset.append(good_text)
        except BaseException as e:
            print(e)
            continue
    num = 0
    for number, goods in enumerate(all_goods):
        if goods.avito_ad_number == avito_id:
            num = number
            break

            

    #print(dataset)
    # Векторизация текста с помощью sklearn
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(dataset)

    result = cosine_similarity(tfidf_matrix, tfidf_matrix)




    all_cosine = list(enumerate(result[num], 1))

    all_cosine_number_sorted = sorted(all_cosine,key=lambda all_cosine: all_cosine[1])

    five_cosine_number_sorted = all_cosine_number_sorted[-6:-1]
    nearest_avito_ad_numbers = []
    for i in five_cosine_number_sorted:
        [nearest_avito_ad_numbers.append(value.avito_ad_number) for num, value in enumerate(all_goods) if num == i[0]]

    recomend = Recomend(avito_ad_number=avito_id, five_nearest=nearest_avito_ad_numbers)
    recomend.save()
    return nearest_avito_ad_numbers


get_recomendation(483225)

