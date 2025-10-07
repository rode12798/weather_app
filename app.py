from flask import Flask, render_template, request
import requests
import os
from collections import OrderedDict
from datetime import datetime

app = Flask(__name__, template_folder="templates")

# Use environment variable if available; otherwise place your key here (for testing)
API_KEY = os.getenv("OPENWEATHER_API_KEY", "cf22a8a215106e50b0b6f60f7e511a48")

CURRENT_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

def get_current_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    r = requests.get(CURRENT_URL, params=params)
    if r.status_code != 200:
        return None, r.json()
    data = r.json()
    weather = {
        "city": data.get("name"),
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"].title(),
        "icon": data["weather"][0]["icon"],
        "wind": data.get("wind", {}).get("speed")
    }
    return weather, None

def get_5day_forecast(city):
    """Return list of daily forecast dicts (date, temp, desc, icon) and arrays for chart."""
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    r = requests.get(FORECAST_URL, params=params)
    if r.status_code != 200:
        return None, r.json()
    data = r.json()
    items = data.get("list", [])

    # Pick one forecast per day: choose the entry with time '12:00:00' if present, else first for that date
    daily = OrderedDict()
    for it in items:
        dt_txt = it["dt_txt"]               # e.g. "2025-10-04 12:00:00"
        date_str = dt_txt.split(" ")[0]     # "2025-10-04"
        time_str = dt_txt.split(" ")[1]     # "12:00:00"
        if date_str not in daily:
            daily[date_str] = it
        # Prefer 12:00 entry if available (overwrite)
        if time_str == "12:00:00":
            daily[date_str] = it

    # Take the next 5 unique days (skip today if needed)
    forecast_list = []
    chart_labels = []
    chart_temps = []
    count = 0
    for date_str, it in daily.items():
        if count >= 5:
            break
        temp = it["main"]["temp"]
        desc = it["weather"][0]["description"].title()
        icon = it["weather"][0]["icon"]
        # Convert date to readable form
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d")
            label = d.strftime("%a %d %b")
        except:
            label = date_str
        forecast_list.append({"date": label, "temp": temp, "desc": desc, "icon": icon})
        chart_labels.append(label)
        chart_temps.append(temp)
        count += 1

    return {"forecast": forecast_list, "labels": chart_labels, "temps": chart_temps}, None

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    forecast = None
    error = None
    city = "Mumbai"  # default city to show on first load

    # If user submitted a city via form
    if request.method == "POST":
        city = request.form.get("city", "").strip() or city
    else:
        # allow query param ?city=Delhi
        city = request.args.get("city", city)

    # Get current weather
    try:
        weather, err = get_current_weather(city)
        if err:
            error = err.get("message", "Could not fetch current weather.")
    except Exception as e:
        error = str(e)

    # Get forecast
    if not error:
        try:
            forecast, ferr = get_5day_forecast(city)
            if ferr:
                error = ferr.get("message", "Could not fetch forecast.")
        except Exception as e:
            error = str(e)

    return render_template("index.html",
                           weather=weather,
                           forecast_data=forecast,
                           error=error,
                           api_key=API_KEY)  # api_key not needed on client, included for completeness

if __name__ == "__main__":
    # local debugging
    app.run(host="0.0.0.0", port=5000, debug=True)
