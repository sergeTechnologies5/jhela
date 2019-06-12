from django.core.management.base import BaseCommand, CommandError
from app.views import *

class Command(BaseCommand):
    args = 'request'
    help = 'registerGroups'
    print 'starting registerGroups'	

    def handle(self, *args, **options):    		  
       registerGroups()  



