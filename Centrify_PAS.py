#PAS Module to install and test the functions/clases 8/18/2020

#importing the libraries
import traceback
import pandas
import configparser
import os
import re
import sys
import requests
import json
from pathlib import Path

pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)
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

#All Query Requests
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

#Other API calls
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

###Connector Check Class###
class Connector_Info(object):
	def __init__(self, Print=False, ExportPath=None):
		#Call_to_Tenant = URL(Call= "/Core/CheckProxyHealth").new_url
	
		try:
			Result = Other_Request(Call= "/Core/CheckProxyHealth").parsed_json
			print('Getting the Connectors...')
			print("\n")
			appended_data = []
			for i in range (len(Result["Result"]["Connectors"])):
				data = Result["Result"]["Connectors"][i]["ConnectorInfo"]
				keys, values = zip(*data.items())
				tupc = list(data.keys())
				tupr = data.keys()
				appended_data.append(values)	
			df = pandas.DataFrame(appended_data, columns=tupc)

			if Print == True:
				print("Current data of Connectors")
				print("\n")
				print(df)

			if ExportPath != None:
				if ".csv" in ExportPath:
					path = Path(ExportPath)
					df.to_csv(os.path.abspath(path))
					print('\n')
					print("Connector Status Saved to " + ExportPath)
				else:
					print('\n')
					print("Need to have file end in .csv")

		except Exception as E:

			traceback.print_exc()

#Query Function that creates tables and exports
def Query(SQLQuery,Print=False, ExportPath=None):

	try:
		
		realQuery = str(SQLQuery)
		print("SQL Query is: " + realQuery)
		print('\n')
		appended_data = []
		for i in range (len(Query_Request(SQL = realQuery).parsed_json["Result"]["Results"])):
			data = Query_Request(SQL = realQuery).parsed_json["Result"]["Results"][i]["Row"]
			keys, values = zip(*data.items())
			tupc = list(data.keys())
			tupr = data.keys()
			appended_data.append(values)	
		df = pandas.DataFrame(appended_data, columns=tupc)

		if Print == True:
			print(df)

		if ExportPath != None:
			if ".csv" in ExportPath:
				path = Path(ExportPath)
				df.to_csv(os.path.abspath(path))
				print('\n')
				print("Query Saved to " + ExportPath)
			else:
				print('\n')
				print("Need to have file end in .csv")

	except Exception as E:

		traceback.print_exc()

###Secret Management###
def Get_Secret(Secret):

	try:

		SecretQuery = """SELECT DataVault.SecretFileName, DataVault.SecretName, DataVault.ID \
		FROM DataVault WHERE DataVault.SecretName = '%s'""" % Secret

		if Query_Request(SQL = SecretQuery).parsed_json['Result']['Count'] != 0:
			ID = Query_Request(SQL = SecretQuery).parsed_json["Result"]["Results"][0]["Row"]['ID']
			r = Other_Request(Call = "/ServerManage/RetrieveSecretContents", ID = '%s' %ID)
			IDs = json.dumps(Other_Request(Call = "/ServerManage/RetrieveSecretContents", ID = '%s' \
				%ID).parsed_json['Result'], indent=4, sort_keys=True)
			print(IDs)

		else:
			print( "Secret Not Found")

	except Exception as E:

		print(E)


class Add_Secret(object):
	Call_to_Tenant_AS = URL(Call= "/ServerManage/AddSecret").new_url
	def __init__(self, **kwargs ):
		kwargs["Call"] = Call_to_Tenant_AS
		kwargs["Debug"] = True
		AS = Other_Request(**kwargs)

class Add_Secret_Folder(object):
	Call_to_Tenant_ASF = URL(Call= "/ServerManage/AddSecretsFolder").new_url

	def __init__(self, **kwargs ):
		kwargs["Call"] = Call_to_Tenant_ASF
		kwargs["Debug"] = True
		ASF = Other_Request(**kwargs)


