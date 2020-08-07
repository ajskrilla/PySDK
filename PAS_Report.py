from PySDK import PAS_Utility
import sys
import json
import requests 
import pandas
import os
import re
from pathlib import Path

null = None
pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)

#will turn into a class

def Query(SQLQuery,Print=False, ExportPath=None):

	try:
		
		realQuery = str(SQLQuery)
		print("SQL Query is: " + realQuery)
		print('\n')
		appended_data = []
		for i in range (len(PAS_Utility.Query_Request(SQL = realQuery).parsed_json["Result"]["Results"])):
			data = PAS_Utility.Query_Request(SQL = realQuery).parsed_json["Result"]["Results"][i]["Row"]
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

		return E

#Example

#Query(SQLQuery = """SELECT Server.DomainId, Server.DomainName, Server.ID, Server.Name FROM Server""", Print=True, ExportPath = "/home/a/Desktop/testtest.csv")