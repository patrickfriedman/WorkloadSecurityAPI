from __future__ import print_function
import sys, warnings
import deepsecurity
from deepsecurity.rest import ApiException
import csv

def write(list):
	count = 0
	computers = 0
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

	sourceFile.close()

def list():
	# Setup
	if not sys.warnoptions:
		warnings.simplefilter("ignore")
	configuration = deepsecurity.Configuration()
	configuration.host = 'https://cloudone.trendmicro.com/api'

	# Authentication
	configuration.api_key['api-secret-key'] = '22A83D1A-197B-5B20-2F0F-2B7B84A061A9:5E986039-3C78-8CCE-AF5A-FD2E4478A830:rCmYF6SEd6hiOwUSNXePB2MGI39SHer6KopDzOzlDic='

	# Initialization
	# Set Any Required Values
	api_instance = deepsecurity.ComputersApi(deepsecurity.ApiClient(configuration))
	api_version = 'v1'
	expand_options = deepsecurity.Expand()
	expand_options.add(expand_options.none)
	expand = expand_options.list()
	overrides = False

	try:
		api_responce = api_instance.list_computers(api_version, expand=expand, overrides=overrides)
		return api_responce

	except ApiException as e:
		print("An exception occurred when calling ComputersApi.list_computers: %s\n" % e)

def description():
	# Setup
	if not sys.warnoptions:
		warnings.simplefilter("ignore")
	configuration = deepsecurity.Configuration()
	configuration.host = 'https://cloudone.trendmicro.com/api/computers/{17}'

	# Authentication
	configuration.api_key['api-secret-key'] = '22A83D1A-197B-5B20-2F0F-2B7B84A061A9:5E986039-3C78-8CCE-AF5A-FD2E4478A830:rCmYF6SEd6hiOwUSNXePB2MGI39SHer6KopDzOzlDic='

	# Initialization
	# Set Any Required Values
	api_instance = deepsecurity.ComputersApi(deepsecurity.ApiClient(configuration))
	computer_id = 1
	api_version = 'v1'
	expand_options = deepsecurity.Expand()
	expand_options.add(expand_options.none)
	expand = expand_options.list()
	overrides = False

	try:
		api_response = api_instance.describe_computer(computer_id, api_version, expand=expand, overrides=overrides)
		return api_response
	except ApiException as e:
		print("An exception occurred when calling ComputersApi.describe_computer: %s\n" % e)


write(list())
# write(description())