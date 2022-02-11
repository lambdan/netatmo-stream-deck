# Netatmo Weather on Stream Deck

This little Python script runs a web server which is basically a wrapper for the great [gonetatmo](https://github.com/tanaikech/gonetatmo) CLI utility I found that can output your Netatmo data in JSON, which we can then use with the [API Ninja Plugin](https://barraider.com/) for your Stream Deck to show your Netatmo data on your Stream Deck.

For Windows users I have made a self-contained `.exe` that you can just run immediately. It contains [gonetatmo](https://github.com/tanaikech/gonetatmo) and everything so you can just run it and input your credentials and you are good to go.

If you prefer doing this manually or use Linux/Mac, you will have to install [gonetatmo](https://github.com/tanaikech/gonetatmo) to your $PATH and then run `shimmy.py`, ideally in a `screen` session or something.

Eitherway, you will need to register an app at Netatmo to get API keys. It's free, no worries: https://dev.netatmo.com/apps/

Once everything is up and running you can drag out a API Ninja square to your deck and configure it as follows:

- Request Type: GET
- API URL: `http://localhost:5551`
- Content Type: `application/json`
- Response Shown: 
	- For indoors: `stations[0].insideData[0].Temperature` 
	- For outdoors: `stations[0].outsideData[0].Temperature`
	- Depending on your setup you might have to change some things around, maybe some 0's should be 1's. It should be pretty easy to figure out.
	- (There are also a bunch of other fields you can use, like humidity, feel free to do whatever you want)
- (Optional) Title Prefix: `Outdoor\n\n\n`
	- A bunch of `\n`'s to push the label up and keeping the temperature along the bottom
- (Optional) Title Suffix: `°C`
- Reponse Type: Response is Text
- Autorun every: 15 mins
	- By default the shimmy script refreshes every 900 seconds (10 mins), so making it any shorter than that is unecessary. But it doesn't hurt either.
- (Optional) Hide the green success indiciator

All other fields should be left blank or default.

Once done, and if you use the Android app's icon, you should end up with something like this:

![Result](https://lambdan.se/img/RustyHomelyLorikeet.png)