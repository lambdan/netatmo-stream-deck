from flask import Flask, redirect, send_file, jsonify, Response, cli
import time, subprocess, yaml, sys, os
from gevent.pywsgi import WSGIServer

INTERVAL = 10*60 # wait this many seconds between weather refreshes

app = Flask(__name__)

if not os.path.isfile("gonetatmo.cfg"):
	# we need to init gonetatmo

	print("# Netatmo configuration")
	print("Create an app here to get client ID and secret: https://dev.netatmo.com/apps/")

	CLIENT_ID = input("Client ID: ")
	CLIENT_SECRET = input("Client Secret: ")
	EMAIL = input("Netatmo Email: ")
	PASSWORD = input("Netatmo Password (will be visible while typing it in!): ")

	print("Setting up gonetatmo... this might take a sec")
	output = subprocess.check_output(["gonetatmo", "--clientid", CLIENT_ID, "--clientsecret", CLIENT_SECRET, "--email", EMAIL, "--password", PASSWORD, "-j"], encoding="utf8")
	if "Updated" in output and "stations" in output:
		print("Success! We are good to go!")
	else:
		print("Hmm, something went wrong...")
		sys.exit(1)
else:
	print("gonetatmo.cfg found, we are good to go :)")

def refreshWeather():
	global wjson
	global refreshed
	print("Refreshing weather")
	wjson = subprocess.check_output(["gonetatmo", "-j"], encoding="utf8")
	refreshed = time.time()

refreshed = 0
wjson = ""

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
	http_server = WSGIServer(('',5551), app)
	
	print("Your weather data JSON should now be visible here: http://localhost:5551")
	print("It will update every " + str(INTERVAL) + " seconds, or you can go to http://localhost:5551/refresh to force it")
	print("(Note that Netatmo doesn't constantly poll your weather either, so refreshing it every second is very uneccessary)")
	print("If you close this window the server will die. Feel free to minimize it though :)")

	http_server.serve_forever()
