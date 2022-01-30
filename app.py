from flask import Flask, render_template, jsonify
from dateWiseAttaindance import dwaScrapper
from subjectWiseAttaindance import swScrapper
from overallAttaindance import oaScrapper

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template('index.html')

@app.route("/datewise-attendance-<int:username>-<string:password>")
def datewise(username, password):
    if(username == 123456 and password == '123456'):
        return jsonify([{
                    'sno.': 0,
                    'date': 0,
                    'period': 0,
                    'subject': 0,
                    'Attend Status': 0
        }])
    else:
        scrapper = dwaScrapper()
        return jsonify(scrapper.scrap(username=username, password=password))

@app.route("/subjectwise-attendance-<int:username>-<string:password>")
def subjectwise(username, password):
    if(username == 123456 and password == '123456'):
        return jsonify([{
                    'subject': 0,
                    'subject_code': 0,
                    'total lectures': 0,
                    'present': 0
        }])
    else:
        scrapper = swScrapper()
        return jsonify(scrapper.scrap(username=username, password=password))

@app.route("/overall-attendance-<int:username>-<string:password>")
def overall(username, password):
    if(username == 123456 and password == '123456'):
        return jsonify([{
                'Total Classes': 0,
                'Present': 0,
                'Percentage': 0,
                'Absent': 0
        }])
    else:
        scrapper = oaScrapper()
        return jsonify(scrapper.scrap(username=username, password=password))

if __name__ == '__main__':
    app.run(debug=False)