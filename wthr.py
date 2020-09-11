#!/usr/bin/env python

#d558084074394c2080730b64d885e0bf
#http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID={APIKEY}

import requests, json, sys, time

api_key = "d558084074394c2080730b64d885e0bf"
base_url = "http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID="
fiveDay_url = "http://api.openweathermap.org/data/2.5/forecast?zip=01562,us&units=imperial&appid=d558084074394c2080730b64d885e0bf"
today_url = "http://api.openweathermap.org/data/2.5/weather?zip=01562,us&units=imperial&appid=d558084074394c2080730b64d885e0bf"

#response = requests.get(complete_url) 
#x = response.json()

arguments = sys.argv

good_weather = ["Clear"]
ok_weather = ["Rain", "Drizzle", "Mist", "Fog", "Clouds"]
bad_weather = ["Squall", "Smoke", "Haze", "Dust", "Sand", "Thunderstorm"]
severe_weather = ["Ash", "Sand", "Tornado"]

def determineSeverity(main, desc):
	severity = "unknown"

	for i in good_weather:
		if (i == main):
			severity = "Good"

	for i in ok_weather:
		if (i == main):
			severity = "Ok"

	for i in bad_weather:
		if (i == main):
			severity = "Bad"

	for i in severe_weather:
		if (i == main):
			severity = "Severe"

	if (severity == "Ok"):
		if (main == "Rain"):
			if (desc == "moderate rain" or desc == "heavy intensity rain" or desc == "very heavy rain"):
				severity = "Bad"
			elif(desc == "extreme rain" or desc == "freezing rain" or desc == "heavy intensity shower rain" or desc == "ragged shower rain"):
				severity = "Severe" 
		elif(main == "Drizzle"):
			if (desc == "heavy intensity drizzle" or desc == "heavy intensity drizzle rain" or desc == "heavy shower rain and drizzle"):
				severity = "Bad"
		elif(main == "Clouds"):
			if (desc == "overcast clouds"):
				severity = "Bad"
	elif (severity == "Bad"):
		if (main == "Thunderstorm"):
			if (desc == "thunderstorm with heavy rain" or desc == "heavy thunderstorm" or desc == "ragged thunderstorm" or desc == "thunderstorm with heavy drizzle"):
				severity = "Severe"

	return severity

def printWthrData(wthrList, hTime):
	main = wthrList["main"]
	wthr = wthrList["weather"][0]
	print(hTime)

	primary_wthr = wthr["main"]
	desc = wthr["description"]

	severity = determineSeverity(primary_wthr, desc)

	#test-case
	#severity = determineSeverity("Ash", "volcanic ash")

	color = "\033[0m"
	end_color = color

	if (severity == "Good"):
		color = "\033[32;1m"
	elif (severity == "Ok"):
		color = "\033[33;1m"
	elif (severity == "Bad"):
		color = "\033[31;1m"
	else:
		color = "\033[35;1m"

	print("Severity: " + color + severity + end_color)
	print("Weather: " + color +wthr["main"] + end_color)
	print("Description: " + color + wthr["description"] + end_color)
	print("Temperature (F): " + str(main["temp"]))
	print("Min temperature (F) " + str(main["temp_min"]))
	print("Max temperature (F) " + str(main["temp_max"]))
	print("Humidity: " + str(main["humidity"]))
	print("Air pressure: " + str(main["pressure"]) + "\n")
	print("=========================================")


if (len(arguments) > 1):
	arg1 = sys.argv[1]
	try:
		arg1 = int(sys.argv[1])
		print(str(arg1) + " day forecast")
	except:
		print(arg1 + "'s forecast")

	response = requests.get(fiveDay_url) 
	x = response.json()	

	if (x["cod"] == "404"):
		print("404 from openweathermap")
		exit()

	theList = x["list"]	

	if (type(arg1) is int):
		days = arg1
		days = days + 1
		
		count = 0
		while days > 0 and count < len(theList):
			current = theList[count]
			epoch = current["dt"]
			time_struct = time.localtime(epoch)
			printWthrData(current, time.asctime(time_struct))
			if (time_struct.tm_hour == 2 and count > 0):
				days = days - 1
			count = count + 1
		
	elif(type(arg1) is str):
		targetDay = arg1
		day_abbrvs = ["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]
		found = False
		day_num = 0

		length = len(day_abbrvs)

		for i in range(length):
			if (targetDay.lower() == day_abbrvs[i].lower()):
				found = True
				day_num = i
				break

		if (found == False):
			print("Invalid day")
			exit()

		do_once = False

		length = len(theList)
		hit_num = 0

		for i in range(length):
			current = theList[i]
			epoch = current["dt"]
			time_struct = time.localtime(epoch)
			


			if (time_struct.tm_wday == day_num):
				if (do_once == False):
					if (i > 0):
						epoch2 = theList[i-1]["dt"]
						time_struct2 = time.localtime(epoch2)
						printWthrData(theList[i-1], time.asctime(time_struct2))
					do_once = True

				printWthrData(current, time.asctime(time_struct))
				hit_num = i
		
		if (hit_num == 0):
			print("Only 5 day forecast available")
			exit()

		if (hit_num < length - 1):
			epoch = theList[hit_num + 1]["dt"]
			time_struct = time.localtime(epoch)
			printWthrData(theList[hit_num + 1], time.asctime(time_struct))
			
else:
	print("Todays forecast: ")

	response = requests.get(today_url) 
	x = response.json()

	if 	(x["cod"] != "404"):
		epoch = x["dt"]
		time_struct = time.localtime(epoch)
		printWthrData(x, time.asctime(time_struct))
	else:
		print("404 from openweathermap")