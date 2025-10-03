from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your free OpenWeatherMap API Key
API_KEY = "cf22a8a215106e50b0b6f60f7e511a48"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    if request.method == "POST":
        city = request.form["city"]
        # API URL
        url = BASE_URL + "appid=" + API_KEY + "&q=" + city + "&units=metric"
        response = requests.get(url).json()

        if response["cod"] == 200:  # Success
            weather_data = {
                "city": response["name"],
                "temperature": response["main"]["temp"],
                "humidity": response["main"]["humidity"],
                "description": response["weather"][0]["description"].title()
            }
        else:
            weather_data = {"error": "City not found!"}

    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

