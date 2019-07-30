from scrape_mars import scrape

from flask import Flask, jsonify, render_template

#connect to mongodb
import pymongo
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


app = Flask(__name__)

@app.route("/")
def home():
	db = client.mars
	data = db.mars.find_one()
	#If there is no data that has been scraped before
	if data is None:
		#Do scraping stuf exactly as if you had been scraping.
		db = client.mars
		db.mars.drop()
		martian_stuff = scrape()
		db.mars.insert(martian_stuff)
		#it takes a while for mongo to update so just keep checking until it is. 
		while data is None:
			data = db.mars.find_one()
		return render_template("index.html", **data)
	else:
		return render_template("index.html", **data)


@app.route("/scrape")
def scrape_route():
	db = client.mars
	db.mars.drop()
	martian_stuff = scrape()
	db.mars.insert(martian_stuff)
	#what if we don't use scraping index? And just reload main page? 
	#Removed old scrape.html stuff
	#A bit of repetitive code here with the thing above. Not enough times to worth refactor. 
	data = db.mars.find_one()
	if data is None:
		while data is None:
			data = db.mars.find_one()
		return render_template("index.html", **data)
	else:
		return render_template("index.html", **data)
	return render_template("index.html", **data)



if __name__ == "__main__":
    app.run(debug=True)
