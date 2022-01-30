from flask import Flask, render_template, jsonify
from dateWiseAttaindance import dwaScrapper
from subjectWiseAttaindance import swScrapper
from overallAttaindance import oaScrapper

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template('index.html')

@app.route("/datewise-attaindance-<int:username>-<string:password>")
def datewise(username, password):
    scrapper = dwaScrapper()
    return jsonify(scrapper.scrap(username=username, password=password))

@app.route("/subjectwise-attaindance-<int:username>-<string:password>")
def subjectwise(username, password):
    scrapper = swScrapper()
    return jsonify(scrapper.scrap(username=username, password=password))

@app.route("/overall-attaindance-<int:username>-<string:password>")
def overall(username, password):
    scrapper = oaScrapper()
    return jsonify(scrapper.scrap(username=username, password=password))

if __name__ == '__main__':
    app.run(debug=False)