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
	print("(============/LOADING(============/")
	print(data['mars_facts'][0]['Equatorial Diameter:'])
	return render_template("index.html", **data)

@app.route("/scrape")
def scrape_route():
	debugging_scrape_template = False
	if not debugging_scrape_template:
		print("============/scrape route hit")
		db = client.mars

		print("============/Dropping old collection of Mars")
		db.mars.drop()
		print("============/Scraping the new stuff")
		martian_stuff = scrape()

		print("============/Scraped new stuff.")
		print(martian_stuff)


		print("============/Updating mongodb")
		
		db.mars.insert(martian_stuff)
	return render_template("scrape.html")



if __name__ == "__main__":
    app.run(debug=True)
