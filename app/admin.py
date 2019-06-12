''' 
VK Maraba
July 2016
@ Copyright -  vincentmaraba@gmail.com
Admin file to determine what features will be available for the admin backend interface
''' 

from django.contrib import admin
from models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


admin.site.register(APILog, APILogAdmin)
admin.site.register(Customer, CustomerAdmin)
