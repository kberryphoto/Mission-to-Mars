from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017")
#client = PyMongo.MongoClient(conn)

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 

    # Find data
    mars_list = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_list=mars_list)
    

    # Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
    mars_list = mongo.db.mars_list
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_mars_feat_img()
    mars_data = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_weather()
    mars_data = scrape_mars.scrape_mars_hemi()
    mars_list.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)
