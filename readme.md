# Netatmo Weather on Elgato Stream Deck

This little Python script runs a web server which uses the [Netatmo library](https://pypi.org/project/netatmo/) to output Netatmo data in JSON, which we can then use with the [API Ninja Plugin](https://barraider.com/) to show your Netatmo weather on your Stream Deck.

For Windows users I have made a self-contained exe that you can just run immediately (find it on the [Releases](https://github.com/lambdan/netatmo-stream-deck/releases) page.)

If you prefer doing this manually or use Linux/Mac, you can just download `netatmo-server.py` and install the required libraries and run it, ideally hidden in a screen or something.

Eitherway, you will need to register an app at Netatmo to get API keys. It's free, no worries: https://dev.netatmo.com/apps/

Once everything is up and running you can drag out a API Ninja square to your deck and configure it as follows:

- Request Type: GET
- API URL: `http://localhost:5552`
- Content Type: `application/json`
- Response Shown: 
	- For indoors: `dashboard_data.Temperature` 
	- For outdoors: `modules[0].dashboard_data.Temperature`
	- Depending on your setup you might have to change some things around, it should be pretty easy to figure out by looking at the json (available at http://localhost:5552)
	- (There are also a bunch of other fields you can use, like humidity, feel free to do whatever you want)
- (Optional) Title Prefix: `Outdoor\n\n\n`
	- A bunch of `\n`'s to push the label up and keeping the temperature along the bottom
- (Optional) Title Suffix: `°C`
- Reponse Type: Response is Text
- Autorun every: 15 mins
	- By default the server refreshes weather every 900 seconds (15 mins), so making it any shorter than that is unecessary.
- (Optional) Hide the green success indiciator

All other fields should be left blank or default.

Once done, and after you've set some custom icons, you should end up with something like this:

![Result](https://lambdan.se/img/shellfish/6950193.jpg)
