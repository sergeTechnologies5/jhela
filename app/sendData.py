
import pycurl, StringIO, json

postfields = "idnumber=MRG3654884&phone=254706971684&first_name=JJUNGLE+MURANGA+WANJENGI+CLUSTER&iphone=254722531106&username=jhelaapi&password=jhelaapi&is_group=yes&fathers_name=postfields"

url = 'http://197.248.124.58:8090/receive/jhela/member/'

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