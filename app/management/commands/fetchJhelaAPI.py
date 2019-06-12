from django.core.management.base import BaseCommand, CommandError
from app.views import *

class Command(BaseCommand):
    args = 'request'
    help = 'Test B2C'

    def handle(self, *args, **options):    		  
        fetchJhelaAPI()  



