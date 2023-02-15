import os
from flask import Flask, render_template, redirect, json
# from flask_pymongo import PyMongo
# import scrape_mars

## Uncomment for MongoDB Cloud usage
# from pymongo import MongoClient
# import config
# user = config.username
# password = config.password

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
# app.config["MONGO_URI"] = f"mongodb+srv://{user}:{password}@cluster0.ktiq9dt.mongodb.net/?retryWrites=true&w=majority"

# mongo = PyMongo(app)

app = Flask(__name__)

@app.route("/")
def index():
    # find one document from our mongo db and return it.
    # mars = mongo.cx.mars_db.mars.find_one()
    
    ## Load Offline Json file instead of MongoDB
    filename = os.path.join(app.static_folder, 'mars.json')
    with open(filename) as file:
        data = json.load(file)
        print(data)
    # pass that mars to render_template
    return render_template("index.html", mars=data[0])

# Route that will trigger the scrape function

# @app.route("/scrape")
# def scraper():
#     mars = mongo.cx.mars_db.mars
#     # call the scrape function in our scrape file. This will scrape and save to mongo.
#     mars_data = scrape_mars.scrape()
#     # update our mars with the data that is being scraped.
#     mongo.db.mars_db.mars.update({}, {"$set": mars_data}, upsert=True)
#     # return a message to our page so we know it was successful.
#     return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)