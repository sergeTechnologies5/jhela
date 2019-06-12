from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import datetime,time,MySQLdb
from models import *
import time, StringIO
import json, pycurl
import MySQLdb
import collections
import urllib, os
import django
from django.conf import settings
from datetime import timedelta
from django.core.mail import send_mail
import suds
from suds.client import Client
import urllib2
import datetime
import time
# credentials

username = 'cX26K2W836QT8Up'
password = 'D57Jc8SdsSJ1gAE'
timeout = 200
#location = "http://ws.crbws.transunion.ke.co"
location = 'https://secure3.transunionafrica.com/crbws/ke'
#location = "https://secure3.crbafrica.com:443/crbws/ke"
crb_url = 'https://secure3.transunionafrica.com/crbws/ke?wsdl'
try:
	t = suds.transport.https.HttpAuthenticated(username=username, password=password)
	t.handler = urllib2.HTTPBasicAuthHandler(t.pm)
	t.urlopener = urllib2.build_opener(t.handler)
	client = suds.client.Client(url=crb_url, location=location, timeout=timeout, transport=t)
	username = "WS_JML1"
	password = "Mptvzb"
	code = "2182"
	infinityCode = "1328KE46406"
	list_of_methods = [method for method in client.wsdl.services[0].ports[0].methods] 
	#print list_of_methods[23]
	#print client.service
except:
	pass

@csrf_exempt		
def addCustomerAPI(request):
	mimetype = 'application/javascript'
	##get IP of the sending phone
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	ip =''
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
	  ip = request.META.get('REMOTE_ADDR')

	if request.method == 'POST':
		data = request.body		
	else:
		data = request.body

	#log data
	log = APILog()
	log.activity = str(data)
	log.save()	

	post_request = json.loads(data)	
	print post_request
	fname = post_request['fname']
	sname = post_request['sname']
	lname = post_request['lname']
	phone = post_request['phone']
	dob = post_request['dob']
	national = post_request['national']
	cluster = post_request['cluster']
	ward = post_request['ward']
	county = post_request['county']
	username = post_request['username']
	password = post_request['password']

	print fname
	print sname
	print lname
	print phone
	print dob
	print national
	print cluster
	print ward
	print county
	print username
	print password
	print 'authentication'
	#checkuser = authenticate(username=username, password=username)
	print checkuser

	reply = json.dumps({'result':'Success'})
	return HttpResponse(reply,mimetype)	

@csrf_exempt		
def payGroup(request):
	import re
	mimetype = 'application/javascript'
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	ip =''
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
	  ip = request.META.get('REMOTE_ADDR')
	if request.method == 'POST':
		data = request.POST		
	else:
		data = request.GET
	print 'data'
	print data
	dict_string = request.body
	print dict_string
	q =  django.http.QueryDict(dict_string)
	print q
	json_object = q.dict()
	print json_object
	pin = ''
	phone_number = ''
	for key in json_object:
		if key == 'pin':
			print json_object[key]
			pin = json_object[key]
		elif key == 'phone':
			print json_object[key]
			phone_number = json_object[key]
			phone_number = phone_number.replace("+", "")
			phone_number = phone_number.replace("(", "")
			phone_number = phone_number.replace(")", "")
			phone_number = phone_number.replace("-", "")
			phone_number = re.sub(r'\s+', '', phone_number)
			if len(phone_number) == 10:
				phone_number = '254'+phone_number[1:]
				amount = json_object[key]
			elif len(phone_number) == 12:
				amount = json_object[key]				
			else:
				pass
	for key in json_object:
		print "key: %s , value: %s" % (key, json_object[key])		
		orig_key = key
		key = key.replace("+", "")
		key = key.replace("(", "")
		key = key.replace(")", "")
		key = key.replace("-", "")
		phone = re.sub(r'\s+', '', key) 
		isPhone=True
		phone = phone.strip()	
		if phone[:2] == '07':
			phone = '254' + phone[1:]	
		elif len(phone) == 10:
			phone = '254'+phone[1:]
			amount = json_object[orig_key]
		elif len(phone) == 12:
			print phone[:3]
			amount = json_object[orig_key]
		else:
			isPhone=False
			print 'invalid phone number'
		if isPhone:
			data = {"phone":phone_number,"pin":pin,"recipient":phone,"amount":amount,"username":"jhelaapi","password":"jhelaapi"}
			postfields = urllib.urlencode(data)
			print 'final data sent'
			print data
			try:
				url = 'http://197.248.124.58/api/pay/group/'				
				c = pycurl.Curl()
				c.setopt(pycurl.URL, url)
				c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
				c.setopt(pycurl.POST, 1)
				c.setopt(pycurl.POSTFIELDS, postfields)
				b = StringIO.StringIO();
				c.setopt(pycurl.WRITEFUNCTION, b.write)
				c.perform()
				ncServerData = b.getvalue()
				ncServerData = json.loads(ncServerData)
				print ncServerData
				print 'ncServerData ncServerData'
			except:
				pass
	try:
		log = APILog()
		log.activity = str(data)
		log.save()
	except:
		pass
	reply = json.dumps({'result':'Success'})			
	return HttpResponse(reply,mimetype)

