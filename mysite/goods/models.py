from django.db import models

# Create your models here.

class Goods(models.Model):
	name = models.CharField(max_length=250)
	avito_ad_number = models.IntegerField()
	publication_date = models.DateField()
	publication_time = models.TimeField()
	photo_link = models.CharField(max_length=250)
	adress = models.CharField(max_length=250)
	price = models.CharField(max_length=250)
	text = models.TextField()
