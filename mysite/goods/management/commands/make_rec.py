from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Uses Tfidf, cosine_similarity to make recommendation'


    def handle(self, *args, **options):
    	print('ok')