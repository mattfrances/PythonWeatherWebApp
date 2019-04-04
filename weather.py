from flask import Flask, render_template, request
import requests
import json
import datetime

APIKEY = '1cba77983ad036a18f2bfeb87032c6a8'

app = Flask(__name__)


# Function to check wether postal code is Canadian
# 		if Canadian, returns true. false otherise
def checkCanadian(postal_code):
	return True if len(postal_code.replace(" ", "")) == 6 else False

# Function used to return first 3 letters from Canadian Postal Code
def getFirstThreeDigitsPostalCode(postal_code):
	return postal_code[:3]

# Function to calculate the current date and time
# NOT USED IN THIS VERSION
# WILL POSSIBLY BE USED IN NEXT VERSION
def calculateDateTime() :
    currentDT = datetime.datetime.now()
    hour = currentDT.hour
    ampm = "AM"

    if hour >= 13:
        hour -= 12
        ampm = "PM"

    minute = currentDT.minute

    time = str(hour) + ':' + str(minute) + ' ' + ampm
    return time


# Route to index.html
@app.route('/')
def index():
	return render_template('index.html')

# Route to temperature.html
@app.route('/temperature', methods=['POST'])
def temperature():
	postal_code = request.form['postal_code']
	country = 'us'	# default

	# Checks if the postal code entered is Canadian
	if checkCanadian(postal_code):
		postal_code = getFirstThreeDigitsPostalCode(postal_code)
		country = 'ca'

	# Send API request
	r = requests.get('https://api.openweathermap.org/data/2.5/weather?zip='+postal_code+','+country+'&appid='+APIKEY)
	# Parse API response
	json_object = r.json()
	description = str(json_object['weather'][0]['description'])
	temperature = str(round((json_object['main']['temp'] - 273.15))) # convert from Kelvin to Celcius
	#longitude = str(json_object['coord']['lon'])
	#latitude = str(json_object['coord']['lat'])
	locationName = str(json_object['name'])

	return render_template('temperature.html', temp=temperature, desc=description, location=locationName)
	# return longitude
	# return latitude
	# return temperature
	# return description
	# return str(json_object)
	# return render_template('temperature.html')
	# return locationName


if __name__ == '__main__':
    app.run(debug=True)
