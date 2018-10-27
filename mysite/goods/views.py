from django.shortcuts import render
from django.http import HttpResponse
from .models import Goods


def product_category(request, product_category):
    goods = Goods.objects.filter(category=product_category)
    return render(request, 'goods/category.html', {'goods': goods})


def item(request, product_category, good_id):
    good = Goods.objects.get(category=product_category, avito_ad_number=good_id)
    photo_links = Goods.objects.get(avito_ad_number=good_id).photo_link
    photo_links = photo_links.split(',')
    return render(request, 'goods/item.html', {'good': good, 'photo_links': photo_links})

