from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

app = Flask(__name__)

mongo = PyMongo(app, uri ="mongodb://localhost:27017/scrape_mars")

#mars_data = scrape()

@app.route("/")
def home():
    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", mars_data = mars_data)

@app.route("/scrape")
def scrape_mars():

    mars_data = mongo.db.collection
    #print('made it after scrape')
    data = scrape()
    print(data)
    mars_data.replace_one(
        {},
        data,
        upsert = True
    )

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)