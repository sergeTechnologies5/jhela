from django.core.management.base import BaseCommand, CommandError
from app.views import *

class Command(BaseCommand):
    args = 'request'
    help = 'addSignatories2Groups'
    print 'starting addSignatories'	

    def handle(self, *args, **options):    		  
       addSignatories()  
       print 'end of ... addSignatories' 	



