#! /usr/bin/python3
import os
import telegram_send
import requests
from datetime import date,datetime
from time import time,ctime,sleep

#Refresh Interval in seconds
ref_interval = 5

d_today = date.today()

age_limit = 18

__district_code = "363"

dt = d_today.strftime("%d/%m/%Y")

__date_today = str(dt).replace("/","-")

def parse_result(input_json):
	final_res = []
	centers = input_json['centers']
	for center in centers:
		if center['pincode'] > 411000:
			if center['pincode'] < 412000:
				sessions = center['sessions']
				for session in sessions:
					if session['available_capacity'] > 0:
						res_str = { 'name': center['name'], 'PINCODE':center['pincode'],'block_name':center['block_name'], 'age_limit':session['min_age_limit'], 'date':session['date'],'available_capacity':session['available_capacity'] }
						if res_str['age_limit'] == age_limit: 
							final_res.append(res_str)
	return final_res
				
	
def check_slot():
	print(ctime(time()))
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	#api = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + __district_code+ "&date="+ __date_today
	api = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=" + __district_code+ "&date="+ __date_today
	api_response = requests.get(api, headers=headers)
	print(api_response)
	if api_response.status_code == 200:
		print ("Successful API Fetch")
		response_json = api_response.json()
		key_check = "centers"
		if key_check in response_json:
			parsed_result = parse_result(response_json)
			if len(parsed_result) > 0:
				print('---------------------------')
				print ("Slots Available")
				print('---------------------------')
				slot_info = ""
				for center in parsed_result:
					slot_info = slot_info + "===================\n"
					slot_info = slot_info + center['name'] + "\n"
					slot_info = slot_info + "Pin Code:"+ str(center['PINCODE']) + "\n"
					slot_info = slot_info + "Block:"+center['block_name'] + "\n"
					slot_info = slot_info + "Vaccine Available:"+str(center['available_capacity']) + "\n"
					slot_info = slot_info + "Date:"+ center['date'] + "\n"
					slot_info = slot_info + "===================\n"
					telegram_send.send(messages = [slot_info])
			else:
				print ("No Vaccine Slot Available \n")

time_now = datetime.now()
if __name__ == '__main__':
	check_slot()
	while True:
		diff = datetime.now()-time_now
		if diff.seconds >= ref_interval:
			check_slot()
			time_now = datetime.now()
