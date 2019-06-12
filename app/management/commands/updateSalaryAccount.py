from django.core.management.base import BaseCommand, CommandError
from app.views import *

class Command(BaseCommand):
    args = 'request'
    help = 'updateSalaryAccount'
    print 'starting updateSalaryAccount'	

    def handle(self, *args, **options):    		  
      updateSalaryAccount()  



