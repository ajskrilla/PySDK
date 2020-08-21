import pip
import traceback

def Install_Libraries(Debug=False):
	print("Installing Libraries.....")

	try:
	    pip.main(['install', '--user', 'pandas'])
	    print('\n')
	    pip.main(['install', '--user', 'requests'])
	    print('\n')
	    pip.main(['install', '--user', 'configparser'])
	    print('\n')

	except Exception as E:

		if Debug == True:
			traceback.print_exc()
		else:
			print(E)
	print('Libraries installed or were already installed.')