import requests	as RQ
def fetchJhelaAPI():
	print 'Starting fetchJhelaAPI >> '
	while True:
		#time.sleep(15)
		mylist = []
		mimetype = 'application/javascript'	
		q=True
		endpoint = 'http://pesaplus.co.ke/api/jHelaApiRequests/pending/?username=jhelaRequestsAPI&password=jhelaRequestsAPI'
		r = RQ.get(endpoint)
		post_request = r.text
		#post_request = crypt.decryptStringENC(post_request)
		post_request = json.loads(post_request)			
		post_request = post_request['Data']	
		if len(str(post_request)) > 5:
			print post_request
		reply = json.dumps({'result':'Success'})

		for i in post_request:
			#try:
			if q:
				phone_number = i['phone_number'] #group number requesting
				p1 = str(i['p1']) #number to be replaced
				p2 = i['p2'] # number to replace with
				code = i['code']  #authorization code
				myid = i['id'] 
				print myid
				request_type = str(i['request_type'])			
				if request_type == '1024':
					print 'replace signatory for >'
					print phone_number
					#get SalaryAccount
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					idsql = "select SalaryAccount,MemId from MembersMasterFile where CellPhone='"+phone_number+"';"
					idresult = cursor.execute(idsql)
					db.commit()
					db.close()
					objects_list = []
					rows = cursor.fetchall()
					for row in rows:
						account_no = row[0]
						mem_id = row[1]

					#get MembersAccountsSignatories
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					idsql = "select CellPhone,MandateExpiriryDate,MemberNames from MembersAccountsSignatories where AccountNo='"+account_no+"';"
					idresult = cursor.execute(idsql)
					db.commit()
					db.close()

					print account_no

					# send SMS
					objects_list = []
					rows = cursor.fetchall()
					for row in rows:
						phone = row[0]
						expiry = row[1]
						name = row[2]
						print phone
						#send message to customer
						ujumbe = 'Jambo '+ str(name.upper()) +', You are requested to approve a change of signatory where member '+ p1+' is to replace '+p2+'. To confirm or reject this request, dial *833# and go to Banking, Group Activities and then select Signatories. Enter the code '+code+' to complete your request. Thank you'
						to = urllib.urlencode({'DESTADDR':phone,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
						url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
						urllib2.urlopen(url)
						print ujumbe

						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						sql = "INSERT INTO ChangeSignatories (MasterFileId,Signatory,Verdict,Code,OldNumber,NewNumber,AccountNo) VALUES ('"+str(mem_id)+"','"+str(phone)+"','Pending','"+str(code)+"','"+str(p1)+"','"+str(p2)+"','"+account_no+"');"
						print sql
						result = cursor.execute(sql)
						db.commit()	
						db.close()

					print 'done'
					# add code to ChangeSignatories
				#1025  - Approve Replace Signatory
				if request_type == '1025':
					#get MembersAccountsSignatories
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					idsql = "select CellPhone,MandateExpiriryDate,MemberNames from MembersAccountsSignatories where CellPhone='"+str(phone_number)+"';"
					idresult = cursor.execute(idsql)
					db.commit()
					db.close()
					# send SMS
					objects_list = []
					rows = cursor.fetchall()
					for row in rows:
						phone = row[0]
						expiry = row[1]
						name = row[2]

					print 'replace signatory for ><<<<<<<<<'
					print phone_number
					#get Signatory status
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					idsql = "SELECT OldNumber, NewNumber,AccountNo from ChangeSignatories where Verdict='Pending' AND Signatory='"+str(phone_number)+"' AND Code='"+str(p1)+"';"
					idresult = cursor.execute(idsql)
					print 'SELECT * from ChangeSignatories  '
					print idsql
					db.commit()
					db.close()
					rows = cursor.fetchall()
					if idresult:
						old_number = ''
						new_number = ''
						AccountNo = ''
						#print rows
						for row in rows:
							old_number = row[0]
							new_number = row[1]
							AccountNo = row[2]
						print 'NewNumber'
						print new_number	
						print 'OldNumber'
						print old_number
						print 'AccountNo >>'
						print AccountNo
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						sql = "UPDATE ChangeSignatories SET Verdict='Approved' where Verdict='Pending' AND Signatory='"+str(phone)+"' AND Code='"+str(p1)+"';"
						result = cursor.execute(sql)
						db.commit()	
						db.close()
						#send message to customer
						ujumbe = 'Jambo '+ str(name.upper()) +', Your approval for a change of signatory has been received. Thank you'
						#check if any signatory feedback is pending
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						idsql = "SELECT * from ChangeSignatories where Verdict='Pending' AND Code='"+str(p1)+"';"
						signresult = cursor.execute(idsql)
						db.commit()
						db.close()
						if signresult:
							#send message to customer
							ujumbe = 'Jambo '+ str(name.upper()) +', Your approval for a change of signatory has been received and is waiting feedback from other signatories. Thank you'
						else:
							print 'yes, change the signatories'	
							print 'NewNumber'
							print new_number	
							print 'OldNumber'
							print old_number							
							db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
							cursor = db.cursor()
							sql = "UPDATE MembersAccountsSignatories SET CellPhone='"+ str(new_number) +"' where CellPhone='"+ str(old_number) +"' AND AccountNo='"+str(AccountNo)+"';"
							result = cursor.execute(sql)
							print sql
							db.commit()	
							db.close()
							ujumbe = 'Jambo '+ str(name.upper()) +', Your approval for a change of signatory for account '+str(AccountNo)+', from '+ str(old_number) +' to '+ str(new_number) +' has been effected successfully. Thank you'
					else:
						#send message to customer
						ujumbe = 'Jambo '+ str(name.upper()) +', Your approval feedback has not been effected as there is no pending request for action. Thank you'
					
					print ujumbe
					to = urllib.urlencode({'DESTADDR':phone,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)
					print ujumbe
					
				#1026  - Reject Replace Signatory
				if request_type == '1026':
					#get MembersAccountsSignatories
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					idsql = "select CellPhone,MandateExpiriryDate,MemberNames from MembersAccountsSignatories where CellPhone='"+str(phone)+"';"
					idresult = cursor.execute(idsql)
					db.commit()
					db.close()
					# send SMS
					objects_list = []
					rows = cursor.fetchall()
					for row in rows:
						phone = row[0]
						expiry = row[1]
						name = row[2]
					#get Signatory status
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					idsql = "SELECT OldNumber, NewNumber,AccountNo from ChangeSignatories where Verdict='Pending' AND Signatory='"+str(phone)+"' AND Code='"+str(p1)+"';"
					idresult = cursor.execute(idsql)
					db.commit()
					db.close()
					if idresult:
						OldNumber = ''
						NewNumber = ''
						AccountNo = ''
						for row in rows:
							OldNumber = row[0]
							NewNumber = row[1]
							AccountNo = row[2]
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						sql = "UPDATE ChangeSignatories SET Verdict='Failed' where Code='"+str(p1)+"' AND  AccountNo='"+str(AccountNo)+"';"
						result = cursor.execute(sql)
						db.commit()	
						db.close()
						ujumbe = 'Jambo '+ str(name.upper()) +', Your rejection for a change of signatory for account '+str(AccountNo)+', from '+ str(OldNumber) +' to '+ str(NewNumber) +' has been effected successfully. Thank you'
					else:
						#send message to customer
						ujumbe = 'Jambo '+ str(name.upper()) +', Your rejection for a change of signatory for account '+str(AccountNo)+', from '+ str(OldNumber) +' to '+ str(NewNumber) +' has NOT been effected as a pending request could not be found. Thank you'
					
					to = urllib.urlencode({'DESTADDR':phone,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)
					print ujumbe

				# Add member to group - 1027
				if request_type == '1027':
					print phone_number
					#get SalaryAccount
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					idsql = "select SalaryAccount,MemId,FirstName,SalaryAccount from MembersMasterFile where CellPhone='"+phone_number+"';"
					idresult = cursor.execute(idsql)
					db.commit()
					db.close()
					objects_list = []
					rows = cursor.fetchall()
					for row in rows:
						account_no = row[0]
						mem_id = row[1]
						group_name = row[2]
						SalaryAccount = str(row[3])

					#check if new member is registered with JHELA
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					idsql = "select SalaryAccount,MemId,FirstName from MembersMasterFile where CellPhone='"+p1+"';"
					idresult = cursor.execute(idsql)
					db.commit()
					db.close()
					objects_list = []
					rows = cursor.fetchall()
					for row in rows:
						mem_name = row[2]

					#Get GroupNo
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "select GroupNo from MicroFinanceMasterFile where GroupAccount='"+SalaryAccount+"';"
					result = cursor.execute(sql)
					db.commit()	
					db.close()
					rows = cursor.fetchall()
					#print sql
					#print rows
					print 'group_no <<>>> group_no:-'
					for row in rows:
						group_no = row[0]						
						print group_no

					if not result:
						#Register in MicroFinanceMasterFile
						print 'Registering MicroFinance Group ....'
						#Get phone number
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						phonesql = 'Select MemId, FirstName, HomeAddress, WorkStationCode,SalaryAccount from MembersMasterFile where CellPhone='+phone_number+' LIMIT 1;'
						#print phonesql
						phoneresult = cursor.execute(phonesql)
						db.commit()
						db.close()

						rows = cursor.fetchall()
						for row in rows:
						    MemId = str(row[0])
						    first_name = str(row[1])	
						    address = str(row[2])	
						    workstation = str(row[3])	
						    SalaryAccount = str(row[4])

						print 'INSERT INTO MicroFinanceMasterFile'
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						sql = "INSERT INTO MicroFinanceMasterFile (GroupName,Address,WorkStationCode,GroupNo,GroupAccount) VALUES ('"+first_name+"','"+address+"','"+workstation+"','"+MemId+"','"+SalaryAccount+"');"
						print sql
						result = cursor.execute(sql)
						db.commit()	
						db.close()

						#Get GroupNo
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						sql = "select GroupNo from MicroFinanceMasterFile where GroupAccount='"+SalaryAccount+"';"
						result = cursor.execute(sql)
						db.commit()	
						db.close()
						rows = cursor.fetchall()
						print sql
						#print rows
						print 'group_no group_no group_no >> <<'
						for row in rows:
							group_no = row[0]							
							print group_no

						'''try:
							db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
							cursor = db.cursor()
							sql = "INSERT INTO MicroFinanceMasterFile (GroupName,Address,WorkStationCode,GroupNo,GroupAccount) VALUES ('"+first_name+"','"+address+"','"+workstation+"','"+MemId+"','"+phone_number+"');"
							print sql
							result = cursor.execute(sql)
							db.commit()	
							db.close()
						except:
							#workstation update
							print workstation update
							workstation = '0' + workstation
							db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
							cursor = db.cursor()
							sql = "INSERT INTO MicroFinanceMasterFile (GroupName,Address,WorkStationCode,GroupNo,GroupAccount) VALUES ('"+first_name+"','"+address+"','"+workstation+"','"+MemId+"','"+phone_number+"');"
							print sql
							result = cursor.execute(sql)
							db.commit()	
							db.close()
						'''

					if not idresult:
						#send message to group number
						ujumbe = 'Jambo '+ str(group_name.upper()) +', There is no J-Hela member registered with the number '+ p1+' Kindly check and try again. @J-Hela by Choice. Thank you'
						to = urllib.urlencode({'DESTADDR':phone_number,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
						url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
						urllib2.urlopen(url)
						#print ujumbe
					else:
						#Add member to group
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						sql = "UPDATE MembersMasterFile SET GroupNo='"+str(group_no)+"' WHERE CellPhone='"+str(p1)+"'";
						result = cursor.execute(sql)
						db.commit()	
						db.close()

						#get MembersAccountsSignatories
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						idsql = "select CellPhone,MandateExpiriryDate,MemberNames from MembersAccountsSignatories where AccountNo='"+str(account_no)+"';"
						idresult = cursor.execute(idsql)
						db.commit()
						db.close()

						# send SMS
						objects_list = []
						rows = cursor.fetchall()
						for row in rows:
							phone = row[0]
							expiry = row[1]
							name = row[2]
							print phone
							#send message to customer
							ujumbe = 'Jambo '+ str(name.upper()) +', A new member '+str(mem_name.upper())+ ' of phone number '+ str(p1)+' has been added to your J-Hela group '+str(group_name.upper())+' via the group number '+phone_number+'. The group is growing! @J-Hela by Choice. Thank you'
							to = urllib.urlencode({'DESTADDR':phone,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
							url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
							urllib2.urlopen(url)
							print ujumbe
						ujumbe = 'Jambo '+ str(group_name.upper()) +', A new member '+str(mem_name.upper())+ ' of phone number '+ str(p1)+' has been added to your J-Hela group '+str(group_name.upper())+' via the group number '+phone_number+'. The group is growing! @J-Hela by Choice. Thank you'	
						to = urllib.urlencode({'DESTADDR':phone_number,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
						url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
						urllib2.urlopen(url)
						'''db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						sql = "INSERT INTO ChangeSignatories (MasterFileId,Signatory,Verdict,Code,OldNumber,NewNumber,AccountNo) VALUES ('"+str(mem_id)+"','"+str(phone)+"','Pending','"+str(code)+"','"+str(p1)+"','"+str(p2)+"','"+account_no+"');"
						print sql
						result = cursor.execute(sql)
						db.commit()	
						db.close()'''
						print 'done'

				# Remove member from group - 1028
				if request_type == '1028':
					print phone_number
					#get SalaryAccount
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					idsql = "select SalaryAccount,MemId,FirstName from MembersMasterFile where CellPhone='"+phone_number+"';"
					idresult = cursor.execute(idsql)
					db.commit()
					db.close()
					objects_list = []
					rows = cursor.fetchall()
					for row in rows:
						account_no = row[0]
						mem_id = row[1]
						group_name = row[2]

					#check if member is registered with JHELA
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					idsql = "select SalaryAccount,MemId,FirstName from MembersMasterFile where CellPhone='"+p1+"';"
					idresult = cursor.execute(idsql)
					db.commit()
					db.close()
					objects_list = []
					rows = cursor.fetchall()
					for row in rows:
						mem_name = row[2]

					if not idresult:
						#send message to group number
						ujumbe = 'Jambo '+ str(group_name.upper()) +', There is no J-Hela member registered with the number '+ p1+' Kindly check and try again. @J-Hela by Choice. Thank you'
						to = urllib.urlencode({'DESTADDR':phone_number,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
						url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
						urllib2.urlopen(url)
						print ujumbe
					else:
						#Remove member from the group
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						sql = "UPDATE MembersMasterFile SET GroupNo='""' WHERE CellPhone='"+str(p1)+"'";
						result = cursor.execute(sql)
						db.commit()	
						db.close()

						#get MembersAccountsSignatories
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						idsql = "select CellPhone,MandateExpiriryDate,MemberNames from MembersAccountsSignatories where AccountNo='"+account_no+"';"
						idresult = cursor.execute(idsql)
						db.commit()
						db.close()

						# send SMS
						objects_list = []
						rows = cursor.fetchall()
						for row in rows:
							phone = row[0]
							expiry = row[1]
							name = row[2]
							print phone
							#send message to customer
							ujumbe = 'Jambo '+ str(name.upper()) +', A member '+str(mem_name.upper())+ ' of phone number '+ str(p1) +' has been removed from your J-Hela group '+str(group_name.upper())+', via the group number '+phone_number+'. @J-Hela by Choice. Thank you'
							to = urllib.urlencode({'DESTADDR':phone,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
							url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
							urllib2.urlopen(url)
							print ujumbe
						ujumbe = 'Jambo '+ str(group_name.upper()) +', A member '+str(mem_name.upper())+ ' of phone number '+ str(p1) +' has been removed from your J-Hela group '+str(group_name.upper())+', via the group number '+phone_number+'. @J-Hela by Choice. Thank you'
						to = urllib.urlencode({'DESTADDR':phone_number,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
						url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
						urllib2.urlopen(url)

					'''data = {"id":myid}
					postfields = urllib.urlencode(data)
					pesaplus_url = 'http://197.248.124.58:8090/api/jHelaApiRequests/feedback/'				
					c = pycurl.Curl()
					c.setopt(pycurl.URL, pesaplus_url)
					c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE',
						'Accept: application/json'])
					c.setopt(pycurl.POST, 1)
					c.setopt(pycurl.POSTFIELDS, postfields)
					b = StringIO.StringIO();
					c.setopt(pycurl.WRITEFUNCTION, b.write)
					c.perform()
					ncServerData = b.getvalue()'''
					#print ncServerData

					#ncServerData = b.getvalue()
					#ncServerData = json.loads(ncServerData)
					#print ncServerData

					#1025  - Approve Replace Signatory
					'''elif saccoid == '45' and request_type == '1025':	
						print '1025'
						parameter4 = i['parameter4']
						transactionRequest = JhelaRequest()
						transactionRequest.name=customer
						transactionRequest.p1=parameter4 #code sent
						transactionRequest.phone_number=phone_number
						transactionRequest.request_type='1025'
						transactionRequest.date_added= timezone.now()
						transactionRequest.save()
						msg2[phone_number] = 'Success'
					#1026  - Reject Replace Signatory
					elif saccoid == '45' and request_type == '1026':	
						print '1026'''
			reply = json.dumps({'result':200})
	return HttpResponse(reply)
					
#adding new JHELA clients
@csrf_exempt		
def addJuniorClientAPI(request):
	mimetype = 'application/javascript'
	##get IP of the sending phone
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	ip =''
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
	  ip = request.META.get('REMOTE_ADDR')

	#data =  {'first_name': 'Ruth','middle_name': 'Jelimo','guardian_first_name': 'vincent',
	#'dob': '06-11-2007','sex': 'Female','idnumber': '7279649','phone': '0712437161','guardian_fathers_name': 'Maraba',
	#'fathers_name': 'maraba','guardian_middle_name': 'kiprop','guardian_phone': '0722531106'}

	if request.method == 'POST':
		data = request.POST		
	else:
		data = request.GET

	try:
		log = APILog()
		log.activity = str(data[0])
		log.save()
	except:
		pass

	print data
	leo = datetime.datetime.now()
	print 'now is'
	print leo


	first_name = data['first_name']
	middle_name = data['middle_name']
	fathers_name = data['fathers_name']
	sex = data['sex']
	idnumber = data['idnumber']
	phone = data['phone']
	guardian_first_name = data['guardian_first_name']
	guardian_middle_name = data['guardian_middle_name']
	guardian_fathers_name = data['guardian_fathers_name']
	guardian_phone = data['guardian_phone']

	profession = ''
	income = 0
	#country = data['country']
	#county = data['county']
	subcounty = ''
	ward = '01'
	cluster = ''
	workstation = '01'
	try:
		subcounty = data['subcounty']
	except:
		pass	
	try:
		ward = data['ward']
	except:
		pass
	try:
		workstation = data['cluster']
	except:
		pass
	kin_names = guardian_first_name 
	#+ ' ' + guardian_middle_name + ' ' + guardian_fathers_name
	kin_idnumber = data['idnumber']
	kinphone = data['guardian_phone']
	relationship = 'Guardian'
	introducerphone = guardian_phone
	dob = data['dob']	
	try:
		dob = datetime.datetime.strptime(dob, '%d-%m-%Y').strftime('%Y-%m-%d')	
	except:
		pass

	#check missing fields
	missing = ''
	if first_name == '':
		missing = missing + ','+'first name'
	if (fathers_name == '' and middle_name):
		missing = missing + ','+'sur name'
	#if county == '':
	#	missing = missing + ','+'county'
	if cluster == '':
		missing = missing + ','+'cluster'
	if dob == '':
		missing = missing + ','+'date of birth'
	if introducerphone == '':
		missing = missing + ','+'introducer phone'
	if profession == '':
		missing = missing + ','+'profession'
	if kin_names == '':
		missing = missing + ','+'kin names'
	if sex == '':
		missing = missing + ','+'sex/gender'	
	if kin_names == '':
		missing = missing + ','+'id number'
	if phone == '':
		missing = missing + ','+'phone number'	
	if subcounty == '':
		missing = missing + ','+'subcounty'	
	if income == '':
		missing = missing + ','+'income'
	if ward == '':
		missing = missing + ','+'ward'	
	if kinphone == '':
		missing = missing + ','+'kin phone'	
	
	if missing != '':
		#u'income': [u'15000'], u'profession': [u'Farmer'],

		if len(phone) == 10:
			phone = '254'+phone[1:]
		if len(kinphone) == 10:
			kinphone = '254'+kinphone[1:]
		if len(introducerphone) == 10:
			introducerphone = '254'+introducerphone[1:]
		if len(guardian_phone) == 10:
			guardian_phone = '254'+guardian_phone[1:]
		
		title = '001'
		if sex == 'Male':
			title = '001'
			sex = 'MALE'
			gender = 'M'
		else:
			title = '002'
			sex = 'FEMALE'
			gender = 'F'
		day = datetime.datetime(1990, 1, 1)
		todaystr = str(day)
		todaystr = '1990-01-01'	
		a = True
		reply = json.dumps({'result':'Registration Failed. Try again later!.'})
		if a:
		#try:
			print middle_name
			print fathers_name
			othersnames = middle_name+' '+fathers_name
			apidata = json.dumps({"phone":phone,"iphone":introducerphone,"first_name":first_name,"fathers_name":othersnames,"idnumber":idnumber})
			url = 'http://197.248.124.58/receive/jhela/member/'
			#log = APILog()
			#log.activity = apidata
			#log.save()

			'''db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
			cursor = db.cursor()
			idsql = 'Select WorkStationCode,WorkStationName from WorkStations where WorkStationName='+workstation+';'
			workstationresult = cursor.execute(idsql)
			db.commit()
			db.close()
			rows = cursor.fetchall()
			for row in rows:
			    workstation = row[0]'''
			
			#Check ID number
			db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
			cursor = db.cursor()
			idsql = 'Select * from MembersMasterFile where IDNumber='+idnumber+' and CellPhone='+guardian_phone+';'
			idresult = cursor.execute(idsql)
			db.commit()
			db.close()

			#Check phone number
			db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
			cursor = db.cursor()
			phonesql = 'Select * from MembersMasterFile where CellPhone='+phone+';'
			phoneresult = cursor.execute(phonesql)
			db.commit()
			db.close()

			#Check introducer phone number
			db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
			cursor = db.cursor()
			introducersql = 'Select * from MembersMasterFile where CellPhone='+introducerphone+';'
			introducerresult = cursor.execute(introducersql)
			db.commit()
			db.close()

			f_name = middle_name +' '+ fathers_name
			data = {"phone":phone,"iphone":introducerphone,"first_name":first_name,"fathers_name":f_name,"idnumber":idnumber,"username":"jhelaapi","password":"jhelaapi"}
			postfields = urllib.urlencode(data)

			print idresult
			print 'idresult'
			print idnumber
			print guardian_phone
			print idsql		
			
			if not introducerresult:
				postfields = urllib.urlencode(data)
				print 'Introducer Phone number is not registered with JHela'
				reply = json.dumps({'result':'Introducer Phone number is not registered with JHela'})	
				#elif phoneresult:	
				#	reply = json.dumps({'result':'Junior\'s Phone number is already registered with JHela. Kindly check and try again'})		
			elif phoneresult:
				postfields = urllib.urlencode(data)
				print 'member is already registered in finextreme'
				#try:	
				print apidata			
				c = pycurl.Curl()
				c.setopt(pycurl.URL, url)
				c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
				c.setopt(pycurl.POST, 1)
				c.setopt(pycurl.POSTFIELDS, postfields)
				b = StringIO.StringIO();
				c.setopt(pycurl.WRITEFUNCTION, b.write)
				c.perform()
				ncServerData = b.getvalue()
				ncServerData = json.loads(ncServerData)
				print ncServerData
				print 'ncServerData ncServerData'
				#except:
				#	pass				
				reply = json.dumps({'result':'Phone number has already been registered'})
			elif len(phone) != 12 :
				print 'phone number has less characters'
				print phone
				reply = json.dumps({'result':'Failed. Phone number has less characters'})
			elif idresult:
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				phonesql = 'Select MemId,WorkStationCode,HomeAddress,PresentAddress from MembersMasterFile where CellPhone='+guardian_phone+' LIMIT 1;'
				#print phonesql
				phoneresult = cursor.execute(phonesql)
				db.commit()
				db.close()
				rows = cursor.fetchall()
				for row in rows:
				    MemId = str(row[0])
				    workstation = str(row[1])
				    ward = str(row[2])
				    subcounty = str(row[3])

				#else:						
				'''log = APILog()
				log.activity = data
				log.save()'''
				#idChecker = confirmID(fathers_name,first_name,middle_name,idnumber)
				idChecker='200'
				print 'No ID Checker huyu ni junior...'
				print idChecker				
				if idChecker == '200':
					#Register client
					print 'Registering client ....'
					print workstation
					if not subcounty:
						subcounty = 'Thika'					
					print subcounty
					if not profession:
						profession = 'Not indicated'
					print profession
					income = str(income)
					print income
					print workstation
					if not ward:
						ward = 'Kamenu'
					print ward


					if True:
					#try:	
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,DOB,Transacted,Profession,Income,AgeStatusCode) VALUES ('001','"+title+"','"+first_name+"','"+fathers_name+"','"+middle_name+"','"+phone+"','000','001','000','"+phone+"','"+sex+"','"+ward+"','"+subcounty+"','"+phone+"','"+phone+"','"+introducerphone+"','"+workstation+"',CURDATE(),CURDATE(),'system','002','New Member','000','"+dob+"','NO','"+profession+"','"+income+"',1);"
						new_member = 'New Member'
						no = 'NO'
						print 'avoiding SQL Injection'
						#sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,IDNumber,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,DOB,Transacted,Profession,income) VALUES ('001',%s,%s,%s,%s,%s,'000','001','000',%s,%s,%s,%s,%s,%s,%s,%s,%s,CURDATE(),CURDATE(),%s,'002',%s,'000',%s,%s,%s,%s);" % (title, first_name, fathers_name, middle_name, phone, phone,idnumber,sex, ward, subcounty, phone, phone,introducerphone,workstation,system,new_member,dob,no,profession,income)
						print sql
						result = cursor.execute(sql)
						db.commit()	
						db.close()	
						#try:							
						#except:
						#workstation update
						'''workstation = '0' + workstation
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,IDNumber,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,DOB,Transacted,Profession,Income,AgeStatusCode) VALUES ('001','"+title+"','"+first_name+"','"+fathers_name+"','"+middle_name+"','"+phone+"','000','001','000','"+phone+"','"+idnumber+"','"+sex+"','"+ward+"','"+subcounty+"','"+phone+"','"+phone+"','"+introducerphone+"','"+workstation+"',CURDATE(),CURDATE(),'system','002','New Member','000','"+dob+"','NO','"+profession+"','"+income+"',1);"
						new_member = 'New Member'
						no = 'NO'
						print 'avoiding SQL Injection'
						#sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,IDNumber,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,DOB,Transacted,Profession,income) VALUES ('001',%s,%s,%s,%s,%s,'000','001','000',%s,%s,%s,%s,%s,%s,%s,%s,%s,CURDATE(),CURDATE(),%s,'002',%s,'000',%s,%s,%s,%s);" % (title, first_name, fathers_name, middle_name, phone, phone,idnumber,sex, ward, subcounty, phone, phone,introducerphone,workstation,system,new_member,dob,no,profession,income)
						print sql
						result = cursor.execute(sql)
						db.commit()	
						db.close()'''	
						print 'db result'
						#print result

						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						phonesql = 'Select MemId from MembersMasterFile where CellPhone="'+phone+'";'
						print phonesql
						phoneresult = cursor.execute(phonesql)
						db.commit()
						db.close()
						rows = cursor.fetchall()
						for row in rows:
						    Junior_MemId = str(row[0])
						print 'MemId'
						print Junior_MemId
						print MemId
						print 'insert member guardian list'
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						sql = "INSERT INTO MemberGuardianList (MemId ,GuardialId) VALUES ('"+Junior_MemId+"','"+MemId+"');"
						result = cursor.execute(sql)
						db.commit()	
						db.close()

						try:
							print 'insert NextOfKins'						
							db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
							cursor = db.cursor()
							sql = "INSERT INTO NextOfKins (EmployerCode,PayrollNo,TitleCode,Names,Gender,IDNumber,PhoneNo,RelationCode,DateLastChanged) VALUES ('000','"+phone+"','"+title+"','"+kin_names+"','"+gender+"','"+kin_idnumber+"','"+kinphone+"','"+relationship+"',CURDATE());"
							print sql
							result = cursor.execute(sql)
							db.commit()	
							db.close()
							print 'done'
						except:
							pass

						'''NextOfKins 
						  `EmployerCode` varchar(20) NOT NULL,
						  `PayrollNo` varchar(20) NOT NULL,
						  `TitleCode` varchar(10) NOT NULL,
						  `Names` varchar(50) NOT NULL,
						  `Gender` enum('M','F') NOT NULL,
						  `IDNumber` varchar(20) DEFAULT NULL,
						  `PhoneNo` varchar(20) DEFAULT '',
						  `RelationCode` varchar(20) NOT NULL,
						  `DateLastChanged` date NOT NULL,'''

						print 'sending data to Pesaplus ....'
						print data
						try:
							postfields = urllib.urlencode(data)
							c = pycurl.Curl()
							c.setopt(pycurl.URL, url)
							c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
							c.setopt(pycurl.POST, 1)
							c.setopt(pycurl.POSTFIELDS, postfields)
							b = StringIO.StringIO();
							c.setopt(pycurl.WRITEFUNCTION, b.write)
							c.perform()
							ncServerData = b.getvalue()
							ncServerData = json.loads(ncServerData)
							print 'ncServerData ncServerData'
							print ncServerData
						except:
							pass	
						#logid = log.id
						#APILog.filter.objects(id=logid).update(syncd=True)					
						#except Exception, e:
						#result = ncServerData['result']
						#trx_id = ncServerData['trx_id']
						#raise e
						#print e	
						#pass
						reply = json.dumps({'result':'Registration Successful!.'})
					#except Exception, e:
						#raise e
					#	print e	
					#	pass		
					#	reply = json.dumps({'result':'Registration Failed. please try again later'})		
				elif idChecker == '300':
					print idChecker
					print 'Govt data feedback'
					reply = json.dumps({'result':'Your ID number and names do not match with government data. Please check again'})
					print "idChecker != '200':"
					print reply
				elif idChecker != '200':
					print idChecker
					print 'Govt data feedback'
					reply = json.dumps({'result':'Your ID number and names do not match with government data. Please check again'})
					print "idChecker != '200':"
					print reply
				else :
					print idChecker
					print 'Govt data feedback'
					reply = json.dumps({'result':'Your ID number and names do not match with government data. Please check again'})
					print "No suitable result"
					print reply

					'''
					elif phoneresult:
						postfields = urllib.urlencode(data)
						print 'member is already registered in finextreme'
						#try:	
						print apidata			
						c = pycurl.Curl()
						c.setopt(pycurl.URL, url)
						c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
						c.setopt(pycurl.POST, 1)
						c.setopt(pycurl.POSTFIELDS, postfields)
						b = StringIO.StringIO();
						c.setopt(pycurl.WRITEFUNCTION, b.write)
						c.perform()
						ncServerData = b.getvalue()
						ncServerData = json.loads(ncServerData)
						print ncServerData
						print 'ncServerData ncServerData'
						#except:
						#	pass				
						reply = json.dumps({'result':'Phone number has already been registered'})
					
						#check if transacted
						#Check ID number
						yes = 'YES'
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						trxsql = "Select * from MembersMasterFile where IDNumber="+idnumber+" AND Transacted='YES';"
						print trxsql
						trxresult = cursor.execute(trxsql)
						db.commit()
						db.close()
						if trxresult:
							reply = json.dumps({'result':'The member has transacted and thus records update is not possible'})
							print reply
						else:
							db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
							cursor = db.cursor()
							sql = "UPDATE MembersMasterFile SET PhoneNo='"+phone+"',CellPhone='"+phone+"',PayrollNo='"+phone+"', MemberNo='"+phone+"' WHERE IDNumber='"+idnumber+"' AND Transacted='NO'";
							result = cursor.execute(sql)
							db.commit()	
							db.close()
							print 'id result'
							print sql
							print result			
							#send to Pesaplus
							c = pycurl.Curl()
							c.setopt(pycurl.URL, url)
							c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
							c.setopt(pycurl.POST, 1)
							c.setopt(pycurl.POSTFIELDS, postfields)
							b = StringIO.StringIO();
							c.setopt(pycurl.WRITEFUNCTION, b.write)
							c.perform()
							ncServerData = b.getvalue()
							ncServerData = json.loads(ncServerData)
							print ncServerData
							reply = json.dumps({'result':'The member record has been updated successfully!'})
							print reply
					'''
		else:
			#except Exception, e:
			reply = json.dumps({'result':'Failed. Technical error encountered, try again after 5 minutes'})
			pass
			#raise e
	else:
		missing_fields = 'Failed. Fill these missing fields: '+ missing
		reply = json.dumps({'result':missing_fields})
	print 'Final reply..........!'
	print reply
	return HttpResponse(reply,mimetype)

#adding new JHELA clients
@csrf_exempt		
def addClientAPI(request):
	mimetype = 'application/javascript'
	##get IP of the sending phone
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	ip =''
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
	  ip = request.META.get('REMOTE_ADDR')

	if request.method == 'POST':
		data = request.POST		
	else:
		data = request.GET

	try:
		log = APILog()
		log.activity = str(data[0])
		log.save()
	except:
		pass

	print data
	leo = datetime.datetime.now()
	print 'now is'
	print leo

	first_name = data['first_name']
	middle_name = data['middle_name']
	fathers_name = data['fathers_name']
	sex = data['sex']
	idnumber = data['idnumber']
	phone = data['phone']
	profession = data['profession']
	income = data['income']
	#country = data['country']
	#county = data['county']
	subcounty = ''
	ward = '01'
	cluster = ''
	workstation = '01'
	try:
		subcounty = data['subcounty']
	except:
		pass	
	try:
		ward = data['ward']
	except:
		pass
	try:
		workstation = data['cluster']
	except:
		pass
	kin_names = data['kin_names']
	#kin_sex = data['kin_sex']
	kin_idnumber = data['kin_idnumber']
	kinphone = data['kinphone']
	relationship = data['relationship']
	introducerphone = data['introducerphone']
	dob = data['dob']	
	try:
		dob = datetime.datetime.strptime(dob, '%d-%m-%Y').strftime('%Y-%m-%d')	
	except:
		pass

	#check missing fields
	missing = ''
	if first_name == '':
		missing = missing + ','+'first name'
	if (fathers_name == '' and middle_name):
		missing = missing + ','+'sur name'
	#if county == '':
	#	missing = missing + ','+'county'
	if cluster == '':
		missing = missing + ','+'cluster'
	if dob == '':
		missing = missing + ','+'date of birth'
	if introducerphone == '':
		missing = missing + ','+'introducer phone'
	if profession == '':
		missing = missing + ','+'profession'
	if kin_names == '':
		missing = missing + ','+'kin names'
	if sex == '':
		missing = missing + ','+'sex/gender'	
	if kin_names == '':
		missing = missing + ','+'id number'
	if phone == '':
		missing = missing + ','+'phone number'	
	if subcounty == '':
		missing = missing + ','+'subcounty'	
	if income == '':
		missing = missing + ','+'income'
	if ward == '':
		missing = missing + ','+'ward'	
	if kinphone == '':
		missing = missing + ','+'kin phone'	
	
	if missing != '':
		#u'income': [u'15000'], u'profession': [u'Farmer'],

		if len(phone) == 10:
			phone = '254'+phone[1:]
		if len(kinphone) == 10:
			kinphone = '254'+kinphone[1:]
		if len(introducerphone) == 10:
			introducerphone = '254'+introducerphone[1:]
		title = '001'
		if sex == 'Male':
			title = '001'
			sex = 'MALE'
			gender = 'M'
		else:
			title = '002'
			sex = 'FEMALE'
			gender = 'F'
		day = datetime.datetime(1990, 1, 1)
		todaystr = str(day)
		todaystr = '1990-01-01'	
		a = True
		if a:
		#try:
			othersnames = middle_name+' '+fathers_name
			apidata = json.dumps({"phone":phone,"iphone":introducerphone,"idnumber":idnumber,"first_name":first_name,"fathers_name":othersnames,"idnumber":idnumber})
			url = 'http://197.248.124.58/receive/jhela/member/'
			#log = APILog()
			#log.activity = apidata
			#log.save()

			'''db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
			cursor = db.cursor()
			idsql = 'Select WorkStationCode,WorkStationName from WorkStations where WorkStationName='+workstation+';'
			workstationresult = cursor.execute(idsql)
			db.commit()
			db.close()
			rows = cursor.fetchall()
			for row in rows:
			    workstation = row[0]'''
			
			#Check ID number
			db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
			cursor = db.cursor()
			idsql = 'Select * from MembersMasterFile where IDNumber='+idnumber+';'
			idresult = cursor.execute(idsql)
			db.commit()
			db.close()

			#Check phone number
			db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
			cursor = db.cursor()
			phonesql = 'Select * from MembersMasterFile where CellPhone='+phone+';'
			phoneresult = cursor.execute(phonesql)
			db.commit()
			db.close()

			#Check introducer phone number
			db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
			cursor = db.cursor()
			introducersql = 'Select * from MembersMasterFile where CellPhone='+introducerphone+';'
			introducerresult = cursor.execute(introducersql)
			db.commit()
			db.close()

			f_name = fathers_name +' '+ middle_name
			data = {"phone":phone,"iphone":introducerphone,"idnumber":idnumber,"first_name":first_name,"fathers_name":f_name,"idnumber":idnumber,"username":"jhelaapi","password":"jhelaapi"}
			postfields = urllib.urlencode(data)
			
			if not introducerresult:
				postfields = urllib.urlencode(data)
				print 'Introducer Phone number is not registered with JHela'
				reply = json.dumps({'result':'Introducer Phone number is not registered with JHela'})
			elif phoneresult:
				postfields = urllib.urlencode(data)
				print 'member is already registered in finextreme'
				#try:	
				print apidata			
				c = pycurl.Curl()
				c.setopt(pycurl.URL, url)
				c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
				c.setopt(pycurl.POST, 1)
				c.setopt(pycurl.POSTFIELDS, postfields)
				b = StringIO.StringIO();
				c.setopt(pycurl.WRITEFUNCTION, b.write)
				c.perform()
				ncServerData = b.getvalue()
				ncServerData = json.loads(ncServerData)
				print ncServerData
				print 'ncServerData ncServerData'
				#except:
				#	pass				
				reply = json.dumps({'result':'Phone number has already been registered'})
			elif idresult:
				#check if transacted
				#Check ID number
				yes = 'YES'
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				trxsql = "Select * from MembersMasterFile where IDNumber="+idnumber+" AND Transacted='YES';"
				print trxsql
				trxresult = cursor.execute(trxsql)
				db.commit()
				db.close()
				if trxresult:
					reply = json.dumps({'result':'The member has transacted and thus records update is not possible'})
					print reply
				else:
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "UPDATE MembersMasterFile SET PhoneNo='"+phone+"',CellPhone='"+phone+"',PayrollNo='"+phone+"', MemberNo='"+phone+"' WHERE IDNumber='"+idnumber+"' AND Transacted='NO'";
					result = cursor.execute(sql)
					db.commit()	
					db.close()
					print 'id result'
					print sql
					print result			
					#send to Pesaplus
					c = pycurl.Curl()
					c.setopt(pycurl.URL, url)
					c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
					c.setopt(pycurl.POST, 1)
					c.setopt(pycurl.POSTFIELDS, postfields)
					b = StringIO.StringIO();
					c.setopt(pycurl.WRITEFUNCTION, b.write)
					c.perform()
					ncServerData = b.getvalue()
					ncServerData = json.loads(ncServerData)
					print ncServerData
					reply = json.dumps({'result':'The member record has been updated successfully!'})
					print reply
			elif len(phone) != 12 :
				print 'phone number has less characters'
				print phone
				reply = json.dumps({'result':'Failed. Phone number has less characters'})
			else:						
				'''log = APILog()
				log.activity = data
				log.save()'''
				idChecker = confirmID(fathers_name,first_name,middle_name,idnumber)
				#idChecker='200'
				print 'returned from ID Checker...'
				print idChecker				
				if idChecker == '200':
					try:				
						#Register client
						print 'Registering client ....'
						try:
							db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
							cursor = db.cursor()
							sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,IDNumber,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,DOB,Transacted,Profession,income) VALUES ('001','"+title+"','"+first_name+"','"+fathers_name+"','"+middle_name+"','"+phone+"','000','001','000','"+phone+"','"+idnumber+"','"+sex+"','"+ward+"','"+subcounty+"','"+phone+"','"+phone+"','"+introducerphone+"','"+workstation+"',CURDATE(),CURDATE(),'system','002','New Member','000','"+dob+"','NO','"+profession+"','"+income+"');"
							new_member = 'New Member'
							no = 'NO'
							print 'avoinding SQL Injection'
							#sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,IDNumber,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,DOB,Transacted,Profession,income) VALUES ('001',%s,%s,%s,%s,%s,'000','001','000',%s,%s,%s,%s,%s,%s,%s,%s,%s,CURDATE(),CURDATE(),%s,'002',%s,'000',%s,%s,%s,%s);" % (title, first_name, fathers_name, middle_name, phone, phone,idnumber,sex, ward, subcounty, phone, phone,introducerphone,workstation,system,new_member,dob,no,profession,income)
							print sql
							result = cursor.execute(sql)
							db.commit()	
							db.close()
						except:
							#workstation update
							workstation = '0' + workstation
							db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
							cursor = db.cursor()
							sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,IDNumber,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,DOB,Transacted,Profession,income) VALUES ('001','"+title+"','"+first_name+"','"+fathers_name+"','"+middle_name+"','"+phone+"','000','001','000','"+phone+"','"+idnumber+"','"+sex+"','"+ward+"','"+subcounty+"','"+phone+"','"+phone+"','"+introducerphone+"','"+workstation+"',CURDATE(),CURDATE(),'system','002','New Member','000','"+dob+"','NO','"+profession+"','"+income+"');"
							new_member = 'New Member'
							no = 'NO'
							print 'avoiding SQL Injection after except'
							#sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,IDNumber,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,DOB,Transacted,Profession,income) VALUES ('001',%s,%s,%s,%s,%s,'000','001','000',%s,%s,%s,%s,%s,%s,%s,%s,%s,CURDATE(),CURDATE(),%s,'002',%s,'000',%s,%s,%s,%s);" % (title, first_name, fathers_name, middle_name, phone, phone,idnumber,sex, ward, subcounty, phone, phone,introducerphone,workstation,system,new_member,dob,no,profession,income)
							print sql
							result = cursor.execute(sql)
							db.commit()	
							db.close()
						print 'db result'
						print result
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )

						cursor = db.cursor()
						sql = "INSERT INTO NextOfKins (EmployerCode,PayrollNo,TitleCode,Names,Gender,IDNumber,PhoneNo,RelationCode,DateLastChanged) VALUES ('000','"+phone+"','"+title+"','"+kin_names+"','"+gender+"','"+kin_idnumber+"','"+kinphone+"','"+relationship+"',CURDATE());"
						result = cursor.execute(sql)
						db.commit()	
						db.close()

						'''NextOfKins 
						  `EmployerCode` varchar(20) NOT NULL,
						  `PayrollNo` varchar(20) NOT NULL,
						  `TitleCode` varchar(10) NOT NULL,
						  `Names` varchar(50) NOT NULL,
						  `Gender` enum('M','F') NOT NULL,
						  `IDNumber` varchar(20) DEFAULT NULL,
						  `PhoneNo` varchar(20) DEFAULT '',
						  `RelationCode` varchar(20) NOT NULL,
						  `DateLastChanged` date NOT NULL,'''

						print 'sending data to Pesaplus ....'
						print data
						try:
							postfields = urllib.urlencode(data)
							c = pycurl.Curl()
							c.setopt(pycurl.URL, url)
							c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
							c.setopt(pycurl.POST, 1)
							c.setopt(pycurl.POSTFIELDS, postfields)
							b = StringIO.StringIO();
							c.setopt(pycurl.WRITEFUNCTION, b.write)
							c.perform()
							ncServerData = b.getvalue()
							ncServerData = json.loads(ncServerData)
							print 'ncServerData ncServerData'
							print ncServerData
						except:
							pass				
						
						#logid = log.id
						#APILog.filter.objects(id=logid).update(syncd=True)
					
						#except Exception, e:
						#result = ncServerData['result']
						#trx_id = ncServerData['trx_id']
						#raise e
						#print e	
						#pass

						reply = json.dumps({'result':'Registration Successful!.'})

					except Exception, e:
						#raise e
						print e	
						pass		
						reply = json.dumps({'result':'Registration Failed. please try again later'})		
				elif idChecker == '300':
					print idChecker
					print 'Govt data feedback'
					reply = json.dumps({'result':'Your ID number and names do not match with government data. Please check again'})
					print "idChecker != '200':"
					print reply
				elif idChecker != '200':
					print idChecker
					print 'Govt data feedback'
					reply = json.dumps({'result':'Your ID number and names do not match with government data. Please check again'})
					print "idChecker != '200':"
					print reply
				else :
					print idChecker
					print 'Govt data feedback'
					reply = json.dumps({'result':'Your ID number and names do not match with government data. Please check again'})
					print "No suitable result"
					print reply
		else:
			#except Exception, e:
			reply = json.dumps({'result':'Failed. Technical error encountered, try again after 5 minutes'})
			pass
			#raise e
	else:
		missing_fields = 'Failed. Fill these missing fields: '+ missing
		reply = json.dumps({'result':missing_fields})
	print 'Final reply..........!'
	print reply
	return HttpResponse(reply,mimetype)

@csrf_exempt		
def changePhone(request):
	mimetype = 'application/javascript'
	##get IP of the sending phone
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	ip =''
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
	  ip = request.META.get('REMOTE_ADDR')

	if request.method == 'POST':
		data = request.POST		
	else:
		data = request.GET

	try:
		log = APILog()
		log.activity = str(data[0])
		log.save()
	except:
		pass

	print data
	leo = datetime.datetime.now()
	print 'now is'
	print leo

	if True:

		phone1 = data['phone1']
		phone2 = data['phone2']
		id_number = data['id_number']
		apidata = json.dumps({"phone1":phone1,"phone2":phone2,"id_number":id_number})
		url = 'http://197.248.124.58/change/jhela/member/'

		#Check ID number
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		idsql = 'Select * from MembersMasterFile where IDNumber='+idnumber+' and CellPhone='+phone1+';'
		idresult = cursor.execute(idsql)
		db.commit()
		db.close()

		#Check phone number
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select * from MembersMasterFile where CellPhone='+phone2+';'
		phoneresult = cursor.execute(phonesql)
		db.commit()
		db.close()

	
		if not idresult:
			print 'There is no such a user with the given National ID and Current Phone Number in JHela. Please check and try again'
			reply = json.dumps({'result':'There is no such a user with the given National ID and Current Phone Number in JHela. Please check and try again'})
		elif phoneresult:
			print 'Your expected New Phone number is already registered with JHela'
			reply = json.dumps({'result':'Your expected New Phone number is already registered with JHela'})

		else:						
			
				try:				
					#Update Client's Register 
					print 'updating client ....'
					try:
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						sql = "UPDATE MembersMasterFile SET PhoneNo='"+phone2+"',CellPhone='"+phone2+"',PayrollNo='"+phone2+"', MemberNo='"+phone2+"' WHERE CellPhone='"+phone1+"' AND IDNumber='"+id_number+"'";
						result = cursor.execute(sql)
						db.commit()	
						db.close()
					except:
						pass
					print 'db result'

					print 'sending data to Pesaplus ....'
					print data
					try:
						postfields = urllib.urlencode(data)
						c = pycurl.Curl()
						c.setopt(pycurl.URL, url)
						c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
						c.setopt(pycurl.POST, 1)
						c.setopt(pycurl.POSTFIELDS, postfields)
						b = StringIO.StringIO();
						c.setopt(pycurl.WRITEFUNCTION, b.write)
						c.perform()
						ncServerData = b.getvalue()
						ncServerData = json.loads(ncServerData)
						print 'ncServerData ncServerData'
						print ncServerData
					except:
						pass	

					reply = json.dumps({'result':'Changing Phone Number Successful!.'})

				except Exception, e:
					#raise e
					print e	
					pass		
					reply = json.dumps({'result':'Changing Phone Number Failed. please try again later'})		
	else:
		#except Exception, e:
		reply = json.dumps({'result':'Failed. Technical error encountered, try again after 5 minutes'})
		pass
		#raise e		
	return HttpResponse(reply,mimetype)	


	
#UPDATE Main.MembersMasterFile SET PhoneNo='072222222',CellPhone='072222222',EmployerCode='000-2547222222' WHERE CellPhone='254722221992';
def getCounties(request):
	#Check phone number
	db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
	cursor = db.cursor()
	phonesql = 'Select OrderOfEntry, AdministrativeUnitName from AdministrativeUnits where ParentCode=1;'
	phoneresult = cursor.execute(phonesql)
	db.commit()
	db.close()
	print phoneresult

	# Convert query to objects of key-value pairs 
	objects_list = []
	rows = cursor.fetchall()
	for row in rows:
	    d = collections.OrderedDict()
	    d['id'] = row[0]
	    d['name'] = row[1]
	    objects_list.append(d)
	#create named array
	arraylist = {}
	arraylist['categories'] = objects_list
	#dump to json string
	json_string = json.dumps(arraylist)
	return HttpResponse(json_string)	

def getChildren(request):
	parent = request.GET['id']
	db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
	cursor = db.cursor()
	phonesql = 'Select OrderOfEntry, AdministrativeUnitName from AdministrativeUnits where ParentCode='+parent+';'	
	phoneresult = cursor.execute(phonesql)
	db.commit()
	db.close()
	print phoneresult

	# Convert query to objects of key-value pairs 
	objects_list = []
	rows = cursor.fetchall()
	for row in rows:
	    d = collections.OrderedDict()
	    d['id'] = row[0]
	    d['name'] = row[1]
	    objects_list.append(d)
	#create named array
	arraylist = {}
	arraylist['categories'] = objects_list
	#dump to json string
	json_string = json.dumps(arraylist)
	return HttpResponse(json_string)


def getWorkStation(request):
	parent = request.GET['id']
	db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
	cursor = db.cursor()
	phonesql = 'Select WorkStationCode, WorkStationName from WorkStations where InsideAdministrativeUnit='+parent+';'	
	phoneresult = cursor.execute(phonesql)
	db.commit()
	db.close()
	print phoneresult

	# Convert query to objects of key-value pairs 
	objects_list = []
	rows = cursor.fetchall()
	for row in rows:
	    d = collections.OrderedDict()
	    d['id'] = row[0]
	    d['name'] = row[1]
	    objects_list.append(d)
	#create named array
	arraylist = {}
	arraylist['categories'] = objects_list
	#dump to json string
	json_string = json.dumps(arraylist)
	return HttpResponse(json_string)

def getAllMembers(request):
	#parent = request.GET['id']
	db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
	cursor = db.cursor()
	#phonesql = 'SELECT MemId,FirstName, Surname, PhoneNo, WorkStationName, AdministrativeUnitName, JoinDate FROM MembersMasterFile, WorkStations, AdministrativeUnits WHERE  MembersMasterFile.WorkStationCode = WorkStations.WorkStationCode AND WorkStations.InsideAdministrativeUnit = AdministrativeUnits.ParentCode AND JoinDate > DATE_SUB(CURDATE(), INTERVAL 2 DAY);'
	phonesql = 'SELECT MemId,FirstName, Surname, PhoneNo, WorkStationName, AdministrativeUnitName, IntroducedBy, JoinDate FROM MembersMasterFile, WorkStations, AdministrativeUnits WHERE  MembersMasterFile.WorkStationCode = WorkStations.WorkStationCode AND WorkStations.InsideAdministrativeUnit = AdministrativeUnits.AdministrativeUnitCode AND JoinDate > DATE_SUB(CURDATE(), INTERVAL 2 DAY) ORDER BY IntroducedBy;'
	phoneresult = cursor.execute(phonesql)
	db.commit()
	db.close()
	print phoneresult

	# Convert query to objects of key-value pairs 
	objects_list = []
	rows = cursor.fetchall()
	for row in rows:
	    d = collections.OrderedDict()
	    d['MemId'] = str(row[0])
	    d['FirstName'] = str(row[1])
	    d['Surname'] = str(row[2])
	    d['PhoneNo'] = str(row[3])
	    d['WorkStationName'] = str(row[4])
	    d['AdministrativeUnitName'] = str(row[5])
	    d['IntroducedBy'] = str(row[6])
	    d['JoinDate'] = str(row[7])
	    objects_list.append(d)
	#create named array
	arraylist = {}
	arraylist['categories'] = objects_list
	#dump to json string
	json_string = json.dumps(arraylist)
	return HttpResponse(json_string)


def getDailyMembers(request):
	db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
	cursor = db.cursor()
	#phonesql = 'SELECT MemId,FirstName, Surname, PhoneNo, WorkStationName, AdministrativeUnitName, JoinDate FROM MembersMasterFile, WorkStations, AdministrativeUnits WHERE  MembersMasterFile.WorkStationCode = WorkStations.WorkStationCode AND WorkStations.InsideAdministrativeUnit = AdministrativeUnits.ParentCode AND JoinDate > DATE_SUB(CURDATE(), INTERVAL 2 DAY);'
	phonesql = 'SELECT MemId,FirstName, Surname, PhoneNo, WorkStationName, AdministrativeUnitName, IntroducedBy, JoinDate FROM MembersMasterFile, WorkStations, AdministrativeUnits WHERE  MembersMasterFile.WorkStationCode = WorkStations.WorkStationCode AND WorkStations.InsideAdministrativeUnit = AdministrativeUnits.AdministrativeUnitCode AND JoinDate > DATE_SUB(CURDATE(), INTERVAL 2 DAY) ORDER BY IntroducedBy;'
	phoneresult = cursor.execute(phonesql)
	db.commit()
	db.close()
	print phoneresult
	# Convert query to objects of key-value pairs 
	objects_list = []
	rows = cursor.fetchall()
	for row in rows:
	    d = collections.OrderedDict()
	    d['MemId'] = str(row[0])
	    d['FirstName'] = str(row[1])
	    d['Surname'] = str(row[2])
	    d['PhoneNo'] = str(row[3])
	    d['WorkStationName'] = str(row[4])
	    d['AdministrativeUnitName'] = str(row[5])
	    d['IntroducedBy'] = str(row[6])
	    d['JoinDate'] = str(row[7])
	    objects_list.append(d)
	#create named array
	arraylist = {}
	arraylist['categories'] = objects_list
	#dump to json string
	json_string = json.dumps(arraylist)
	return HttpResponse(json_string)



def countByRegistrar(request):
	if request.method == 'POST':
		json_string = "Only GET accepted"		
	else:
		data = request.GET
		print data
		leo = datetime.datetime.now()
		print 'now is'
		print leo

		fday = data['start']
		lday = data['end']

		try:
			fday = time.strptime(fday, '%Y-%m-%d')
			fday = time.strftime("%Y-%m-%d",fday)
		except:
			fday = time.strptime(fday, '%d-%m-%Y')
			fday = time.strftime("%Y-%m-%d",fday)
		try:
			lday = time.strptime(lday, '%Y-%m-%d')
			lday = time.strftime("%Y-%m-%d",lday)
		except:
			lday = time.strptime(lday, '%d-%m-%Y')
			lday = time.strftime("%Y-%m-%d",lday)

		print fday
		print lday

		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor1 = db.cursor()
		#phonesql1 = 'SELECT COUNT(*) as count FROM MembersMasterFile WHERE JoinDate >= "'+fday+'" AND JoinDate <= "'+lday+'";'#DATE_SUB(CURDATE(), INTERVAL 2 DAY);'
		#phonesql1 = 'SELECT COUNT(*) as count FROM MembersMasterFile a,MembersMasterFile b WHERE a.JoinDate >= "'+fday+'" AND a.JoinDate <= "'+lday+'" AND a.IntroducedBy = b.PhoneNo;'
		phonesql1 = 'SELECT COUNT(*) as count FROM MembersMasterFile a,MembersMasterFile b WHERE a.JoinDate >= "'+fday+'" AND a.JoinDate <= "'+lday+'" AND a.IntroducedBy = b.CellPhone;'
		print phonesql1
		phoneresult1 = cursor1.execute(phonesql1)	
		db.commit()
		db.close()

		rows = cursor1.fetchall()
		for row in rows:
		    total = str(row[0])
		print total
		
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		#phonesql = 'SELECT MemId,FirstName, Surname, PhoneNo, WorkStationName, AdministrativeUnitName, JoinDate FROM MembersMasterFile, WorkStations, AdministrativeUnits WHERE  MembersMasterFile.WorkStationCode = WorkStations.WorkStationCode AND WorkStations.InsideAdministrativeUnit = AdministrativeUnits.ParentCode AND JoinDate > DATE_SUB(CURDATE(), INTERVAL 2 DAY);'
		#phonesql = 'SELECT IntroducedBy COUNT(*) as count FROM MembersMasterFile WHERE JoinDate > DATE_SUB(CURDATE(), INTERVAL 2 DAY) GROUP BY IntroducedBy ORDER BY count DESC;'
		#phonesql = 'SELECT a.IntroducedBy,b.FirstName, b.Surname, COUNT(*) as count FROM MembersMasterFile a,MembersMasterFile b WHERE a.JoinDate > DATE_SUB(CURDATE(), INTERVAL 2 DAY) AND a.IntroducedBy = b.PhoneNo GROUP BY IntroducedBy ORDER BY count DESC;'
		#phonesql = 'SELECT MemId,FirstName, Surname, PhoneNo, WorkStationName, AdministrativeUnitName, IntroducedBy, JoinDate FROM MembersMasterFile, WorkStations, AdministrativeUnits WHERE  MembersMasterFile.WorkStationCode = WorkStations.WorkStationCode AND WorkStations.InsideAdministrativeUnit = AdministrativeUnits.AdministrativeUnitCode AND JoinDate > DATE_SUB(CURDATE(), INTERVAL 2 DAY) ORDER BY IntroducedBy;'
		##phonesql = 'SELECT a.IntroducedBy,b.FirstName, b.Surname, COUNT(*) as count FROM MembersMasterFile a,MembersMasterFile b WHERE a.JoinDate > DATE_SUB(CURDATE(), INTERVAL 2 DAY) AND a.IntroducedBy = b.PhoneNo GROUP BY IntroducedBy ORDER BY count DESC;'
		#phonesql = 'SELECT a.IntroducedBy,b.FirstName, b.Surname, COUNT(*) as count FROM MembersMasterFile a,MembersMasterFile b WHERE a.JoinDate >= "'+fday+'" AND a.JoinDate <= "'+lday+'" AND a.IntroducedBy = b.PhoneNo GROUP BY IntroducedBy ORDER BY count DESC;'
		phonesql = 'SELECT b.CellPhone,b.FirstName, b.Surname, COUNT(*) as count FROM MembersMasterFile a,MembersMasterFile b WHERE a.JoinDate >= "'+fday+'" AND a.JoinDate <= "'+lday+'" AND a.IntroducedBy = b.CellPhone GROUP BY b.CellPhone ORDER BY count DESC;'
		phoneresult = cursor.execute(phonesql)
		db.commit()
		db.close()
		print phoneresult
		# Convert query to objects of key-value pairs 
		objects_list = []
		rows = cursor.fetchall()
		for row in rows:
		    d = collections.OrderedDict()
		    d['IntroducedBy'] = str(row[0])
		    d['FirstName'] = str(row[1])
		    d['Surname'] = str(row[2])
		    d['count'] = str(row[3])
		    d['total'] = str(total)
		    objects_list.append(d)
		#create named array
		arraylist = {}
		arraylist['categories'] = objects_list
		#dump to json string
		json_string = json.dumps(arraylist)
		print json_string
	return HttpResponse(json_string)


def countByWorkStationName(request):
	if request.method == 'POST':
		json_string = "Only GET accepted"		
	else:
		data = request.GET
		print data
		leo = datetime.datetime.now()
		print 'now is'
		print leo

		fday = data['start']
		lday = data['end']

		try:
			fday = time.strptime(fday, '%Y-%m-%d')
			fday = time.strftime("%Y-%m-%d",fday)
		except:
			fday = time.strptime(fday, '%d-%m-%Y')
			fday = time.strftime("%Y-%m-%d",fday)
		try:
			lday = time.strptime(lday, '%Y-%m-%d')
			lday = time.strftime("%Y-%m-%d",lday)
		except:
			lday = time.strptime(lday, '%d-%m-%Y')
			lday = time.strftime("%Y-%m-%d",lday)

		print fday
		print lday
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor1 = db.cursor()
		#phonesql1 = 'SELECT COUNT(*) as count FROM MembersMasterFile WHERE JoinDate >= "'+fday+'" AND JoinDate <= "'+lday+'";'#DATE_SUB(CURDATE(), INTERVAL 2 DAY);'
		phonesql1 = 'SELECT MembersMasterFile.WorkStationCode,  WorkStations.WorkStationName, AdministrativeUnits.AdministrativeUnitName, COUNT(*) as count FROM MembersMasterFile,  WorkStations, AdministrativeUnits  WHERE MembersMasterFile.WorkStationCode = WorkStations.WorkStationCode AND WorkStations.WorkStationCode = AdministrativeUnits.OrderOfEntry AND MembersMasterFile.JoinDate >= "'+fday+'" AND MembersMasterFile.JoinDate <= "'+lday+'";'
		print phonesql1
		phoneresult1 = cursor1.execute(phonesql1)	
		db.commit()
		db.close()

		rows = cursor1.fetchall()
		for row in rows:
		    total = str(row[3])
		print total

		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'SELECT MembersMasterFile.WorkStationCode,  WorkStations.WorkStationName, AdministrativeUnits.AdministrativeUnitName, COUNT(*) as count FROM MembersMasterFile,  WorkStations, AdministrativeUnits  WHERE MembersMasterFile.WorkStationCode = WorkStations.WorkStationCode AND WorkStations.WorkStationCode = AdministrativeUnits.OrderOfEntry AND MembersMasterFile.JoinDate >= "'+fday+'" AND MembersMasterFile.JoinDate <= "'+lday+'"  GROUP BY MembersMasterFile.WorkStationCode ORDER BY count DESC;'
		phoneresult = cursor.execute(phonesql)
		db.commit()
		db.close()
		print phoneresult
		# Convert query to objects of key-value pairs 
		objects_list = []
		rows = cursor.fetchall()
		for row in rows:
		    d = collections.OrderedDict()
		    d['WorkStationCode'] = str(row[0])
		    d['WorkStationName'] = str(row[1])
		    d['AdministrativeUnitName'] = str(row[2])
		    d['count'] = str(row[3])	 
		    d['total'] = str(total)   
		    objects_list.append(d)
		#create named array
		arraylist = {}
		arraylist['categories'] = objects_list
		#dump to json string
		json_string = json.dumps(arraylist)
		print json_string
	return HttpResponse(json_string)

@csrf_exempt
def sendMail(request):
	today = datetime.datetime.now()
	jana = datetime.datetime.today() - timedelta(days=1)

	db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
	cursor = db.cursor()
	phonesql = 'SELECT MemId,FirstName, Surname, PhoneNo, WorkStationName, AdministrativeUnitName, JoinDate FROM MembersMasterFile, WorkStations, AdministrativeUnits WHERE  MembersMasterFile.WorkStationCode = WorkStations.WorkStationCode AND WorkStations.InsideAdministrativeUnit = AdministrativeUnits.ParentCode AND JoinDate > DATE_SUB(CURDATE(), INTERVAL 2 DAY);'
	phoneresult = cursor.execute(phonesql)
	db.commit()
	db.close()
	print phoneresult
	j = ''
	# Convert query to objects of key-value pairs 
	rows = cursor.fetchall()
	k=0
	if rows:
		for row in rows:
			j = j+'\n'+str(row[0])+': '+ str(row[1]) +' ' + str(row[2])+' '+str(row[3])+' ' + str(row[4])+' '+str(row[5])+'\n'
			k=k+1		
	else:
		j='No clients registered today :('

	send_mail(
    'Subject here',
    'Here is the message.',
    settings.EMAIL_HOST_USER,
    ['vincentmaraba@gmail.com']
	)

	message = 'Duration:' + str(jana) +' - ' + str(today) +'\nNo of J-Hela registered = ' +str(k) +'\n' + j

	send_mail('J-Hela Registrations Update', message, settings.EMAIL_HOST_USER, ['vincentmaraba@gmail.com'], fail_silently=False) #vincentmaraba@gmail.com patrick@junglenuts.co.ke

	return HttpResponse('email sent!')

def confirmID(surname,first_name,second_name,national_id):
	import re
	name1 = surname
	name2 = first_name
	name3 = second_name
	name4 = '' 
	nationalID = national_id
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
 	print 'check CRB ....'
	product102 = client.service.getProduct102(username=username,password=password,code=code,infinityCode=infinityCode,nationalID=nationalID,name1=name1,name2=name2,name3=name3,reportReason=reportReason,reportSector=reportSector)
	reply = str(product102.responseCode)
	print reply
	if reply == '200' or reply == '203':
		print 'success'
		reply='300'
		'''if (name1 == personalProfile['surname'] and name2 == personalProfile['otherNames']):
			reply = 200
			print personalProfile['otherNames']			
			print 
		'''
		try:
			print product102
			print product102.responseCode
			print product102.header
			header = product102.header
			personalProfile =  product102.personalProfile
			#print header
			#print personalProfile
			'''
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
			print personalProfile['surname']
			print personalProfile['otherNames']			
			print personalProfile['nationalID']
			print personalProfile['nationality']
			print personalProfile['gender']
			#print personalProfile['passportNo']
			print personalProfile['salutation']'''
			#print personalProfile['serviceID']	

			a = personalProfile['fullName']
			print "name1 searching .."
			print a
			print name1
			score=0
			matchObj = re.search(name1, a, re.M|re.I)
			if matchObj:
				print "matchObj.group() : ", matchObj.group()
				score = score + 1
			else:
			   print "name1 No match!!"

			print "name2 searching .."
			print a
			print name2
			matchObj = re.search(name2, a, re.M|re.I)
			if matchObj:
				print "matchObj.group() : ", matchObj.group()
				score = score + 1
			else:
			   print "name2 No match!!"

			print "name2 searching .."
			print a
			print name2
			matchObj = re.search(name3, a, re.M|re.I)
			if matchObj:
				print "matchObj.group() : ", matchObj.group()
				score = score + 1
			else:
			   print "name3 No match!!"

			if score > 1:
				reply='200'
		except:
			reply='300'
			pass
	else:
		print 'CRB check failed...'
		#product102 = client.service.getProduct102(username=username,password=password,code=code,infinityCode=infinityCode,nationalID=nationalID,name1=name1,reportReason=reportReason,reportSector=reportSector)
		#reply = str(product102.responseCode)
		reply='300'
		print reply
	return reply

############
'''
CRB CODES
No Code Description
301 Insufficient Credit
'''
@csrf_exempt
def checkCRB(request):
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
	if product102 == '301':
		print 'Insufficient Credit'
		
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
	return HttpResponse('check CRB')


def getJSokoRecords(request):
	db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
	cursor1 = db.cursor()
	phonesql1 = 'SELECT COUNT(*) as count FROM InboundRecords WHERE ResposeErr="0" AND RequestType="036";'
	print phonesql1
	phoneresult1 = cursor1.execute(phonesql1)	
	db.commit()
	db.close()

	rows = cursor1.fetchall()
	for row in rows:
	    total = str(row[0])
	print total

	db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
	cursor = db.cursor()	
	#SELECT MembersMasterFile.FirstName,MembersMasterFile.Surname,MembersMasterFile.CellPhone, InboundRecords.IncomingData,InboundRecords.RequestAmt,WorkStations.WorkStationCode, a.AdministrativeUnitName,b.ParentCode FROM MembersMasterFile,InboundRecords,WorkStations,AdministrativeUnits a,AdministrativeUnits b WHERE InboundRecords.XtremeMemID = MembersMasterFile.MemId AND InboundRecords.ResposeErr='0' AND InboundRecords.RequestType='036' AND MembersMasterFile.WorkStationCode = WorkStations.WorkStationCode AND WorkStations.InsideAdministrativeUnit = a.OrderOfEntry AND a.ParentCode = b.OrderOfEntry ORDER BY TrxID ASC;
	#phonesql = 'SELECT MembersMasterFile.FirstName,MembersMasterFile.Surname,MembersMasterFile.CellPhone, InboundRecords.IncomingData,InboundRecords.RequestAmt,WorkStations.WorkStationCode, AdministrativeUnits.AdministrativeUnitName FROM MembersMasterFile,InboundRecords,WorkStations,AdministrativeUnits WHERE InboundRecords.XtremeMemID = MembersMasterFile.MemId AND InboundRecords.ResposeErr='0' AND InboundRecords.RequestType='036' AND MembersMasterFile.WorkStationCode = WorkStations.WorkStationCode AND WorkStations.InsideAdministrativeUnit = AdministrativeUnits.OrderOfEntry ORDER BY TrxID ASC;'
	phonesql = "SELECT MembersMasterFile.FirstName,MembersMasterFile.Surname,MembersMasterFile.CellPhone, InboundRecords.IncomingData,InboundRecords.RequestAmt,WorkStations.WorkStationCode, WorkStations.WorkStationName,a.AdministrativeUnitName,b.AdministrativeUnitName,c.AdministrativeUnitName FROM MembersMasterFile,InboundRecords,WorkStations,AdministrativeUnits a,AdministrativeUnits b,AdministrativeUnits c WHERE InboundRecords.XtremeMemID = MembersMasterFile.MemId AND InboundRecords.ResposeErr='0' AND InboundRecords.Delivered='N' AND InboundRecords.RequestType='036' AND MembersMasterFile.WorkStationCode = WorkStations.WorkStationCode AND WorkStations.InsideAdministrativeUnit = a.OrderOfEntry AND a.ParentCode = b.OrderOfEntry AND b.ParentCode = c.OrderOfEntry ORDER BY TrxID ASC;"
	phoneresult = cursor.execute(phonesql)
	db.commit()
	db.close()
	print phoneresult
	total = phoneresult
	# Convert query to objects of key-value pairs 
	objects_list = []
	rows = cursor.fetchall()
	for row in rows:
	    d = collections.OrderedDict()
	    d['FirstName'] = str(row[0])
	    d['Surname'] = str(row[1])
	    d['CellPhone'] = str(row[2])
	    d['IncomingData'] = str(row[3])
	    d['Amount'] = str(row[4])
	    d['Cluster'] = str(row[6])
	    d['Ward'] = str(row[7])
	    d['SubCounty'] = str(row[8])
	    d['County'] = str(row[9])
	    d['total'] = str(total) 
	    objects_list.append(d)
	#create named array
	arraylist = {}
	arraylist['categories'] = objects_list
	#dump to json string
	json_string = json.dumps(arraylist)
	return HttpResponse(json_string)


def getJSokoRecords2(request):
	if request.method == 'POST':
		json_string = "Only GET accepted"		
	else:
		data = request.GET
		print data
		leo = datetime.datetime.now()
		print 'now is'
		print leo

		fday = data['start']
		lday = data['end']

		try:
			fday = time.strptime(fday, '%Y-%m-%d')
			fday = time.strftime("%Y-%m-%d",fday)
		except:
			fday = time.strptime(fday, '%d-%m-%Y')
			fday = time.strftime("%Y-%m-%d",fday)
		try:
			lday = time.strptime(lday, '%Y-%m-%d')
			lday = time.strftime("%Y-%m-%d",lday)
		except:
			lday = time.strptime(lday, '%d-%m-%Y')
			lday = time.strftime("%Y-%m-%d",lday)

		print fday
		print lday

		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor1 = db.cursor()
		phonesql1 = 'SELECT COUNT(*) as count FROM InboundRecords WHERE ResposeErr="0" AND RequestType="036" AND InboundRecords.SubmitReplyTime >= "'+fday+'" AND InboundRecords.SubmitReplyTime <= "'+lday+'";'			
		print phonesql1
		phoneresult1 = cursor1.execute(phonesql1)	
		db.commit()
		db.close()

		rows = cursor1.fetchall()
		for row in rows:
		    total = str(row[0])
		print total


		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		#phonesql = "SELECT MembersMasterFile.FirstName,MembersMasterFile.Surname,MembersMasterFile.CellPhone, InboundRecords.IncomingData,InboundRecords.RequestAmt,WorkStations.WorkStationCode,WorkStations.WorkStationName, a.AdministrativeUnitName,b.AdministrativeUnitName FROM MembersMasterFile,InboundRecords,WorkStations,AdministrativeUnits a,AdministrativeUnits b WHERE InboundRecords.XtremeMemID = MembersMasterFile.MemId AND InboundRecords.ResposeErr='0' AND InboundRecords.RequestType='036' AND InboundRecords.Delivered='Y' AND InboundRecords.SubmitReplyTime >= '"+fday+"' AND InboundRecords.SubmitReplyTime <= '"+lday+"' AND MembersMasterFile.WorkStationCode = WorkStations.WorkStationCode AND WorkStations.InsideAdministrativeUnit = a.OrderOfEntry AND a.ParentCode = b.OrderOfEntry ORDER BY TrxID ASC;"
		phonesql = "SELECT MembersMasterFile.FirstName,MembersMasterFile.Surname,MembersMasterFile.CellPhone, InboundRecords.IncomingData,InboundRecords.RequestAmt,WorkStations.WorkStationCode, WorkStations.WorkStationName,a.AdministrativeUnitName,b.AdministrativeUnitName,c.AdministrativeUnitName FROM MembersMasterFile,InboundRecords,WorkStations,AdministrativeUnits a,AdministrativeUnits b,AdministrativeUnits c WHERE InboundRecords.XtremeMemID = MembersMasterFile.MemId AND InboundRecords.ResposeErr='0' AND InboundRecords.Delivered='Y' AND InboundRecords.RequestType='036' AND MembersMasterFile.WorkStationCode = WorkStations.WorkStationCode AND WorkStations.InsideAdministrativeUnit = a.OrderOfEntry AND a.ParentCode = b.OrderOfEntry AND b.ParentCode = c.OrderOfEntry ORDER BY TrxID ASC;"
		phoneresult = cursor.execute(phonesql)
		db.commit()
		db.close()
		print phoneresult
		total = phoneresult
		# Convert query to objects of key-value pairs 
		objects_list = []
		rows = cursor.fetchall()
		for row in rows:
		    d = collections.OrderedDict()
		    d['FirstName'] = str(row[0])
		    d['Surname'] = str(row[1])
		    d['CellPhone'] = str(row[2])
		    d['IncomingData'] = str(row[3])
		    d['Amount'] = str(row[4])
		    d['Cluster'] = str(row[6])
		    d['Ward'] = str(row[7])
		    d['SubCounty'] = str(row[8])
		    d['County'] = str(row[9])
		    d['total'] = str(total) 
		    objects_list.append(d)
		#create named array
		arraylist = {}
		arraylist['categories'] = objects_list
		#dump to json string
		json_string = json.dumps(arraylist)
	return HttpResponse(json_string)

@csrf_exempt		
def addGroupClientAPISuspended(request):
	mimetype = 'application/javascript'
	##get IP of the sending phone
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	ip =''
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
	  ip = request.META.get('REMOTE_ADDR')

	if request.method == 'POST':
		data = request.POST		
	else:
		data = request.GET

	try:
		log = APILog()
		log.activity = str(data[0])
		log.save()
	except:
		pass

	print data
	leo = datetime.datetime.now()
	print 'now is'
	print leo

	first_name = data['group_name']
	middle_name = ''
	fathers_name = ''
	sex = 'Male'
	idnumber = data['regnumber']
	phone = data['phone'].strip()
	#profession = data['profession']
	income = data['income']
	try:
		group_type = data['group_type']
	except:
		group_type = ''
		pass
	#country = data['country']
	#county = data['county']
	subcounty = ''
	ward = '01'
	cluster = ''
	workstation = '01'
	try:
		subcounty = data['subcounty']
	except:
		pass	
	try:
		ward = data['ward']
	except:
		pass
	try:
		workstation = data['cluster']
	except:
		pass
	phone1 = data['phone1'].strip()
	phone2 = data['phone2'].strip()
	phone3 = data['phone3']
	introducerphone = data['introducerphone'].strip()
	dob = data['dateofbirth']	

	try:
		dob = time.strptime(dob, '%Y-%m-%d')
		dob = time.strftime("%Y-%m-%d",dob)
	except:
		try:
			dob = time.strptime(dob, '%d-%m-%Y')
			dob = time.strftime("%Y-%m-%d",dob)
		except:
			dob = time.strptime(dob, '%d/%m/%Y')
			dob = time.strftime("%Y-%m-%d",dob)

	if len(phone) == 10:
		phone = '254'+phone[1:]
	if len(phone1) == 10:
		phone1 = '254'+phone1[1:]
	if len(phone2) == 10:
		phone2 = '254'+phone2[1:]
	if len(phone3) == 10:
		phone3 = '254'+phone3[1:]
	if len(introducerphone) == 10:
		introducerphone = '254'+introducerphone[1:]
	title = '001'
	if sex == 'Male':
		title = '001'
		sex = 'MALE'
		gender = 'M'
	else:
		title = '002'
		sex = 'FEMALE'
		gender = 'F'
	day = datetime.datetime(1990, 1, 1)
	todaystr = str(day)
	todaystr = '1990-01-01'	
	a = True
	reply = json.dumps({'result':'Failed. Technical error encountered, try again later'})
	return HttpResponse(reply,mimetype)	

@csrf_exempt		
def addGroupClientAPI(request):
	mimetype = 'application/javascript'
	##get IP of the sending phone
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	ip =''
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
	  ip = request.META.get('REMOTE_ADDR')

	#data = {u'cluster': [u'9040113'], u'phone': [u'0700863271'], u'phone2': [u'0725109628'], u'country': [u'Kenya'], u'introducerphone': [u'0722531106'],u'phone1': [u'0722531106'], u'group_name': [u'Thika CDF'], u'county': [u'Kiambu county'],  u'dateofbirth': [u'21-12-2017'], u'regnumber': [u'CDF001'], u'subcounty': [u'THIKA TOWN'], u'income': [u'100000'], u'ward': [u'TOWNSHIP'], u'phone3': [u'0708570900'], u'group_type': [u'Chama']}

	if request.method == 'POST':
		data = request.POST		
	else:
		data = request.GET

	try:
		log = APILog()
		log.activity = str(data[0])
		log.save()
	except:
		pass

	print data
	leo = datetime.datetime.now()
	print 'now is'
	print leo

	first_name = data['group_name']
	middle_name = ''
	fathers_name = ''
	sex = 'Male'
	idnumber = data['regnumber']
	phone = data['phone']
	#.strip()
	#profession = data['profession']
	income = data['income']
	try:
		group_type = data['group_type']
	except:
		group_type = ''
		pass
	#country = data['country']
	#county = data['county']
	subcounty = ''
	ward = '01'
	cluster = ''
	workstation = '01'
	try:
		subcounty = data['subcounty']
	except:
		pass	
	try:
		ward = data['ward']
	except:
		pass
	try:
		workstation = data['cluster']
	except:
		pass
	phone1 = data['phone1']
	#.strip()
	phone2 = data['phone2']
	#.strip()
	phone3 = data['phone3']
	introducerphone = data['introducerphone']
	#.strip()
	dob = data['dateofbirth']	
	print dob

	try:
		dob = time.strptime(dob, '%Y-%m-%d')
		dob = time.strftime("%Y-%m-%d",dob)
	except:
		try:
			dob = time.strptime(dob, '%d-%m-%Y')
			dob = time.strftime("%Y-%m-%d",dob)
		except:
			dob = time.strptime(dob, '%d/%m/%Y')
			dob = time.strftime("%Y-%m-%d",dob)

	if len(phone) == 10:
		phone = '254'+phone[1:]
	if len(phone1) == 10:
		phone1 = '254'+phone1[1:]
	if len(phone2) == 10:
		phone2 = '254'+phone2[1:]
	if len(phone3) == 10:
		phone3 = '254'+phone3[1:]
	if len(introducerphone) == 10:
		introducerphone = '254'+introducerphone[1:]
	title = '001'
	if sex == 'Male':
		title = '001'
		sex = 'MALE'
		gender = 'M'
	else:
		title = '002'
		sex = 'FEMALE'
		gender = 'F'
	day = datetime.datetime(1990, 1, 1)
	todaystr = str(day)
	todaystr = '1990-01-01'	
	a = True
	if a:
	#try:
		apidata = json.dumps({"phone":phone,"iphone":introducerphone,"idnumber":idnumber,"first_name":first_name,"fathers_name":fathers_name,"idnumber":idnumber})
		url = 'http://197.248.124.58/receive/jhela/member/'
				
		#Check ID number
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		idsql = 'Select * from MembersMasterFile where IDNumber="'+idnumber+'";'
		idresult = cursor.execute(idsql)
		db.commit()
		db.close()

		#Check phone number
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select * from MembersMasterFile where CellPhone="'+phone+'";'
		phoneresult = cursor.execute(phonesql)
		db.commit()
		db.close()

		#Check chairman
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select * from MembersMasterFile where CellPhone="'+phone1+'";'
		phoneresult1 = cursor.execute(phonesql)
		db.commit()
		db.close()

		#Check treasurer
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select * from MembersMasterFile where CellPhone="'+phone2+'";'
		phoneresult2 = cursor.execute(phonesql)
		db.commit()
		db.close
		#Check secretary
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select * from MembersMasterFile where CellPhone="'+phone3+'";'
		phoneresult3 = cursor.execute(phonesql)
		db.commit()
		db.close()

		#Check introducer phone number
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		introducersql = 'Select * from MembersMasterFile where CellPhone='+introducerphone+';'
		introducerresult = cursor.execute(introducersql)
		db.commit()
		db.close()

		data = {"phone":phone,"iphone":introducerphone,"idnumber":idnumber,"first_name":first_name,"fathers_name":fathers_name,"idnumber":idnumber,"username":"jhelaapi","password":"jhelaapi"}
		postfields = urllib.urlencode(data)
		print data
		print postfields
		#data = {"phone":phone,"iphone":introducerphone,"idnumber":idnumber,"first_name":first_name,"fathers_name":fathers_name,"idnumber":idnumber,"username":"jhelaapi","password":"jhelaapi"}
				
		if not introducerresult:
			postfields = urllib.urlencode(data)
			print 'Introducer Phone number is not registered with JHela'
			reply = json.dumps({'result':'Introducer Phone number is not registered with JHela'})		
		elif len(phone) != 12 :
			print 'phone number has less characters'
			print phone
			reply = json.dumps({'result':'Failed. Phone number has less characters'})
		elif len(phone1) != 12 :
			print 'phone1 has less characters'
			print phone1
			reply = json.dumps({'result':"Failed. Chairman's phone number has less characters"})
		elif len(phone2) != 12:
			print 'phone2 has less characters'
			print phone2
			reply = json.dumps({'result':"Failed. Treasurer's phone number has less characters"})
		elif len(phone3) != 12 :
			print 'phone2 has less characters'
			print phone3
			reply = json.dumps({'result':"Failed. Secretary's phone number has less characters"})
		elif not phoneresult1:
			reply = json.dumps({'result':'The chairman is not a J-Hela member. Please confirm phone number and try again'})
		elif not phoneresult2:
			reply = json.dumps({'result':'The treasurer is not a J-Hela member. Please confirm phone number and try again'})
		elif not phoneresult3:
			reply = json.dumps({'result':'The secretary is not a J-Hela mmeber. Please confirm phone number and try again'})
		elif phoneresult:
			postfields = urllib.urlencode(data)
			print 'member is already registered in finextreme'
			try:
				reply = json.dumps({'result':'Phone number has already been registered'})
				c = pycurl.Curl()
				c.setopt(pycurl.URL, url)
				c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
				c.setopt(pycurl.POST, 1)
				c.setopt(pycurl.POSTFIELDS, postfields)
				b = StringIO.StringIO();
				c.setopt(pycurl.WRITEFUNCTION, b.write)
				c.perform()
				ncServerData = b.getvalue()
				ncServerData = json.loads(ncServerData)
				print ncServerData
				print 'ncServerData ncServerData'
			except:
				reply = json.dumps({'result':'Phone number has already been registered'})
				pass	
			reply = json.dumps({'result':'Phone number has already been registered'})
		elif idresult:
			reply = json.dumps({'result':'ID number has already been registered'})		
		else:

			try:				
				#Register client
				print 'Registering client ....'
				workstate = False
				try:
					workstate = '0' + workstation
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,IDNumber,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,DOB,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,income,GroupType) VALUES ('001','"+title+"','"+first_name+"','"+fathers_name+"','"+middle_name+"','"+phone+"','000','001','000','"+phone+"','"+idnumber+"','"+sex+"','"+ward+"','"+subcounty+"','"+phone+"','"+phone+"','"+introducerphone+"','"+workstate+"','"+dob+"',CURDATE(),CURDATE(),'system','002','New Member','000','"+income+"','"+group_type+"');"
					new_member = 'New Member'
					no = 'NO'
					print 'avoinding SQL Injection'
					#sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,IDNumber,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,DOB,Transacted,Profession,income) VALUES ('001',%s,%s,%s,%s,%s,'000','001','000',%s,%s,%s,%s,%s,%s,%s,%s,%s,CURDATE(),CURDATE(),%s,'002',%s,'000',%s,%s,%s,%s);" % (title, first_name, fathers_name, middle_name, phone, phone,idnumber,sex, ward, subcounty, phone, phone,introducerphone,workstation,system,new_member,dob,no,profession,income)
					print sql
					result = cursor.execute(sql)
					print result
					print cursor.fetchall()
					db.commit()	
					db.close()					
				except:
					#workstation update
					#try:
					#workstation = '0' + workstation
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,IDNumber,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,DOB,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,income,GroupType) VALUES ('001','"+title+"','"+first_name+"','"+fathers_name+"','"+middle_name+"','"+phone+"','000','001','000','"+phone+"','"+idnumber+"','"+sex+"','"+ward+"','"+subcounty+"','"+phone+"','"+phone+"','"+introducerphone+"','"+workstation+"','"+dob+"',CURDATE(),CURDATE(),'system','002','New Member','000','"+income+"','"+group_type+"');"
					new_member = 'New Member'
					no = 'NO'
					print 'avoiding SQL Injection after except'
					#sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,IDNumber,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,DOB,Transacted,Profession,income) VALUES ('001',%s,%s,%s,%s,%s,'000','001','000',%s,%s,%s,%s,%s,%s,%s,%s,%s,CURDATE(),CURDATE(),%s,'002',%s,'000',%s,%s,%s,%s);" % (title, first_name, fathers_name, middle_name, phone, phone,idnumber,sex, ward, subcounty, phone, phone,introducerphone,workstation,system,new_member,dob,no,profession,income)
					print sql
					result = cursor.execute(sql)
					db.commit()	
					db.close()
					#except:
					#	pass
				if workstate:
					workstation  = workstate
				#Register in MicroFinanceMasterFile
				print 'Registering MicroFinance Group ....'
				#Get phone number
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				phonesql = 'Select MemId, FirstName, SalaryAccount from MembersMasterFile where CellPhone='+phone+' LIMIT 1;'
				print phonesql
				phoneresult = cursor.execute(phonesql)
				print phoneresult
				db.commit()
				db.close()
				rows = cursor.fetchall()
				print rows
				print 'check MemId'
				for row in rows:
				    MemId = str(row[0])
				    print MemId
				    FirstName = str(row[1])	
				    print FirstName
				    SalaryAccount = str(row[2])	

				address  = ward + ' ,' + subcounty	

				if True:
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "INSERT INTO MicroFinanceMasterFile (GroupName,Address,WorkStationCode,GroupNo,Description,GroupAccount) VALUES ('"+first_name+"','"+address+"','"+workstation+"','"+MemId+"','"+group_type+"','"+SalaryAccount+"');"
					print sql
					result = cursor.execute(sql)
					db.commit()	
					db.close()
				else:
					#workstation update
					try:
						workstation = '0' + workstation
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						sql = "INSERT INTO MicroFinanceMasterFile (GroupName,Address,WorkStationCode,GroupNo,Description,GroupAccount) VALUES ('"+first_name+"','"+address+"','"+workstation+"','"+MemId+"','"+group_type+"','"+SalaryAccount+"');"
						print sql
						result = cursor.execute(sql)
						db.commit()	
						db.close()
					except:
						pass
						
				#Register Signatories
				print 'Registering Signatories ....'
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				sql = "INSERT INTO Signatories (MasterFileId,ChairpersonPhone,TreasurerPhone,SecretaryPhone) VALUES ('"+MemId+"', '"+phone1+"','"+phone2+"','"+phone3+"');"  #,CURDATE()
				print sql
				result = cursor.execute(sql)
				db.commit()	
				db.close()
										
				print 'Link officials to group  ....'
				#ChairpersonPhone
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone1+"'";
				print sql
				result = cursor.execute(sql)
				db.commit()	
				db.close()
				#get member name
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				phonesql = 'Select FirstName from MembersMasterFile where CellPhone="'+phone1+'";'
				phoneresult = cursor.execute(phonesql)
				db.commit()
				db.close()
				rows = cursor.fetchall()
				for row in rows:
					name = str(row[0])
					#send message to customer
					ujumbe = 'Jambo '+ str(name.upper()) +', You have been registered as a signatory of a group account called '+ str(first_name).upper() +' of phone number '+phone+'. Thank you'
					#send sms to chair
					to = urllib.urlencode({'DESTADDR':phone1,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)

				#TreasurerPhone
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone2+"'";
				result = cursor.execute(sql)
				db.commit()	
				db.close()
				#get member name
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				phonesql = 'Select FirstName from MembersMasterFile where CellPhone="'+phone2+'";'
				phoneresult = cursor.execute(phonesql)
				db.commit()
				db.close()
				rows = cursor.fetchall()
				for row in rows:
					name = str(row[0])
					#send message to customer
					ujumbe = 'Jambo '+ str(name.upper()) +', You have been registered as a signatory of a group account called '+ str(first_name).upper() +' of phone number '+phone+'. Thank you'
					#send sms to chair
					to = urllib.urlencode({'DESTADDR':phone2,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)

				#SecretaryPhone
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone3+"'";
				result = cursor.execute(sql)
				db.commit()	
				db.close()
				#get member name
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				phonesql = 'Select FirstName from MembersMasterFile where CellPhone="'+phone3+'";'
				phoneresult = cursor.execute(phonesql)
				db.commit()
				db.close()
				rows = cursor.fetchall()
				for row in rows:
					name = str(row[0])
					#send message to customer
					ujumbe = 'Jambo '+ str(name.upper()) +', You have been registered as a signatory of a group account called '+ str(first_name).upper() +' of phone number '+phone+'. Thank you'
					#send sms to chair
					to = urllib.urlencode({'DESTADDR':phone3,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)
				'''	
				try:
					#ChairpersonPhone
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone1+"'";
					result = cursor.execute(sql)
					db.commit()	
					db.close()

					#TreasurerPhone
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone2+"'";
					result = cursor.execute(sql)
					db.commit()	
					db.close()

					#SecretaryPhone
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone3+"'";
					result = cursor.execute(sql)
					db.commit()	
					db.close()

					#Send Messages
					#send message to customer
					ujumbe = 'Jambo '+ str(name.upper()) +', You have been registered as a signatory of a group account called '+ str(first_name).upper() +' of phone number '+phone+'. Thank you'
					#send sms to chair
					to = urllib.urlencode({'DESTADDR':phone1,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)
					#send sms to treasurer
					to = urllib.urlencode({'DESTADDR':phone2,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)
					#send sms to secretary
					to = urllib.urlencode({'DESTADDR':phone3,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)
					print ujumbe
				except:
					pass
				'''

				print 'sending data to Pesaplus ....'
				print data
				try:
					postfields = urllib.urlencode(data)
					c = pycurl.Curl()
					c.setopt(pycurl.URL, url)
					c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
					c.setopt(pycurl.POST, 1)
					c.setopt(pycurl.POSTFIELDS, postfields)
					b = StringIO.StringIO();
					c.setopt(pycurl.WRITEFUNCTION, b.write)
					c.perform()
					ncServerData = b.getvalue()
					ncServerData = json.loads(ncServerData)
					print 'ncServerData ncServerData'
					print ncServerData
				except:
					pass	
				reply = json.dumps({'result':'Registration Successful!.'})
			except Exception, e:
				#raise e
				print e	
				pass		
				reply = json.dumps({'result':'Registration Failed. please try again later'})		
	else:
		#except Exception, e:
		reply = json.dumps({'result':'Failed. Technical error encountered, try again after 5 minutes'})
		pass
		#raise e		
	return HttpResponse(reply,mimetype)	

@csrf_exempt		
def addGroupClientAPITest(request):
	mimetype = 'application/javascript'
	##get IP of the sending phone
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	ip =''
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
	  ip = request.META.get('REMOTE_ADDR')

	if request.method == 'POST':
		data = request.POST		
	else:
		data = request.GET

	
	try:
		log = APILog()
		log.activity = str(data[0])
		log.save()
	except:
		pass

	print data
	leo = datetime.datetime.now()
	print 'now is'
	print leo

	first_name = 'Jhela test 4 Group'
	middle_name = ''
	fathers_name = ''
	sex = 'Male'
	idnumber = '444'
	phone = '0742371225'
	#profession = data['profession']
	income = '300000'
	try:
		group_type = 'Chama'
	except:
		group_type = ''
		pass
	#country = data['country']
	#county = data['county']
	subcounty = ''
	ward = '01'
	cluster = ''
	workstation = '01'
	try:
		subcounty = 'THIKA TOWN'
	except:
		pass	
	try:
		ward = 'JUNGLE HOLDINGS'
	except:
		pass
	try:
		workstation = data['cluster']
	except:
		pass

	phone1 = '0722531106'
	phone2 = '0725958948'
	phone3 = '0728294040'
	introducerphone = '0728294040'
	dob = '30-03-1974'	

	try:
		dob = time.strptime(dob, '%Y-%m-%d')
		dob = time.strftime("%Y-%m-%d",dob)
	except:
		try:
			dob = time.strptime(dob, '%d-%m-%Y')
			dob = time.strftime("%Y-%m-%d",dob)
		except:
			dob = time.strptime(dob, '%d/%m/%Y')
			dob = time.strftime("%Y-%m-%d",dob)

	if len(phone) == 10:
		phone = '254'+phone[1:]
	if len(phone1) == 10:
		phone1 = '254'+phone1[1:]
	if len(phone2) == 10:
		phone2 = '254'+phone2[1:]
	if len(phone3) == 10:
		phone3 = '254'+phone3[1:]
	if len(introducerphone) == 10:
		introducerphone = '254'+introducerphone[1:]
	title = '001'
	if sex == 'Male':
		title = '001'
		sex = 'MALE'
		gender = 'M'
	else:
		title = '002'
		sex = 'FEMALE'
		gender = 'F'
	day = datetime.datetime(1990, 1, 1)
	todaystr = str(day)
	todaystr = '1990-01-01'	
	a = True
	if a:
	#try:
		apidata = json.dumps({"phone":phone,"iphone":introducerphone,"idnumber":idnumber,"first_name":first_name,"fathers_name":fathers_name,"idnumber":idnumber})
		url = 'http://197.248.124.58/receive/jhela/member/'
				
		#Check ID number
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		idsql = 'Select * from MembersMasterFile where IDNumber="'+idnumber+'";'
		idresult = cursor.execute(idsql)
		db.commit()
		db.close()

		#Check phone number
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select * from MembersMasterFile where CellPhone="'+phone+'";'
		phoneresult = cursor.execute(phonesql)
		db.commit()
		db.close()

		#Check chairman
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select * from MembersMasterFile where CellPhone="'+phone1+'";'
		phoneresult1 = cursor.execute(phonesql)
		db.commit()
		db.close()

		#Check treasurer
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select * from MembersMasterFile where CellPhone="'+phone2+'";'
		phoneresult2 = cursor.execute(phonesql)
		db.commit()
		db.close
		#Check secretary
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select * from MembersMasterFile where CellPhone="'+phone3+'";'
		phoneresult3 = cursor.execute(phonesql)
		db.commit()
		db.close()

		#Check introducer phone number
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		introducersql = 'Select * from MembersMasterFile where CellPhone='+introducerphone+';'
		introducerresult = cursor.execute(introducersql)
		db.commit()
		db.close()

		data = {"phone":phone,"iphone":introducerphone,"idnumber":idnumber,"first_name":first_name,"fathers_name":fathers_name,"idnumber":idnumber,"username":"jhelaapi","password":"jhelaapi"}
		postfields = urllib.urlencode(data)
		#data = {"phone":phone,"iphone":introducerphone,"idnumber":idnumber,"first_name":first_name,"fathers_name":fathers_name,"idnumber":idnumber,"username":"jhelaapi","password":"jhelaapi"}
				
		if not introducerresult:
			postfields = urllib.urlencode(data)
			print 'Introducer Phone number is not registered with JHela'
			reply = json.dumps({'result':'Introducer Phone number is not registered with JHela'})		
		elif len(phone) != 12 :
			print 'phone number has less characters'
			print phone
			reply = json.dumps({'result':'Failed. Phone number has less characters'})
		elif len(phone1) != 12 :
			print 'phone1 has less characters'
			print phone1
			reply = json.dumps({'result':"Failed. Chairman's phone number has less characters"})
		elif len(phone2) != 12:
			print 'phone2 has less characters'
			print phone2
			reply = json.dumps({'result':"Failed. Treasurer's phone number has less characters"})
		elif len(phone3) != 12 :
			print 'phone2 has less characters'
			print phone3
			reply = json.dumps({'result':"Failed. Secretary's phone number has less characters"})
		elif not phoneresult1:
			reply = json.dumps({'result':'The chairman is not a J-Hela member. Please confirm phone number and try again'})
		elif not phoneresult2:
			reply = json.dumps({'result':'The treasurer is not a J-Hela member. Please confirm phone number and try again'})
		elif not phoneresult3:
			reply = json.dumps({'result':'The secretary is not a J-Hela mmeber. Please confirm phone number and try again'})
		elif not phoneresult:
			postfields = urllib.urlencode(data)
			print 'member is already registered in finextreme; reaalyy?'
			try:
				reply = json.dumps({'result':'< Phone number > has already been registered'})
				c = pycurl.Curl()
				c.setopt(pycurl.URL, url)
				c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
				c.setopt(pycurl.POST, 1)
				c.setopt(pycurl.POSTFIELDS, postfields)
				b = StringIO.StringIO();
				c.setopt(pycurl.WRITEFUNCTION, b.write)
				c.perform()
				ncServerData = b.getvalue()
				ncServerData = json.loads(ncServerData)
				print ncServerData
				print 'ncServerData ncServerData'
			except:
				reply = json.dumps({'result':'Phone number has already been registered'})
				pass	
			reply = json.dumps({'result':'Phone number has already been registered'})
		elif not idresult:
			reply = json.dumps({'result':'ID number has already been registered'})		
		else:
			try:				
				#Register client
				print 'Registering client ....'
				try:
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,IDNumber,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,DOB,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,income,GroupType) VALUES ('001','"+title+"','"+first_name+"','"+fathers_name+"','"+middle_name+"','"+phone+"','000','001','000','"+phone+"','"+idnumber+"','"+sex+"','"+ward+"','"+subcounty+"','"+phone+"','"+phone+"','"+introducerphone+"','"+workstation+"','"+dob+"',CURDATE(),CURDATE(),'system','002','New Member','000','"+income+"','"+group_type+"');"
					print sql
					result = cursor.execute(sql)
					db.commit()	
					db.close()
				except:
					pass
					#workstation update
					'''workstation = '0' + workstation
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,IDNumber,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,DOB,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,income,GroupType) VALUES ('001','"+title+"','"+first_name+"','"+fathers_name+"','"+middle_name+"','"+phone+"','000','001','000','"+phone+"','"+idnumber+"','"+sex+"','"+ward+"','"+subcounty+"','"+phone+"','"+phone+"','"+introducerphone+"','"+workstation+"','"+dob+"',CURDATE(),CURDATE(),'system','002','New Member','000','"+income+"','"+group_type+"');"
					print sql
					result = cursor.execute(sql)
					db.commit()	
					db.close()'''

				#Register in MicroFinanceMasterFile
				print 'Registering MicroFinance Group ....'
				#Get phone number
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				phonesql = 'Select MemId, FirstName, SalaryAccount from MembersMasterFile where CellPhone='+phone+' LIMIT 1;'
				phoneresult = cursor.execute(phonesql)
				db.commit()
				db.close()

				rows = cursor.fetchall()
				for row in rows:
				    MemId = str(row[0])
				    FirstName = str(row[1])	
				    SalaryAccount = str(row[2])	

				address  = ward + ' ,' + subcounty	
				try:
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "INSERT INTO MicroFinanceMasterFile (GroupName,Address,WorkStationCode,GroupNo,Description,GroupAccount) VALUES ('"+first_name+"','"+address+"','"+workstation+"','"+MemId+"','"+group_type+"','"+SalaryAccount+"');"
					print sql
					result = cursor.execute(sql)
					db.commit()	
					db.close()
				except:
					try:
						#workstation update
						workstation = '0' + workstation
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						sql = "INSERT INTO MicroFinanceMasterFile (GroupName,Address,WorkStationCode,GroupNo,Description,GroupAccount) VALUES ('"+first_name+"','"+address+"','"+workstation+"','"+MemId+"','"+group_type+"','"+SalaryAccount+"');"
						print sql
						result = cursor.execute(sql)
						db.commit()	
						db.close()
					except:
						pass

				#Register Signatories
				print 'Registering Signatories ....'
				try:
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "INSERT INTO Signatories (MasterFileId,ChairpersonPhone,TreasurerPhone,SecretaryPhone) VALUES ('"+MemId+"', '"+phone1+"','"+phone2+"','"+phone3+"',CURDATE());"
					print sql
					result = cursor.execute(sql)
					db.commit()	
					db.close()
				except:
					pass	
										
				print 'Link officials to group  ....'
				#ChairpersonPhone
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone1+"'";
				print sql
				result = cursor.execute(sql)
				db.commit()	
				db.close()
				#get member name
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				phonesql = 'Select FirstName from MembersMasterFile where CellPhone="'+phone1+'";'
				phoneresult = cursor.execute(phonesql)
				db.commit()
				db.close()
				rows = cursor.fetchall()
				for row in rows:
					name = str(row[0])
					#send message to customer
					ujumbe = 'Jambo '+ str(name.upper()) +', You have been registered as a signatory of a group account called '+ str(first_name).upper() +' of phone number '+phone+'. Thank you'
					#send sms to chair
					to = urllib.urlencode({'DESTADDR':phone1,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)


				#TreasurerPhone
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone2+"'";
				result = cursor.execute(sql)
				db.commit()	
				db.close()
				#get member name
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				phonesql = 'Select FirstName from MembersMasterFile where CellPhone="'+phone2+'";'
				phoneresult = cursor.execute(phonesql)
				db.commit()
				db.close()
				rows = cursor.fetchall()
				for row in rows:
					name = str(row[0])
					#send message to customer
					ujumbe = 'Jambo '+ str(name.upper()) +', You have been registered as a signatory of a group account called '+ str(first_name).upper() +' of phone number '+phone+'. Thank you'
					#send sms to chair
					to = urllib.urlencode({'DESTADDR':phone2,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)

				#SecretaryPhone
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone3+"'";
				result = cursor.execute(sql)
				db.commit()	
				db.close()
				#get member name
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				phonesql = 'Select FirstName from MembersMasterFile where CellPhone="'+phone3+'";'
				phoneresult = cursor.execute(phonesql)
				db.commit()
				db.close()
				rows = cursor.fetchall()
				for row in rows:
					name = str(row[0])
					#send message to customer
					ujumbe = 'Jambo '+ str(name.upper()) +', You have been registered as a signatory of a group account called '+ str(first_name).upper() +' of phone number '+phone+'. Thank you'
					#send sms to chair
					to = urllib.urlencode({'DESTADDR':phone3,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)

				'''
				try:
					#ChairpersonPhone
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone1+"'";
					result = cursor.execute(sql)
					db.commit()	
					db.close()

					#TreasurerPhone
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone2+"'";
					result = cursor.execute(sql)
					db.commit()	
					db.close()

					#SecretaryPhone
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone3+"'";
					result = cursor.execute(sql)
					db.commit()	
					db.close()

					#Send Messages
					#send message to customer
					ujumbe = 'Jambo '+ str(name.upper()) +', You have been registered as a signatory of a group account called '+ str(first_name).upper() +' of phone number '+phone+'. Thank you'
					#send sms to chair
					to = urllib.urlencode({'DESTADDR':phone1,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)
					#send sms to treasurer
					to = urllib.urlencode({'DESTADDR':phone2,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)
					#send sms to secretary
					to = urllib.urlencode({'DESTADDR':phone3,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)
					print ujumbe
				except:
					pass
				'''

				print 'sending data to Pesaplus ....'
				print data
				try:
					postfields = urllib.urlencode(data)
					c = pycurl.Curl()
					c.setopt(pycurl.URL, url)
					c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
					c.setopt(pycurl.POST, 1)
					c.setopt(pycurl.POSTFIELDS, postfields)
					b = StringIO.StringIO();
					c.setopt(pycurl.WRITEFUNCTION, b.write)
					c.perform()
					ncServerData = b.getvalue()
					ncServerData = json.loads(ncServerData)
					print 'ncServerData ncServerData'
					print ncServerData
				except:
					pass	
				reply = json.dumps({'result':'Registration Successful!.'})
			except Exception, e:
				#raise e
				print e	
				pass		
				reply = json.dumps({'result':'Registration Failed. please try again later'})		
	else:
		#except Exception, e:
		reply = json.dumps({'result':'Failed. Technical error encountered, try again after 5 minutes'})
		pass
		#raise e		
	return HttpResponse(reply,mimetype)	

@csrf_exempt		
def addCorporateClientAPI2(request):
	mimetype = 'application/javascript'
	##get IP of the sending phone
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	ip =''
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
	  ip = request.META.get('REMOTE_ADDR')

	if request.method == 'POST':
		data = request.POST		
	else:
		data = request.GET

	try:
		log = APILog()
		log.activity = str(data[0])
		log.save()
	except:
		pass

	print data
	leo = datetime.datetime.now()
	print 'now is'
	print leo

	first_name = data['group_name']
	middle_name = ''
	fathers_name = ''
	sex = 'Male'
	idnumber = data['regnumber']
	phone = data['phone'].strip()
	#profession = data['profession']
	income = data['income']
	try:
		group_type = data['group_type']
	except:
		group_type = ''
		pass
	#country = data['country']
	#county = data['county']
	subcounty = ''
	ward = '01'
	cluster = ''
	workstation = '01'
	try:
		subcounty = data['subcounty']
	except:
		pass	
	try:
		ward = data['ward']
	except:
		pass
	try:
		workstation = data['cluster']
	except:
		pass
	phone1 = data['phone1'].strip()
	phone2 = data['phone2'].strip()
	phone3 = data['phone3']
	introducerphone = data['introducerphone'].strip()
	dob = data['dateofbirth']	

	try:
		dob = time.strptime(dob, '%Y-%m-%d')
		dob = time.strftime("%Y-%m-%d",dob)
	except:
		try:
			dob = time.strptime(dob, '%d-%m-%Y')
			dob = time.strftime("%Y-%m-%d",dob)
		except:
			dob = time.strptime(dob, '%d/%m/%Y')
			dob = time.strftime("%Y-%m-%d",dob)

	if len(phone) == 10:
		phone = '254'+phone[1:]
	if len(phone1) == 10:
		phone1 = '254'+phone1[1:]
	if len(phone2) == 10:
		phone2 = '254'+phone2[1:]
	if len(phone3) == 10:
		phone3 = '254'+phone3[1:]
	if len(introducerphone) == 10:
		introducerphone = '254'+introducerphone[1:]
	title = '001'
	if sex == 'Male':
		title = '001'
		sex = 'MALE'
		gender = 'M'
	else:
		title = '002'
		sex = 'FEMALE'
		gender = 'F'
	day = datetime.datetime(1990, 1, 1)
	todaystr = str(day)
	todaystr = '1990-01-01'	
	a = True
	if a:
	#try:
		apidata = json.dumps({"phone":phone,"iphone":introducerphone,"idnumber":idnumber,"first_name":first_name,"fathers_name":fathers_name,"idnumber":idnumber})
		url = 'http://197.248.124.58/receive/jhela/member/'
				
		#Check ID number
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		idsql = 'Select * from MembersMasterFile where IDNumber="'+idnumber+'";'
		idresult = cursor.execute(idsql)
		db.commit()
		db.close()

		#Check phone number
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select * from MembersMasterFile where CellPhone="'+phone+'";'
		phoneresult = cursor.execute(phonesql)
		db.commit()
		db.close()

		#Check chairman
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select * from MembersMasterFile where CellPhone="'+phone1+'";'
		phoneresult1 = cursor.execute(phonesql)
		db.commit()
		db.close()

		#Check treasurer
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select * from MembersMasterFile where CellPhone="'+phone2+'";'
		phoneresult2 = cursor.execute(phonesql)
		db.commit()
		db.close
		#Check secretary
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select * from MembersMasterFile where CellPhone="'+phone3+'";'
		phoneresult3 = cursor.execute(phonesql)
		db.commit()
		db.close()

		#Check introducer phone number
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		introducersql = 'Select * from MembersMasterFile where CellPhone='+introducerphone+';'
		introducerresult = cursor.execute(introducersql)
		db.commit()
		db.close()

		data = {"phone":phone,"iphone":introducerphone,"idnumber":idnumber,"first_name":first_name,"fathers_name":fathers_name,"idnumber":idnumber,"username":"jhelaapi","password":"jhelaapi"}
		postfields = urllib.urlencode(data)
		#data = {"phone":phone,"iphone":introducerphone,"idnumber":idnumber,"first_name":first_name,"fathers_name":fathers_name,"idnumber":idnumber,"username":"jhelaapi","password":"jhelaapi"}
				
		if not introducerresult:
			postfields = urllib.urlencode(data)
			print 'Introducer Phone number is not registered with JHela'
			reply = json.dumps({'result':'Introducer Phone number is not registered with JHela'})		
		elif len(phone) != 12 :
			print 'phone number has less characters'
			print phone
			reply = json.dumps({'result':'Failed. Phone number has less characters'})
		elif len(phone1) != 12 :
			print 'phone1 has less characters'
			print phone1
			reply = json.dumps({'result':"Failed. Chairman's phone number has less characters"})
		elif len(phone2) != 12:
			print 'phone2 has less characters'
			print phone2
			reply = json.dumps({'result':"Failed. Treasurer's phone number has less characters"})
		elif len(phone3) != 12 :
			print 'phone2 has less characters'
			print phone3
			reply = json.dumps({'result':"Failed. Secretary's phone number has less characters"})
		elif not phoneresult1:
			reply = json.dumps({'result':'The chairman is not a J-Hela member. Please confirm phone number and try again'})
		elif not phoneresult2:
			reply = json.dumps({'result':'The treasurer is not a J-Hela member. Please confirm phone number and try again'})
		elif not phoneresult3:
			reply = json.dumps({'result':'The secretary is not a J-Hela mmeber. Please confirm phone number and try again'})
		elif phoneresult:
			postfields = urllib.urlencode(data)
			print 'member is already registered in finextreme'
			try:
				#Get phone number
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				phonesql = 'Select MemId, FirstName, SalaryAccount from MembersMasterFile where CellPhone='+phone+' LIMIT 1;'
				phoneresult = cursor.execute(phonesql)
				db.commit()
				db.close()
				
				rows = cursor.fetchall()
				for row in rows:
				    MemId = str(row[0])
				    FirstName = str(row[1])	
				    SalaryAccount = str(row[2])	

				#Check if this group had been registered
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				registeredsql = 'Select * from MicroFinanceMasterFile where GroupNo='+MemId+';'
				registeredresult = cursor.execute(registeredsql)
				db.commit()
				db.close()

				if not registeredresult:
					address  = ward + ' ,' + subcounty	
					try:
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						sql = "INSERT INTO MicroFinanceMasterFile (GroupName,Address,WorkStationCode,GroupNo,Description,GroupAccount) VALUES ('"+first_name+"','"+address+"','"+workstation+"','"+MemId+"','"+group_type+"','"+SalaryAccount+"');"
						print sql
						result = cursor.execute(sql)
						db.commit()	
						db.close()
					except:
						#workstation update
						workstation = '0' + workstation
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						sql = "INSERT INTO MicroFinanceMasterFile (GroupName,Address,WorkStationCode,GroupNo,Description,GroupAccount) VALUES ('"+first_name+"','"+address+"','"+workstation+"','"+MemId+"','"+group_type+"','"+SalaryAccount+"');"
						print sql
						result = cursor.execute(sql)
						db.commit()	
						db.close()

					#Register Signatories
					#changed to only one signatory
					print 'Registering Signatories ....'
					try:
						db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
						cursor = db.cursor()
						sql = "INSERT INTO Signatories (MasterFileId,ChairpersonPhone,TreasurerPhone,SecretaryPhone) VALUES ('"+MemId+"', '"+phone1+"','"+phone2+"','"+phone3+"',CURDATE());"
						print sql
						result = cursor.execute(sql)
						db.commit()	
						db.close()
					except:
						pass

					print 'Link officials to group  ....'
					#ChairpersonPhone
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone1+"'";
					print sql
					result = cursor.execute(sql)
					db.commit()	
					db.close()
					#get member name
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					phonesql = 'Select FirstName from MembersMasterFile where CellPhone="'+phone1+'";'
					phoneresult = cursor.execute(phonesql)
					db.commit()
					db.close()
					rows = cursor.fetchall()
					for row in rows:
						name = str(row[0])
						#send message to customer
						ujumbe = 'Jambo '+ str(name.upper()) +', You have been registered as a signatory of a group account called '+ str(first_name).upper() +' of phone number '+phone+'. Thank you'
						#send sms to chair
						to = urllib.urlencode({'DESTADDR':phone1,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
						url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
						urllib2.urlopen(url)

					#TreasurerPhone
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone2+"'";
					result = cursor.execute(sql)
					db.commit()	
					db.close()
					#get member name
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					phonesql = 'Select FirstName from MembersMasterFile where CellPhone="'+phone2+'";'
					phoneresult = cursor.execute(phonesql)
					db.commit()
					db.close()
					rows = cursor.fetchall()
					for row in rows:
						name = str(row[0])
						#send message to customer
						ujumbe = 'Jambo '+ str(name.upper()) +', You have been registered as a signatory of a group account called '+ str(first_name).upper() +' of phone number '+phone+'. Thank you'
						#send sms to chair
						to = urllib.urlencode({'DESTADDR':phone2,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
						url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
						urllib2.urlopen(url)

					#SecretaryPhone
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone3+"'";
					result = cursor.execute(sql)
					db.commit()	
					db.close()
					#get member name
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					phonesql = 'Select FirstName from MembersMasterFile where CellPhone="'+phone3+'";'
					phoneresult = cursor.execute(phonesql)
					db.commit()
					db.close()
					rows = cursor.fetchall()
					for row in rows:
						name = str(row[0])
						#send message to customer
						ujumbe = 'Jambo '+ str(name.upper()) +', You have been registered as a signatory of a group account called '+ str(first_name).upper() +' of phone number '+phone+'. Thank you'
						#send sms to chair
						to = urllib.urlencode({'DESTADDR':phone3,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
						url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
						urllib2.urlopen(url)				

				reply = json.dumps({'result':'Phone number has already been registered'})
				c = pycurl.Curl()
				c.setopt(pycurl.URL, url)
				c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
				c.setopt(pycurl.POST, 1)
				c.setopt(pycurl.POSTFIELDS, postfields)
				b = StringIO.StringIO();
				c.setopt(pycurl.WRITEFUNCTION, b.write)
				c.perform()
				ncServerData = b.getvalue()
				ncServerData = json.loads(ncServerData)
				print ncServerData
				print 'ncServerData ncServerData'
			except:
				reply = json.dumps({'result':'Phone number has already been registered'})
				pass	
			reply = json.dumps({'result':'Phone number has already been registered'})
		elif idresult:
			reply = json.dumps({'result':'ID number has already been registered'})		
		else:
			try:				
				#Register client
				print 'Registering client ....'
				try:
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,IDNumber,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,DOB,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,income,GroupType) VALUES ('001','"+title+"','"+first_name+"','"+fathers_name+"','"+middle_name+"','"+phone+"','000','001','000','"+phone+"','"+idnumber+"','"+sex+"','"+ward+"','"+subcounty+"','"+phone+"','"+phone+"','"+introducerphone+"','"+workstation+"','"+dob+"',CURDATE(),CURDATE(),'system','002','New Member','000','"+income+"','"+group_type+"');"
					print sql
					result = cursor.execute(sql)
					db.commit()	
					db.close()
				except:
					#workstation update
					print 'avoiding SQL Injection after except'
					workstation = '0' + workstation
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,IDNumber,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,DOB,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,income,GroupType) VALUES ('001','"+title+"','"+first_name+"','"+fathers_name+"','"+middle_name+"','"+phone+"','000','001','000','"+phone+"','"+idnumber+"','"+sex+"','"+ward+"','"+subcounty+"','"+phone+"','"+phone+"','"+introducerphone+"','"+workstation+"','"+dob+"',CURDATE(),CURDATE(),'system','002','New Member','000','"+income+"','"+group_type+"');"
					print sql
					result = cursor.execute(sql)
					db.commit()	
					db.close()

				isSalaryAccount = True
				i = 0

				while isSalaryAccount:
					SalaryAccount = ''
					#Register in MicroFinanceMasterFile
					print 'Registering MicroFinance Group ....'
					#Get phone number
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					phonesql = 'Select MemId, FirstName, SalaryAccount from MembersMasterFile where CellPhone='+phone+' LIMIT 1;'
					phoneresult = cursor.execute(phonesql)
					db.commit()
					db.close()
					
					rows = cursor.fetchall()
					for row in rows:
					    MemId = str(row[0])
					    FirstName = str(row[1])	
					    SalaryAccount = str(row[2])	

					if SalaryAccount == 'None' or SalaryAccount == '':
						isSalaryAccount = False
						if i == 0:
							#send message to applicant, inform them of delay
							ujumbe = 'Jambo , You J-Hela group registration request has been received and is being processed. Kindly wait completion. Thank you'
							#send sms to chair
							to = urllib.urlencode({'DESTADDR':phone,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
							url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
							urllib2.urlopen(url)
					i = i + 1

				address  = ward + ' ,' + subcounty	
				try:
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "INSERT INTO MicroFinanceMasterFile (GroupName,Address,WorkStationCode,GroupNo,Description,GroupAccount) VALUES ('"+first_name+"','"+address+"','"+workstation+"','"+MemId+"','"+group_type+"','"+SalaryAccount+"');"
					print sql
					result = cursor.execute(sql)
					db.commit()	
					db.close()
				except:
					#workstation update
					workstation = '0' + workstation
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "INSERT INTO MicroFinanceMasterFile (GroupName,Address,WorkStationCode,GroupNo,Description,GroupAccount) VALUES ('"+first_name+"','"+address+"','"+workstation+"','"+MemId+"','"+group_type+"','"+SalaryAccount+"');"
					print sql
					result = cursor.execute(sql)
					db.commit()	
					db.close()

				#Register Signatories
				#changed to only one signatory
				print 'Registering Signatories ....'
				try:
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "INSERT INTO Signatories (MasterFileId,ChairpersonPhone,TreasurerPhone,SecretaryPhone) VALUES ('"+MemId+"', '"+phone1+"','"+phone2+"','"+phone3+"',CURDATE());"
					print sql
					result = cursor.execute(sql)
					db.commit()	
					db.close()
				except:
					pass

				print 'Link officials to group  ....'
				print 'Link officials to group  ....'
				#ChairpersonPhone
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone1+"'";
				print sql
				result = cursor.execute(sql)
				db.commit()	
				db.close()
				#get member name
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				phonesql = 'Select FirstName from MembersMasterFile where CellPhone="'+phone1+'";'
				phoneresult = cursor.execute(phonesql)
				db.commit()
				db.close()
				rows = cursor.fetchall()
				for row in rows:
					name = str(row[0])
					#send message to customer
					ujumbe = 'Jambo '+ str(name.upper()) +', You have been registered as a signatory of a group account called '+ str(first_name).upper() +' of phone number '+phone+'. Thank you'
					#send sms to chair
					to = urllib.urlencode({'DESTADDR':phone1,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)


				#TreasurerPhone
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone2+"'";
				result = cursor.execute(sql)
				db.commit()	
				db.close()
				#get member name
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				phonesql = 'Select FirstName from MembersMasterFile where CellPhone="'+phone2+'";'
				phoneresult = cursor.execute(phonesql)
				db.commit()
				db.close()
				rows = cursor.fetchall()
				for row in rows:
					name = str(row[0])
					#send message to customer
					ujumbe = 'Jambo '+ str(name.upper()) +', You have been registered as a signatory of a group account called '+ str(first_name).upper() +' of phone number '+phone+'. Thank you'
					#send sms to chair
					to = urllib.urlencode({'DESTADDR':phone2,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)

				#SecretaryPhone
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone3+"'";
				result = cursor.execute(sql)
				db.commit()	
				db.close()
				#get member name
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				phonesql = 'Select FirstName from MembersMasterFile where CellPhone="'+phone3+'";'
				phoneresult = cursor.execute(phonesql)
				db.commit()
				db.close()
				rows = cursor.fetchall()
				for row in rows:
					name = str(row[0])
					#send message to customer
					ujumbe = 'Jambo '+ str(name.upper()) +', You have been registered as a signatory of a group account called '+ str(first_name).upper() +' of phone number '+phone+'. Thank you'
					#send sms to chair
					to = urllib.urlencode({'DESTADDR':phone3,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)
				'''
				try:
					#ChairpersonPhone
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone1+"'";
					result = cursor.execute(sql)
					db.commit()	
					db.close()

					#TreasurerPhone
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone2+"'";
					result = cursor.execute(sql)
					db.commit()	
					db.close()

					#SecretaryPhone
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "UPDATE MembersMasterFile SET GroupNo='"+MemId+"',GroupId='"+MemId+"' WHERE CellPhone='"+phone3+"'";
					result = cursor.execute(sql)
					db.commit()	
					db.close()

					#Send Messages
					#send message to customer
					ujumbe = 'Jambo '+ str(name.upper()) +', You have been registered as a signatory of a group account called '+ str(first_name).upper() +' of phone number '+phone+'. Thank you'
					#send sms to chair
					to = urllib.urlencode({'DESTADDR':phone1,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)
					#send sms to treasurer
					to = urllib.urlencode({'DESTADDR':phone2,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)
					#send sms to secretary
					to = urllib.urlencode({'DESTADDR':phone3,'SOURCEADDR':'JungleMhela','MESSAGE':ujumbe,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)
					print ujumbe
				except:
					pass
				'''

				print 'sending data to Pesaplus ....'
				print data
				try:
					postfields = urllib.urlencode(data)
					c = pycurl.Curl()
					c.setopt(pycurl.URL, url)
					c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
					c.setopt(pycurl.POST, 1)
					c.setopt(pycurl.POSTFIELDS, postfields)
					b = StringIO.StringIO();
					c.setopt(pycurl.WRITEFUNCTION, b.write)
					c.perform()
					ncServerData = b.getvalue()
					ncServerData = json.loads(ncServerData)
					print 'ncServerData ncServerData'
					print ncServerData
				except:
					pass	
				reply = json.dumps({'result':'Registration Successful!.'})
			except Exception, e:
				#raise e
				print e	
				pass		
				reply = json.dumps({'result':'Registration Failed. please try again later'})		
	else:
		#except Exception, e:
		reply = json.dumps({'result':'Failed. Technical error encountered, try again after 5 minutes'})
		pass
		#raise e		
	return HttpResponse(reply,mimetype)	

@csrf_exempt		
def addCorporateClientAPI(request):
	mimetype = 'application/javascript'
	##get IP of the sending phone
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	ip =''
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
	  ip = request.META.get('REMOTE_ADDR')

	if request.method == 'POST':
		data = request.POST		
	else:
		data = request.GET

	try:
		log = APILog()
		log.activity = str(data[0])
		log.save()
	except:
		pass

	print data
	leo = datetime.datetime.now()
	print 'now is'
	print leo

	first_name = data['group_name']
	middle_name = ''
	fathers_name = ''
	sex = 'Male'
	idnumber = data['regnumber']
	phone = data['phone'].strip()
	#profession = data['profession']
	income = data['income']
	#country = data['country']
	#county = data['county']
	subcounty = ''
	ward = '01'
	cluster = ''
	workstation = '01'
	try:
		subcounty = data['subcounty']
	except:
		pass	
	try:
		ward = data['ward']
	except:
		pass
	try:
		workstation = data['cluster']
	except:
		pass
	phone1 = data['phone1'].strip()
	#phone2 = data['phone2'].strip()
	#phone3 = data['phone3']
	introducerphone = data['introducerphone'].strip()
	dob = data['dateofbirth']	

	try:
		dob = time.strptime(dob, '%Y-%m-%d')
		dob = time.strftime("%Y-%m-%d",dob)
	except:
		dob = time.strptime(dob, '%d-%m-%Y')
		dob = time.strftime("%Y-%m-%d",dob)

	if len(phone) == 10:
		phone = '254'+phone[1:]
	if len(phone1) == 10:
		phone1 = '254'+phone1[1:]
		#if len(phone2) == 10:
		#	phone2 = '254'+phone2[1:]
		#if len(phone3) == 10:
		#	phone3 = '254'+phone3[1:]
	if len(introducerphone) == 10:
		introducerphone = '254'+introducerphone[1:]
	title = '001'
	if sex == 'Male':
		title = '001'
		sex = 'MALE'
		gender = 'M'
	else:
		title = '002'
		sex = 'FEMALE'
		gender = 'F'
	day = datetime.datetime(1990, 1, 1)
	todaystr = str(day)
	todaystr = '1990-01-01'	
	try:
		apidata = json.dumps({"phone":phone,"iphone":introducerphone,"idnumber":idnumber,"first_name":first_name,"fathers_name":fathers_name,"idnumber":idnumber})
		url = 'http://197.248.124.58/receive/jhela/member/'
				
		#Check ID number
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		idsql = 'Select * from MembersMasterFile where IDNumber="'+idnumber+'";'
		idresult = cursor.execute(idsql)
		db.commit()
		db.close()

		#Check phone number
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select * from MembersMasterFile where CellPhone="'+phone+'";'
		phoneresult = cursor.execute(phonesql)
		db.commit()
		db.close()

		#Check chairman
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select * from MembersMasterFile where CellPhone="'+phone1+'";'
		phoneresult1 = cursor.execute(phonesql)
		db.commit()
		db.close()

		#Check treasurer
		'''db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select * from MembersMasterFile where CellPhone="'+phone2+'";'
		phoneresult2 = cursor.execute(phonesql)
		db.commit()
		db.close'''
		#Check secretary
		'''db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select * from MembersMasterFile where CellPhone="'+phone3+'";'
		phoneresult3 = cursor.execute(phonesql)
		db.commit()
		db.close()'''

		data = {"phone":phone,"iphone":introducerphone,"idnumber":idnumber,"first_name":first_name,"fathers_name":fathers_name,"idnumber":idnumber,"username":"jhelaapi","password":"jhelaapi"}
		
		#Check introducer phone number
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		introducersql = 'Select * from MembersMasterFile where CellPhone='+introducerphone+';'
		introducerresult = cursor.execute(introducersql)
		db.commit()
		db.close()

		if not introducerresult:
			postfields = urllib.urlencode(data)
			print 'Introducer Phone number is not registered with JHela'
			reply = json.dumps({'result':'Introducer Phone number is not registered with JHela'})
		elif len(phone) != 12 :
			print 'phone number has less characters'
			print phone
			reply = json.dumps({'result':'Failed. Phone number has less characters'})
		elif len(phone1) != 12 :
			print 'phone1 has less characters'
			print phone1
			reply = json.dumps({'result':"Failed. Signatory's phone number has less characters"})
			#elif len(phone2) < 10 :
			#print 'phone2 has less characters'
			#print phone2
			#reply = json.dumps({'result':"Failed. Second Signatory's phone number has less characters"})
			'''elif len(phone3) < 10 :
				print 'phone2 has less characters'
				print phone3
				reply = json.dumps({'result':"Failed. Secretary's phone number has less characters"})
			'''
		elif not phoneresult1:
			reply = json.dumps({'result':'The signatory is not a J-Hela member. Please confirm phone number and try again'})
			#elif not phoneresult2:
			#reply = json.dumps({'result':'The treasurer is not a J-Hela member. Please confirm phone number and try again'})
			#elif not phoneresult3:
			#	reply = json.dumps({'result':'The secretary is not a J-Hela mmeber. Please confirm phone number and try again'})
		elif phoneresult:
			postfields = urllib.urlencode(data)
			print 'member is already registered in finextreme'
			try:
				reply = json.dumps({'result':'Phone number has already been registered'})
				c = pycurl.Curl()
				c.setopt(pycurl.URL, url)
				c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
				c.setopt(pycurl.POST, 1)
				c.setopt(pycurl.POSTFIELDS, postfields)
				b = StringIO.StringIO();
				c.setopt(pycurl.WRITEFUNCTION, b.write)
				c.perform()
				ncServerData = b.getvalue()
				ncServerData = json.loads(ncServerData)
				print ncServerData
				print 'ncServerData ncServerData'
			except:
				reply = json.dumps({'result':'Phone number has already been registered'})
				pass	
			reply = json.dumps({'result':'Phone number has already been registered'})
		elif idresult:
			reply = json.dumps({'result':'ID number has already been registered'})		
		else:
			try:				
				#Register client
				print 'Registering client ....'
				try:
					print 'MAKOSA ....'
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,IDNumber,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,DOB,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,income) VALUES ('001','"+title+"','"+first_name+"','"+fathers_name+"','"+middle_name+"','"+phone+"','000','001','000','"+phone+"','"+idnumber+"','"+sex+"','"+ward+"','"+subcounty+"','"+phone+"','"+phone+"','"+introducerphone+"','"+workstation+"','"+dob+"',CURDATE(),CURDATE(),'system','002','New Member','000','"+income+"');"
					print sql
					result = cursor.execute(sql)
					db.commit()	
					db.close()
				except:
					#workstation update
					workstation = '0' + workstation
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "INSERT INTO MembersMasterFile (MemberTypeCode,TitleCode,FirstName,Surname,OtherNames,PayrollNo,EmployerCode,BranchCode,CategoryCode,MemberNo,IDNumber,MemberGender,HomeAddress,PresentAddress,PhoneNo,CellPhone,IntroducedBy,WorkStationCode,DOB,JoinDate,BOSAStatusDate,BOSAStatusLogUser,BOSAStatusCode,BOSAStatusComment,DesignationCode,income) VALUES ('001','"+title+"','"+first_name+"','"+fathers_name+"','"+middle_name+"','"+phone+"','000','001','000','"+phone+"','"+idnumber+"','"+sex+"','"+ward+"','"+subcounty+"','"+phone+"','"+phone+"','"+introducerphone+"','"+workstation+"','"+dob+"',CURDATE(),CURDATE(),'system','002','New Member','000','"+income+"');"
					print sql
					result = cursor.execute(sql)
					db.commit()	
					db.close()
				#Get phone number
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				phonesql = 'Select MemId, FirstName from MembersMasterFile where CellPhone='+phone+' LIMIT 1;'
				phoneresult = cursor.execute(phonesql)
				db.commit()
				db.close()
				rows = cursor.fetchall()
				for row in rows:
				    MemId = str(row[0])
				    FirstName = str(row[1])
				#Register Signatories
				#changed to only one signatory
				print 'Registering Signatories ....'
				try:
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					sql = "INSERT INTO Signatories (MasterFileId,ChairpersonPhone) VALUES ('"+MemId+"','"+phone1+"');"#ChairpersonPhone,TreasurerPhone,SecretaryPhone  #'"+phone1+"','"+phone2+"','"+phone2+"',CURDATE());"
					print sql
					result = cursor.execute(sql)
					db.commit()	
					db.close()
				except:
					pass
				print 'sending data to Pesaplus ....'
				print data
				try:
					postfields = urllib.urlencode(data)
					c = pycurl.Curl()
					c.setopt(pycurl.URL, url)
					c.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE','Accept: application/json'])
					c.setopt(pycurl.POST, 1)
					c.setopt(pycurl.POSTFIELDS, postfields)
					b = StringIO.StringIO();
					c.setopt(pycurl.WRITEFUNCTION, b.write)
					c.perform()
					ncServerData = b.getvalue()
					ncServerData = json.loads(ncServerData)
					print 'ncServerData ncServerData'
					print ncServerData
				except:
					pass
				reply = json.dumps({'result':'Registration Successful!.'})			
			except Exception, e:
				#raise e
				print e	
				pass		
				reply = json.dumps({'result':'Registration Failed. please try again later'})		
	except Exception, e:
		reply = json.dumps({'result':'Failed. Technical error encountered, try again after 5 minutes'})
		pass		
	return HttpResponse(reply,mimetype)	


#UPDATE Main.MembersMasterFile SET PhoneNo='072222222',CellPhone='072222222',EmployerCode='000-2547222222' WHERE CellPhone='254722221992';
def getWithAllCounties(request):
	#Check phone number
	db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
	cursor = db.cursor()
	phonesql = 'Select OrderOfEntry, AdministrativeUnitName from AdministrativeUnits where ParentCode=1;'
	phoneresult = cursor.execute(phonesql)
	db.commit()
	db.close()
	print phoneresult

	# Convert query to objects of key-value pairs 
	objects_list = []
	rows = cursor.fetchall()
	d = collections.OrderedDict()
	d['id'] = '999999'
	d['name'] = 'All Counties'
	objects_list.append(d)
	for row in rows:		
	    d = collections.OrderedDict()
	    d['id'] = row[0]
	    d['name'] = row[1]
	    objects_list.append(d)
	#create named array
	arraylist = {}
	arraylist['categories'] = objects_list
	#dump to json string
	json_string = json.dumps(arraylist)
	return HttpResponse(json_string)

def getWithAllSubCounties(request):
	parent = request.GET['id']
	db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
	cursor = db.cursor()
	phonesql = 'Select OrderOfEntry, AdministrativeUnitName from AdministrativeUnits where ParentCode='+parent+';'	
	phoneresult = cursor.execute(phonesql)
	db.commit()
	db.close()
	print phoneresult

	# Convert query to objects of key-value pairs 
	objects_list = []
	rows = cursor.fetchall()
	d = collections.OrderedDict()
	d['id'] = '999999'
	d['name'] = 'All Sub-Counties'
	objects_list.append(d)
	for row in rows:
	    d = collections.OrderedDict()
	    d['id'] = row[0]
	    d['name'] = row[1]
	    objects_list.append(d)
	#create named array
	arraylist = {}
	arraylist['categories'] = objects_list
	#dump to json string
	json_string = json.dumps(arraylist)
	return HttpResponse(json_string)

def getWithAllWards(request):
	parent = request.GET['id']
	db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
	cursor = db.cursor()
	phonesql = 'Select OrderOfEntry, AdministrativeUnitName from AdministrativeUnits where ParentCode='+parent+';'	
	phoneresult = cursor.execute(phonesql)
	db.commit()
	db.close()
	print phoneresult

	# Convert query to objects of key-value pairs 
	objects_list = []
	rows = cursor.fetchall()
	d = collections.OrderedDict()
	d['id'] = '999999'
	d['name'] = 'All Wards'
	objects_list.append(d)
	for row in rows:
	    d = collections.OrderedDict()
	    d['id'] = row[0]
	    d['name'] = row[1]
	    objects_list.append(d)
	#create named array
	arraylist = {}
	arraylist['categories'] = objects_list
	#dump to json string
	json_string = json.dumps(arraylist)
	return HttpResponse(json_string)


def getWithAllClusters(request):
	parent = request.GET['id']
	db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
	cursor = db.cursor()
	phonesql = 'Select WorkStationCode, WorkStationName from WorkStations where InsideAdministrativeUnit='+parent+';'	
	phoneresult = cursor.execute(phonesql)
	db.commit()
	db.close()
	print phoneresult
	# Convert query to objects of key-value pairs 
	objects_list = []
	rows = cursor.fetchall()
	d = collections.OrderedDict()
	d['id'] = '999999'
	d['name'] = 'All Clusters'
	objects_list.append(d)
	for row in rows:
	    d = collections.OrderedDict()
	    d['id'] = row[0]
	    d['name'] = row[1]
	    objects_list.append(d)
	#create named array
	arraylist = {}
	arraylist['categories'] = objects_list
	#dump to json string
	json_string = json.dumps(arraylist)
	return HttpResponse(json_string)
	
@csrf_exempt
def sendSMSAPI(request):
	if request.method == 'POST':
		data = request.POST		
	else:
		data = request.GET

	print data
	leo = datetime.datetime.now()
	print 'now is'
	print leo
	country = data['country']
	county = data['county']
	subcounty = data['subcounty']	
	ward = data['ward']
	cluster = data['cluster']
	message = data['message']
	print 'county'
	print county
	print 'subcounty'
	print subcounty
	print 'cluster'
	print cluster
	print 'ward'
	print ward
	print 'message'
	print message
	JungleMhela = 'JungleMhela'
	reply = json.dumps({'result':'Message not sent, contact system admin'})
	if cluster == '999999':		
		if ward == '999999':
			if subcounty == '999999':
				if county == '999999':
					print 'All counties'
					print 'select all workstations'
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					phonesql = 'Select CellPhone from MembersMasterFile;'	
					phoneresult = cursor.execute(phonesql)
					db.commit()
					db.close()
					print phoneresult
					rows = cursor.fetchall()
					i=0
					phones = ''
					for row in rows:
						phone = str(row[0])
						print phone
						if i==0:
							phones=phone
						else:
							phones = phones +','+phone
						i=i+1
					if (i >1):
						to = urllib.urlencode({'DESTADDR':phones,'SOURCEADDR':JungleMhela,'MESSAGE':message,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
						url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
						urllib2.urlopen(url)
					print 'those were all the records'
					print i
					msg = str(i)+' messages sent to J-Hela clients'
					reply = json.dumps({'result':msg})
				else:
					print 'select subcounties for this county'
					print 'All counties'
					print 'select all workstations'
					db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
					cursor = db.cursor()
					phonesql = 'Select MembersMasterFile.CellPhone,WorkStations.WorkStationCode,a.OrderOfEntry FROM MembersMasterFile, WorkStations,AdministrativeUnits a,AdministrativeUnits b WHERE MembersMasterFile.WorkStationCode=WorkStations.WorkStationCode AND WorkStations.InsideAdministrativeUnit = a.OrderOfEntry AND a.ParentCode = b.OrderOfEntry AND b.ParentCode = '+county+';'	
					phoneresult = cursor.execute(phonesql)
					db.commit()
					db.close()
					print phoneresult
					rows = cursor.fetchall()
					i=0
					for row in rows:
						phone = str(row[0])
						print phone
						if i==0:
							phones=phone
						else:
							phones = phones +','+phone
						i=i+1
					if (i >1):
						to = urllib.urlencode({'DESTADDR':phones,'SOURCEADDR':JungleMhela,'MESSAGE':message,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
						url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
						urllib2.urlopen(url)
					print 'those were all the records'
					print i
					msg = str(i)+' messages sent to J-Hela clients'
					reply = json.dumps({'result':msg})
			else:
				print 'select wards for this subcounty'
				db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
				cursor = db.cursor()
				phonesql = 'Select MembersMasterFile.CellPhone,WorkStations.WorkStationCode,a.OrderOfEntry FROM MembersMasterFile, WorkStations,AdministrativeUnits a WHERE MembersMasterFile.WorkStationCode=WorkStations.WorkStationCode AND WorkStations.InsideAdministrativeUnit = a.OrderOfEntry AND a.ParentCode = '+subcounty+';'	
				phoneresult = cursor.execute(phonesql)
				db.commit()
				db.close()
				print phoneresult
				rows = cursor.fetchall()
				i=0
				for row in rows:
					phone = str(row[0])
					print phone
					if i==0:
						phones=phone
					else:
						phones = phones +','+phone
					i=i+1
				if (i >1):
					to = urllib.urlencode({'DESTADDR':phones,'SOURCEADDR':JungleMhela,'MESSAGE':message,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
					url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
					urllib2.urlopen(url)
				print 'those were the wards records for the subcounty'
				msg = str(i)+' messages sent to J-Hela clients'
				reply = json.dumps({'result':msg})
		else:
			print 'select this ward'
			db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
			cursor = db.cursor()
			phonesql = 'Select MembersMasterFile.CellPhone,WorkStations.WorkStationCode FROM MembersMasterFile, WorkStations WHERE MembersMasterFile.WorkStationCode=WorkStations.WorkStationCode AND WorkStations.InsideAdministrativeUnit = '+ward+';'	
			phoneresult = cursor.execute(phonesql)
			db.commit()
			db.close()
			print phoneresult
			rows = cursor.fetchall()
			i=0
			phones=''
			for row in rows:
				phone = str(row[0])
				print phone
				if i==0:
					phones=phone
				else:
					phones = phones +','+phone
				i=i+1
			if (i >1):
				to = urllib.urlencode({'DESTADDR':phones,'SOURCEADDR':JungleMhela,'MESSAGE':message,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
				url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
				urllib2.urlopen(url)
			print i
			print 'those were the ward records'
			print ward
			msg = str(i)+' messages sent to J-Hela clients'
			reply = json.dumps({'result':msg})
	else:
		print 'select this cluster'
		db = MySQLdb.connect("localhost","root","UPKFA<72-(","Main" )
		cursor = db.cursor()
		phonesql = 'Select CellPhone from MembersMasterFile where WorkStationCode='+cluster+';'	
		phoneresult = cursor.execute(phonesql)
		db.commit()
		db.close()
		print phoneresult
		rows = cursor.fetchall()
		i=0
		phones=''
		for row in rows:
			phone = str(row[0])
			print phone
			if i==0:
				phones=phone
			else:
				phones = phones +','+phone
			i=i+1
		if (i>1):
			print 'numbers receiving the message'
			print phones
			to = urllib.urlencode({'DESTADDR':phones,'SOURCEADDR':JungleMhela,'MESSAGE':message,'USERNAME':'JungleMhela','PASSWORD':'fiHoKe'})
			url = 'http://sms.habary.co.ke/bulkMessages/api/bulkSMSapi.php?'+to
			urllib2.urlopen(url)
		print 'those were the cluster records'
		print i
		msg = str(i)+' messages sent to J-Hela clients'
		reply = json.dumps({'result':msg})
	return HttpResponse(reply)

'''
301 = Insufficient Credit
'''
@csrf_exempt
def testConfirmID(request):
	import re
	surname='NDUMIA'
	first_name='PETER'
	second_name='NDUNGU'
	national_id='10966995'
	name1 = surname
	name2 = first_name
	name3 = second_name
	name4 = '' 
	nationalID = national_id
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
 	print 'check CRB ....'
	product102 = client.service.getProduct102(username=username,password=password,code=code,infinityCode=infinityCode,nationalID=nationalID,name1=name1,name2=name2,name3=name3,reportReason=reportReason,reportSector=reportSector)
	print product102
	reply = str(product102.responseCode)
	print 'CRB FEEBACK'
	print reply
	if reply == '200' or reply == '203':
		print 'success'
		reply='300'
		'''if (name1 == personalProfile['surname'] and name2 == personalProfile['otherNames']):
			reply = 200
			print personalProfile['otherNames']			
			print 
		'''
		try:
			print product102
			print product102.responseCode
			print product102.header
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
			print personalProfile['surname']
			print personalProfile['otherNames']			
			print personalProfile['nationalID']
			print personalProfile['nationality']
			print personalProfile['gender']
			#print personalProfile['passportNo']
			print personalProfile['salutation']
			#print personalProfile['serviceID']	

			a = personalProfile['fullName']
			print "name1 searching .."
			print a
			print name1
			score=0
			matchObj = re.search(name1, a, re.M|re.I)
			if matchObj:
				print "matchObj.group() : ", matchObj.group()
				score = score + 1
			else:
			   print "name1 No match!!"

			print "name2 searching .."
			print a
			print name2
			matchObj = re.search(name2, a, re.M|re.I)
			if matchObj:
				print "matchObj.group() : ", matchObj.group()
				score = score + 1
			else:
			   print "name2 No match!!"

			print "name2 searching .."
			print a
			print name2
			matchObj = re.search(name3, a, re.M|re.I)
			if matchObj:
				print "matchObj.group() : ", matchObj.group()
				score = score + 1
			else:
			   print "name3 No match!!"

			if score > 1:
				reply='200'
		except:
			reply='300'
			pass
	else:
		print 'CRB check failed...'
		#product102 = client.service.getProduct102(username=username,password=password,code=code,infinityCode=infinityCode,nationalID=nationalID,name1=name1,reportReason=reportReason,reportSector=reportSector)
		#reply = str(product102.responseCode)
		reply='300'
		print reply
	return reply


def checkCreditWorthiness(request):
	from suds.client import Client
	import suds
	import urllib2
	import datetime

	# Credentials
	username = 'cX26K2W836QT8Up'
	password = 'D57Jc8SdsSJ1gAE'
	timeout = 200
	try:

		#location = "http://ws.crbws.transunion.ke.co"
		location = "https://secure3.transunionafrica.com/crbws/ke"
		#location = "https://secure3.crbafrica.com:443/crbws/ke"
		url = "https://secure3.transunionafrica.com/crbws/ke?wsdl"

		t = suds.transport.https.HttpAuthenticated(username=username, password=password)

		t.handler = urllib2.HTTPBasicAuthHandler(t.pm)
		t.urlopener = urllib2.build_opener(t.handler)

		client = suds.client.Client(url=url, location=location, timeout=timeout, transport=t)

		username = "WS_JML1"
		password = "Mptvzb"
		code = "2182"
		infinityCode = "1328KE46406"

		list_of_methods = [method for method in client.wsdl.services[0].ports[0].methods] 

		print list_of_methods[23]

		#print client.service

		name1 = 'VINCENT' #'VINCENT'#'Maina'
		name2 = 'MARABA' #'MARABA'#'PETER'
		name3 = '' #''#'KINUTHIA' 
		name4 = '' 
		nationalID = '24917521' #'24917521'#'24625040'
		passportNo = ''
		serviceID = ''
		alienID = '' 
		taxID = ''
		today = datetime.datetime.now()
		postalBoxNo = '' 
		postalTown = ''
		postalCountry = '' 
		reportSector = 2
		reportReason = 1

		product115 = client.service.getProduct115(username=username,password=password,code=code,infinityCode=infinityCode,name1=name1,name2=name2,name3=name3,nationalID=nationalID,reportReason=reportReason,reportSector=reportSector)

		#product102 = client.service.getProduct102(username,password,code,infinityCode,nationalID,serviceID,reportSector,reportReason)

		#reportSector=reportSector,
		print product115
		##print product102.responseCode
		##print product102.header

		header = product115.header
		personalProfile =  product115.personalProfile
		print product115.summary
		print product115.scoreOutput

		print 'score Output score Output'
		print product115.scoreOutput['grade']
		print product115.scoreOutput['positiveScore']

		grade = product115.scoreOutput['grade']
		positiveScore = product115.scoreOutput['positiveScore']
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
		#print personalProfile['dateOfBirth']
		#print personalProfile['drivingLicenseNo']
		print personalProfile['fullName']
		arraylist = {}
		arraylist['grade'] = grade
		arraylist['positiveScore'] = positiveScore
		reply = json.dumps(arraylist)
		print reply

		reply=json.loads(reply)

		print reply["grade"]
		print reply["positiveScore"]
	except:
		reply = ''
	return HttpResponse(reply)



################## @vincentmaraba@gmail.com the end :) ##########################################