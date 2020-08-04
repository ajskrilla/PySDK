from PySDK import PAS_Utility
from PAS_Utility import *
import json
import requests 

Call_to_Tenant_ASF = PAS_Utility.URL(Call= "/ServerManage/AddSecretsFolder").new_url
Call_to_Tenant_AS = PAS_Utility.URL(Call= "/ServerManage/AddSecret").new_url

def Get_Secret(Secret):

	try:

		SecretQuery = """SELECT DataVault.SecretFileName, DataVault.SecretName, DataVault.ID \
		FROM DataVault WHERE DataVault.SecretName = '%s'""" % Secret

		if PAS_Utility.Query_Request(SQL = SecretQuery).parsed_json['Result']['Count'] != 0:
			ID = PAS_Utility.Query_Request(SQL = SecretQuery).parsed_json["Result"]["Results"][0]["Row"]['ID']
			r = PAS_Utility.Other_Request(Call = "/ServerManage/RetrieveSecretContents", ID = '%s' %ID)
			IDs = json.dumps(PAS_Utility.Other_Request(Call = '%s' % Call_to_Tenant, ID = '%s' \
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
		
		
#Ex on how to use clases/functions:

#Add_Secret_Folder( Name="Test", Description="Test")
#Get_Secret('text')
#Get SSH, Delete SSH, Add SSH