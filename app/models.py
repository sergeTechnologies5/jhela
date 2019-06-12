from django.db import models
from django.contrib import admin, messages
from django.db.models.fields import IntegerField
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _ 
from django import forms
import datetime
from django.forms.widgets import *

class APILog(models.Model):
    activity = models.TextField(null=True)
    syncd = models.BooleanField(default=False)
    date = models.DateTimeField(_('Date Updated'),auto_now=True)

    def __unicode__(self):
        return self.activity
 
class APILogAdmin(admin.ModelAdmin):
	list_display = ("activity","syncd","date")	 
	search_fields = ['activity']

class Counties(models.Model):
    AdministrativeUnitCode = models.CharField(max_length=50,blank=True,null=True)
    ParentCode = models.CharField(max_length=50,blank=True,null=True)
    AdministrativeUnitName = models.CharField(max_length=50,blank=True,null=True)
    OrderOfEntry = models.CharField(max_length=50,blank=True,null=True)

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50,blank=True)    
    last_name = models.CharField(max_length=50,blank=True)    
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateTimeField(_('DOB'),null=True) 
    email = models.EmailField(max_length=70,blank=True)
    address = models.CharField(max_length=50,blank=True)
    national_id = models.CharField(max_length=50,blank=True)
    acc_number = models.CharField(max_length=50) 
    pin = models.IntegerField(default=2222)
    profession = models.CharField(max_length=50,blank=True)
    cluster = models.CharField(max_length=50,blank=True) 
    center = models.CharField(max_length=50,blank=True) 
    town = models.CharField(max_length=50,blank=True)
    county = models.CharField(max_length=50,blank=True)    
    country = models.CharField(default="Kenya",max_length=50,blank=True)         		    
    active = models.BooleanField(default=True)
    bal_amount = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)
    date_added = models.DateTimeField(_('Date Added'),blank=False)  
    date = models.DateTimeField(_('Date Updated'),auto_now=True)
        
    def to_dict(self):	
        return  {"phone_number":self.phone_number,"first_name":self.first_name,
        "second_name":self.second_name,"pin":self.pin,'sacco':self.sacco.sacco_name}
    
    def __unicode__(self):
    	return self.first_name + ' ' + self.second_name
        
#class to provide neat administration for Customer model
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','first_name', 'second_name','phone_number',
    'acc_number','active','national_id','cluster','pin','date')
    search_fields = ['phone_number']
