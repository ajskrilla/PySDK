#Module
import getpass
import os
import sys
import json
import requests
import subprocess

#Module for Oauth config maker

#make arguments for the command line and then have the password
#have null arguments go to UI, else use params selected
#if null argument exists, then go to function.
#Will remake as a class

def MakeConfig():

	#You can get rid of the input if you want it to straight script
	TenantID = input("What is your tenant ID? Ex ABC1234:     ")
	AppID = input("What is the AppID? This needs to match 'Application ID':     ")
	Scope = input("What is the name of the scope for the token?:     ")
	SvcAccount =  input("What is the name of the Service Account [upn]:     ")
	PW = getpass.getpass("Please input PW for the Service Account:    ")

	URL = 'https://' + TenantID + '.my.centrify.net'

	headers = {
		'X-CENTRIFY-NATIVE-CLIENT': 'true',
		'Content-Type': 'application/x-www-form-urlencoded'
		}

	OauthURL = URL + "/oauth2/token/" + '%s' % AppID

	OauthBody = {
		"client_id": "%s" % SvcAccount,
		"client_secret": "%s" % PW,
		"scope": "%s" % Scope,
		"grant_type":"client_credentials"
		}

	OauthBody1 = str(OauthBody)
	body = OauthBody1.replace("'", '"')
	load = json.loads(body)

	try: 

		#data is needed 
		#####################################################################
		r = requests.post(url= OauthURL , headers=headers, data=load).json()
		#####################################################################

		responseobject = r
		jsonlist = json.dumps(responseobject)
		parsed_json = (json.loads(jsonlist))
		print("\n")
		print("\n")

		print(json.dumps(parsed_json, indent=4, sort_keys=True))

		token = parsed_json["access_token"]
	except Exception as E:

		print(E)

	try:

		if os.name == "posix":
			path = os.path.join(os.path.join(os.path.expanduser('~')), 'config.config') 

		elif os.name == "nt":
			path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'config.config')

		else:
			pass

		Open = open(path, "w+")
		Open.write('[Properties]'+ "\n") 
		Open.write('Tenant = %s' %URL + "\n")
		Open.write('Bearer = %s' %token)
		Open.close()

		print("")
		print("")
		print("Config file made")

	except Exception as E:

		print("")
		print("")
		print(E)

#subprocess.check_call(['chmod', '0444', 'path'])
#Maybe make the file hidden and encrypted?
#subprocess.check_call(["attrib","+H", path])

####For Linux
#os.chmod(path, stat.S_IRUSR | stat.S_IRWXU | stat.S_IWUSR)
#stat.S_IRWXU    Mask for file owner permissions
#stat.S_IRUSR    Owner has read permission
#stat.S_IWUSR    Owner has write permission
