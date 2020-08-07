from PySDK import PAS_Utility
import sys
import traceback
import json
import requests 
import pandas
import os
import re
from pathlib import Path


Call_to_Tenant = PAS_Utility.URL(Call= "/Core/CheckProxyHealth").new_url

pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)
class Connector_Info(object):
	def __init__(self, Print=False, ExportPath=None):
	
		try:
			Result = PAS_Utility.Other_Request(Call= '%s' % Call_to_Tenant).parsed_json
			print('Getting the Connectors')
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

#Connector_Info(Print=True, ExportPath="/home/a/Desktop/test1.csv")