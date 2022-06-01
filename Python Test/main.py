import csv, datetime, json, pytz
import xml.etree.ElementTree as ET

def update_values(root, x, y):
	now = datetime.datetime.now()
	for element in root:
		if(element.tag == 'DEPART'):
			element.text = (now + datetime.timedelta(days = x)).strftime('%Y%m%d')
		elif(element.tag == 'RETURN'):
			element.text = (now + datetime.timedelta(days = y)).strftime('%Y%m%d')
		update_values(element, x, y)

def update_csv(x, y):
	tree = ET.parse('resources/test_payload1.xml')
	root = tree.getroot()
	update_values(root, x, y)
	output = ET.tostring(root)
	with open("output/test_payload1.xml", "wb") as f:
    		f.write(output)
			

def delete_keys(json_file, x):
	if x in json_file:
		del json_file[x]
	for j in json_file:
		if isinstance(json_file[j], dict):
			delete_keys(json_file[j], x)

def remove_elements(*del_data):
	f = open('resources/test_payload.json')
	data = json.load(f)
	for x in del_data:
		delete_keys(data, x)
	with open("output/test_payload.json", "w") as outfile:
    		json.dump(data, outfile, indent=4)
	f.close()


def convert_to_utc(my_date):
	utc_datetime = datetime.datetime.utcfromtimestamp(float(my_date) / 1000.)
	utc_datetime.replace(tzinfo = pytz.timezone('UTC')).astimezone(pytz.timezone('America/Los_Angeles')).strftime('%Y-%m-%d %H:%M:%S %Z')
	return utc_datetime

def jmeter_log_files(file_path):
	log_file = open(file_path)
	csvreader = csv.reader(log_file)
	header = next(csvreader)
	index = ["label", "responseCode", "responseMessage", "failureMessage"]
	for row in csvreader:
		if(not row[header.index("responseCode")] == '200'):
			print(convert_to_utc(row[header.index("timeStamp")]), end = ", ")
			for i in index:
				print(row[header.index(i)], end = ", ")
			print()

	log_file.close()