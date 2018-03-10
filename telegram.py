import requests
from botconfig import *

def telegram_api(method, parameters):
	URL = "https://api.telegram.org/bot"+config_telegram_key+"/"+method;
	r = requests.post(URL, data=parameters)
	return r.json()
