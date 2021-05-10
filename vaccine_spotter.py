#! /usr/bin/python3
import os
import telegram_send
from datetime import date,datetime
from time import time,ctime,sleep

#Refresh Interval in seconds
ref_interval = 5

d_today = date.today()

age_limit = 18

__district_code = "363"

d1 = d_today.strftime("%d/%m/%Y")

__date = str(d1).replace("/","-")

def parse_result(result):
	output = []
	centers = result['centers']
	for center in centers:
		if center['pincode'] > 411000:
			if center['pincode'] < 412000:
				sessions = center['sessions']
				for session in sessions:
					if session['available_capacity'] > 0:
						res = { 'name': center['name'], 'PINCODE':center['pincode'],'block_name':center['block_name'], 'age_limit':session['min_age_limit'], 'date':session['date'],'available_capacity':session['available_capacity'] }
						if res['age_limit'] == age_limit: 
							output.append(res)
	return output
				
	
def call_api():
	print(ctime(time()))
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	#api = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + __district_code+ "&date="+ __date
	api = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=" + __district_code+ "&date="+ __date
	response = requests.get(api, headers=headers)
	print(response)
	if response.status_code == 200:
		print ("API call success")
		result = response.json()
		print(result)
		key_check = "centers"
		if key_check in result:
			output = parse_result(result)
			if len(output) > 0:
				print ("Vaccines available")
				print('\007')
				result_str = ""
				for center in output:
					result_str = result_str + center['name'] + "\n"
					result_str = result_str + "block:"+center['block_name'] + "\n"
					result_str = result_str + "vaccine count:"+str(center['available_capacity']) + "\n"
					result_str = result_str + "Pin Code:"+ str(center['PINCODE']) + "\n"
					result_str = result_str + "-----------------------------------------------------\n"
					telegram_send.send(messages = [result_str])
			else:
				print ("Vaccines not available \n")

t = datetime.now()

if __name__ == '__main__':
	call_api()
	while True:
		delta = datetime.now()-t
		if delta.seconds >= ref_interval:
			call_api()
			t = datetime.now()