class Delete_Secret(object):
	Call_to_Tenant_DS = URL(Call= "/ServerManage/DeleteSecret").new_url
	def __init__(self, Secret, **kwargs ):
		kwargs["ID"] = None
		try:

			SecretQuery = """SELECT DataVault.SecretFileName, DataVault.SecretName, DataVault.ID \
			FROM DataVault WHERE DataVault.SecretName = '%s'""" % Secret

			if Query_Request(SQL = SecretQuery).parsed_json['Result']['Count'] != 0:
				ID = Query_Request(SQL = SecretQuery).parsed_json["Result"]["Results"][0]["Row"]['ID']
				kwargs["ID"] = ID
				IDs = json.dumps(Other_Request(Call= "/ServerManage/DeleteSecret", Debug=True, **kwargs).parsed_json['Result'], indent=4, sort_keys=True)
				print(IDs)
			else:
				print( "Secret Not Found")

		except Exception as E:

			#Debug functionality!
			traceback.print_exc()

###System Management###
class Get_System(object):
		#if Result['Result']['Count'] != 0:

	def __init__(self, Name=None):

		try:

			if Name == None:
				SystemQuery = """SELECT Server.DomainId, Server.DomainName, Server.ID, Server.Name 
				FROM Server WHERE Server.Name LIKE '%'""" 
				Systems = Query_Request(SQL = SystemQuery).parsed_json

				for i in range (len(Systems["Result"]["Results"])):
					print("System Name: " + Systems["Result"]["Results"][i]["Row"]['Name'])
					print("System ID :" + Systems["Result"]["Results"][i]["Row"]['ID'])
					print("System Domain: " + Systems["Result"]["Results"][i]["Row"]['DomainName'])
					DiD = str(Systems["Result"]["Results"][i]["Row"]['DomainId'])
					print("Domain ID: " + DiD)
					print('\n')

			if Name != None:
				SystemQuery = """SELECT Server.DomainId, Server.DomainName, Server.ID, Server.Name 
				FROM Server WHERE Server.Name = '%s'""" % Name

				Systems = Query_Request(SQL = SystemQuery).parsed_json

				if Systems['Result']['Count'] == 0:
					print("No System Found")	

				else:
					print('\n')
					print("System Name: " + Systems["Result"]["Results"][0]["Row"]['Name']) 
					print("System ID: " + Systems["Result"]["Results"][0]["Row"]['ID'])
					print("System Domain: " + Systems["Result"]["Results"][0]["Row"]['DomainName'])
					DiD = str(Systems["Result"]["Results"][0]["Row"]['DomainId'])
					print("Domain ID: " + DiD)

		except Exception as E:

			traceback.print_exc()

class Add_System(object):
	def __init__(self, **kwargs ):
		kwargs["Call"] = URL(Call= "/ServerManage/AddResource").new_url
		try:
			Add_System = Other_Request(Debug=True,**kwargs)

		except Exception as E:

			traceback.print_exc()

class Delete_System(object):

		def __init__(self, System, **kwargs ):
			kwargs["ID"] = None
			try:

				SystemQuery = """SELECT Server.ID, Server.Name FROM Server WHERE Server.Name  = '%s'""" % System

				if Query_Request(SQL = SystemQuery).parsed_json['Result']['Count'] != 0:
					ID = Query_Request(SQL = SystemQuery).parsed_json["Result"]["Results"][0]["Row"]['ID']
					kwargs["ID"] = ID
					IDs = json.dumps(Other_Request(Call= "/ServerManage/DeleteResource", Debug=True, **kwargs).parsed_json['Result'], indent=4, sort_keys=True)
					print(IDs)
				else:
					print( "Secret Not Found")

			except Exception as E:

				#Debug functionality!
				traceback.print_exc()

