import os
import requests
from requests.exceptions import HTTPError
import json

env_list = ['OS_SERVICE_TOKEN', 'OS_USERNAME', 'OS_PASSWORD', 'OS_AUTH_URL', 'OS_PROJECT_NAME', 'OS_USER_DOMAIN_NAME', 'OS_PROJECT_DOMAIN_NAME', 'OS_IDENTITY_API_VERSION']

try:
    #OS_SERVICE_TOKEN = os.environ['OS_SERVICE_TOKEN']
    OS_USERNAME = os.environ['OS_USERNAME']
    OS_PASSWORD = os.environ['OS_PASSWORD']
    OS_AUTH_URL = os.environ['OS_AUTH_URL']
    OS_PROJECT_NAME = os.environ['OS_PROJECT_NAME']
    OS_USER_DOMAIN_NAME = os.environ['OS_USER_DOMAIN_NAME']
    OS_PROJECT_DOMAIN_NAME = os.environ['OS_PROJECT_DOMAIN_NAME']
    OS_IDENTITY_API_VERSION = os.environ['OS_IDENTITY_API_VERSION']
except KeyError as err:
    print "KeyError: "+ str(err)
except Exception as err:
    print "Error occured "+ str(err)

#print OS_USERNAME
url = OS_AUTH_URL+'/auth/tokens?nocatalog'

payload = { "auth": { "identity": { "methods": ["password"],"password": {"user": {"domain": {"name": OS_USER_DOMAIN_NAME},"name": OS_USERNAME, "password": OS_PASSWORD} } }, "scope": { "project": { "domain": { "name": OS_PROJECT_DOMAIN_NAME }, "name": OS_PROJECT_NAME} } }}

headers = {'content-type': 'application/json'}
#print json.dumps(payload)

try:
    resp = requests.post(url, data=json.dumps(payload), headers=headers)
    resp.raise_for_status()
except HTTPError as http_err:
    print "HTTPError "+ str(http_err)
except Exception as err:
    print "Error occured "+ str(err)

data = resp.json()
print "OS_SERVICE_TOKEN=" + resp.headers['X-Subject-Token']
print "Access Token Expiry:" + data['token']['expires_at']
print "OS Project Id:" + data['token']['project']['id']

#curl -s -H "X-Auth-Token: $OS_SERVICE_TOKEN" http://10.0.2.5:8774/v2/c257ebaec9774f9b93b9fcb3cbb6998b/flavors| python -m json.tool
