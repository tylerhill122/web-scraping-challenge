from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    # find one document from our mongo db and return it.
    mars = mongo.db.mars_db.mars.find_one()
    # pass that mars to render_template
    return render_template("index.html", mars=mars)

# Route that will trigger the scrape function
@app.route("/scrape")
def scraper():
    mars = mongo.db.mars_db.mars
    # call the scrape function in our scrape_phone file. This will scrape and save to mongo.
    mars_data = scrape_mars.scrape()
    # update our mars with the data that is being scraped.
    mars.update_one({}, {"$set": mars_data}, upsert=True)
    # return a message to our page so we know it was successful.
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)