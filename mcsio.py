#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import sys
import http.client as http
import urllib
import json
import Adafruit_DHT
GPIO_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
deviceId = "DIfiiQka"
deviceKey = "UNfsEdWeHFYYTGTt" 
def post_to_mcs(payload): 
	headers = {"Content-type": "application/json", "deviceKey": deviceKey} 
	not_connected = 1 
	while (not_connected):
		try:
			conn = http.HTTPConnection("api.mediatek.com:80")
			conn.connect() 
			not_connected = 0 
		except (http.HTTPException, socket.error) as ex: 
			print ("Error: %s" % ex)
 			#time.sleep(10)
	conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers) 
	response = conn.getresponse() 
	print( response.status, response.reason, json.dumps(payload), time.strftime("%c")) 
	data = response.read() 
	conn.close()
while True:
	h0, t0= Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, GPIO_PIN)
	SwitchStatus = GPIO.input(24)
	if(SwitchStatus == 1):
		print('Button pressed')
		print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(t0, h0))
	else:
		print('Button released')
		print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(t0, h0))

	payload = {"datapoints":[{"dataChnId":"Humidity","values":{"value":h0}}
		,{"dataChnId":"Temperature","values":{"value":t0}}	
		,{"dataChnId":"SwitchStatus","values":{"value":SwitchStatus}}]}
	
	post_to_mcs(payload)
	time.sleep(1)