###Account Management###
def Add_Account(DomainName=None, SystemName=None, DatabaseName=None, **kwargs):

	kwargs["Call"] = URL(Call= "/ServerManage/AddAccount").new_url
	kwargs['Debug'] = True

	if DomainName != None:

		UpDomainName = DomainName.upper()	
		Domain_PAS_Search = """SELECT VaultDomain.ID FROM VaultDomain WHERE UPPER(VaultDomain.Name) = '%s'""" % UpDomainName
		Domain_Query = Query_Request(SQL = Domain_PAS_Search).parsed_json
		
		if Domain_Query['Result']['Count'] == 0:
			print("Domain: %s not found" % DomainName)
		else:
			kwargs['DomainID'] = Domain_Query["Result"]["Results"][0]["Row"]['ID']
			Other_Request(**kwargs)

	if SystemName != None:

		UpSystemName = SystemName.upper()	
		System_PAS_Search = """SELECT Server.ID FROM Server WHERE UPPER(Server.Name) = '%s'""" % UpSystemName
		System_Query = Query_Request(SQL = System_PAS_Search).parsed_json
		
		if System_Query['Result']['Count'] == 0:
			print("System: %s not found" % SystemName)
		else:
			kwargs['Host'] = System_Query["Result"]["Results"][0]["Row"]['ID']
			Other_Request(**kwargs)


	if DatabaseName != None:

		UpDBName = DatabaseName.upper()
		DB_PAS_Search = """SELECT VaultDatabase.ID FROM VaultDatabase WHERE UPPER(VaultDatabase.Name) = '%s'""" % UpDBName
		DB_Query = Query_Request(SQL = DB_PAS_Search).parsed_json
		
		if DB_Query['Result']['Count'] == 0:
			print("Database: %s not found" % DatabaseName)
		else:
			kwargs['DatabaseID'] = DB_Query["Result"]["Results"][0]["Row"]['ID']
			Other_Request(**kwargs)


def Delete_Account(Name, **kwargs):
	kwargs["Call"] = URL(Call= "/ServerManage/DeleteAccount").new_url
	Account_Query = """SELECT VaultAccount.ID FROM VaultAccount WHERE VaultAccount.User LIKE '%%%s%%'""" % Name
	D_Query = Query_Request(SQL = Account_Query).parsed_json
	
	if D_Query['Result']['Count'] == 0:
		print("Account: %s not found" % Name)
	else:
		kwargs['ID'] = D_Query["Result"]["Results"][0]["Row"]['ID']
		Other_Request(**kwargs)
		print("Account: %s Deleted" % Name)


def Get_Vault_Account(Name=None):

	try: 

		if Name == None:
			Get_Account_Query = """SELECT VaultAccount.User, VaultAccount.ID FROM VaultAccount \
			WHERE VaultAccount.User Like '%'""" 
			Get_Account = Query_Request(SQL = Get_Account_Query).parsed_json

			for i in range (len(Get_Account["Result"])):
				print("Account Name: " + Get_Account["Result"]["Results"][i]["Row"]['User'])
				print("ID :" + Get_Account["Result"]["Results"][i]["Row"]['ID'])
				print('\n')

		if Name != None:
			UpName = Name.upper()
			Get_Account_Query = """SELECT VaultAccount.User, VaultAccount.ID FROM VaultAccount \
			WHERE UPPER(VaultAccount.User) = '%s'""" % UpName
			Get_Account = Query_Request(SQL = Get_Account_Query, Debug=True).parsed_json

			if Get_Account['Result']['Count'] == 0:
				print ("No Account Found")
			else:
				print('\n')
				print("Account Name: " + Get_Account["Result"]["Results"][0]["Row"]['User']) 
				print("Account ID: " + Get_Account["Result"]["Results"][0]["Row"]['ID'])
				DiD = str(Get_Account["Result"]["Results"][0]["Row"]['DomainId'])
				print("Domain ID: " + DiD)

	except Exception as E:

		print(E)