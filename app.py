from flask import Flask, render_template, request, jsonify
import requests
import os
from collections import OrderedDict
from datetime import datetime
import openai

app = Flask(__name__, template_folder="templates")

# --- Keys ---
API_KEY = os.getenv("OPENWEATHER_API_KEY", "cf22a8a215106e50b0b6f60f7e511a48")
openai.api_key = os.getenv("OPENAI_API_KEY", "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")

# --- URLs ---
CURRENT_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

# --- Helpers ---
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
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    r = requests.get(FORECAST_URL, params=params)
    if r.status_code != 200:
        return None, r.json()
    data = r.json()
    items = data.get("list", [])

    daily = OrderedDict()
    for it in items:
        dt_txt = it["dt_txt"]
        date_str, time_str = dt_txt.split(" ")
        if date_str not in daily:
            daily[date_str] = it
        if time_str == "12:00:00":
            daily[date_str] = it

    forecast_list, chart_labels, chart_temps = [], [], []
    for i, (date_str, it) in enumerate(daily.items()):
        if i >= 5:
            break
        temp = it["main"]["temp"]
        desc = it["weather"][0]["description"].title()
        icon = it["weather"][0]["icon"]
        d = datetime.strptime(date_str, "%Y-%m-%d")
        label = d.strftime("%a %d %b")
        forecast_list.append({"date": label, "temp": temp, "desc": desc, "icon": icon})
        chart_labels.append(label)
        chart_temps.append(temp)

    return {"forecast": forecast_list, "labels": chart_labels, "temps": chart_temps}, None


# --- Main Route ---
@app.route("/", methods=["GET", "POST"])
def index():
    weather = forecast = error = None
    city = request.form.get("city", "").strip() or request.args.get("city", "Mumbai")

    try:
        weather, err = get_current_weather(city)
        if err:
            error = err.get("message", "Could not fetch current weather.")
        if not error:
            forecast, ferr = get_5day_forecast(city)
            if ferr:
                error = ferr.get("message", "Could not fetch forecast.")
    except Exception as e:
        error = str(e)

    return render_template("index.html", weather=weather, forecast_data=forecast, error=error)


# --- Voice + Chatbot Route ---
@app.route('/voice_query', methods=['POST'])
def voice_query():
    data = request.get_json()
    query = data.get("query", "").lower()

    if "weather" in query or "temperature" in query:
        # detect city from query
        words = query.split()
        city = next((w.capitalize() for w in words if w.capitalize() not in ["Weather", "Temperature", "In", "The", "What’s", "What's", "Is", "Of"]), "Mumbai")

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url).json()
        if "main" in res:
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            ai_text = f"The temperature in {city} is {temp}°C with {desc}."
        else:
            ai_text = f"Sorry, I couldn't fetch the weather for {city}."
    else:
        ai_text = "Sorry, I can only answer weather-related questions right now."

    return jsonify({"reply": ai_text})


# --- Flask Run ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
