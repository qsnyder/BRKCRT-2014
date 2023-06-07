import requests, json, urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings()

BASE_PATH = "https://10.10.20.48:443"
USER = "developer"
PASSWORD = "C1sco12345"
HEADERS = {'content-type': 'application/yang-data+json',
          'accept': 'application/yang-data+json'}


url = BASE_PATH + "/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet=2"
result = requests.get(url, auth=(USER, PASSWORD), headers=HEADERS, verify=False)
print(result.text)

payload = json.dumps({
  "Cisco-IOS-XE-native:GigabitEthernet": {
    "name": "2",
    "description": "Description updated by RESTCONF"
  }
})
url = BASE_PATH + "/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet"
result = requests.patch(url, auth=(USER, PASSWORD),
                        headers=HEADERS, verify=False, data=payload)
print(result.text)

url = BASE_PATH + "/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet=2"
result = requests.get(url, auth=(USER, PASSWORD), headers=HEADERS, verify=False)
print(result.text)