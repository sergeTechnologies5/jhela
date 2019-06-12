import pycurl

postfields = {'idnumber': '29994785', 'phone': '254728408711', 'first_name': 'DAVID', 'iphone': '254722531106', 'username': 'jhelaapi', 'password': 'jhelaapi', 'is_group': 'no', 'fathers_name': 'NGANGA  NJOROGE'}

url = 'http://197.248.124.58/send/jhela/sms/'
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
