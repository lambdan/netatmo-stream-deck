from flask import Flask, redirect, Response
from gevent.pywsgi import WSGIServer
import netatmo, time, os, json
from datetime import datetime

INTERVAL = 15*60 # wait this many seconds between weather refreshes
CONFIG_FILE = "netatmo.cfg"

LOGGING = True
LOG_INDOOR = "netatmo_indoor.tsv"
LOG_OUTDOOR = "netatmo_outdoor.tsv"

refreshed = 0
wjson = ""

app = Flask(__name__)


if not os.path.isfile(CONFIG_FILE):
	# onboarding

	print(CONFIG_FILE, "not found, lets make one")
	print()
	print("# Netatmo Configuration")
	print("To get Client ID and Secret keys, register an app here: https://dev.netatmo.com/apps/")
	print()
	CLIENT_ID = input("Client ID: ")
	CLIENT_SECRET = input("Client Secret: ")
	EMAIL = input("Netatmo Account/Email: ")
	PASSWORD = input("Netatmo Password (will be visible while typing it in): ")

	# write cfg, theres probably a better way to do this
	with open(CONFIG_FILE, "w") as f:
		f.write("[netatmo]\n")
		f.write("client_id = " + CLIENT_ID + "\n")
		f.write("client_secret = " + CLIENT_SECRET + "\n")
		f.write("username = " + EMAIL + "\n")
		f.write("password = " + PASSWORD + "\n")
	print(CONFIG_FILE, "written. We're good to go.")
else:
	print(CONFIG_FILE, "found! We're good to go.")


ws = netatmo.WeatherStation(CONFIG_FILE)

def refreshWeather():
	print("Refreshing weather...")

	global refreshed
	global wjson

	ws.get_data()
	json_output = ""

	for d in ws.devices:
		j = json.dumps(d, indent=4, ensure_ascii=False)
		json_output += j

	wjson = json_output
	refreshed = time.time()

	if LOGGING:
		j = json.loads(wjson)
		indoor = ""
		outdoor = ""
		
		if not os.path.isfile(LOG_INDOOR):
			# create headers (first row) if file doesnt exist
			indoor += "Date/Time (UTC)\tTemperature\tCO2\tHumidity\tNoise\tPressure\tAbsolute Pressure\n"

		if not os.path.isfile(LOG_OUTDOOR):
			outdoor += "Date/Time\tTemperature\tHumidity\n"
		
		# add data

		# DateTime	IndoorTemp	IndoorCO2	IndoorHumidity	IndoorNoise	IndoorPressure
		#indoor += str(j["dashboard_data"]["time_utc"]) + "\t"
		indoor += datetime.fromtimestamp(j["dashboard_data"]["time_utc"]).strftime("%Y-%m-%d %H:%M:%S") + "\t"
		indoor += str(j["dashboard_data"]["Temperature"]) + "\t"
		indoor += str(j["dashboard_data"]["CO2"]) + "\t"
		indoor += str(j["dashboard_data"]["Humidity"]) + "\t"
		indoor += str(j["dashboard_data"]["Noise"]) + "\t"
		indoor += str(j["dashboard_data"]["Pressure"]) + "\t"
		indoor += str(j["dashboard_data"]["AbsolutePressure"]) + "\n"

		# OutdoorTemp	OutdoorHumidity
		#outdoor += str(j["modules"][0]["dashboard_data"]["time_utc"]) + "\t"
		outdoor += datetime.fromtimestamp(j["modules"][0]["dashboard_data"]["time_utc"]).strftime("%Y-%m-%d %H:%M:%S") + "\t"
		outdoor += str(j["modules"][0]["dashboard_data"]["Temperature"]) + "\t"
		outdoor += str(j["modules"][0]["dashboard_data"]["Humidity"]) + "\n"

		with open(LOG_INDOOR, "a") as f:
			f.write(indoor)

		with open(LOG_OUTDOOR, "a") as f:
			f.write(outdoor)

@app.route('/')
def index():
	global refreshed
	global wjson

	if wjson == "" or time.time() > (refreshed + INTERVAL):
		refreshWeather()

	return Response(wjson, mimetype="application/json")

@app.route("/refresh")
def forceRefresh():
	refreshWeather()
	return redirect('/')

if __name__ == "__main__":
	#app.run(debug=False, port=5551, host='0.0.0.0')
	http_server = WSGIServer(('',5552), app)
	
	print("Your weather data JSON should now be visible here: http://localhost:5552")
	print("It will update every " + str(INTERVAL) + " seconds, or you can go to http://localhost:5552/refresh to force it")
	print("(Note that Netatmo doesn't constantly poll your weather either, so refreshing it every second is very uneccessary)")
	print("If you close this window the server will die. Feel free to minimize it though :)")

	http_server.serve_forever()