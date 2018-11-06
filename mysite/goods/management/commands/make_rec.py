from django.core.management.base import BaseCommand, CommandError
import re
from django.db import models
from goods.models import Goods
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class Command(BaseCommand):
    help = 'Uses Tfidf, cosine_similarity to make recommendation'



    def handle(self, *args, **options):


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

        all_goods_id_list = list(Goods.objects.values_list('avito_ad_number', flat=True).distinct())

        for good_avito_id in all_goods_id_list:
            num = 0
            for number, goods in enumerate(all_goods):
                if goods.avito_ad_number == good_avito_id:
                    numb = number
                    break

            # Векторизация текста с помощью sklearn
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform(dataset)

            result = cosine_similarity(tfidf_matrix, tfidf_matrix)
            all_cosine = list(enumerate(result[numb], 1))
            all_cosine_number_sorted = sorted(all_cosine,key=lambda all_cosine: all_cosine[1])
            five_cosine_number_sorted = all_cosine_number_sorted[-6:-1]
            nearest_avito_ad_numbers = []
            for i in five_cosine_number_sorted:
                [nearest_avito_ad_numbers.append(value.avito_ad_number) for num, value in enumerate(all_goods) if num == i[0]]

            print(str(nearest_avito_ad_numbers))
            good_rec = Goods.objects.get(avito_ad_number=good_avito_id)
            good_rec.recommendation_list = str(nearest_avito_ad_numbers)
            good_rec.recommendation_list = re.sub("^.|.$", '', good_rec.recommendation_list)
            good_rec.save()
            
            
    

            
