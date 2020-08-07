from PySDK import PAS_Utility
from PAS_Utility import *
import json
import requests 
import traceback

#Major iteration issue that needs to be fixed 

class Get_System(object):
		#if Result['Result']['Count'] != 0:

	def __init__(self, Name=None):

		try:

			if Name == None:
				SystemQuery = """SELECT Server.DomainId, Server.DomainName, Server.ID, Server.Name 
				FROM Server WHERE Server.Name LIKE '%'""" 
				#fix the iteration issue!!

				for i in range (len(PAS_Utility.Query_Request(SQL = SystemQuery).parsed_json["Result"]["Results"])):
					print("System Name: " + PAS_Utility.Query_Request(SQL = SystemQuery).parsed_json["Result"]["Results"][i]["Row"]['Name'])
					print("System ID :" + PAS_Utility.Query_Request(SQL = SystemQuery).parsed_json["Result"]["Results"][i]["Row"]['ID'])
					print("System Domain: " + PAS_Utility.Query_Request(SQL = SystemQuery).parsed_json["Result"]["Results"][i]["Row"]['DomainName'])
					DiD = str(PAS_Utility.Query_Request(SQL = SystemQuery).parsed_json["Result"]["Results"][i]["Row"]['DomainId'])
					print("Domain ID: " + DiD)
					print('\n')

			if Name != None:
				SystemQuery = """SELECT Server.DomainId, Server.DomainName, Server.ID, Server.Name 
				FROM Server WHERE Server.Name = '%s'""" % Name

				if PAS_Utility.Query_Request(SQL = SystemQuery).parsed_json['Result']['Count'] == 0:
					print("No System Found")	

				else:
					print('\n')
					print("System Name: " + PAS_Utility.Query_Request(SQL = SystemQuery).parsed_json["Result"]["Results"][0]["Row"]['Name']) 
					print("System ID: " + PAS_Utility.Query_Request(SQL = SystemQuery).parsed_json["Result"]["Results"][0]["Row"]['ID'])
					print("System Domain: " + PAS_Utility.Query_Request(SQL = SystemQuery).parsed_json["Result"]["Results"][0]["Row"]['DomainName'])
					DiD = str(PAS_Utility.Query_Request(SQL = SystemQuery).parsed_json["Result"]["Results"][0]["Row"]['DomainId'])
					print("Domain ID: " + DiD)

		except Exception as E:

			traceback.print_exc()

class Add_System(object):
	def __init__(self, **kwargs ):
		kwargs["Call"] = PAS_Utility.URL(Call= "/ServerManage/AddResource").new_url
		try:
			Add_System = PAS_Utility.Other_Request(Debug=True,**kwargs)

		except Exception as E:

			traceback.print_exc()

class Delete_System(object):

		def __init__(self, System, **kwargs ):
			kwargs["ID"] = None
			try:

				SystemQuery = """SELECT Server.ID, Server.Name FROM Server WHERE Server.Name  = '%s'""" % System

				if PAS_Utility.Query_Request(SQL = SystemQuery).parsed_json['Result']['Count'] != 0:
					ID = PAS_Utility.Query_Request(SQL = SystemQuery).parsed_json["Result"]["Results"][0]["Row"]['ID']
					kwargs["ID"] = ID
					IDs = json.dumps(Other_Request(Call= "/ServerManage/DeleteResource", Debug=True, **kwargs).parsed_json['Result'], indent=4, sort_keys=True)
					print(IDs)
				else:
					print( "Secret Not Found")

			except Exception as E:

				#Debug functionality!
				traceback.print_exc()

#Update_Resource
#fix the Bug

#Add_System(Name = "Test" ,FQDN="test.test.net", Description="test", ComputerClass="Unix", SessionType="Ssh")
#Get_System(Name = "Test")
#Get_System()
#Delete_System("Test")



