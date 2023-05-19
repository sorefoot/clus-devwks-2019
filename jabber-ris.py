 
from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from lxml import etree
 
 
disable_warnings(InsecureRequestWarning)

# Cluster specific variables
server = 'cucm1.dcloud.cisco.com'
username = 'administrator'
password = 'dCloud123!'

wsdl = f'https://{server}:8443/realtimeservice2/services/RISService70?wsdl'
location = f'https://{server}:8443/realtimeservice2/services/RISService70'
binding = '{http://schemas.cisco.com/ast/soap}RisBinding'


session = Session()
session.verify = False
session.auth = HTTPBasicAuth(username, password)

transport = Transport(cache=SqliteCache(), session=session, timeout=20)
history = HistoryPlugin()
client = Client(wsdl=wsdl, transport=transport, plugins=[history])
service = client.create_service(binding, location)

def show_history():
    for hist in [history.last_sent, history.last_received]:
        print(etree.tostring(hist["envelope"], encoding="unicode", pretty_print=True))
CmSelectionCriteria = {
    'MaxReturnedDevices': '10',
    'DeviceClass': 'Phone',
    'Model': '503',
    'Status': 'Any',
    'NodeName': '',
    'SelectBy': 'Name',
    'SelectItems': {
        'item': '*'        
    },
    'Protocol': 'Any',
    'DownloadStatus': 'Any'
}

StateInfo = ''

try:
    resp = service.selectCmDevice(CmSelectionCriteria=CmSelectionCriteria, StateInfo=StateInfo)
except Fault:
    show_history()

print(resp)
