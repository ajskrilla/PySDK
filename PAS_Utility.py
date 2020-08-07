import configparser
import os
import sys
import requests
import json
#module for the configReader

Config = configparser.ConfigParser()

if os.name == "posix":
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'config.config') 

elif os.name == "nt":
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'config.config')

try:
    isFile = os.path.isfile(desktop)

    if isFile == False:
        print("file is not there") 

except Exception as E:
    print(E)


Config = configparser.ConfigParser()
Config.read(desktop)
    
class tenant(object):
	tenant= ""
	def __init__(self):
		super(tenant, self).__init__()
		self.tenant = Config.get('Properties', 'Tenant')

 #!!!!Maybe make as a variable and not a class!!!!!       
class bearer_token(object):
    bearer_token= ""
    def __init__(self):
        super(bearer_token, self).__init__()
        self.bearer_token = Config.get('Properties', 'Bearer')
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

headers = {
    'X-CENTRIFY-NATIVE-CLIENT': 'true',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % bearer_token().bearer_token
    
}

class URL(object):
    def __init__(self, Call, Debug=False):
        tenantID = str(tenant().tenant)
        super(URL, self).__init__()
        self.URL = Call 
        self.new_url = str('{0}'.format(tenantID) + self.URL)



class Query_Request(object):
    def __init__(self, SQL, Debug=False):
        url = '%s/Redrock/Query' % tenant().tenant
        super(Query_Request, self).__init__()
        self.Query_Request = requests.post(url=url, headers=headers, json={"Script": SQL}).json()
        self.responseobject = self.Query_Request
        self.jsonlist = json.dumps(self.responseobject)
        self.parsed_json = (json.loads(self.jsonlist))

        if Debug == True:
            print(json.dumps(self.parsed_json, indent=4, sort_keys=True))

class Other_Request(object):
    def __init__(self,Call, Debug=False, **kwargs):
        tenantID = str(tenant().tenant)
        new_url = str('{0}'.format(tenantID)) + Call
        tenantID = str(tenant().tenant)
        super(Other_Request, self).__init__()
        self.kwargs = kwargs
        self.__dict__.update(**self.kwargs)
        self.String = str(self.kwargs)
        self.replace = self.String.replace("'", '"')
        self.Final_Body = json.loads(self.replace)
        self.Other_Request = requests.post(url=new_url, headers=headers, json=self.Final_Body).json()
        self.responseobject = self.Other_Request
        self.jsonlist = json.dumps(self.responseobject)
        self.parsed_json = (json.loads(self.jsonlist))

        if Debug == True:
            print(json.dumps(self.parsed_json, indent=4, sort_keys=True))

#Examples of how to use Utility Classes

#Query_Request(SQL = """SELECT Server.DomainId, Server.DomainName, Server.ID, Server.Name FROM Server""", Debug=True)#
#Call1 = URL(Call= "/ServerManage/AddResource").new_url
#Other_Request(Call="/ServerManage/AddResource",Debug= True, FQDN = "Gotem.net", ComputerClass= "Unix", \
    #Sessiontype= "Ssh", Description="Test", Name="test.test.net")


