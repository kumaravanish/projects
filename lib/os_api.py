#!/usr/bin/python
import os
import requests
from requests.exceptions import HTTPError
import json


class OSCommon:
    '''Class provides common methods for OS interations'''
    def __init__(self):
        try:
        #OS_SERVICE_TOKEN = os.environ['OS_SERVICE_TOKEN']
            self.OS_USERNAME = os.environ['OS_USERNAME']
            self.OS_PASSWORD = os.environ['OS_PASSWORD']
            self.OS_AUTH_URL = os.environ['OS_AUTH_URL']
            self.OS_PROJECT_NAME = os.environ['OS_PROJECT_NAME']
            self.OS_USER_DOMAIN_NAME = os.environ['OS_USER_DOMAIN_NAME']
            self.OS_PROJECT_DOMAIN_NAME = os.environ['OS_PROJECT_DOMAIN_NAME']
            self.OS_IDENTITY_API_VERSION = os.environ['OS_IDENTITY_API_VERSION']
            self.OS_NOVA_API_URL = os.environ['OS_NOVA_API_URL']
        except KeyError as err:
            print "KeyError: "+ str(err)
        except Exception as err:
            print "Error occured "+ str(err)

    def get_os_token(self):
        '''Method to issue keystone auth token''' 
        url = self.OS_AUTH_URL+'/auth/tokens?nocatalog'
        token_details = {}
        payload = { "auth": { "identity": { "methods": ["password"],"password": {"user": {"domain": {"name": self.OS_USER_DOMAIN_NAME},"name": self.OS_USERNAME, "password": self.OS_PASSWORD} } }, "scope": { "project": { "domain": { "name": self.OS_PROJECT_DOMAIN_NAME }, "name": self.OS_PROJECT_NAME} } }}
        headers = {'content-type': 'application/json'}
        try:
            resp = requests.post(url, data=json.dumps(payload), headers=headers)
            resp.raise_for_status()
        except HTTPError as http_err:
            print "HTTPError "+ str(http_err)
        except Exception as err:
            print "Error occured "+ str(err)
        data = resp.json()
        token_details['OS_SERVICE_TOKEN'] = resp.headers['X-Subject-Token']
        token_details['EXPIRY'] = data['token']['expires_at']
        token_details['OS_PROJECT_ID'] = data['token']['project']['id']
        return token_details

    def get_operation_url(self, url, headers):
        '''Method requests get operation and resturns response data'''
        try:
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except HTTPError as http_err:
            print "HTTPError "+ str(http_err)
        except Exception as err:
            print "Error occured "+ str(err)

class OSNovaApi(OSCommon):
    def __init__(self):
        OSCommon.__init__(self)
        self.OS_SERVICE_TOKEN = self.get_os_token()['OS_SERVICE_TOKEN']

    def get_flavors_details(self):
        '''Method returns complete flavor details in json'''
        token_details = self.get_os_token()
        token = token_details['OS_SERVICE_TOKEN']
        project_id = token_details['OS_PROJECT_ID']
        url = self.OS_NOVA_API_URL+'/'+project_id+'/flavors' 
        headers = {'X-Auth-Token': token}
        return self.get_operation_url(url, headers)

    def get_flavor_name_list(self):
        '''Method returns flavor list'''
        flavor_list = []
        for item in self.get_flavors_details()['flavors']:
            flavor_list.append(item['name'])
        return flavor_list
