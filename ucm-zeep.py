from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport
from zeep.cache import SqliteCache
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cucm = 'cucm1.dcloud.cisco.com'
username = 'administrator'
passwd = 'dCloud123!'
WSDL_URL = 'file:///c:/DEVWKS-2019/axlsqltoolkit/schema/12.5/AXLAPI.wsdl'
CUCM_URL = 'https://'+cucm+':8443/axl/'

session = Session()
session.verify = False
session.auth = HTTPBasicAuth(username, passwd)
transport = Transport(session=session, timeout=10, cache=SqliteCache())

client = Client(WSDL_URL, transport=transport)
service = client.create_service("{http://www.cisco.com/AXLAPIService/}AXLAPIBinding", CUCM_URL)

# list tags that you want to see returned or else result is None
tags = {'pattern': '',
        'description': '',
        'usage': ''}

# Get a list of DNs returning the tags identified above
resp = service.listLine(searchCriteria={'pattern': '%'}, returnedTags=tags)
#print(resp)

linelist = resp['return'].line
for line in linelist:
    print(line.pattern, line.description, line.routePartitionName)
