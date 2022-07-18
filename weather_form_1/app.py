from crypt import methods
from ssl import HAS_TLSv1_1
from time import strftime
from flask import Flask,render_template,request,abort
import requests
import pytz
import datetime

app = Flask(__name__)

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/error.html")
def error():
    return render_template("error.html")

@app.route("/result", methods=["POST","GET"])
def result():
    city_name = request.form["city_name"]
    
    time_zone = pytz.timezone("ASIA/BANGKOK")
    date_time = datetime.datetime.now(time_zone).strftime("%d.%m.%Y - %H.%M")

    api_key = "c53e332dc516ab13f41651cb872a1a4e"
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric".format(city_name,api_key)
    data = requests.get(url).json()

    try:
        description = data["weather"][0]["description"]
        temp = round(data["main"]["temp"])
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        return render_template("/result.html", date_time=date_time,city_name=city_name,description=description,temp=temp,humidity=humidity,wind=wind)
    except KeyError:
        return render_template("/error.html")
        
if __name__ == "__main__":
    app.run()