from suds.client import Client
import suds
import urllib2
import datetime

# Credentials
username = 'cX26K2W836QT8Up'
password = 'D57Jc8SdsSJ1gAE'
timeout = 200

#location = "http://ws.crbws.transunion.ke.co"
location = "https://secure3.transunionafrica.com/crbws/ke"
#location = "https://secure3.crbafrica.com:443/crbws/ke"
url = "https://secure3.transunionafrica.com/crbws/ke?wsdl"

t = suds.transport.https.HttpAuthenticated(username=username, password=password)

t.handler = urllib2.HTTPBasicAuthHandler(t.pm)
t.urlopener = urllib2.build_opener(t.handler)

client = suds.client.Client(url=url, location=location, timeout=timeout, transport=t)

username = "WS_JML1"
password = "nQtwbd"
code = "2182"
infinityCode = "1328KE46406"


list_of_methods = [method for method in client.wsdl.services[0].ports[0].methods] 

print list_of_methods[23]

#print client.service

name1 = 'Maraba'
name2 = 'Vincent Kiprop'
name3 = '' 
name4 = '' 
nationalID = '24917521'
passportNo = ''
serviceID = ''
alienID = '' 
taxID = ''
today = datetime.datetime.now()
postalBoxNo = '' 
postalTown = ''
postalCountry = '' 
reportSector = 1/2
reportReason = 1


 
product102 = client.service.getProduct102(username=username,password=password,code=code,infinityCode=infinityCode,nationalID=nationalID,reportReason=reportReason,reportSector=reportSector)

#product102 = client.service.getProduct102(username,password,code,infinityCode,nationalID,serviceID,reportSector,reportReason)

#reportSector=reportSector,
print product102
##print product102.responseCode
##print product102.header

header = product102.header
personalProfile =  product102.personalProfile

#print header
#print personalProfile

print 'header'
print header['crbName']
print header['productDisplayName']
print header['reportDate']
print header['reportType']
print header['requestNo']
print header['requester']

print 'personalProfile'
#print personalProfile['alienID']
print personalProfile['crn']
print personalProfile['dateOfBirth']
#print personalProfile['drivingLicenseNo']
print personalProfile['fullName']
print personalProfile['gender']
print personalProfile['nationalID']
print personalProfile['nationality']
print personalProfile['otherNames']
#print personalProfile['passportNo']
print personalProfile['salutation']
#print personalProfile['serviceID']
print personalProfile['surname']


#print client


