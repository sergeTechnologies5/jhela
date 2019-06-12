from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from app.views import *
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    #url(r'^$','app.views.getCounties'),    
    url(r'^checkCRB/$','app.views.checkCRB'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/add/customer/$','app.views.addCustomerAPI'), 
    url(r'^api/add/client/$','app.views.addClientAPI'),
    url(r'^api/add/junior/client/$','app.views.addJuniorClientAPI'),
    url(r'^api/change/phone/$','app.views.changePhone'),
    url(r'^api/add/groupclient/$','app.views.addGroupClientAPI'),
    url(r'^api/add/groupclientTest/$','app.views.addGroupClientAPI5'),    
    url(r'^api/add/corporateclient/$','app.views.addCorporateClientAPI'),
    url(r'^api/add/corporateclient2/$','app.views.addCorporateClientAPI2'),
    url(r'^count/by/registrar/$','app.views.countByRegistrar'),
    url(r'^count/by/workstation/$','app.views.countByWorkStationName'),    
    #J-Hela App APIs
    url(r'^api/get/counties/$','app.views.getCounties'),  
    url(r'^api/get/subcounties/$','app.views.getChildren'),
    url(r'^api/get/wards/$','app.views.getChildren'),
    url(r'^api/get/clusters/$','app.views.getWorkStation'),
    #J-Hela App APIs with All something...
    url(r'^api/get/withall/counties/$','app.views.getWithAllCounties'),  
    url(r'^api/get/withall/subcounties/$','app.views.getWithAllSubCounties'),
    url(r'^api/get/withall/wards/$','app.views.getWithAllWards'),
    url(r'^api/get/withall/clusters/$','app.views.getWithAllClusters'),
    url(r'^api/send/sms/$','app.views.sendSMSAPI'),
    #J-Hela Reports APIs
    url(r'^api/get/daily/members/$','app.views.getDailyMembers'),
    url(r'^api/get/all/members/$','app.views.getAllMembers'),
    url(r'^api/get/all/JSokoRecords/$','app.views.getJSokoRecords'),
    url(r'^api/get/all/JSokoRecords2/$','app.views.getJSokoRecords2'),
    url(r'^testConfirmID/$','app.views.testConfirmID'),   
    url('^sendMail/$','app.views.sendMail'),
    url('^checkCreditWorthiness/$','app.views.checkCreditWorthiness'), 
    url(r'^api/pay/group/$','app.views.payGroup'),  
    url(r'^addSignatories2Groups/$','app.views.addSignatories2Groups'),
    url(r'^addGroupClientAPITester/$','app.views.addGroupClientAPITester'),    
)
