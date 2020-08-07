from PySDK import PAS_Utility
from PAS_Utility import *
import json
import requests 
import traceback


Call_to_Tenant_ASF = PAS_Utility.URL(Call= "/ServerManage/AddSecretsFolder").new_url
Call_to_Tenant_AS = PAS_Utility.URL(Call= "/ServerManage/AddSecret").new_url
Call_to_Tenant_DS = PAS_Utility.URL(Call= "/ServerManage/DeleteSecret").new_url
#remake to a class

def Get_Secret(Secret):

	try:

		SecretQuery = """SELECT DataVault.SecretFileName, DataVault.SecretName, DataVault.ID \
		FROM DataVault WHERE DataVault.SecretName = '%s'""" % Secret

		if PAS_Utility.Query_Request(SQL = SecretQuery).parsed_json['Result']['Count'] != 0:
			ID = PAS_Utility.Query_Request(SQL = SecretQuery).parsed_json["Result"]["Results"][0]["Row"]['ID']
			r = PAS_Utility.Other_Request(Call = "/ServerManage/RetrieveSecretContents", ID = '%s' %ID)
			IDs = json.dumps(PAS_Utility.Other_Request(Call = "/ServerManage/RetrieveSecretContents", ID = '%s' \
				%ID).parsed_json['Result'], indent=4, sort_keys=True)
			print(IDs)

		else:
			print( "Secret Not Found")

	except Exception as E:

		print(E)


class Add_Secret(object):

	def __init__(self, **kwargs ):
		kwargs["Call"] = Call_to_Tenant_AS
		kwargs["Debug"] = True
		AS = PAS_Utility.Other_Request(**kwargs)

class Add_Secret_Folder(object):

	def __init__(self, **kwargs ):
		kwargs["Call"] = Call_to_Tenant_ASF
		kwargs["Debug"] = True
		ASF = PAS_Utility.Other_Request(**kwargs)


class Delete_Secret(object):

	def __init__(self, Secret, **kwargs ):
		kwargs["ID"] = None
		try:

			SecretQuery = """SELECT DataVault.SecretFileName, DataVault.SecretName, DataVault.ID \
			FROM DataVault WHERE DataVault.SecretName = '%s'""" % Secret

			if PAS_Utility.Query_Request(SQL = SecretQuery).parsed_json['Result']['Count'] != 0:
				ID = PAS_Utility.Query_Request(SQL = SecretQuery).parsed_json["Result"]["Results"][0]["Row"]['ID']
				kwargs["ID"] = ID
				IDs = json.dumps(Other_Request(Call= "/ServerManage/DeleteSecret", Debug=True, **kwargs).parsed_json['Result'], indent=4, sort_keys=True)
				print(IDs)
			else:
				print( "Secret Not Found")

		except Exception as E:

			#Debug functionality!
			traceback.print_exc()


		
class Update_Resource(object):
	def __init__(self, System, **kwargs):
		#/ServerManage/UpdateResource
		

#Ex on how to use clases/functions:
#Get_Secret('test')
#Add_Secret_Folder( Name="Test", Description="Test")
#Delete_Secret(Secret='text')
#Get SSH, Delete SSH, Add SSH