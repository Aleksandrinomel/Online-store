from django.shortcuts import render
from django.http import HttpResponse
from goods.models import Goods
from recomend import get_recomendation


def product_category(request, product_category):
    goods = Goods.objects.filter(category=product_category)
    return render(request, 'goods/category2.html', {'goods': goods, 'product_category': product_category})


def item(request, product_category, good_id):
    good = Goods.objects.get(category=product_category, avito_ad_number=good_id)
    photo_links = Goods.objects.get(avito_ad_number=good_id).photo_link
    photo_links = photo_links.split(',')
    rec_list = Goods.objects.get(avito_ad_number=good_id).recommendation_list.split(', ')
    rec_goods = Goods.objects.filter(avito_ad_number__in=rec_list)
    return render(request, 'goods/item.html', {'good': good, 'photo_links': photo_links, 'rec_list': rec_list, 
    	                                       'rec_goods': rec_goods, 'product_category': product_category})

