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
	account_sid = 'AC20aef97ee2405b157s43111b5ae30439'
	auth_token = 'ae15fdef547d1235d992c4bd32917f5aa'
	client = Client(account_sid, auth_token)
	message = client.messages \
						.create(
								body="Some unauthorized changes were made to your agent: " + str(lists),
								from_='+19725034512',
								to='+12141597159'
						)
	print(message.sid)

def write(list):
	count = 0
	computers = 0
	ec2 = 0
	sourceFile = open('api.csv', 'w')

	csvreader = csv.writer(sourceFile, delimiter=',')
	csvreader.writerow(['COMPUTER NAME', 'PLATFORM', 'POLICY NAME', 'STATUS'])
	
	api = str(list).split('\n')
	api.pop(0)

	for i in api:
		print(i)
		sourceFile.writelines(i)
		count = count + 1
		computers = computers + 1

		if (count == 4):
			sourceFile.write('\n')
			count = 0
		if (computers == 42):
			print('\n')
			csvreader.writerow([])
			computers = 0
			ec2 = ec2 + 1
	
	csvreader.writerow([])
	csvreader.writerow(['COMPUTER NAME', 'PLATFORM', 'POLICY NAME', 'STATUS'])

	flag = 0
	for x in range(ec2 + 1): 
		flag = flag + 1
		name = api.pop((x * 38) + 12)
		sourceFile.write(name)

		platform = api.pop((x * 38) + 30)
		sourceFile.write(platform)

		policyname = api.pop((x * 38) + 4)
		sourceFile.write(policyname)

		status = api.pop((x * 38) + 1)
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
	configuration.api_key['api-secret-key'] = '22A83D1A-197B-5B20-2F0F-2B7B5267f1A9:5E986039-3C78-8CCE-AF5A-FD2E4478A830:rCmYF6SEd6hiOwUSNXePB2MGI39SHer6KopDzOzlDic='

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

noerror = True
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
