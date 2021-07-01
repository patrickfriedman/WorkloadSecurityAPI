from __future__ import print_function
import sys, warnings
import deepsecurity
from deepsecurity.rest import ApiException
from playsound import playsound
from twilio.rest import Client
import csv
import time
# play a sound when a parameter changes and send a message

lists = []

def text():
	account_sid = ''
	auth_token = ''
	client = Client(account_sid, auth_token)
	message = client.messages \
						.create(
								body="Some unauthorized changes were made to your agent: " + str(lists),
								from_='+1',
								to='+1'
						)
	print(message.sid)

def write(list):
	count = 0
	computers = 0
	ec2 = 0
	sourceFile = open('api.csv', 'w')

	csvreader = csv.writer(sourceFile, delimiter=',', lineterminator='\n')
	#csvreader.writerow(['Information: '])
	
	api = str(list).split('\n')
	api.pop(0)

	for i in api:
		print(i)
		#sourceFile.writelines(i)
		count = count + 1
		computers = computers + 1

		if (count == 4):
			#sourceFile.write('\n')
			count = 0
		if (computers == 42):
			print('\n')
			#csvreader.writerow([])
			computers = 0
			ec2 = ec2 + 1
	
	#csvreader.writerow([])
	csvreader.writerow(['COMPUTER NAME:', 'PLATFORM:', 'POLICY NAME:', 'STATUS:'])


	flag = 0
	for x in range(ec2 + 1): 
		flag = flag + 1
		name = api.pop((x * 38) + 12)
		name = format(name)
		sourceFile.write(name)

		platform = api.pop((x * 38) + 24)		#change to fix output/api error 30*
		platform = format(platform)
		sourceFile.write(platform)

		policyname = api.pop((x * 38) + 30)
		policyname = format(policyname)
		sourceFile.write(policyname)

		status = api.pop((x * 38) + 1)
		status = format(status)
		sourceFile.write(status)

		sourceFile.write('\n')
		flag = True

		if(flag == 1):
			lists.append(name)
			lists.append(platform)
			lists.append(policyname)
			lists.append(status)

	sourceFile.close()

def list():
	# Setup
	if not sys.warnoptions:
		warnings.simplefilter("ignore")
	configuration = deepsecurity.Configuration()
	configuration.host = 'https://cloudone.trendmicro.com/api'

	# Authentication
	configuration.api_key['api-secret-key'] = apikey

	# Initialization
	# Set Any Required Values
	api_instance = deepsecurity.ComputersApi(deepsecurity.ApiClient(configuration))
	api_version = 'v1'
	expand_options = deepsecurity.Expand()
	expand_options.add(expand_options.none)
	expand = expand_options.list()
	overrides = False

	try:
		api_response = api_instance.list_computers(api_version, expand=expand, overrides=overrides)
		return api_response

	except ApiException as e:
		print("An exception occurred when calling ComputersApi.list_computers: %s\n" % e)

def format(string):
	nameSubString = "display_name"
	platformSubString = "platform"
	policySubString = "policy_id"
	statusSubString = "0.0.0.0"

	extra = "last_appliance_communication"

	print(string)
	if nameSubString in string:
		string = string.replace("'", '')
		return string.replace("display_name: ", '')
	if extra in string:
		# return string.replace("'platform': ", 'AWS Linux') 
		return string.replace("'last_appliance_communication': None", 'AWS Linux')	# error in the api so hardcoded
	if policySubString in string:
		return string.replace("'policy_id': ", '')
	if statusSubString in string:
		return string.replace("'agent_version': '0.0.0.0'", 'Activation Needed.')
	else:
		return string.replace("'agent_version': ", 'Activated.')

noerror = True
apikey = input("Enter API key: ")
while(noerror):
	api_response = list()
	write(api_response)
	time.sleep(5)

	lists = []
	newapi = list()
	write(newapi)

	if(api_response != newapi):
		playsound('startup.mp3')
		print("\n" + str(lists) + "\n")
		text()
		noerror = False
